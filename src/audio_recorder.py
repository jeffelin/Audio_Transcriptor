"""
Audio recording module for the Hotkey Audio Transcriber MVP
"""
import pyaudio
import wave
import threading
import time
from pathlib import Path
from config import (
    AUDIO_SAMPLE_RATE, AUDIO_CHANNELS, AUDIO_CHUNK_SIZE, 
    AUDIO_FORMAT, TEMP_AUDIO_FILE, ENABLE_CONSOLE_FEEDBACK
)


class AudioRecorder:
    def __init__(self):
        self.audio = None
        self.stream = None
        self.recording = False
        self.frames = []
        self.recording_thread = None
        
    def list_audio_devices(self):
        """List available audio devices for debugging"""
        try:
            if not self.audio:
                self.audio = pyaudio.PyAudio()
            
            print("Available audio devices:")
            for i in range(self.audio.get_device_count()):
                info = self.audio.get_device_info_by_index(i)
                if info['maxInputChannels'] > 0:  # Input device
                    print(f"  {i}: {info['name']} (Input)")
        except Exception as e:
            print(f"Error listing devices: {e}")
        
    def start_recording(self):
        """Start audio recording"""
        try:
            if self.recording:
                if ENABLE_CONSOLE_FEEDBACK:
                    print("WARNING: Already recording!")
                return False
                
            # Initialize PyAudio
            self.audio = pyaudio.PyAudio()
            
            # Open audio stream - ensure it only captures microphone input
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=AUDIO_CHANNELS,
                rate=AUDIO_SAMPLE_RATE,
                input=True,
                input_device_index=None,  # Use default microphone
                frames_per_buffer=AUDIO_CHUNK_SIZE
            )
            
            # Start recording
            self.recording = True
            self.frames = []
            
            # Start recording thread
            self.recording_thread = threading.Thread(target=self._record_audio)
            self.recording_thread.start()
            
            if ENABLE_CONSOLE_FEEDBACK:
                print("Recording started...")
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to start recording: {e}")
            self.recording = False
            return False
    
    def stop_recording(self):
        """Stop audio recording and save to file"""
        try:
            if not self.recording:
                if ENABLE_CONSOLE_FEEDBACK:
                    print("WARNING: Not currently recording!")
                return False
                
            # Stop recording
            self.recording = False
            
            # Wait for recording thread to finish
            if self.recording_thread:
                self.recording_thread.join()
            
            # Save audio to file
            if self.frames:
                self._save_audio()
                if ENABLE_CONSOLE_FEEDBACK:
                    print("Recording stopped and saved")
                return True
            else:
                if ENABLE_CONSOLE_FEEDBACK:
                    print("WARNING: No audio recorded!")
                return False
                
        except Exception as e:
            print(f"ERROR: Failed to stop recording: {e}")
            return False
    
    def is_recording(self):
        """Check if currently recording"""
        return self.recording
    
    def _record_audio(self):
        """Internal method to record audio in a separate thread"""
        try:
            while self.recording:
                data = self.stream.read(AUDIO_CHUNK_SIZE, exception_on_overflow=False)
                self.frames.append(data)
        except Exception as e:
            print(f"ERROR: Recording thread failed: {e}")
    
    def _save_audio(self):
        """Save recorded audio to temporary file"""
        try:
            # Ensure temp directory exists
            TEMP_AUDIO_FILE.parent.mkdir(parents=True, exist_ok=True)
            
            # Save as WAV file
            with wave.open(str(TEMP_AUDIO_FILE), 'wb') as wf:
                wf.setnchannels(AUDIO_CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(AUDIO_SAMPLE_RATE)
                wf.writeframes(b''.join(self.frames))
                
        except Exception as e:
            print(f"ERROR: Failed to save audio: {e}")
    
    def cleanup(self):
        """Clean up audio resources"""
        try:
            if self.stream:
                try:
                    self.stream.stop_stream()
                except:
                    pass
                try:
                    self.stream.close()
                except:
                    pass
                self.stream = None
            
            if self.audio:
                try:
                    self.audio.terminate()
                except:
                    pass
                self.audio = None
                
            if ENABLE_CONSOLE_FEEDBACK:
                print("Audio resources cleaned up")
        except Exception as e:
            # Don't print cleanup errors as they're not critical
            pass
