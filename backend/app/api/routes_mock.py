"""
Mock API routes for testing purposes.
Uses mock services instead of real ones.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional

from app.models.document import Document, DocumentCreate, DocumentUpdate
from app.services.document_service_mock import DocumentServiceMock
from app.services.embedding_service_mock import EmbeddingServiceMock
from app.services.summarization_service_mock import SummarizationServiceMock
from app.services.web_service_mock import WebServiceMock

router = APIRouter()
document_service = DocumentServiceMock()
embedding_service = EmbeddingServiceMock()
summarization_service = SummarizationServiceMock()
web_service = WebServiceMock()

@router.post("/documents", response_model=Document, status_code=201)
async def create_document(document: DocumentCreate):
    """Create a new document in the archive."""
    try:
        # Generate embedding for the document
        embedding = await embedding_service.generate_embedding(document.content)
        
        # Create the document with the embedding
        return await document_service.create_document(document, embedding)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create document: {str(e)}")

@router.get("/documents/{document_id}", response_model=Document)
async def get_document(document_id: str):
    """Get a document by ID."""
    document = await document_service.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.put("/documents/{document_id}", response_model=Document)
async def update_document(document_id: str, document_update: DocumentUpdate):
    """Update a document."""
    document = await document_service.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # If content is updated, regenerate the embedding
    if document_update.content:
        embedding = await embedding_service.generate_embedding(document_update.content)
        return await document_service.update_document(document_id, document_update, embedding)
    
    return await document_service.update_document(document_id, document_update)

@router.delete("/documents/{document_id}", status_code=204)
async def delete_document(document_id: str):
    """Delete a document."""
    document = await document_service.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    await document_service.delete_document(document_id)
    return None

@router.get("/documents", response_model=List[Document])
async def search_documents(
    query: Optional[str] = None,
    semantic: bool = False,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """
    Search for documents.
    
    - If query is provided and semantic is True, perform semantic search.
    - If query is provided and semantic is False, perform full-text search.
    - If query is not provided, return the most recent documents.
    """
    if query and semantic:
        # Generate embedding for the query
        query_embedding = await embedding_service.generate_embedding(query)
        
        # Perform semantic search
        return await document_service.semantic_search(query_embedding, limit, offset)
    
    if query:
        # Perform full-text search
        return await document_service.full_text_search(query, limit, offset)
    
    # Return the most recent documents
    return await document_service.get_recent_documents(limit, offset)

@router.post("/web/fetch", response_model=Document)
async def fetch_web_page(url: str, save: bool = True, summarize: bool = True):
    """
    Fetch a web page, optionally summarize it, and optionally save it to the archive.
    """
    try:
        # Fetch the web page
        content, title = await web_service.fetch_web_page(url)
        
        # Create a document
        document = DocumentCreate(
            content=content,
            title=title,
            url=url,
            metadata={
                "source": "web",
                "url": url,
            }
        )
        
        # Summarize the content if requested
        if summarize:
            summary = await summarization_service.summarize(content)
            document.summary = summary
        
        # Save the document if requested
        if save:
            # Generate embedding for the document
            embedding = await embedding_service.generate_embedding(content)
            
            # Create the document with the embedding
            return await document_service.create_document(document, embedding)
        
        # Return the document without saving
        return Document(
            id="",
            content=content,
            title=title,
            url=url,
            summary=document.summary if summarize else None,
            metadata=document.metadata,
            embedding=[],
            version=1,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch web page: {str(e)}")

@router.get("/documents/{document_id}/similar", response_model=List[Document])
async def get_similar_documents(
    document_id: str,
    limit: int = Query(10, ge=1, le=100),
):
    """Get documents similar to the given document."""
    document = await document_service.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return await document_service.find_similar_documents(document.embedding, limit, exclude_ids=[document_id])

@router.post("/embeddings", response_model=List[float])
async def generate_embedding(text: str):
    """Generate an embedding for the given text."""
    try:
        return await embedding_service.generate_embedding(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate embedding: {str(e)}")

@router.post("/summarize", response_model=str)
async def summarize_text(text: str):
    """Summarize the given text."""
    try:
        return await summarization_service.summarize(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to summarize text: {str(e)}")
