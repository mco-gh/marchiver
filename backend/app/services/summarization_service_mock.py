"""
Mock summarization service for testing purposes.
Returns predefined summaries instead of calling Google Gemini.
"""

class SummarizationServiceMock:
    """Mock service for generating text summaries."""
    
    def __init__(self):
        """Initialize the mock summarization service."""
        print("Initialized Mock Summarization Service")
    
    async def summarize(self, text: str) -> str:
        """
        Generate a mock summary for the given text.
        
        Args:
            text: The text to summarize.
            
        Returns:
            A mock summary of the text.
        """
        # Get the first few words and last few words to create a mock summary
        words = text.split()
        
        if len(words) <= 10:
            return text  # Text is already short enough
        
        # Take first 10 words
        first_part = " ".join(words[:10])
        
        # Take last 5 words
        last_part = " ".join(words[-5:])
        
        # Create a mock summary
        mock_summary = f"{first_part} [...] {last_part}"
        
        print(f"Generated mock summary for text: {text[:50]}...")
        return mock_summary
