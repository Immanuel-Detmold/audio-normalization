# Audio Processor - Installation Guide

## Required Components

1. **Python 3.6+** - The programming language runtime
2. **Python Packages:**
   - `colorama` - For colored terminal output
   - `tkinter` - For file dialogs (typically included with Python)

3. **SoX (Sound eXchange)** - External command-line utility for audio processing

## Installation Steps

### 1. Install Python (if not already installed)
Download and install Python from [python.org](https://www.python.org/downloads/).
   - Make sure to check "Add Python to PATH" during installation.

### 2. Install Required Python Packages

Open a terminal/command prompt and run:

```bash
pip install colorama
```

### 3. Install SoX (Sound eXchange)

#### Windows:
1. Download SoX from [SourceForge](https://sourceforge.net/projects/sox/files/sox/)
2. Run the installer and follow the instructions
3. Add SoX to your PATH environment variable:
   - Search for "Environment Variables" in Windows search
   - Edit the PATH variable and add the path to SoX (typically `C:\Program Files (x86)\sox-14-4-2`)

#### macOS:
Using Homebrew:
```bash
brew install sox
```

#### Linux (Debian/Ubuntu):
```bash
sudo apt-get update
sudo apt-get install sox
```

### 4. Verify Installation

To verify that everything is installed correctly, open a terminal/command prompt and run:

```bash
python -c "import colorama; print('Colorama installed successfully!')"
sox --version
```

If both commands run without errors, your installation is complete!

## Running the Program

1. Save the `audio_processor.py` script to your computer
2. Open a terminal/command prompt
3. Navigate to the directory containing the script
4. Run:

```bash
python audio_processor.py
```

## Troubleshooting

### "SoX not found" error
- Make sure SoX is installed
- Ensure SoX is in your system PATH
- Try restarting your terminal/command prompt

### File dialog not appearing
- Make sure tkinter is properly installed
- On Linux, you might need to install the python3-tk package:
  ```bash
  sudo apt-get install python3-tk
  ```

### Permission errors
- Make sure you have read/write permissions for the audio files
- Try running the script as administrator/sudo

### Audio normalization not working
- Ensure SoX is correctly installed
- Some audio formats may require additional SoX plugins or libraries