#!/usr/bin/env python3
"""
Script to delete all documents from the Firestore collection.
"""

import os
import sys
import asyncio

# Add the backend directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.document_service import DocumentService

async def main():
    """Delete all documents from the Firestore collection."""
    print("Initializing document service...")
    document_service = DocumentService()
    
    print("\nRetrieving all documents from Firestore...")
    # Get all documents from the collection
    all_docs = document_service.collection.get()
    
    total_docs = len(list(all_docs))
    print(f"Found {total_docs} documents to delete.")
    
    if total_docs == 0:
        print("No documents to delete. Collection is already empty.")
        return
    
    # Ask for confirmation
    confirm = input(f"Are you sure you want to delete all {total_docs} documents? (y/n): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        return
    
    # Delete each document
    print("\nDeleting documents...")
    deleted_count = 0
    
    # Get all documents again (since we consumed the iterator above)
    all_docs = document_service.collection.get()
    
    for doc in all_docs:
        doc_id = doc.id
        print(f"Deleting document with ID: {doc_id}")
        await document_service.delete_document(doc_id)
        deleted_count += 1
        print(f"Progress: {deleted_count}/{total_docs}")
    
    print(f"\nSuccessfully deleted {deleted_count} documents.")
    print("The Firestore collection is now empty.")

if __name__ == "__main__":
    asyncio.run(main())
