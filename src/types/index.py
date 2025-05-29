from typing import Any, Dict, List, Optional, Tuple

# Define a type for the user input
UserInput = str

# Define a type for the chatbot response
ChatbotResponse = str

# Define a type for conversation history
ConversationHistory = List[Tuple[UserInput, ChatbotResponse]]

# Define a type for document types that can be processed
DocumentType = str

# Define a type for the memory structure
Memory = Dict[str, Any]

# Define a type for the supported file formats
SupportedFileFormats = Tuple[str, str, str]  # e.g., ('pdf', 'csv', 'arxiv')

# Define a type for the summarization result
SummarizationResult = str

# Define a type for the question-answering result
QuestionAnsweringResult = Optional[str]  # Can be None if no answer is found

# Define a type for the chatbot configuration
ChatbotConfig = Dict[str, Any]