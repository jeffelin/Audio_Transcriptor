"""
Main application for the Hotkey Audio Transcriber MVP
"""
import sys
import time
import signal
from pynput import keyboard
from pynput.keyboard import Key, Listener

from config import HOTKEY_COMBINATION, ENABLE_CONSOLE_FEEDBACK, APP_NAME, VERSION
from audio_recorder import AudioRecorder
from transcriber import Transcriber
from file_manager import ensure_transcripts_dir, save_transcript, cleanup_temp_files, get_transcript_count


class HotkeyAudioTranscriber:
    def __init__(self):
        self.audio_recorder = AudioRecorder()
        self.transcriber = Transcriber()
        self.listener = None
        self.running = False
        self.cmd_pressed = False
        self.shift_pressed = False
        
    def start(self):
        """Start the application"""
        try:
            if ENABLE_CONSOLE_FEEDBACK:
                self._print_welcome()
            
            # Setup directories
            if not ensure_transcripts_dir():
                print("ERROR: Failed to setup directories")
                return False
            
            # Load Whisper model
            if not self.transcriber.load_model():
                print("ERROR: Failed to load Whisper model")
                return False
            
            # Show audio device info (optional debug)
            if ENABLE_CONSOLE_FEEDBACK:
                print("🎤 Audio device info:")
                self.audio_recorder.list_audio_devices()
                print()
            
            # Start hotkey listener
            self._start_hotkey_listener()
            
            if ENABLE_CONSOLE_FEEDBACK:
                print("✅ Application ready!")
                print(f"🎯 Press {'+'.join(HOTKEY_COMBINATION).upper()} to START recording")
                print(f"🛑 Press {'+'.join(HOTKEY_COMBINATION).upper()} again to CLOSE app")
                print("🛑 Press Ctrl+C to quit")
                print("\n" + "="*60)
                print("🎤 WAITING FOR HOTKEY...")
                print("="*60)
            
            self.running = True
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to start application: {e}")
            return False
    
    def stop(self):
        """Stop the application"""
        try:
            self.running = False
            
            # Stop any ongoing recording
            if self.audio_recorder.is_recording():
                self.audio_recorder.stop_recording()
            
            # Stop hotkey listener
            if self.listener:
                self.listener.stop()
            
            # Cleanup resources
            self.audio_recorder.cleanup()
            cleanup_temp_files()
            
            if ENABLE_CONSOLE_FEEDBACK:
                print(f"{APP_NAME} stopped")
            
        except Exception as e:
            print(f"ERROR: Failed to stop application: {e}")
    
    def _print_welcome(self):
        """Print welcome message"""
        print(f"\n🎤 {APP_NAME} v{VERSION}")
        print("=" * 60)
        print("📝 Local audio transcription with global hotkeys")
        print("🔒 No external APIs required - everything runs locally")
        print("⏺️  Continuous recording mode - records until stopped")
        print("=" * 60)
        
        # Show existing transcript count
        count = get_transcript_count()
        if count > 0:
            print(f"📁 Found {count} existing transcripts")
        
        print("\n🚨 IMPORTANT SETUP:")
        print("1. Grant accessibility permissions when prompted")
        print("2. Allow microphone access when requested")
        print("3. Install ffmpeg if not already installed: brew install ffmpeg")
        print()
    
    def _start_hotkey_listener(self):
        """Start the global hotkey listener"""
        try:
            self.listener = Listener(
                on_press=self._on_key_press,
                on_release=self._on_key_release,
                suppress=False
            )
            self.listener.start()
        except Exception as e:
            print(f"ERROR: Failed to start hotkey listener: {e}")
            raise
    
    def _on_key_press(self, key):
        """Handle hotkey press events"""
        try:
            # Track modifier keys
            if key == Key.cmd:
                self.cmd_pressed = True
            elif key == Key.shift:
                self.shift_pressed = True
            elif hasattr(key, 'char') and key.char == 'r':
                # Check if Cmd and Shift are pressed
                if self.cmd_pressed and self.shift_pressed:
                    self._handle_recording_toggle()
        except Exception as e:
            print(f"❌ ERROR: Failed to handle hotkey: {e}")
    
    def _on_key_release(self, key):
        """Handle key release events"""
        try:
            # Track modifier keys
            if key == Key.cmd:
                self.cmd_pressed = False
            elif key == Key.shift:
                self.shift_pressed = False
        except Exception as e:
            pass
    
    def _is_hotkey_pressed(self):
        """Check if the hotkey combination is pressed"""
        # This method is no longer used - hotkey detection is handled in _on_key_press
        return False
    
    def _handle_recording_toggle(self):
        """Handle recording start/stop toggle"""
        try:
            if self.audio_recorder.is_recording():
                # Stop recording, transcribe, and close app
                print("\n" + "="*60)
                print("⏹️  STOPPING RECORDING...")
                print("="*60)
                
                if self.audio_recorder.stop_recording():
                    self._process_recording()
                
                # Close the app
                print("\n" + "="*60)
                print("🛑 CLOSING APP...")
                print("="*60)
                self.stop()
                sys.exit(0)
            else:
                # Start continuous recording
                print("\n" + "="*60)
                print("🎤 RECORDING STARTED!")
                print("💬 Speak now - recording everything you say...")
                print(f"🛑 Press {'+'.join(HOTKEY_COMBINATION).upper()} to CLOSE app")
                print("="*60)
                self.audio_recorder.start_recording()
                
        except Exception as e:
            print(f"❌ ERROR: Failed to handle recording toggle: {e}")
    
    def _process_recording(self):
        """Process the recorded audio"""
        try:
            from config import TEMP_AUDIO_FILE
            
            if not TEMP_AUDIO_FILE.exists():
                print("❌ ERROR: No audio file to process")
                return
            
            print("🔄 Processing audio...")
            print("🤖 Transcribing with Whisper AI...")
            
            # Transcribe the audio
            transcript = self.transcriber.transcribe_audio(str(TEMP_AUDIO_FILE))
            
            if transcript:
                # Save the transcript
                filepath = save_transcript(transcript)
                if filepath:
                    print("\n" + "="*60)
                    print("✅ TRANSCRIPTION COMPLETE!")
                    print("="*60)
                    print(f"📁 Saved to: {filepath}")
                    print(f"📝 Preview: {transcript[:150]}...")
                    print("="*60)
                    print("🎤 WAITING FOR NEXT RECORDING...")
                    print("="*60)
                else:
                    print("❌ ERROR: Failed to save transcript")
            else:
                print("❌ ERROR: Transcription failed")
                print("💡 Try: brew install ffmpeg")
            
            # Cleanup
            cleanup_temp_files()
            
        except Exception as e:
            print(f"❌ ERROR: Failed to process recording: {e}")
            print("💡 Try: brew install ffmpeg")


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n" + "="*60)
    print("🛑 SHUTTING DOWN...")
    print("="*60)
    if 'app' in globals():
        app.stop()
    sys.exit(0)


def main():
    """Main entry point"""
    # Setup signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Create and start the application
        global app
        app = HotkeyAudioTranscriber()
        
        if not app.start():
            print("ERROR: Failed to start application")
            sys.exit(1)
        
        # Keep the application running
        try:
            while app.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        
    except Exception as e:
        print(f"ERROR: Fatal error: {e}")
        sys.exit(1)
    finally:
        if 'app' in globals():
            app.stop()


if __name__ == "__main__":
    main()
