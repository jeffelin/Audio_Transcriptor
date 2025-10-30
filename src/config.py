"""
Configuration settings for the Hotkey Audio Transcriber MVP
"""
import os
from pathlib import Path

# Hotkey Configuration
HOTKEY_COMBINATION = ['cmd', 'shift', 'r']

# Audio Recording Settings
AUDIO_SAMPLE_RATE = 44100
AUDIO_CHANNELS = 1  # Mono
AUDIO_CHUNK_SIZE = 1024
AUDIO_FORMAT = 'wav'

# Whisper Model Settings
WHISPER_MODEL = 'base.en'  # Fast, local, good quality
WHISPER_LANGUAGE = 'en'

# File Paths
PROJECT_DIR = Path(__file__).parent.parent  # Go up one level from src/
TRANSCRIPTS_DIR = PROJECT_DIR / 'transcripts'
TEMP_DIR = Path('/tmp')
TEMP_AUDIO_FILE = TEMP_DIR / 'audio_recording.wav'

# Application Settings
APP_NAME = 'Hotkey Audio Transcriber'
VERSION = '1.0.0'

# Feedback Settings
ENABLE_CONSOLE_FEEDBACK = True
ENABLE_AUDIO_FEEDBACK = False  # Optional beep sounds

# Formatting Settings
# Insert a new line when a silence between segments exceeds this threshold (seconds)
PAUSE_BREAK_THRESHOLD_S = 1.2

# Include timestamps like [00:00 - 00:07] before each segment/paragraph
INCLUDE_TIMESTAMPS = True

# Wrap lines approximately to this many characters (0 to disable wrapping)
MAX_LINE_LENGTH = 100

# Whether to force capitalization and end punctuation for each segment
ENFORCE_SENTENCE_CASING = True
