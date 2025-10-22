"""
Transcription module for the Hotkey Audio Transcriber MVP
"""
import whisper
import os
from pathlib import Path
from config import WHISPER_MODEL, WHISPER_LANGUAGE, ENABLE_CONSOLE_FEEDBACK


class Transcriber:
    def __init__(self):
        self.model = None
        self.model_loaded = False
        
    def load_model(self):
        """Load the Whisper model (one-time setup)"""
        try:
            if ENABLE_CONSOLE_FEEDBACK:
                print(f"Loading Whisper model: {WHISPER_MODEL}")
                print("This may take a moment on first run...")
            
            self.model = whisper.load_model(WHISPER_MODEL)
            self.model_loaded = True
            
            if ENABLE_CONSOLE_FEEDBACK:
                print("Whisper model loaded successfully")
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to load Whisper model: {e}")
            print("Make sure you have internet connection for first-time model download")
            return False
    
    def transcribe_audio(self, audio_file_path):
        """Transcribe audio file using Whisper"""
        try:
            if not self.model_loaded:
                if ENABLE_CONSOLE_FEEDBACK:
                    print("WARNING: Model not loaded, attempting to load now...")
                if not self.load_model():
                    return None
            
            if not Path(audio_file_path).exists():
                print(f"ERROR: Audio file not found: {audio_file_path}")
                return None
            
            if ENABLE_CONSOLE_FEEDBACK:
                print("Transcribing audio...")
            
            # Transcribe the audio
            result = self.model.transcribe(
                audio_file_path,
                language=WHISPER_LANGUAGE,
                fp16=False  # Use fp32 for better compatibility
            )
            
            # Extract text and format it
            raw_text = result["text"].strip()
            formatted_text = self.format_text(raw_text)
            
            if ENABLE_CONSOLE_FEEDBACK:
                print("Transcription completed")
                print(f"Length: {len(formatted_text)} characters")
            
            return formatted_text
            
        except Exception as e:
            print(f"ERROR: Transcription failed: {e}")
            return None
    
    def format_text(self, text):
        """Apply basic formatting to transcribed text"""
        try:
            if not text:
                return ""
            
            # Basic text formatting
            formatted = text.strip()
            
            # Ensure proper sentence capitalization
            if formatted:
                # Capitalize first letter
                formatted = formatted[0].upper() + formatted[1:]
                
                # Ensure proper sentence endings
                if not formatted.endswith(('.', '!', '?')):
                    formatted += '.'
            
            return formatted
            
        except Exception as e:
            print(f"ERROR: Text formatting failed: {e}")
            return text  # Return original text if formatting fails
    
    def is_model_loaded(self):
        """Check if model is loaded and ready"""
        return self.model_loaded
    
    def get_model_info(self):
        """Get information about the loaded model"""
        if self.model_loaded:
            return {
                'model_name': WHISPER_MODEL,
                'language': WHISPER_LANGUAGE,
                'loaded': True
            }
        return {'loaded': False}
