import streamlit as st
from chatbot.chatbot import Chatbot
from chatbot.memory import Memory
from chatbot.pdf_handler import extract_text_from_pdf, summarize_pdf
from chatbot.csv_handler import read_csv, summarize_csv
from chatbot.TTS import speak_with_elevenlabs
from chatbot.STT import SpeechToText
import sys
import os
import logging
import os
import shutil
import datetime
import re
import time 

current_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(current_dir,"utils"))
from helpers import clean_for_tts 


#from utils.helpers import clean_for_tts
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Calculate project root and recordings directory dynamically
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RECORDINGS_DIR = os.path.join(PROJECT_ROOT, 'recordings')

# Create the recordings directory if it doesn't exist
os.makedirs(RECORDINGS_DIR, exist_ok=True)

def main():
    st.title("LLM-Powered Chatbot")
    st.write("Ask me anything or upload a document (PDF, CSV, arXiv) for summarization or question-answering.")

    # Initialize STT
    if 'stt' not in st.session_state:
        try:
            st.session_state.stt = SpeechToText(RECORDINGS_DIR)
            logger.info("STT initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing STT: {str(e)}")
            st.error("Failed to initialize speech recognition. Please refresh the page.")
            return
    
    # Initialize recording state
    if 'is_recording' not in st.session_state:
        st.session_state.is_recording = False

    memory = Memory()
    pdf_handler = {
        "extract_text_from_pdf": extract_text_from_pdf,
        "summarize_pdf": summarize_pdf
    }
    csv_handler = {
        "read_csv": read_csv,
        "summarize_csv": summarize_csv
    }
    chatbot = Chatbot(memory, pdf_handler, csv_handler)

    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    # Create a single column layout for text input and voice input
    col1 = st.container()
    
    # Initialize last_voice_input in session state if it doesn't exist
    if 'last_voice_input' not in st.session_state:
        st.session_state.last_voice_input = ""

    with col1:
        # Use session state to manage the text input value
        user_input = st.text_input("You:", value=st.session_state.last_voice_input)
        # Reset last_voice_input after using it to populate the text_input
        st.session_state.last_voice_input = ""

        # Place the voice input button below the text input within the same column
        if st.button("🎤 Voice Input"):
            # Set the recording state and trigger a rerun to show the spinner
            st.session_state.is_recording = True
            # Clear any previous voice input before starting a new recording
            st.session_state.last_voice_input = ""
            st.rerun() # Trigger a rerun

    # This block runs on the rerun triggered by the voice input button click
    if st.session_state.is_recording:
        try:
            with st.spinner("Recording... Press Enter to stop"):
                # Record and transcribe (blocking call)
                text = st.session_state.stt.listen()

            # Add a small delay to allow spinner to disappear
            time.sleep(0.1)

            # Once listen() returns, the spinner should disappear.
            # Process the result on the next rerun.
            if text and text != "No audio recorded.":
                st.session_state.last_voice_input = text
                st.success("Recording completed!")
            else:
                st.error("No audio was recorded or transcription failed.")

            # Reset recording state regardless of success/failure of transcription
            st.session_state.is_recording = False
            st.rerun() # Trigger a rerun

        except Exception as e:
            logger.error(f"Error during voice input: {str(e)}")
            st.error("An error occurred during voice recording. Please try again.")
            # Reset recording state on error
            st.session_state.is_recording = False
            st.rerun() # Trigger a rerun

    # Process text input or transcribed voice input (if available)
    # This will run after the rerun triggered by successful recording
    if user_input and not st.session_state.is_recording:
        try:
            response = chatbot.get_response(user_input)
            st.session_state.conversation.append({"user": user_input, "bot": response})
            cleaned_response = clean_for_tts(response)
            speak_with_elevenlabs(cleaned_response, RECORDINGS_DIR)
            # Clear the text input field after sending
            st.session_state.last_voice_input = "" # Clear the session state variable used for text_input
            st.rerun() # Trigger a rerun to clear the input box and show new conversation
        except Exception as e:
            logger.error(f"Error processing user input: {str(e)}")
            st.error("An error occurred while processing your message. Please try again.")

    # Display conversation history
    if st.session_state.conversation:
        st.write("---")
        st.subheader("Conversation History")
        for chat in st.session_state.conversation:
            st.write(f"You: {chat['user']}")
            st.write(f"Bot: {chat['bot']}")
            st.write("---")

    # Document upload section
    st.write("---")
    st.subheader("Document Processing")
    uploaded_file = st.file_uploader("Upload a document", type=["pdf", "csv"])
    if uploaded_file is not None:
        try:
            document_summary = chatbot.process_document(uploaded_file)
            st.write("Document Summary:")
            st.write(document_summary)
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            st.error("An error occurred while processing the document. Please try again.")

if __name__ == "__main__":
    main()