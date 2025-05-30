from .RAG import RAG
import asyncio
import re

class Chatbot:
    def __init__(self, memory, pdf_handler, csv_handler):
        self.memory = memory
        self.pdf_handler = pdf_handler
        self.csv_handler = csv_handler
        self.rag = RAG()  # Initialize the RAG class

    def process_input(self, user_input):
        # Add user message to memory (bot response will be added after generation)
        self.memory.add_message(user_input, None)
        response = self.generate_response(user_input)
        # Update last memory entry with bot response
        self.memory.conversation_history[-1]['bot'] = response
        return response

    def get_history_string(self):
        history = self.memory.get_history()
        history_str = ""
        for turn in history:
            history_str += f"User: {turn['user']}\n"
            if turn['bot']:
                history_str += f"Bot: {turn['bot']}\n"
        return history_str

    def generate_response(self, user_input):
        if self.is_question(user_input):
            return self.answer_question(user_input)
        elif self.is_summarization_request(user_input):
            return self.summarize_content(user_input)
        else:
            return "I'm sorry, I didn't understand that."

    def is_question(self, user_input):
        # Implement logic to identify questions
        return user_input.endswith('?')

    def is_summarization_request(self, user_input):
        # Implement logic to identify summarization requests
        return "summarize" in user_input.lower()

    def answer_question(self, question):
        history_str = self.get_history_string()
        response = asyncio.run(self.rag.user_input(question, history_str))
        return response

    def summarize_content(self, request):
        # Implement logic to summarize content based on the request
        return "Summary of the content."

    def get_conversation_history(self):
        return self.memory.get_history()

    def get_response(self, user_input):
        return self.process_input(user_input)

    def process_document(self, uploaded_file):
        if uploaded_file.type == "application/pdf":
            text = self.pdf_handler["extract_text_from_pdf"](uploaded_file)
            chunks = self.rag.get_text_chunks(text)
            self.rag.get_vector_store(chunks)  # Create the FAISS index
            summary = asyncio.run(self.pdf_handler["summarize_pdf"](text, self.rag))
            return summary
        elif uploaded_file.type == "text/csv":
            data = self.csv_handler["read_csv"](uploaded_file)
            chunks = self.rag.get_text_chunks(data.to_string())
            self.rag.get_vector_store(chunks)  # Create the FAISS index
            summary = asyncio.run(self.csv_handler["summarize_csv"](data, self.rag))
            return summary
        else:
            return "Unsupported file format."