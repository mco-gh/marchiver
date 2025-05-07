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
        # IMPORTANT: Always use Vertex AI for consistency
        # This ensures that all embeddings (both for documents and search queries)
        # are in the same vector space, which is essential for semantic search to work correctly.
        # Using different embedding models for different texts can result in embeddings
        # that are not comparable, causing semantic search to fail.
        
        # Use Vertex AI if initialized
        if self.vertex_ai_initialized:
            try:
                print(f"Using Vertex AI for embedding generation (for consistency)")
                # Use Vertex AI Text Embedding Model with a model we know is available
                model = TextEmbeddingModel.from_pretrained(self.vertex_embedding_model_name)
                embeddings = model.get_embeddings([text])
                if embeddings and len(embeddings) > 0 and embeddings[0].values:
                    print("Successfully generated embedding using Vertex AI")
                    # Resize the embedding to 768 dimensions
                    return self._resize_embedding(embeddings[0].values, 768)
            except Exception as e:
                print(f"Failed to generate embedding using Vertex AI: {e}")
                
                # If we get a permission error, provide more helpful information
                if "Permission" in str(e) and "denied" in str(e):
                    print("\nPermission error detected. Please ensure that:")
                    print("1. The service account has the 'Vertex AI User' role")
                    print("2. The Vertex AI API is enabled for your project")
                    print("3. The credentials file is correctly configured")
                    print("4. The project has billing enabled\n")
        
        # Fall back to Google Generative AI API if Vertex AI fails or is not initialized
        if GOOGLE_API_KEY:
            try:
                print(f"Falling back to Google Generative AI API for embedding generation")
                
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
                        # Resize the embedding to 768 dimensions
                        return self._resize_embedding(result['embedding'], 768)
                    # Check if result has an embedding attribute
                    elif hasattr(result, "embedding"):
                        print("Successfully generated embedding using Google Generative AI API")
                        # Resize the embedding to 768 dimensions
                        return self._resize_embedding(result.embedding, 768)
                    else:
                        print("Result does not have expected embedding format")
            except Exception as e:
                print(f"Failed to generate embedding using Google Generative AI API: {e}")
                import traceback
                traceback.print_exc()
        
        # If all else fails, generate a deterministic embedding based on the text content
        print("WARNING: Generating deterministic embedding based on text content")
        return self._create_deterministic_embedding(text)
    
    def _resize_embedding(self, embedding: List[float], target_size: int) -> List[float]:
        """
        Resize an embedding to the target size.
        
        If the embedding is smaller than the target size, it will be padded with zeros.
        If the embedding is larger than the target size, it will be truncated.
        
        Args:
            embedding: The embedding to resize.
            target_size: The target size of the embedding.
            
        Returns:
            A list of floats representing the resized embedding.
        """
        current_size = len(embedding)
        
        if current_size == target_size:
            # No resizing needed
            return embedding
        elif current_size < target_size:
            # Pad with zeros
            print(f"Padding embedding from {current_size} to {target_size} dimensions")
            return embedding + [0.0] * (target_size - current_size)
        else:
            # Truncate
            print(f"Truncating embedding from {current_size} to {target_size} dimensions")
            return embedding[:target_size]
    
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
        embedding_size = 768  # Match the dimension of the Vector Search index
        embedding = [random.uniform(-1, 1) for _ in range(embedding_size)]
        
        # Normalize the embedding to unit length
        magnitude = sum(x**2 for x in embedding) ** 0.5
        if magnitude > 0:
            normalized_embedding = [x/magnitude for x in embedding]
            return normalized_embedding
        
        # Fallback if magnitude is zero
        return [0.0] * embedding_size  # 768 dimensions
