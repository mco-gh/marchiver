import asyncio
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.services.embedding_service import EmbeddingService

async def test_embedding_service():
    """Test the embedding service."""
    print("Initializing embedding service...")
    embedding_service = EmbeddingService()
    
    # Test text
    test_text = "This is a test of the embedding service. It should generate an embedding vector for this text."
    
    print(f"Generating embedding for text: '{test_text}'")
    try:
        embedding = await embedding_service.generate_embedding(test_text)
        
        # Print the first 5 values of the embedding and its length
        print(f"Embedding generated successfully!")
        print(f"Embedding length: {len(embedding)}")
        print(f"First 5 values: {embedding[:5]}")
        
        return True
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_embedding_service())
    if success:
        print("Test completed successfully!")
    else:
        print("Test failed!")
        sys.exit(1)
