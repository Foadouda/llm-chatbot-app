import re

def format_response(response):
    """Format the chatbot's response for display."""
    return response.strip()

def manage_file_upload(uploaded_file):
    """Handle file uploads and return the file content."""
    if uploaded_file is not None:
        return uploaded_file.read()
    return None

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    # Placeholder for PDF extraction logic
    return "Extracted text from PDF."

def extract_text_from_csv(csv_file):
    """Extract text from a CSV file."""
    # Placeholder for CSV extraction logic
    return "Extracted text from CSV."

def extract_text_from_arxiv(arxiv_id):
    """Fetch and extract text from an arXiv document."""
    # Placeholder for arXiv fetching logic
    return "Extracted text from arXiv."

def clean_for_tts(text):
    # Remove markdown bullet points, asterisks, and extra whitespace
    text = re.sub(r'[\*•]+', '', text)  # Remove asterisks and bullet points
    text = re.sub(r'\n+', '. ', text)  # Replace newlines with a period and space
    text = re.sub(r'\s+', ' ', text)   # Collapse multiple spaces
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Remove bold markdown
    text = re.sub(r'\*([^*]+)\*', r'\1', text)        # Remove italic markdown
    return text.strip()