"""
Mock embedding service for testing purposes.
Returns dummy embeddings instead of calling Google Vertex AI.
"""

from typing import List
import random

class EmbeddingServiceMock:
    """Mock service for generating and managing embeddings."""
    
    def __init__(self):
        """Initialize the mock embedding service."""
        print("Initialized Mock Embedding Service")
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate a mock embedding for the given text.
        
        Args:
            text: The text to generate an embedding for.
            
        Returns:
            A list of floats representing the mock embedding.
        """
        # Generate a deterministic but unique embedding based on the text
        # This ensures that the same text always gets the same embedding
        random.seed(hash(text))
        embedding_size = 768  # Common embedding dimension
        mock_embedding = [random.uniform(-1, 1) for _ in range(embedding_size)]
        
        # Normalize the embedding
        magnitude = sum(x**2 for x in mock_embedding) ** 0.5
        normalized_embedding = [x/magnitude for x in mock_embedding]
        
        print(f"Generated mock embedding for text: {text[:50]}...")
        return normalized_embedding
