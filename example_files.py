import os
import wave
import struct

def create_directory(directory):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Verzeichnis erstellt: {directory}")
    else:
        print(f"Verzeichnis existiert bereits: {directory}")

def create_empty_wav(filepath):
    """Create an empty WAV file (1 second of silence)"""
    # WAV-Parameter
    sample_rate = 44100
    channels = 2
    sample_width = 2  # 16-bit
    duration = 1  # 1 Sekunde
    
    # Prüfen, ob das Verzeichnis für die Datei existiert
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Leere WAV-Datei erstellen
    with wave.open(filepath, 'w') as wav_file:
        wav_file.setparams((channels, sample_width, sample_rate, sample_rate * duration, 'NONE', 'not compressed'))
        
        # 1 Sekunde Stille (Nullen) schreiben
        silent_data = struct.pack('<' + ('h' * channels * sample_rate * duration), *([0] * channels * sample_rate * duration))
        wav_file.writeframes(silent_data)
    
    print(f"Datei erstellt: {filepath}")

def main():
    # Dateien-Liste
    filenames = [
        "Main_2025-04-18 17-25-06_Pre Bass.wav",
        "Main_2025-04-18 17-25-06_Pre Black.wav",
        "Main_2025-04-18 17-25-06_Pre F-Tom.wav",
        "Main_2025-04-18 17-25-06_Pre Geige.wav",
        "Main_2025-04-18 17-25-06_Pre Gelb.wav",
        "Main_2025-04-18 17-25-06_Pre Gitarre.wav",
        "Main_2025-04-18 17-25-06_Pre Helix.wav",
        "Main_2025-04-18 17-25-06_Pre H-Hat.wav",
        "Main_2025-04-18 17-25-06_Pre Keys.wav",
        "Main_2025-04-18 17-25-06_Pre Kick.wav",
        "Main_2025-04-18 17-25-06_Pre KM-1.wav",
        "Main_2025-04-18 17-25-06_Pre Orange.wav",
        "Main_2025-04-18 17-25-06_Pre Raummikros L.wav",
        "Main_2025-04-18 17-25-06_Pre Raummikros R.wav",
        "Main_2025-04-18 17-25-06_Pre Snare.wav",
        "Main_2025-04-18 17-25-06_Pre Teller.wav",
        "Main_2025-04-18 17-25-06_Pre Tom.wav",
        "Main_2025-04-18 17-25-06_Pre Track.wav",
        "Main_2025-04-18 17-25-06_Recording.wav",
        "Main_2025-04-18 17-18-40_Pre Bass.wav",
        "Main_2025-04-18 17-18-40_Pre Black.wav",
        "Main_2025-04-18 17-18-40_Pre F-Tom.wav",
        "Main_2025-04-18 17-18-40_Pre Geige.wav",
        "Main_2025-04-18 17-18-40_Pre Gelb.wav",
        "Main_2025-04-18 17-18-40_Pre Gitarre.wav",
        "Main_2025-04-18 17-18-40_Pre Helix.wav",
        "Main_2025-04-18 17-18-40_Pre H-Hat.wav",
        "Main_2025-04-18 17-18-40_Pre Keys.wav",
        "Main_2025-04-18 17-18-40_Pre Kick.wav"
    ]
    
    # Verzeichnis erstellen
    examples_dir = "examples"
    create_directory(examples_dir)
    
    # WAV-Dateien erstellen
    for filename in filenames:
        filepath = os.path.join(examples_dir, filename)
        create_empty_wav(filepath)

if __name__ == "__main__":
    main()
    print("Alle WAV-Dateien wurden im Verzeichnis 'examples/' erstellt.")