import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import wave
import os
import tempfile
import keyboard
import threading
import queue
import time
import warnings
import logging
import shutil
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress the FP16 warning
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

RECORDINGS_DIR = r"C:/Courses/Sem 6/Selected Topics In Ai/Selected proj/llm-chatbot-app/recordings"
os.makedirs(RECORDINGS_DIR, exist_ok=True)

class SpeechToText:
    def __init__(self):
        logger.info("Initializing SpeechToText...")
        try:
            # Initialize Whisper model with CPU-optimized settings
            self.model = whisper.load_model("base", device="cpu")
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading Whisper model: {str(e)}")
            raise
        
        self.sample_rate = 16000
        self.channels = 1
        self.recording = False
        self.audio_queue = queue.Queue()
        self.recording_thread = None
        
    def record_audio(self):
        """Record audio until user presses Enter"""
        logger.info("Starting audio recording...")
        print("🎤 Recording... Press Enter to stop")
        
        def audio_callback(indata, frames, time, status):
            if status:
                logger.warning(f"Audio callback status: {status}")
            self.audio_queue.put(indata.copy())
        
        # Start recording
        self.recording = True
        try:
            with sd.InputStream(samplerate=self.sample_rate, 
                              channels=self.channels, 
                              callback=audio_callback,
                              blocksize=1024):
                while self.recording:
                    if keyboard.is_pressed('enter'):
                        self.recording = False
                        print("⏹️ Recording stopped")
                    time.sleep(0.1)
        except Exception as e:
            logger.error(f"Error during recording: {str(e)}")
            self.recording = False
            return None
        
        # Collect all recorded audio data
        audio_data = []
        while not self.audio_queue.empty():
            audio_data.append(self.audio_queue.get())
        
        if not audio_data:
            logger.warning("No audio data recorded")
            return None
            
        # Combine all audio chunks
        audio_data = np.concatenate(audio_data, axis=0)
        logger.info(f"Recorded audio shape: {audio_data.shape}")
        return audio_data

    def save_audio(self, audio_data, filename):
        """Save audio data to a WAV file"""
        try:
            logger.info(f"Saving audio to {filename}")
            wav.write(filename, self.sample_rate, audio_data)
            # Verify the file was created and has content
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                logger.info("Audio file saved successfully")
                return filename
            else:
                logger.error("Audio file was not created or is empty")
                return None
        except Exception as e:
            logger.error(f"Error saving audio: {str(e)}")
            return None

    def transcribe_audio(self, audio_file):
        """Transcribe audio file using Whisper"""
        try:
            logger.info(f"Starting transcription of {audio_file}")
            # Verify file exists and has content
            if not os.path.exists(audio_file):
                logger.error(f"Audio file {audio_file} does not exist")
                return None
            if os.path.getsize(audio_file) == 0:
                logger.error(f"Audio file {audio_file} is empty")
                return None

            # Use CPU-optimized settings for transcription
            result = self.model.transcribe(
                audio_file,
                fp16=False,  # Force FP32 for CPU
                language="en"  # Specify language for better accuracy
            )
            logger.info("Transcription completed successfully")
            return result["text"].strip()
        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            return None

    def listen(self):
        """Main function to record and transcribe audio"""
        try:
            # Record audio
            audio_data = self.record_audio()
            if audio_data is None:
                logger.warning("No audio data recorded")
                return "No audio recorded."

            # Create a temporary file for the audio
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_filename = temp_file.name
                logger.info(f"Created temporary file: {temp_filename}")

            # Save the recorded audio
            if not self.save_audio(audio_data, temp_filename):
                logger.error("Failed to save audio recording")
                return "Error saving audio recording."

            # Save a copy of the recording in the hard-coded directory
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            recording_path = os.path.join(RECORDINGS_DIR, f"recording_{timestamp}.wav")
            shutil.copy(temp_filename, recording_path)
            logger.info(f"Saved a copy of the recording at: {recording_path}")

            # Transcribe the audio BEFORE deleting the temp file
            transcription = self.transcribe_audio(temp_filename)
            if transcription:
                logger.info(f"Transcription result: {transcription}")
            else:
                logger.warning("No transcription result")

            # Now delete the temp file
            try:
                os.unlink(temp_filename)
                logger.info("Temporary file cleaned up")
            except Exception as e:
                logger.warning(f"Could not delete temporary file: {str(e)}")

            return transcription if transcription else "Could not transcribe audio."

        except Exception as e:
            logger.error(f"Error in listen function: {str(e)}")
            return "An error occurred during speech recognition."

def main():
    stt = SpeechToText()
    print("Speech-to-Text System Ready!")
    print("Press Enter to start recording, then press Enter again to stop.")
    
    while True:
        input("Press Enter to start recording...")
        text = stt.listen()
        print(f"Transcription: {text}")
        
        if input("Continue? (y/n): ").lower() != 'y':
            break

if __name__ == "__main__":
    main()
