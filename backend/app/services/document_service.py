from typing import List, Optional, Dict, Any
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import aiplatform
import os
import json

from app.models.document import Document, DocumentCreate, DocumentUpdate
from app.core.config import (
    GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_REGION,
    VERTEX_AI_INDEX_ENDPOINT, VERTEX_AI_INDEX, FIRESTORE_COLLECTION
)

class DocumentService:
    """Service for document operations."""
    
    def __init__(self):
        """Initialize the document service."""
        # Initialize Firestore
        if not firebase_admin._apps:
            # Use environment variable or default to a local file
            cred_path = GOOGLE_APPLICATION_CREDENTIALS or "firebase-credentials.json"
            try:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            except Exception as e:
                print(f"Failed to initialize Firebase: {e}")
                # For development, we can use a mock implementation
                pass
        
        self.db = firestore.client()
        self.collection = self.db.collection(FIRESTORE_COLLECTION)
        
        # Initialize Vertex AI Vector Search
        self.vector_search_initialized = False
        try:
            aiplatform.init(
                project=GOOGLE_CLOUD_PROJECT,
                location=GOOGLE_CLOUD_REGION,
            )
            self.vector_search_initialized = True
            self.index_endpoint_name = VERTEX_AI_INDEX_ENDPOINT
            self.index_name = VERTEX_AI_INDEX
        except Exception as e:
            print(f"Failed to initialize Vertex AI Vector Search: {e}")
    
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
            date=document.date or Document().date,
        )
        
        # Save to Firestore
        doc_ref = self.collection.document(doc.id)
        doc_ref.set(doc.dict())
        
        # If Vector Search is initialized, add the embedding
        if self.vector_search_initialized:
            try:
                self._add_embedding_to_vector_search(doc.id, embedding)
            except Exception as e:
                print(f"Failed to add embedding to Vector Search: {e}")
        
        return doc
    
    async def get_document(self, document_id: str) -> Optional[Document]:
        """Get a document by ID."""
        doc_ref = self.collection.document(document_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return None
        
        return Document(**doc.to_dict())
    
    async def update_document(
        self, document_id: str, document_update: DocumentUpdate, embedding: Optional[List[float]] = None
    ) -> Document:
        """Update a document."""
        doc_ref = self.collection.document(document_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return None
        
        # Get the current document
        current_doc = Document(**doc.to_dict())
        
        # Update the document
        update_data = document_update.dict(exclude_unset=True)
        
        # If embedding is provided, update it
        if embedding:
            update_data["embedding"] = embedding
            
            # If Vector Search is initialized, update the embedding
            if self.vector_search_initialized:
                try:
                    self._update_embedding_in_vector_search(document_id, embedding)
                except Exception as e:
                    print(f"Failed to update embedding in Vector Search: {e}")
        
        # Increment the version
        update_data["version"] = current_doc.version + 1
        
        # Update the document
        doc_ref.update(update_data)
        
        # Get the updated document
        updated_doc = doc_ref.get()
        
        return Document(**updated_doc.to_dict())
    
    async def delete_document(self, document_id: str) -> None:
        """Delete a document."""
        doc_ref = self.collection.document(document_id)
        
        # Delete from Firestore
        doc_ref.delete()
        
        # If Vector Search is initialized, delete the embedding
        if self.vector_search_initialized:
            try:
                self._delete_embedding_from_vector_search(document_id)
            except Exception as e:
                print(f"Failed to delete embedding from Vector Search: {e}")
    
    async def semantic_search(
        self, query_embedding: List[float], limit: int = 10, offset: int = 0
    ) -> List[Document]:
        """
        Perform semantic search using the query embedding.
        """
        if not self.vector_search_initialized:
            # If Vector Search is not initialized, return empty list
            return []
        
        try:
            # Get similar documents from Vector Search
            similar_doc_ids = self._find_similar_embeddings(query_embedding, limit + offset)
            
            # Get the documents from Firestore
            docs = []
            for doc_id in similar_doc_ids[offset:]:
                doc = await self.get_document(doc_id)
                if doc:
                    docs.append(doc)
            
            return docs
        except Exception as e:
            print(f"Failed to perform semantic search: {e}")
            return []
    
    async def full_text_search(
        self, query: str, limit: int = 10, offset: int = 0
    ) -> List[Document]:
        """
        Perform full-text search.
        """
        # For simplicity, we'll just do a basic search in Firestore
        # In a real implementation, you might want to use a dedicated search engine
        
        # Search in content, title, and summary
        content_docs = self.collection.where("content", ">=", query).where("content", "<=", query + "\uf8ff").limit(limit).get()
        title_docs = self.collection.where("title", ">=", query).where("title", "<=", query + "\uf8ff").limit(limit).get()
        summary_docs = self.collection.where("summary", ">=", query).where("summary", "<=", query + "\uf8ff").limit(limit).get()
        
        # Combine the results
        docs = []
        doc_ids = set()
        
        for doc_list in [content_docs, title_docs, summary_docs]:
            for doc in doc_list:
                if doc.id not in doc_ids:
                    docs.append(Document(**doc.to_dict()))
                    doc_ids.add(doc.id)
                    
                    if len(docs) >= limit + offset:
                        break
            
            if len(docs) >= limit + offset:
                break
        
        return docs[offset:limit + offset]
    
    async def get_recent_documents(
        self, limit: int = 10, offset: int = 0
    ) -> List[Document]:
        """
        Get the most recent documents.
        """
        docs = self.collection.order_by("date", direction=firestore.Query.DESCENDING).limit(limit + offset).get()
        
        return [Document(**doc.to_dict()) for doc in docs][offset:]
    
    async def find_similar_documents(
        self, embedding: List[float], limit: int = 10, exclude_ids: List[str] = None
    ) -> List[Document]:
        """
        Find documents similar to the given embedding.
        """
        if not self.vector_search_initialized:
            # If Vector Search is not initialized, return empty list
            return []
        
        try:
            # Get similar documents from Vector Search
            similar_doc_ids = self._find_similar_embeddings(embedding, limit * 2)
            
            # Filter out excluded IDs
            if exclude_ids:
                similar_doc_ids = [doc_id for doc_id in similar_doc_ids if doc_id not in exclude_ids]
            
            # Get the documents from Firestore
            docs = []
            for doc_id in similar_doc_ids[:limit]:
                doc = await self.get_document(doc_id)
                if doc:
                    docs.append(doc)
            
            return docs
        except Exception as e:
            print(f"Failed to find similar documents: {e}")
            return []
    
    def _add_embedding_to_vector_search(self, document_id: str, embedding: List[float]) -> None:
        """Add an embedding to Vector Search."""
        if not self.vector_search_initialized:
            return
        
        # This is a placeholder for the actual implementation
        # In a real implementation, you would use the Vertex AI Vector Search API
        pass
    
    def _update_embedding_in_vector_search(self, document_id: str, embedding: List[float]) -> None:
        """Update an embedding in Vector Search."""
        if not self.vector_search_initialized:
            return
        
        # This is a placeholder for the actual implementation
        # In a real implementation, you would use the Vertex AI Vector Search API
        pass
    
    def _delete_embedding_from_vector_search(self, document_id: str) -> None:
        """Delete an embedding from Vector Search."""
        if not self.vector_search_initialized:
            return
        
        # This is a placeholder for the actual implementation
        # In a real implementation, you would use the Vertex AI Vector Search API
        pass
    
    def _find_similar_embeddings(self, embedding: List[float], limit: int = 10) -> List[str]:
        """Find similar embeddings in Vector Search."""
        if not self.vector_search_initialized:
            return []
        
        # This is a placeholder for the actual implementation
        # In a real implementation, you would use the Vertex AI Vector Search API
        return []
