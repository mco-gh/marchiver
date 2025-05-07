#!/usr/bin/env python3
"""
Script to test the consistency of embeddings between different embedding generators.
"""

import os
import sys
import asyncio
import argparse
import json
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel

# Add the backend directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.embedding_service import EmbeddingService
from app.core.config import (
    GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_REGION
)

async def main(args):
    """Test the consistency of embeddings between different embedding generators."""
    print("Initializing embedding service...")
    embedding_service = EmbeddingService()
    
    # Get the search query from the command line arguments
    search_query = args.query
    
    print(f"\nGenerating embedding for search query using Google Generative AI API: '{search_query}'")
    
    # Generate embedding for the search query using Google Generative AI API
    query_embedding_google = await embedding_service.generate_embedding(search_query)
    print(f"Generated embedding with {len(query_embedding_google)} dimensions")
    
    # Now let's force the use of Vertex AI for the same query
    print(f"\nGenerating embedding for search query using Vertex AI: '{search_query}'")
    
    # Initialize Vertex AI
    aiplatform.init(
        project=GOOGLE_CLOUD_PROJECT,
        location=GOOGLE_CLOUD_REGION,
    )
    
    # Use Vertex AI Text Embedding Model directly
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings([search_query])
    
    if embeddings and len(embeddings) > 0 and embeddings[0].values:
        query_embedding_vertex = embeddings[0].values
        print(f"Generated embedding with {len(query_embedding_vertex)} dimensions")
        
        # Resize the embedding to 768 dimensions if needed
        if len(query_embedding_vertex) != 768:
            print(f"Resizing embedding from {len(query_embedding_vertex)} to 768 dimensions")
            if len(query_embedding_vertex) < 768:
                # Pad with zeros
                query_embedding_vertex = query_embedding_vertex + [0.0] * (768 - len(query_embedding_vertex))
            else:
                # Truncate
                query_embedding_vertex = query_embedding_vertex[:768]
    else:
        print("Failed to generate embedding using Vertex AI")
        return
    
    # Compare the two embeddings
    print("\nComparing the two embeddings:")
    
    # Calculate cosine similarity
    dot_product = sum(a * b for a, b in zip(query_embedding_google, query_embedding_vertex))
    magnitude_a = sum(a * a for a in query_embedding_google) ** 0.5
    magnitude_b = sum(b * b for b in query_embedding_vertex) ** 0.5
    
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
            print("This suggests that the two embedding generators are producing embeddings in different vector spaces.")
            print("This could explain why searches using one embedding generator don't find documents embedded with the other.")
    else:
        print("Could not calculate cosine similarity due to zero magnitude")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test embedding consistency")
    parser.add_argument("query", help="The search query")
    args = parser.parse_args()
    
    asyncio.run(main(args))
