import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import wave
import os
import traceback
import sys
import google.generativeai as genai
import requests
from io import BytesIO
import tempfile
import pygame
import time
import re
import datetime
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "pqHfZKP75CvOlQylNhV4"  


def play_mp3_file(filepath):
    """Play an MP3 file using pygame and delete it after playback."""
    print(f"🔊 Playing MP3 file: {filepath}")
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        
        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        print("✅ MP3 playback completed")
    except Exception as e:
        print(f"❌ Error playing MP3: {str(e)}")
        print(traceback.format_exc())
    finally:
        # Clean up the file after playback
        try:
            os.remove(filepath)
            print(f"🗑️ Deleted temporary MP3 file: {filepath}")
        except Exception as e:
            print(f"⚠️ Could not delete temporary MP3 file: {str(e)}")

def speak_with_elevenlabs(text):
    print("🔊 Speaking with ElevenLabs...")
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json",
            "accept": "audio/mpeg"  # Request MP3 format instead of WAV
        }

        data = {
            "text": text,
            "model_id": "eleven_turbo_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.7}
        }

        print("Sending request to ElevenLabs API...")
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            print("Audio received, saving to file...")
            
            # Save to a unique temporary file
            temp_file = f"C:\\Courses\\Sem 7\\NLP\\Assignments\\project_rag_quantum\\temp_response_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.mp3"
            with open(temp_file, "wb") as audio_file:
                audio_file.write(response.content)
            
            print(f"✅ Audio saved to {temp_file}")
            
            # Play the MP3 file automatically using pygame
            play_mp3_file(temp_file)
            
        else:
            print(f"❌ ElevenLabs API Error: {response.json()}")
            
    except Exception as e:
        print(f"❌ Error with ElevenLabs API: {str(e)}")
        print(traceback.format_exc())