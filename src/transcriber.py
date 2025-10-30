"""
Transcription module for the Hotkey Audio Transcriber MVP
"""
import whisper
import os
import textwrap
from pathlib import Path
from config import (
    WHISPER_MODEL,
    WHISPER_LANGUAGE,
    ENABLE_CONSOLE_FEEDBACK,
    PAUSE_BREAK_THRESHOLD_S,
    INCLUDE_TIMESTAMPS,
    MAX_LINE_LENGTH,
    ENFORCE_SENTENCE_CASING,
)


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
            
            # Transcribe the audio (segments contain timestamps)
            result = self.model.transcribe(
                audio_file_path,
                language=WHISPER_LANGUAGE,
                fp16=False  # Use fp32 for better compatibility
            )

            # Prefer segment-aware formatting for better readability
            segments = result.get("segments") or []
            if segments:
                formatted_text = self.format_from_segments(segments)
            else:
                # Fallback to simple formatting
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
        """Apply basic formatting to transcribed text (fallback)."""
        try:
            if not text:
                return ""
            
            formatted = self._clean_sentence(text.strip())

            if MAX_LINE_LENGTH and MAX_LINE_LENGTH > 0:
                return "\n".join(textwrap.fill(line, width=MAX_LINE_LENGTH) for line in formatted.splitlines())
            return formatted
            
        except Exception as e:
            print(f"ERROR: Text formatting failed: {e}")
            return text  # Return original text if formatting fails

    def format_from_segments(self, segments):
        """Format transcript using Whisper segments and pauses.

        - Inserts blank lines on long pauses
        - Optionally prefixes each segment with timestamps
        - Wraps lines to MAX_LINE_LENGTH if configured
        - Enforces sentence casing and punctuation per segment
        """
        lines = []
        previous_end = None

        for seg in segments:
            start = float(seg.get("start", 0.0))
            end = float(seg.get("end", 0.0))
            txt = (seg.get("text") or "").strip()
            if not txt:
                continue

            # Insert a paragraph break on long pauses
            if previous_end is not None and (start - previous_end) >= PAUSE_BREAK_THRESHOLD_S:
                lines.append("")  # blank line

            cleaned = self._clean_sentence(txt)

            if INCLUDE_TIMESTAMPS:
                ts = f"[{self._format_ts(start)} - {self._format_ts(end)}] "
            else:
                ts = ""

            if MAX_LINE_LENGTH and MAX_LINE_LENGTH > 0:
                wrapped = textwrap.fill(cleaned, width=MAX_LINE_LENGTH)
                # Prefix only the first physical line with timestamp
                wrapped_lines = wrapped.splitlines()
                if wrapped_lines:
                    wrapped_lines[0] = ts + wrapped_lines[0]
                lines.extend(wrapped_lines)
            else:
                lines.append(ts + cleaned)

            previous_end = end

        return "\n".join(lines).strip()

    def _clean_sentence(self, text: str) -> str:
        """Normalize spacing, enforce casing and terminal punctuation."""
        s = " ".join(text.split())  # collapse whitespace
        if ENFORCE_SENTENCE_CASING and s:
            s = s[0].upper() + s[1:]
        if s and s[-1] not in ".!?":
            s += "."
        return s

    def _format_ts(self, seconds: float) -> str:
        m = int(seconds // 60)
        s = int(round(seconds - m * 60))
        return f"{m:02d}:{s:02d}"
    
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
