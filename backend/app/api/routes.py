from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional

from app.models.document import Document, DocumentCreate, DocumentUpdate
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.summarization_service import SummarizationService
from app.services.web_service import WebService

router = APIRouter()
document_service = DocumentService()
embedding_service = EmbeddingService()
summarization_service = SummarizationService()
web_service = WebService()

@router.post("/documents", response_model=Document, status_code=201)
async def create_document(document: DocumentCreate):
    """Create a new document in the archive."""
    try:
        print(f"Creating new document: '{document.title}'")
        print(f"Content length: {len(document.content)} bytes")
        
        # Generate embedding for the document
        print(f"Generating embedding...")
        embedding = await embedding_service.generate_embedding(document.content)
        print(f"Embedding generated ({len(embedding)} dimensions)")
        
        # Create the document with the embedding
        print(f"Saving document to database...")
        result = await document_service.create_document(document, embedding)
        print(f"Document created successfully with ID: {result.id}")
        return result
    except Exception as e:
        print(f"Error creating document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create document: {str(e)}")

@router.get("/documents/{document_id}", response_model=Document)
async def get_document(document_id: str):
    """Get a document by ID."""
    print(f"Retrieving document with ID: {document_id}")
    
    document = await document_service.get_document(document_id)
    if not document:
        print(f"Document with ID {document_id} not found")
        raise HTTPException(status_code=404, detail="Document not found")
    
    print(f"Found document: '{document.title}'")
    return document

@router.put("/documents/{document_id}", response_model=Document)
async def update_document(document_id: str, document_update: DocumentUpdate):
    """Update a document."""
    print(f"Updating document with ID: {document_id}")
    
    document = await document_service.get_document(document_id)
    if not document:
        print(f"Document with ID {document_id} not found")
        raise HTTPException(status_code=404, detail="Document not found")
    
    print(f"Found document: '{document.title}'")
    
    # If content is updated, regenerate the embedding
    if document_update.content:
        print(f"Content updated. Generating new embedding...")
        print(f"New content length: {len(document_update.content)} bytes")
        embedding = await embedding_service.generate_embedding(document_update.content)
        print(f"Embedding generated ({len(embedding)} dimensions)")
        
        print(f"Updating document with new content and embedding...")
        result = await document_service.update_document(document_id, document_update, embedding)
        print(f"Document updated successfully")
        return result
    
    print(f"Updating document metadata only (no content change)...")
    result = await document_service.update_document(document_id, document_update)
    print(f"Document updated successfully")
    return result

@router.delete("/documents/{document_id}", status_code=204)
async def delete_document(document_id: str):
    """Delete a document."""
    print(f"Deleting document with ID: {document_id}")
    
    document = await document_service.get_document(document_id)
    if not document:
        print(f"Document with ID {document_id} not found")
        raise HTTPException(status_code=404, detail="Document not found")
    
    print(f"Found document: '{document.title}'")
    print(f"Deleting document from database and vector search...")
    
    await document_service.delete_document(document_id)
    print(f"Document deleted successfully")
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
        print(f"Performing semantic search for query: '{query}'")
        print(f"Parameters: limit={limit}, offset={offset}")
        
        # Generate embedding for the query
        print(f"Generating embedding for query...")
        query_embedding = await embedding_service.generate_embedding(query)
        print(f"Embedding generated ({len(query_embedding)} dimensions)")
        
        # Perform semantic search
        print(f"Executing semantic search...")
        results = await document_service.semantic_search(query_embedding, limit, offset)
        print(f"Search completed. Found {len(results)} results.")
        return results
    
    if query:
        print(f"Performing full-text search for query: '{query}'")
        print(f"Parameters: limit={limit}, offset={offset}")
        
        # Perform full-text search
        print(f"Executing full-text search...")
        results = await document_service.full_text_search(query, limit, offset)
        print(f"Search completed. Found {len(results)} results.")
        return results
    
    # Return the most recent documents
    print(f"Retrieving most recent documents")
    print(f"Parameters: limit={limit}, offset={offset}")
    
    results = await document_service.get_recent_documents(limit, offset)
    print(f"Retrieved {len(results)} recent documents.")
    return results

@router.post("/web/fetch", response_model=Document)
async def fetch_web_page(url: str, save: bool = True, summarize: bool = True):
    """
    Fetch a web page, optionally summarize it, and optionally save it to the archive.
    If a document with the same URL already exists, it will be updated instead of creating a new one.
    """
    try:
        print(f"Starting to fetch web page: {url}")
        print(f"Options: save={save}, summarize={summarize}")
        
        # Fetch the web page
        print(f"Fetching content from {url}...")
        content, title = await web_service.fetch_web_page(url)
        print(f"Successfully fetched page: '{title}' ({len(content)} bytes)")
        
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
            print(f"Generating summary...")
            summary = await summarization_service.summarize(content)
            document.summary = summary
            print(f"Summary generated ({len(summary)} characters)")
        
        # Save the document if requested
        if save:
            # Generate embedding for the document
            print(f"Generating embedding...")
            embedding = await embedding_service.generate_embedding(content)
            print(f"Embedding generated ({len(embedding)} dimensions)")
            
            # Check if a document with the same URL already exists
            print(f"Checking if document with URL {url} already exists...")
            existing_document = await document_service.find_document_by_url(url)
            
            if existing_document:
                print(f"Document with URL {url} already exists with ID: {existing_document.id}")
                print(f"Updating existing document...")
                
                # Update the existing document
                document_update = DocumentUpdate(
                    content=content,
                    title=title,
                    summary=document.summary if summarize else None,
                    metadata=document.metadata
                )
                result = await document_service.update_document(existing_document.id, document_update, embedding)
                print(f"Successfully updated document with ID: {result.id}")
                return result
            else:
                print(f"Document with URL {url} does not exist. Creating new document...")
                
                # Create a new document
                result = await document_service.create_document(document, embedding)
                print(f"Successfully created document with ID: {result.id}")
                return result
        
        print(f"Document processed but not saved (save={save})")
        
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
    print(f"Finding documents similar to document with ID: {document_id}")
    print(f"Parameters: limit={limit}")
    
    document = await document_service.get_document(document_id)
    if not document:
        print(f"Document with ID {document_id} not found")
        raise HTTPException(status_code=404, detail="Document not found")
    
    print(f"Found document: '{document.title}'")
    print(f"Searching for similar documents...")
    
    results = await document_service.find_similar_documents(document.embedding, limit, exclude_ids=[document_id])
    print(f"Found {len(results)} similar documents")
    return results

@router.post("/embeddings", response_model=List[float])
async def generate_embedding(text: str):
    """Generate an embedding for the given text."""
    try:
        print(f"Generating embedding for text ({len(text)} bytes)...")
        embedding = await embedding_service.generate_embedding(text)
        print(f"Embedding generated successfully ({len(embedding)} dimensions)")
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate embedding: {str(e)}")

@router.post("/summarize", response_model=str)
async def summarize_text(text: str):
    """Summarize the given text."""
    try:
        print(f"Summarizing text ({len(text)} bytes)...")
        summary = await summarization_service.summarize(text)
        print(f"Summary generated successfully ({len(summary)} characters)")
        return summary
    except Exception as e:
        print(f"Error summarizing text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to summarize text: {str(e)}")
