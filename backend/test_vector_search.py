#!/usr/bin/env python3
"""
Script to test the vector search functionality from the command line.
"""

import os
import sys
import asyncio
import argparse
import json
from google.cloud import aiplatform

# Add the backend directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.core.config import (
    GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_REGION,
    VERTEX_AI_INDEX_ENDPOINT, VERTEX_AI_INDEX
)

async def main(args):
    """Test the vector search functionality from the command line."""
    print("Initializing services...")
    document_service = DocumentService()
    embedding_service = EmbeddingService()
    
    # Check if vector search is initialized
    print(f"\nVector search initialized: {document_service.vector_search_initialized}")
    print(f"Index endpoint: {document_service.index_endpoint.name if document_service.index_endpoint else 'None'}")
    print(f"Deployed index ID: {document_service.deployed_index_id}")
    
    # Get the search query from the command line arguments
    search_query = args.query
    
    print(f"\nGenerating embedding for search query: '{search_query}'")
    
    # Generate embedding for the search query
    query_embedding = await embedding_service.generate_embedding(search_query)
    print(f"Generated embedding with {len(query_embedding)} dimensions")
    
    # Perform semantic search
    print("\nPerforming semantic search...")
    results = await document_service.semantic_search(query_embedding, limit=args.limit)
    
    # Print results
    print(f"\nFound {len(results)} results:")
    for i, doc in enumerate(results):
        print(f"\n{i+1}. {doc.title}")
        print(f"   URL: {doc.url}")
        print(f"   Summary: {doc.summary[:100]}..." if doc.summary and len(doc.summary) > 100 else f"   Summary: {doc.summary}")
    
    # Convert the results to JSON
    if args.json:
        results_json = []
        for doc in results:
            results_json.append({
                "id": doc.id,
                "title": doc.title,
                "url": doc.url,
                "summary": doc.summary,
                "tags": doc.tags,
                "category": doc.category,
                "date": doc.date,
            })
        
        # Print the JSON response
        print("\nJSON response:")
        print(json.dumps(results_json, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test vector search functionality")
    parser.add_argument("query", help="The search query")
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of results to return")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()
    
    asyncio.run(main(args))
