"""
File management module for the Hotkey Audio Transcriber MVP
"""
import os
import shutil
from datetime import datetime
from pathlib import Path
from config import TRANSCRIPTS_DIR, TEMP_AUDIO_FILE, ENABLE_CONSOLE_FEEDBACK


def ensure_transcripts_dir():
    """Create the transcripts directory if it doesn't exist"""
    try:
        TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
        if ENABLE_CONSOLE_FEEDBACK:
            print(f"Transcripts directory ready: {TRANSCRIPTS_DIR}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to create transcripts directory: {e}")
        return False


def save_transcript(text):
    """Save transcribed text to a timestamped file"""
    try:
        # Generate human-readable timestamped filename
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H-%M-%S")
        filename = f"transcript_{date_str}_{time_str}.txt"
        filepath = TRANSCRIPTS_DIR / filename
        
        # Save the transcript
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        
        if ENABLE_CONSOLE_FEEDBACK:
            print(f"Transcript saved: {filepath}")
        return str(filepath)
    except Exception as e:
        print(f"ERROR: Failed to save transcript: {e}")
        return None


def cleanup_temp_files():
    """Remove temporary audio files"""
    try:
        if TEMP_AUDIO_FILE.exists():
            TEMP_AUDIO_FILE.unlink()
            if ENABLE_CONSOLE_FEEDBACK:
                print("Temporary audio file cleaned up")
        return True
    except Exception as e:
        print(f"ERROR: Failed to cleanup temp files: {e}")
        return False


def get_transcript_count():
    """Get the number of existing transcripts"""
    try:
        if TRANSCRIPTS_DIR.exists():
            return len(list(TRANSCRIPTS_DIR.glob("transcript_*.txt")))
        return 0
    except Exception as e:
        print(f"ERROR: Failed to count transcripts: {e}")
        return 0
