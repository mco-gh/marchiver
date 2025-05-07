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
        self.index = None
        self.index_endpoint = None
        self.deployed_index_id = VERTEX_AI_INDEX  # This is the ID of the deployed index
        
        try:
            aiplatform.init(
                project=GOOGLE_CLOUD_PROJECT,
                location=GOOGLE_CLOUD_REGION,
            )
            
            # Initialize the index endpoint
            try:
                self.index_endpoint = aiplatform.MatchingEngineIndexEndpoint(index_endpoint_name=VERTEX_AI_INDEX_ENDPOINT)
                print(f"Successfully initialized MatchingEngineIndexEndpoint with name: {self.index_endpoint.name}")
                
                # Get the actual index resource name from the deployed indexes
                if hasattr(self.index_endpoint, 'deployed_indexes') and self.index_endpoint.deployed_indexes:
                    for deployed_index in self.index_endpoint.deployed_indexes:
                        if isinstance(deployed_index, dict) and 'id' in deployed_index and deployed_index['id'] == self.deployed_index_id:
                            # Found the deployed index with the matching ID
                            if 'index' in deployed_index:
                                actual_index_name = deployed_index['index']
                                print(f"Found actual index resource name: {actual_index_name}")
                                
                                # Initialize the index with the actual resource name
                                try:
                                    self.index = aiplatform.MatchingEngineIndex(index_name=actual_index_name)
                                    print(f"Successfully initialized MatchingEngineIndex with name: {self.index.name}")
                                    self.vector_search_initialized = True
                                except Exception as e:
                                    print(f"Failed to initialize MatchingEngineIndex with actual resource name: {e}")
                                    self.index = None
                                
                                break
                
                # If we couldn't find the actual index resource name, try to list all indexes
                if self.index is None:
                    try:
                        indexes = aiplatform.MatchingEngineIndex.list()
                        if indexes and len(indexes) > 0:
                            # Use the first index
                            self.index = indexes[0]
                            print(f"Using first available index: {self.index.name}")
                            self.vector_search_initialized = True
                    except Exception as e:
                        print(f"Failed to list indexes: {e}")
                        self.index = None
            except Exception as e:
                print(f"Failed to initialize MatchingEngineIndexEndpoint: {e}")
                self.index_endpoint = None
            
            # Check if both index and index endpoint are initialized
            if self.index is None or self.index_endpoint is None:
                print("Vector search is not fully initialized. Some operations may not work.")
                if self.index_endpoint is not None:
                    print("Only search operations will be available.")
                    self.vector_search_initialized = True
                else:
                    self.vector_search_initialized = False
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
    
    async def find_document_by_url(self, url: str) -> Optional[Document]:
        """Find a document by URL."""
        # Query Firestore for documents with the given URL
        docs = self.collection.where("url", "==", url).limit(1).get()
        
        # Return the first document if found
        for doc in docs:
            return Document(**doc.to_dict())
        
        # Return None if no document is found
        return None
    
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
        if not self.vector_search_initialized or self.index is None:
            print("Vector search is not fully initialized. Cannot add embedding.")
            return
        
        try:
            # Import the necessary types
            from google.cloud.aiplatform_v1.types.index_service import UpsertDatapointsRequest
            from google.cloud.aiplatform_v1.types.index import IndexDatapoint
            
            # Create an IndexDatapoint object
            datapoint = IndexDatapoint(
                datapoint_id=document_id,
                feature_vector=embedding,
            )
            
            # Create the request
            request = UpsertDatapointsRequest(
                index="projects/1082996892307/locations/us-central1/indexes/5627179564678512640",  # Use the 768d index directly
                datapoints=[datapoint],
            )
            
            # Call the API
            self.index.api_client.upsert_datapoints(request)
            print(f"Successfully added embedding for document {document_id} to Vector Search")
        except Exception as e:
            print(f"Error adding embedding to Vector Search: {e}")
            print(f"Error details: {str(e)}")
            print("WARNING: Could not add embedding to Vector Search. Document will be saved without vector search capability.")
    
    def _update_embedding_in_vector_search(self, document_id: str, embedding: List[float]) -> None:
        """Update an embedding in Vector Search."""
        if not self.vector_search_initialized:
            return
        
        # For Vertex AI Vector Search, updating is the same as adding (upsert operation)
        self._add_embedding_to_vector_search(document_id, embedding)
    
    def _delete_embedding_from_vector_search(self, document_id: str) -> None:
        """Delete an embedding from Vector Search."""
        if not self.vector_search_initialized or self.index is None:
            print("Vector search is not fully initialized. Cannot delete embedding.")
            return
        
        try:
            # Import the necessary types
            from google.cloud.aiplatform_v1.types.index_service import RemoveDatapointsRequest
            
            # Create the request
            request = RemoveDatapointsRequest(
                index="projects/1082996892307/locations/us-central1/indexes/5627179564678512640",  # Use the 768d index directly
                datapoint_ids=[document_id],
            )
            
            # Call the API
            self.index.api_client.remove_datapoints(request)
            print(f"Successfully deleted embedding for document {document_id} from Vector Search")
        except Exception as e:
            print(f"Error deleting embedding from Vector Search: {e}")
            print(f"Error details: {str(e)}")
            print("WARNING: Could not delete embedding from Vector Search. Document will be deleted from Firestore only.")
    
    def _find_similar_embeddings(self, embedding: List[float], limit: int = 10) -> List[str]:
        """Find similar embeddings in Vector Search."""
        if not self.vector_search_initialized or self.index_endpoint is None:
            print("Vector search is not fully initialized. Cannot find similar embeddings.")
            return []
        
        try:
            # Use the MatchingEngineIndexEndpoint class to find similar embeddings
            # According to our check, this class has the find_neighbors method
            response = self.index_endpoint.find_neighbors(
                deployed_index_id="marchiver_streaming_768d_1746631997838",  # Use the correct deployed index ID
                queries=[embedding],
                num_neighbors=limit,
            )
            
            # Extract document IDs from the response
            if response and len(response) > 0:
                # The response format might be different depending on the API version
                # Try different ways to extract the neighbors
                if hasattr(response[0], 'neighbors'):
                    # Return the document IDs of the nearest neighbors
                    return [neighbor.id for neighbor in response[0].neighbors]
                elif isinstance(response[0], dict) and 'neighbors' in response[0]:
                    # Alternative format where response is a list of dicts
                    return [neighbor['id'] for neighbor in response[0]['neighbors']]
                elif isinstance(response, dict) and 'results' in response:
                    # Another possible format
                    return [neighbor['id'] for neighbor in response['results'][0]['neighbors']]
                elif isinstance(response[0], list):
                    # Format from the test output: a list of MatchNeighbor objects
                    return [neighbor.id for neighbor in response[0]]
            
            print("\nDetailed response information:")
            print(f"Response type: {type(response)}")
            print(f"Response: {response}")
            
            if response:
                print(f"Response length: {len(response)}")
                if len(response) > 0:
                    print(f"First item type: {type(response[0])}")
                    print(f"First item: {response[0]}")
                    
                    # Try to print attributes or keys
                    if hasattr(response[0], '__dict__'):
                        print(f"First item attributes: {response[0].__dict__}")
                    elif isinstance(response[0], dict):
                        print(f"First item keys: {response[0].keys()}")
            return []
        except Exception as e:
            print(f"Error finding similar embeddings in Vector Search: {e}")
            
            # Try alternative method name
            try:
                # Some API versions use match instead of find_neighbors
                response = self.index_endpoint.match(
                    deployed_index_id=self.deployed_index_id,  # Use the deployed index ID, not the index name
                    queries=[embedding],
                    num_neighbors=limit,
                )
                
                # Extract document IDs from the response
                if response and len(response) > 0:
                    # Try different ways to extract the neighbors
                    if hasattr(response[0], 'neighbors'):
                        return [neighbor.id for neighbor in response[0].neighbors]
                    elif isinstance(response[0], dict) and 'neighbors' in response[0]:
                        return [neighbor['id'] for neighbor in response[0]['neighbors']]
                
                print("Warning: Could not extract neighbors from response format (match method)")
                print(f"Response: {response}")
                return []
            except Exception as e2:
                print(f"Error using match method: {e2}")
                print("WARNING: Could not find similar embeddings in Vector Search. Returning empty list.")
                return []
