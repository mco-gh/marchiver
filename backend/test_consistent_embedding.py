#!/usr/bin/env python3
"""
Script to test the consistent embedding service.
"""

import os
import sys
import asyncio
import argparse
import json
import importlib.util

# Add the backend directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the consistent embedding service
spec = importlib.util.spec_from_file_location(
    "embedding_service_consistent", 
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "app/services/embedding_service_consistent.py")
)
embedding_service_consistent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(embedding_service_consistent)

# Import the original embedding service for comparison
from app.services.embedding_service import EmbeddingService as OriginalEmbeddingService

async def main(args):
    """Test the consistent embedding service."""
    print("Initializing embedding services...")
    original_embedding_service = OriginalEmbeddingService()
    consistent_embedding_service = embedding_service_consistent.EmbeddingService()
    
    # Get the search query from the command line arguments
    search_query = args.query
    
    print(f"\nGenerating embedding for search query using original embedding service: '{search_query}'")
    
    # Generate embedding for the search query using the original embedding service
    query_embedding_original = await original_embedding_service.generate_embedding(search_query)
    print(f"Generated embedding with {len(query_embedding_original)} dimensions")
    
    print(f"\nGenerating embedding for search query using consistent embedding service: '{search_query}'")
    
    # Generate embedding for the search query using the consistent embedding service
    query_embedding_consistent = await consistent_embedding_service.generate_embedding(search_query)
    print(f"Generated embedding with {len(query_embedding_consistent)} dimensions")
    
    # Compare the two embeddings
    print("\nComparing the two embeddings:")
    
    # Calculate cosine similarity
    dot_product = sum(a * b for a, b in zip(query_embedding_original, query_embedding_consistent))
    magnitude_a = sum(a * a for a in query_embedding_original) ** 0.5
    magnitude_b = sum(b * b for b in query_embedding_consistent) ** 0.5
    
    if magnitude_a > 0 and magnitude_b > 0:
        cosine_similarity = dot_product / (magnitude_a * magnitude_b)
        print(f"Cosine similarity: {cosine_similarity}")
        
        # Interpret the similarity
        if cosine_similarity > 0.9:
            print("The embeddings are very similar (>0.9)")
        elif cosine_similarity > 0.7:
            print("The embeddings are somewhat similar (0.7-0.9)")
        elif cosine_similarity > 0.5:
            print("The embeddings are moderately similar (0.5-0.7)")
        else:
            print("The embeddings are not very similar (<0.5)")
    else:
        print("Could not calculate cosine similarity due to zero magnitude")
    
    # Now test with a longer text that would normally use different embedding generators
    print("\n\nTesting with a longer text that would normally use different embedding generators:")
    
    # Create a longer text (simulating a Wikipedia page)
    longer_text = "The University of Surrey is a public research university in Guildford, Surrey, England. " * 100
    print(f"Text length: {len(longer_text)} characters")
    
    print("\nGenerating embedding for longer text using original embedding service:")
    
    # Generate embedding for the longer text using the original embedding service
    longer_embedding_original = await original_embedding_service.generate_embedding(longer_text)
    print(f"Generated embedding with {len(longer_embedding_original)} dimensions")
    
    print("\nGenerating embedding for longer text using consistent embedding service:")
    
    # Generate embedding for the longer text using the consistent embedding service
    longer_embedding_consistent = await consistent_embedding_service.generate_embedding(longer_text)
    print(f"Generated embedding with {len(longer_embedding_consistent)} dimensions")
    
    # Compare the embeddings for the search query and the longer text using the consistent embedding service
    print("\nComparing the search query embedding and longer text embedding using the consistent embedding service:")
    
    # Calculate cosine similarity
    dot_product = sum(a * b for a, b in zip(query_embedding_consistent, longer_embedding_consistent))
    magnitude_a = sum(a * a for a in query_embedding_consistent) ** 0.5
    magnitude_b = sum(b * b for b in longer_embedding_consistent) ** 0.5
    
    if magnitude_a > 0 and magnitude_b > 0:
        cosine_similarity = dot_product / (magnitude_a * magnitude_b)
        print(f"Cosine similarity: {cosine_similarity}")
        
        # Interpret the similarity
        if cosine_similarity > 0.9:
            print("The embeddings are very similar (>0.9)")
        elif cosine_similarity > 0.7:
            print("The embeddings are somewhat similar (0.7-0.9)")
        elif cosine_similarity > 0.5:
            print("The embeddings are moderately similar (0.5-0.7)")
        else:
            print("The embeddings are not very similar (<0.5)")
            print("But they are at least in the same vector space, so semantic search should work.")
    else:
        print("Could not calculate cosine similarity due to zero magnitude")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test consistent embedding service")
    parser.add_argument("query", help="The search query")
    args = parser.parse_args()
    
    asyncio.run(main(args))
