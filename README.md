# Hotkey Audio Transcriber MVP

A macOS utility that uses a global hotkey (Cmd+Shift+R) to record audio and transcribe it locally using Whisper, saving organized text files without any external API dependencies.

## Features

- **Global Hotkey**: Press `Cmd+Shift+R` anywhere on your Mac to start/stop recording
- **Local Transcription**: Uses Whisper AI model running entirely on your machine
- **No Internet Required**: Everything works offline after initial setup
- **Automatic File Management**: Saves transcripts with timestamps to `./transcripts/` folder
- **High Quality Audio**: Records at 44.1kHz for clear transcription

## Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# On macOS, you may need to install portaudio for pyaudio
brew install portaudio
```

### 2. Run the Application

```bash
python src/main.py
```

### 3. Use the Hotkey

- Press `Cmd+Shift+R` to start continuous recording
- Press `Cmd+Shift+R` again to stop recording and transcribe
- Your transcript will be saved automatically to `./transcripts/` folder

## Installation Details

### System Requirements

- macOS 10.15+ (Catalina or later)
- Python 3.10+
- Microphone access
- ~2GB free disk space (for Whisper model)

### First Run Setup

1. **Microphone Permission**: The app will request microphone access on first run
2. **Model Download**: Whisper will download the `base.en` model (~150MB) on first use
3. **Directory Creation**: The app creates `./transcripts/` folder automatically

### Dependencies

- `pynput`: Global hotkey detection
- `pyaudio`: Audio recording
- `whisper`: Local AI transcription
- `numpy`: Audio processing

## Usage

### Recording Process

1. **Start Recording**: Press `Cmd+Shift+R` anywhere on your Mac
2. **Speak**: The app continuously records from your default microphone
3. **Stop Recording**: Press `Cmd+Shift+R` again to stop and transcribe
4. **Transcription**: The app automatically transcribes using Whisper
5. **File Saved**: Transcript saved to `./transcripts/transcript_YYYY-MM-DD_HH-MM-SS.txt`

### File Organization

Transcripts are saved with human-readable timestamped filenames:
```
./transcripts/
├── transcript_2025-01-22_14-30-22.txt
├── transcript_2025-01-22_14-31-56.txt
└── transcript_2025-01-22_14-33-01.txt
```

### Console Output

The app provides real-time feedback:
```
Hotkey Audio Transcriber v1.0.0
==================================================
Local audio transcription with global hotkeys
No external APIs required - everything runs locally
==================================================

Transcripts directory ready: /Users/jeffelin/audio_recorder/transcripts
Loading Whisper model: base.en
   This may take a moment on first run...
Whisper model loaded successfully
Hotkey Audio Transcriber is running!
   Press cmd+shift+r to start continuous recording
   Press cmd+shift+r again to stop and transcribe
   Press Ctrl+C to quit

Starting continuous recording...
Recording started...
Press Cmd+Shift+R again to stop and transcribe
Stopping continuous recording...
Recording stopped and saved
Transcribing audio...
Transcription completed
   Length: 245 characters
Transcript saved: /Users/jeffelin/audio_recorder/transcripts/transcript_2025-01-22_14-30-22.txt
Temporary audio file cleaned up
```

## Configuration

Edit `src/config.py` to customize:

- **Hotkey**: Change the key combination
- **Audio Quality**: Adjust sample rate and format
- **Model Size**: Switch between Whisper models
- **File Paths**: Customize save locations

## Troubleshooting

### Common Issues

**"No module named 'pyaudio'"**
```bash
brew install portaudio
pip install pyaudio
```

**"Permission denied" for microphone**
- Go to System Preferences > Security & Privacy > Privacy > Microphone
- Add Terminal or your Python app to the list

**"Model download failed"**
- Check internet connection for first-time model download
- Ensure you have ~2GB free disk space

**"Hotkey not working"**
- Make sure the app is running in the foreground
- Check for conflicts with other apps
- Try restarting the application

### Performance Tips

- **Model Loading**: First run takes longer to download the model
- **Memory Usage**: The app uses ~300-500MB RAM when running
- **Transcription Speed**: Depends on audio length and system performance
- **Background Usage**: The app runs efficiently in the background

## Development

### Project Structure

```
/Users/jeffelin/audio_recorder/
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore file
├── src/                     # Source code directory
│   ├── __init__.py          # Package init
│   ├── main.py              # Main application
│   ├── config.py            # Configuration settings
│   ├── audio_recorder.py      # Audio recording module
│   ├── transcriber.py       # Whisper transcription
│   └── file_manager.py      # File management
├── transcripts/             # Generated transcripts (gitignored)
└── README.md                # This file
```

### Key Components

- **AudioRecorder**: Handles microphone input and WAV file creation
- **Transcriber**: Manages Whisper model and text formatting
- **FileManager**: Creates directories and saves transcripts
- **HotkeyAudioTranscriber**: Main app class with hotkey handling

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Ensure all dependencies are properly installed
3. Verify microphone permissions are granted
4. Check that the Whisper model downloaded successfully

---

**Note**: This is an MVP (Minimum Viable Product) focused on core functionality. The app prioritizes simplicity and reliability over advanced features.