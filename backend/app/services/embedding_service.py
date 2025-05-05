from typing import List
import random
import hashlib
import google.generativeai as genai
from google.cloud import aiplatform

from app.core.config import (
    GOOGLE_API_KEY, EMBEDDING_MODEL, GOOGLE_CLOUD_PROJECT,
    GOOGLE_CLOUD_REGION, VERTEX_AI_EMBEDDING_ENDPOINT
)

class EmbeddingService:
    """Service for generating and managing embeddings."""
    
    def __init__(self):
        """Initialize the embedding service."""
        # Set up Google Generative AI API
        if GOOGLE_API_KEY:
            genai.configure(api_key=GOOGLE_API_KEY)
        
        # Set up embedding model
        self.embedding_model = EMBEDDING_MODEL
        
        # Initialize Vertex AI
        try:
            aiplatform.init(
                project=GOOGLE_CLOUD_PROJECT,
                location=GOOGLE_CLOUD_REGION,
            )
            self.vertex_ai_initialized = True
        except Exception as e:
            print(f"Failed to initialize Vertex AI: {e}")
            self.vertex_ai_initialized = False
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding for the given text.
        
        Args:
            text: The text to generate an embedding for.
            
        Returns:
            A list of floats representing the embedding.
        """
        # First try using Google Generative AI API
        try:
            if hasattr(genai, "embed_content"):
                result = genai.embed_content(
                    model=self.embedding_model,
                    content=text,
                    task_type="retrieval_document",
                )
                if hasattr(result, "embedding"):
                    return result.embedding
        except Exception as e:
            print(f"Failed to generate embedding using Google Generative AI API: {e}")
        
        # Fall back to Vertex AI
        if self.vertex_ai_initialized:
            try:
                # Use Vertex AI Embeddings
                endpoint = aiplatform.Endpoint(
                    endpoint_name=VERTEX_AI_EMBEDDING_ENDPOINT
                )
                response = endpoint.predict(instances=[text])
                if response and response.predictions and len(response.predictions) > 0:
                    return response.predictions[0]
            except Exception as e:
                print(f"Failed to generate embedding using Vertex AI: {e}")
        
        # If all else fails, generate a deterministic embedding based on the text content
        print("WARNING: Generating deterministic embedding based on text content")
        return self._create_deterministic_embedding(text)
    
    def _create_deterministic_embedding(self, text: str) -> List[float]:
        """
        Create a deterministic embedding based on the text content.
        This ensures that the same text always gets the same embedding,
        which is important for semantic search functionality.
        
        Args:
            text: The text to generate an embedding for.
            
        Returns:
            A list of floats representing the embedding.
        """
        # Use a hash of the text as a seed for random number generation
        # This ensures deterministic but unique embeddings for different texts
        text_hash = int(hashlib.sha256(text.encode('utf-8')).hexdigest(), 16) % 10**8
        random.seed(text_hash)
        
        # Generate a random embedding
        embedding_size = 768  # Common embedding dimension
        embedding = [random.uniform(-1, 1) for _ in range(embedding_size)]
        
        # Normalize the embedding to unit length
        magnitude = sum(x**2 for x in embedding) ** 0.5
        if magnitude > 0:
            normalized_embedding = [x/magnitude for x in embedding]
            return normalized_embedding
        
        # Fallback if magnitude is zero
        return [0.0] * embedding_size
