import tkinter as tk
from tkinter import filedialog
import subprocess
import os


def main():
    # Hide the root tkinter window
    root = tk.Tk()
    root.withdraw()

    # Prompt for audio files (multiple selection allowed)
    input_files = filedialog.askopenfilenames(
        title="Select Audio Files to Normalize",
        filetypes=[
            (
                "Audio Files",
                "*.wav *.mp3 *.flac *.ogg *.aiff *.aif *.au *.m4a *.m4b *.aac *.wma *.wv *.caf *.raw",
            ),
            ("All Files", "*.*"),
        ],
    )

    if not input_files:
        print("No files selected. Exiting.")
        return

    # Normalize each file in the same directory
    for file_path in input_files:
        dir_name = os.path.dirname(file_path)
        base_name, extension = os.path.splitext(os.path.basename(file_path))

        # Construct the output filename (e.g., "song_normalized.wav")
        output_file = os.path.join(dir_name, f"{base_name}_normalized{extension}")

        print(f"Normalizing: {file_path}")
        try:
            # Run the SoX command: sox in.wav out.wav gain -n
            subprocess.run(["sox", file_path, output_file, "gain", "-n"], check=True)
            print(f" --> Saved normalized file to: {output_file}\n")
        except subprocess.CalledProcessError as e:
            print(f"Error normalizing {file_path}: {e}\n")

    print("Normalization completed.")


if __name__ == "__main__":
    main()
