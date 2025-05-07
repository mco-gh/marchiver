#!/usr/bin/env python3
"""
Script to test the vector search functionality.
"""

import os
import sys
import asyncio
import random
from typing import List

# Add the backend directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.models.document import DocumentCreate

async def main():
    """Test the vector search functionality."""
    print("Initializing services...")
    document_service = DocumentService()
    embedding_service = EmbeddingService()
    
    # Check if vector search is initialized
    print(f"Vector search initialized: {document_service.vector_search_initialized}")
    print(f"Index: {document_service.index}")
    print(f"Index endpoint: {document_service.index_endpoint}")
    print(f"Deployed index ID: {document_service.deployed_index_id}")
    
    # Create a test document
    print("\nCreating a test document...")
    test_document = DocumentCreate(
        content="This is a test document for vector search.",
        title="Vector Search Test",
        url="https://example.com/vector-search-test",
        summary="A test document for vector search functionality.",
        metadata={},
        tags=["test", "vector-search"],
        category="test",
        author="Test User",
    )
    
    # Generate an embedding for the test document
    print("\nGenerating embedding for the test document...")
    embedding = await embedding_service.generate_embedding(test_document.content)
    
    # Create the document
    print("\nSaving the document to Firestore and Vector Search...")
    document = await document_service.create_document(test_document, embedding)
    print(f"Document created with ID: {document.id}")
    
    # Wait a moment for the embedding to be indexed
    print("\nWaiting for the embedding to be indexed...")
    await asyncio.sleep(5)
    
    # Test semantic search
    print("\nTesting semantic search...")
    query_text = "vector search test"
    query_embedding = await embedding_service.generate_embedding(query_text)
    
    search_results = await document_service.semantic_search(query_embedding, limit=5)
    
    print(f"\nFound {len(search_results)} results for query: '{query_text}'")
    for i, doc in enumerate(search_results):
        print(f"{i+1}. {doc.title} - {doc.url}")
    
    # Delete the test document
    print("\nDeleting the test document...")
    await document_service.delete_document(document.id)
    print(f"Document {document.id} deleted.")

if __name__ == "__main__":
    asyncio.run(main())
