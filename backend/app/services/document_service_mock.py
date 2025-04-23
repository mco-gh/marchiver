"""
Mock document service for testing purposes.
Uses in-memory storage instead of Firestore and Vertex AI.
"""

from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
import json

from app.models.document import Document, DocumentCreate, DocumentUpdate

class DocumentServiceMock:
    """Mock service for document operations."""
    
    def __init__(self):
        """Initialize the mock document service."""
        print("Initialized Mock Document Service")
        # Use an in-memory dictionary to store documents
        self.documents = {}
    
    async def create_document(self, document: DocumentCreate, embedding: List[float]) -> Document:
        """Create a new document."""
        # Create a new document
        doc = Document(
            content=document.content,
            title=document.title,
            url=document.url,
            summary=document.summary,
            metadata=document.metadata,
            tags=document.tags,
            category=document.category,
            embedding=embedding,
            author=document.author,
            date=document.date or datetime.now(),
        )
        
        # Save to in-memory storage
        self.documents[doc.id] = doc.dict()
        
        print(f"Created document: {doc.id} - {doc.title}")
        return doc
    
    async def get_document(self, document_id: str) -> Optional[Document]:
        """Get a document by ID."""
        if document_id not in self.documents:
            return None
        
        return Document(**self.documents[document_id])
    
    async def update_document(
        self, document_id: str, document_update: DocumentUpdate, embedding: Optional[List[float]] = None
    ) -> Document:
        """Update a document."""
        if document_id not in self.documents:
            return None
        
        # Get the current document
        current_doc = Document(**self.documents[document_id])
        
        # Update the document
        update_data = document_update.dict(exclude_unset=True)
        
        # If embedding is provided, update it
        if embedding:
            update_data["embedding"] = embedding
        
        # Increment the version
        update_data["version"] = current_doc.version + 1
        
        # Update the document
        self.documents[document_id].update(update_data)
        
        print(f"Updated document: {document_id}")
        return Document(**self.documents[document_id])
    
    async def delete_document(self, document_id: str) -> None:
        """Delete a document."""
        if document_id in self.documents:
            del self.documents[document_id]
            print(f"Deleted document: {document_id}")
    
    async def semantic_search(
        self, query_embedding: List[float], limit: int = 10, offset: int = 0
    ) -> List[Document]:
        """
        Perform semantic search using the query embedding.
        For mock purposes, just return some documents.
        """
        # For simplicity, just return some documents
        docs = list(self.documents.values())
        return [Document(**doc) for doc in docs[offset:offset+limit]]
    
    async def full_text_search(
        self, query: str, limit: int = 10, offset: int = 0
    ) -> List[Document]:
        """
        Perform full-text search.
        For mock purposes, just return documents that contain the query.
        """
        matching_docs = []
        
        for doc_id, doc_data in self.documents.items():
            # Check if query is in content, title, or summary
            if (query.lower() in doc_data.get("content", "").lower() or
                query.lower() in doc_data.get("title", "").lower() or
                query.lower() in doc_data.get("summary", "").lower()):
                matching_docs.append(Document(**doc_data))
                
                if len(matching_docs) >= limit + offset:
                    break
        
        return matching_docs[offset:offset+limit]
    
    async def get_recent_documents(
        self, limit: int = 10, offset: int = 0
    ) -> List[Document]:
        """
        Get the most recent documents.
        """
        # Convert to list of Document objects
        docs = [Document(**doc) for doc in self.documents.values()]
        
        # Sort by date
        docs.sort(key=lambda x: x.date, reverse=True)
        
        return docs[offset:offset+limit]
    
    async def find_similar_documents(
        self, embedding: List[float], limit: int = 10, exclude_ids: List[str] = None
    ) -> List[Document]:
        """
        Find documents similar to the given embedding.
        For mock purposes, just return some documents.
        """
        # For simplicity, just return some documents
        docs = list(self.documents.values())
        
        # Filter out excluded IDs
        if exclude_ids:
            docs = [doc for doc in docs if doc["id"] not in exclude_ids]
        
        return [Document(**doc) for doc in docs[:limit]]
