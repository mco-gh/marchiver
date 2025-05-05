import google.generativeai as genai

from app.core.config import GOOGLE_API_KEY, SUMMARIZATION_MODEL

class SummarizationService:
    """Service for summarizing content."""
    
    def __init__(self):
        """Initialize the summarization service."""
        # Set up Google Generative AI API
        if GOOGLE_API_KEY:
            genai.configure(api_key=GOOGLE_API_KEY)
        
        # Set up summarization model
        self.model_name = SUMMARIZATION_MODEL
        try:
            self.model = genai.GenerativeModel(self.model_name)
            self.model_initialized = True
        except Exception as e:
            print(f"Failed to initialize Gemini model: {e}")
            self.model_initialized = False
    
    async def summarize(self, text: str) -> str:
        """
        Summarize the given text.
        
        Args:
            text: The text to summarize.
            
        Returns:
            A summary of the text.
        """
        if not self.model_initialized:
            return self._create_fallback_summary(text)
        
        try:
            # Prepare the prompt
            prompt = f"""
            Please provide a concise summary of the following text. 
            Focus on the main points and key information.
            
            TEXT:
            {text}
            
            SUMMARY:
            """
            
            # Generate the summary
            response = self.model.generate_content(prompt)
            
            # Extract the summary from the response
            if hasattr(response, "text"):
                return response.text.strip()
            else:
                return self._create_fallback_summary(text)
        except Exception as e:
            print(f"Failed to summarize text: {e}")
            return self._create_fallback_summary(text)
    
    def _create_fallback_summary(self, text: str) -> str:
        """
        Create a simple fallback summary when the API fails.
        
        Args:
            text: The text to summarize.
            
        Returns:
            A simple summary of the text.
        """
        # Get the first few sentences as a simple summary
        sentences = text.split('.')
        if len(sentences) <= 3:
            return text  # Text is already short enough
        
        # Take first 3 sentences
        summary = '. '.join(sentences[:3]) + '.'
        
        return summary.strip()
