import pandas as pd
import asyncio # Import asyncio for awaiting

def read_csv(file_path):
    """Read a CSV file and return its content as a pandas DataFrame."""
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        return str(e)

async def summarize_csv(data: pd.DataFrame, rag_model):
    """Generate a natural language summary of a pandas DataFrame using the LLM."""
    try:
        # Convert DataFrame to a string format for summarization
        # Include column names and some sample data or the whole data as a string
        # For potentially large CSVs, summarizing the head or a representation might be better
        # For simplicity, let's convert the whole dataframe to string for now, similar to RAG chunking
        text_data = data.to_string()
        
        # Use the RAG model's summarize method
        summary = await rag_model.summarize(text_data)
        return summary
    except Exception as e:
        # Log the error and return an informative message
        print(f"Error during CSV summarization: {e}") # Consider using logger here
        return "An error occurred while generating the CSV summary."

def process_csv(file_path):
    """Process a CSV file by reading and summarizing its content."""
    data = read_csv(file_path)
    if isinstance(data, str):
        return {"error": data}
    
    # The summarization is now async and happens in chatbot.py's process_document
    # This function might become redundant or need refactoring depending on overall flow.
    # For now, we'll keep it but the primary summarization call is elsewhere.
    return "CSV processed for summarization."