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
    
    # Test with small text (should use Google API)
    small_text = "This is a test of the embedding service. It should generate an embedding vector for this text."
    
    print("\n=== Testing with small text ===")
    print(f"Generating embedding for text: '{small_text}'")
    try:
        small_embedding = await embedding_service.generate_embedding(small_text)
        
        # Print the first 5 values of the embedding and its length
        print(f"Embedding generated successfully!")
        print(f"Embedding length: {len(small_embedding)}")
        print(f"First 5 values: {small_embedding[:5]}")
    except Exception as e:
        print(f"Error generating embedding for small text: {e}")
        return False
    
    # Test with large text (should skip Google API and use Vertex AI)
    large_text = "x" * 40000  # Create a text larger than the 36000 byte limit
    
    print("\n=== Testing with large text ===")
    print(f"Generating embedding for large text (length: {len(large_text)} characters)")
    try:
        large_embedding = await embedding_service.generate_embedding(large_text)
        
        # Print the first 5 values of the embedding and its length
        print(f"Embedding generated successfully!")
        print(f"Embedding length: {len(large_embedding)}")
        print(f"First 5 values: {large_embedding[:5]}")
        
        return True
    except Exception as e:
        print(f"Error generating embedding for large text: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_embedding_service())
    if success:
        print("Test completed successfully!")
    else:
        print("Test failed!")
        sys.exit(1)
