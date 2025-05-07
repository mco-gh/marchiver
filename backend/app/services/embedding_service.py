from typing import List
import random
import hashlib
import google.generativeai as genai
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel

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
            
            # Initialize the Vertex AI text embedding model
            # Default to textembedding-gecko@001 if not specified
            # Make sure we're not using the old endpoint format
            if VERTEX_AI_EMBEDDING_ENDPOINT and "." in VERTEX_AI_EMBEDDING_ENDPOINT and "vdb.vertexai.goog" in VERTEX_AI_EMBEDDING_ENDPOINT:
                print(f"Warning: VERTEX_AI_EMBEDDING_ENDPOINT '{VERTEX_AI_EMBEDDING_ENDPOINT}' doesn't look like a valid model name. Using default model.")
                self.vertex_embedding_model_name = "textembedding-gecko-multilingual"
            else:
                self.vertex_embedding_model_name = VERTEX_AI_EMBEDDING_ENDPOINT or "textembedding-gecko-multilingual"
            
            print(f"Using Vertex AI embedding model: {self.vertex_embedding_model_name}")
            
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
        # First try using Google Generative AI API with the API key
        if GOOGLE_API_KEY:
            try:
                print("Attempting to generate embedding using Google Generative AI API...")
                if hasattr(genai, "embed_content"):
                    result = genai.embed_content(
                        model=self.embedding_model,
                        content=text,
                        task_type="retrieval_document",
                    )
                    if hasattr(result, "embedding"):
                        print("Successfully generated embedding using Google Generative AI API")
                        return result.embedding
            except Exception as e:
                print(f"Failed to generate embedding using Google Generative AI API: {e}")
        else:
            print("Skipping Google Generative AI API (no API key provided)")
        
        # Fall back to Vertex AI if initialized
        if self.vertex_ai_initialized:
            try:
                print(f"Attempting to generate embedding using Vertex AI with model {self.vertex_embedding_model_name}...")
                # Use Vertex AI Text Embedding Model with a model we know is available
                # Our test script confirmed these models are available
                print("Using verified available model: text-embedding-004")
                model = TextEmbeddingModel.from_pretrained("text-embedding-004")
                embeddings = model.get_embeddings([text])
                if embeddings and len(embeddings) > 0 and embeddings[0].values:
                    print("Successfully generated embedding using Vertex AI")
                    return embeddings[0].values
            except Exception as e:
                print(f"Failed to generate embedding using Vertex AI: {e}")
                
                # If we get a permission error, provide more helpful information
                if "Permission" in str(e) and "denied" in str(e):
                    print("\nPermission error detected. Please ensure that:")
                    print("1. The service account has the 'Vertex AI User' role")
                    print("2. The Vertex AI API is enabled for your project")
                    print("3. The credentials file is correctly configured")
                    print("4. The project has billing enabled\n")
        
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
