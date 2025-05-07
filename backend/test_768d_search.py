#!/usr/bin/env python3
"""
Script to test the vector search functionality with the new 768-dimensional index.
"""

import os
import sys
import asyncio
from google.cloud import aiplatform

# Add the backend directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.core.config import (
    GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_REGION,
    VERTEX_AI_INDEX_ENDPOINT, VERTEX_AI_INDEX
)

async def main():
    """Test the vector search functionality with the new 768-dimensional index."""
    print("Initializing services...")
    document_service = DocumentService()
    embedding_service = EmbeddingService()
    
    # Check if vector search is initialized
    print(f"\nVector search initialized: {document_service.vector_search_initialized}")
    print(f"Index endpoint: {document_service.index_endpoint.name if document_service.index_endpoint else 'None'}")
    print(f"Deployed index ID: {document_service.deployed_index_id}")
    
    # Test query
    test_query = "How to implement vector search in a web application"
    print(f"\nGenerating embedding for test query: '{test_query}'")
    
    # Generate embedding for the test query
    query_embedding = await embedding_service.generate_embedding(test_query)
    print(f"Generated embedding with {len(query_embedding)} dimensions")
    
    # Perform semantic search
    print("\nPerforming semantic search...")
    results = await document_service.semantic_search(query_embedding, limit=5)
    
    # Print results
    print(f"\nFound {len(results)} results:")
    for i, doc in enumerate(results):
        print(f"\n{i+1}. {doc.title}")
        print(f"   URL: {doc.url}")
        print(f"   Summary: {doc.summary[:100]}..." if doc.summary and len(doc.summary) > 100 else f"   Summary: {doc.summary}")

if __name__ == "__main__":
    asyncio.run(main())
