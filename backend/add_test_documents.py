#!/usr/bin/env python3
"""
Script to add test documents to the new 768-dimensional index.
"""

import os
import sys
import asyncio
import random
from datetime import datetime, timezone

# Add the backend directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.document import DocumentCreate
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService

async def main():
    """Add test documents to the new 768-dimensional index."""
    print("Initializing services...")
    document_service = DocumentService()
    embedding_service = EmbeddingService()
    
    # Check if vector search is initialized
    print(f"\nVector search initialized: {document_service.vector_search_initialized}")
    print(f"Index endpoint: {document_service.index_endpoint.name if document_service.index_endpoint else 'None'}")
    print(f"Deployed index ID: {document_service.deployed_index_id}")
    
    # Test documents
    test_documents = [
        {
            "title": "Vector Search Implementation Guide",
            "content": """
            Vector search is a powerful technique for finding similar items in a large dataset.
            It works by converting items into high-dimensional vectors and finding the nearest neighbors in the vector space.
            This guide will show you how to implement vector search in your application using Google Vertex AI Vector Search.
            
            First, you need to create an index with the appropriate dimensions and distance measure.
            Then, you need to add your embeddings to the index.
            Finally, you can query the index to find similar items.
            
            Vector search is particularly useful for semantic search, recommendation systems, and image search.
            """,
            "url": "https://example.com/vector-search-guide",
            "summary": "A comprehensive guide to implementing vector search in your application using Google Vertex AI Vector Search.",
            "tags": ["vector search", "machine learning", "google cloud", "vertex ai"],
            "category": "Technical Guide",
        },
        {
            "title": "Introduction to Embeddings",
            "content": """
            Embeddings are dense vector representations of data that capture semantic meaning.
            They are used in various machine learning applications, including natural language processing and recommendation systems.
            
            There are several ways to generate embeddings, including:
            1. Using pre-trained models like BERT, GPT, or Word2Vec
            2. Training your own embedding model on your specific data
            3. Using cloud services like Google's Vertex AI
            
            Embeddings work by mapping similar items to nearby points in a high-dimensional space.
            This allows for efficient similarity search and clustering.
            """,
            "url": "https://example.com/embeddings-intro",
            "summary": "An introduction to embeddings, their applications, and how they work.",
            "tags": ["embeddings", "machine learning", "nlp"],
            "category": "Educational",
        },
        {
            "title": "Building a Semantic Search Engine",
            "content": """
            Semantic search goes beyond keyword matching to understand the meaning behind a query.
            By using embeddings and vector search, you can build a search engine that returns results based on semantic similarity.
            
            Here's how to build a semantic search engine:
            1. Generate embeddings for your documents
            2. Store the embeddings in a vector database
            3. When a user submits a query, generate an embedding for the query
            4. Find the documents with embeddings most similar to the query embedding
            5. Return the results to the user
            
            This approach can significantly improve search quality compared to traditional keyword-based search.
            """,
            "url": "https://example.com/semantic-search-engine",
            "summary": "A guide to building a semantic search engine using embeddings and vector search.",
            "tags": ["semantic search", "vector search", "search engine"],
            "category": "Tutorial",
        },
        {
            "title": "Chrome Extension Development",
            "content": """
            Chrome extensions are a powerful way to extend the functionality of the Chrome browser.
            They can add new features, modify web pages, and integrate with other services.
            
            To develop a Chrome extension, you need to:
            1. Create a manifest.json file that defines the extension's properties
            2. Implement the extension's functionality using HTML, CSS, and JavaScript
            3. Test the extension in Chrome
            4. Publish the extension to the Chrome Web Store
            
            Chrome extensions can use various APIs to interact with the browser and web pages.
            """,
            "url": "https://example.com/chrome-extension-dev",
            "summary": "A guide to developing Chrome extensions, including manifest configuration and API usage.",
            "tags": ["chrome", "extension", "web development"],
            "category": "Development",
        },
        {
            "title": "Web Archiving Techniques",
            "content": """
            Web archiving is the process of collecting and preserving web content for future access.
            It's important for preserving digital history, research, and compliance purposes.
            
            Common web archiving techniques include:
            1. Crawling websites and saving the content
            2. Taking screenshots or full-page captures
            3. Saving the HTML, CSS, and JavaScript files
            4. Using specialized archiving tools like Archive.org's Wayback Machine
            
            When archiving web content, it's important to consider issues like JavaScript-heavy sites,
            dynamic content, authentication requirements, and robots.txt restrictions.
            """,
            "url": "https://example.com/web-archiving",
            "summary": "An overview of web archiving techniques and considerations for preserving web content.",
            "tags": ["web archiving", "digital preservation", "web crawling"],
            "category": "Information Management",
        },
    ]
    
    # Add each test document
    for i, doc_data in enumerate(test_documents):
        print(f"\nAdding test document {i+1}/{len(test_documents)}: {doc_data['title']}")
        
        # Create a DocumentCreate object
        doc_create = DocumentCreate(
            title=doc_data["title"],
            content=doc_data["content"],
            url=doc_data["url"],
            summary=doc_data["summary"],
            tags=doc_data["tags"],
            category=doc_data["category"],
            metadata={
                "source": "test_script",
                "test_id": f"test_{i+1}",
            },
            author="Test Script",
            date=datetime.now(timezone.utc).isoformat(),
        )
        
        # Generate embedding for the document
        print(f"Generating embedding for document...")
        embedding = await embedding_service.generate_embedding(doc_data["content"])
        print(f"Generated embedding with {len(embedding)} dimensions")
        
        # Create the document
        print(f"Creating document in Firestore and Vector Search...")
        doc = await document_service.create_document(doc_create, embedding)
        print(f"Successfully created document with ID: {doc.id}")
    
    print("\nAll test documents added successfully!")

if __name__ == "__main__":
    asyncio.run(main())
