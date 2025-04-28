import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import shutil
from colorama import init, Fore, Style
import sys
import tempfile

# Initialize colorama for colored terminal output
init()

def print_fancy(text, color=Fore.WHITE, newline=True):
    """Print text with color without typing effect"""
    sys.stdout.write(f"{color}{text}{Style.RESET_ALL}")
    if newline:
        print()
    else:
        sys.stdout.flush()

def print_header():
    """Print a fancy header for the application"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n")
    print_fancy("=" * 70, Fore.CYAN)
    print_fancy("                AUDIO FILE PROCESSOR", Fore.YELLOW)
    print_fancy("=" * 70, Fore.CYAN)
    print("\n")

def get_yes_no_input(prompt):
    """Get a yes/no input from the user with fancy formatting"""
    while True:
        print_fancy(prompt + " (y/n): ", Fore.GREEN, newline=False)
        response = input().strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print_fancy("Please enter 'y' or 'n'", Fore.RED)

def rename_file(file_path):
    """Rename file to remove prefix"""
    dir_name = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    
    # Extract the part after "_Pre " in the filename
    if "_Pre " in base_name:
        new_name = base_name.split("_Pre ")[1]
        return os.path.join(dir_name, new_name)
    return file_path

def normalize_audio(input_file, output_file):
    """Normalize audio file using SoX"""
    try:
        # Run SoX with detailed error capture
        result = subprocess.run(
            ["sox", input_file, output_file, "gain", "-n"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Check if the command was successful
        if result.returncode != 0:
            stderr = result.stderr.decode()
            print_fancy(f"  Detailed Sox error: {stderr}", Fore.RED)
            return False
        return True
    except FileNotFoundError:
        print_fancy("SoX not found. Please install SoX and make sure it's in your PATH.", Fore.RED)
        print_fancy("On Windows: https://sourceforge.net/projects/sox/", Fore.YELLOW)
        print_fancy("On macOS: brew install sox", Fore.YELLOW)
        print_fancy("On Linux: sudo apt-get install sox", Fore.YELLOW)
        return False
    except Exception as e:
        print_fancy(f"  Unexpected error: {e}", Fore.RED)
        return False

def process_files(input_files, should_rename, should_normalize, should_replace):
    """Process all selected files"""
    if not input_files:
        print_fancy("No files selected. Exiting.", Fore.RED)
        return
    
    # Create output directory if not replacing files
    output_dir = None
    if not should_replace:
        first_file_dir = os.path.dirname(input_files[0])
        folder_name = "audio_renamed" if should_rename and not should_normalize else "audio_normalized" if should_normalize else "audio_processed"
        output_dir = os.path.join(first_file_dir, folder_name)
        os.makedirs(output_dir, exist_ok=True)
        print_fancy(f"Created output directory: {output_dir}", Fore.CYAN)
    
    # Create a temporary directory for processing
    temp_dir = tempfile.mkdtemp()
    print_fancy(f"Created temporary working directory", Fore.CYAN)
    
    total_files = len(input_files)
    success_count = 0
    
    try:
        for index, file_path in enumerate(input_files):
            # Display progress
            print_fancy(f"[{index+1}/{total_files}] Processing: {os.path.basename(file_path)}", Fore.CYAN)
            
            try:
                # Determine the final output path
                if should_replace:
                    # If replacing, the final path is the original or a renamed version
                    if should_rename:
                        final_path = rename_file(file_path)
                    else:
                        final_path = file_path
                else:
                    # If not replacing, put in output directory
                    if should_rename:
                        new_name = os.path.basename(rename_file(file_path))
                    else:
                        new_name = os.path.basename(file_path)
                    final_path = os.path.join(output_dir, new_name)
                
                # Work with temporary files in the temp directory
                temp_filename = f"temp_{index}_{os.path.basename(file_path)}"
                temp_path = os.path.join(temp_dir, temp_filename)
                
                # Copy the original to a temporary location
                shutil.copy2(file_path, temp_path)
                
                # Normalize audio if requested
                if should_normalize:
                    print_fancy("  Normalizing audio levels...", Fore.YELLOW)
                    norm_temp_path = os.path.join(temp_dir, f"norm_{temp_filename}")
                    
                    # Normalize directly without chained temp files
                    normalize_success = normalize_audio(temp_path, norm_temp_path)
                    
                    if normalize_success:
                        # Use the normalized version
                        os.remove(temp_path)
                        temp_path = norm_temp_path
                    else:
                        print_fancy("  Normalization failed, skipping file", Fore.RED)
                        os.remove(temp_path)
                        continue
                
                # Move to final destination
                if os.path.exists(final_path) and final_path != file_path:
                    os.remove(final_path)
                
                # Move the processed file to its final location
                shutil.copy2(temp_path, final_path)
                
                # If we're replacing and it's a rename, remove the original
                if should_replace and should_rename and final_path != file_path:
                    os.remove(file_path)
                
                success_count += 1
                print_fancy(f"  ✓ Success: {os.path.basename(final_path)}", Fore.GREEN)
                
            except Exception as e:
                print_fancy(f"  ✗ Error processing {file_path}: {e}", Fore.RED)
    
    finally:
        # Clean up the temporary directory
        try:
            shutil.rmtree(temp_dir)
            print_fancy("Cleaned up temporary files", Fore.CYAN)
        except Exception as e:
            print_fancy(f"Warning: Could not clean up temp directory: {e}", Fore.YELLOW)
    
    # Final summary
    print_fancy("\n" + "=" * 50, Fore.CYAN)
    print_fancy(f"Processing complete: {success_count}/{total_files} files successful", 
               Fore.GREEN if success_count == total_files else Fore.YELLOW)
    if not should_replace and success_count > 0:
        print_fancy(f"Files saved to: {output_dir}", Fore.CYAN)
    print_fancy("=" * 50, Fore.CYAN)

def check_sox_installed():
    """Check if SoX is installed"""
    try:
        result = subprocess.run(["sox", "--version"], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def main():
    print_header()
    
    # Check if SoX is installed
    if check_sox_installed():
        print_fancy("✓ SoX audio processor found", Fore.GREEN)
    else:
        print_fancy("✗ SoX audio processor not found", Fore.RED)
        print_fancy("This program requires SoX to normalize audio files.", Fore.YELLOW)
        print_fancy("Please install SoX:", Fore.YELLOW)
        print_fancy("  • Windows: https://sourceforge.net/projects/sox/", Fore.CYAN)
        print_fancy("  • macOS: brew install sox", Fore.CYAN)
        print_fancy("  • Linux: sudo apt-get install sox", Fore.CYAN)
        
        if not get_yes_no_input("Continue anyway?"):
            print_fancy("Exiting program.", Fore.RED)
            return
    
    # Hide the root tkinter window
    root = tk.Tk()
    root.withdraw()

    # Prompt for audio files (multiple selection allowed)
    print_fancy("Select audio files to process...", Fore.YELLOW)
    input_files = list(filedialog.askopenfilenames(
        title="Select Audio Files to Process",
        filetypes=[
            (
                "Audio Files",
                "*.wav *.mp3 *.flac *.ogg *.aiff *.aif *.au *.m4a *.m4b *.aac *.wma *.wv *.caf *.raw",
            ),
            ("All Files", "*.*"),
        ],
    ))

    if not input_files:
        print_fancy("No files selected. Exiting.", Fore.RED)
        return
    
    print_fancy(f"Selected {len(input_files)} files", Fore.GREEN)
    
    # Ask for renaming option
    should_rename = get_yes_no_input("Do you want to rename files (remove prefix before instrument name)?")
    
    # Ask for normalization option
    should_normalize = get_yes_no_input("Do you want to normalize audio levels?")
    
    # Ask for replacement option
    should_replace = get_yes_no_input("Do you want to replace original files?")
    
    # Summary before processing
    print_fancy("\nSummary of operations:", Fore.CYAN)
    print_fancy(f"• Files to process: {len(input_files)}", Fore.WHITE)
    print_fancy(f"• Rename files: {'Yes' if should_rename else 'No'}", 
               Fore.GREEN if should_rename else Fore.RED)
    print_fancy(f"• Normalize audio: {'Yes' if should_normalize else 'No'}", 
               Fore.GREEN if should_normalize else Fore.RED)
    print_fancy(f"• Replace originals: {'Yes' if should_replace else 'No'}", 
               Fore.GREEN if should_replace else Fore.RED)
    
    if not get_yes_no_input("\nProceed with these settings?"):
        print_fancy("Operation cancelled. Exiting.", Fore.RED)
        return
    
    # Process the files
    process_files(input_files, should_rename, should_normalize, should_replace)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_fancy("\nOperation cancelled by user. Exiting.", Fore.RED)
    except Exception as e:
        print_fancy(f"\nAn unexpected error occurred: {e}", Fore.RED)
    
    print_fancy("\nPress Enter to exit...", Fore.CYAN, newline=False)
    input()