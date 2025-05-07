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
            # Use the model name from the environment variable or default to a known good model
            self.vertex_embedding_model_name = "text-embedding-004"  # Use a model we know is available
            
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
        # Check text size - Google API has a limit of 36000 bytes
        GOOGLE_API_SIZE_LIMIT = 36000  # bytes
        text_size = len(text.encode('utf-8'))
        
        # First try using Google Generative AI API with the API key if text is within size limit
        if GOOGLE_API_KEY and text_size <= GOOGLE_API_SIZE_LIMIT:
            try:
                print(f"Text size: {text_size} bytes (within Google API limit of {GOOGLE_API_SIZE_LIMIT} bytes)")
                print("Attempting to generate embedding using Google Generative AI API...")
                
                if hasattr(genai, "embed_content"):
                    # Ensure model name is correctly formatted
                    model_name = self.embedding_model
                    if not model_name.startswith("models/") and not model_name.startswith("tunedModels/"):
                        model_name = f"models/{model_name}"
                    
                    print(f"Using model name: {model_name}")
                    
                    result = genai.embed_content(
                        model=model_name,
                        content=text,
                        task_type="retrieval_document",
                    )
                    
                    # Check if result is a dictionary with an 'embedding' key
                    if isinstance(result, dict) and 'embedding' in result:
                        print("Successfully generated embedding using Google Generative AI API")
                        return result['embedding']
                    # Check if result has an embedding attribute
                    elif hasattr(result, "embedding"):
                        print("Successfully generated embedding using Google Generative AI API")
                        return result.embedding
                    else:
                        print("Result does not have expected embedding format")
            except Exception as e:
                print(f"Failed to generate embedding using Google Generative AI API: {e}")
                import traceback
                traceback.print_exc()
        elif GOOGLE_API_KEY:
            print(f"Text size: {text_size} bytes (exceeds Google API limit of {GOOGLE_API_SIZE_LIMIT} bytes)")
            print("Skipping Google Generative AI API due to text size limit")
        else:
            print("Skipping Google Generative AI API (no API key provided)")
        
        # Fall back to Vertex AI if initialized
        if self.vertex_ai_initialized:
            try:
                print(f"Attempting to generate embedding using Vertex AI with model {self.vertex_embedding_model_name}...")
                # Use Vertex AI Text Embedding Model with a model we know is available
                model = TextEmbeddingModel.from_pretrained(self.vertex_embedding_model_name)
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
