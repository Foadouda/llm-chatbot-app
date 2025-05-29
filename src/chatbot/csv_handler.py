import pandas as pd

def read_csv(file_path):
    """Read a CSV file and return its content as a pandas DataFrame."""
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        return str(e)

def summarize_csv(data):
    """Summarize the content of a pandas DataFrame."""
    summary = {
        "columns": data.columns.tolist(),
        "num_rows": len(data),
        "sample_data": data.head().to_dict(orient='records')
    }
    return summary

def process_csv(file_path):
    """Process a CSV file by reading and summarizing its content."""
    data = read_csv(file_path)
    if isinstance(data, str):
        return {"error": data}
    
    summary = summarize_csv(data)
    return summary