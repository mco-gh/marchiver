# Vector Search Implementation

This document explains how vector search is implemented in the Marchiver application using Google Vertex AI Vector Search.

## Overview

Vector search allows for semantic searching of documents based on the meaning of the text rather than just keyword matching. This is achieved by converting text into high-dimensional vectors (embeddings) and finding the nearest neighbors in the vector space.

## Components

### 1. Embedding Generation

The `EmbeddingService` class in `backend/app/services/embedding_service.py` is responsible for generating embeddings for documents and search queries. It uses Google's Generative AI API to generate 768-dimensional embeddings.

```python
async def generate_embedding(self, text: str) -> List[float]:
    """Generate an embedding for the given text."""
    # Generate embedding using Google Generative AI API
    embedding = await self._generate_embedding_with_genai(text)
    return embedding
```

### 2. Vector Index

We use Google Vertex AI Vector Search to store and search embeddings. The index is configured with the following parameters:

- Dimensions: 768
- Distance measure: DOT_PRODUCT_DISTANCE
- Streaming updates: Enabled

### 3. Document Service

The `DocumentService` class in `backend/app/services/document_service.py` handles the interaction with the vector search index:

- Adding embeddings to the index when documents are created
- Updating embeddings when documents are modified
- Removing embeddings when documents are deleted
- Searching for similar documents using the index

```python
async def semantic_search(self, query_embedding: List[float], limit: int = 10, offset: int = 0) -> List[Document]:
    """Perform semantic search using the query embedding."""
    similar_doc_ids = self._find_similar_embeddings(query_embedding, limit + offset)
    docs = []
    for doc_id in similar_doc_ids[offset:]:
        doc = await self.get_document(doc_id)
        if doc:
            docs.append(doc)
    return docs
```

### 4. API Routes

The API routes in `backend/app/api/routes.py` expose the vector search functionality through the `/documents` endpoint with the `semantic=true` parameter:

```python
@router.get("/documents", response_model=List[Document])
async def search_documents(
    query: Optional[str] = None,
    semantic: bool = False,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Search for documents."""
    if query and semantic:
        # Generate embedding for the query
        query_embedding = await embedding_service.generate_embedding(query)
        
        # Perform semantic search
        return await document_service.semantic_search(query_embedding, limit, offset)
    
    # ... other search methods ...
```

### 5. Chrome Extension Integration

The Chrome extension's popup interface in `frontend/js/popup.js` allows users to perform semantic searches:

```javascript
chrome.runtime.sendMessage(
  { 
    action: 'search',
    query: query,
    semantic: true,  // Use semantic search
    limit: 5         // Limit to 5 results
  },
  function(response) {
    // Handle response...
  }
);
```

The background script in `frontend/js/background.js` forwards these requests to the API:

```javascript
const searchUrl = new URL(`${API_BASE_URL}/documents`);
if (query) {
  searchUrl.searchParams.append('query', query);
  searchUrl.searchParams.append('semantic', semantic);
}
```

## Setup and Configuration

### Environment Variables

The following environment variables are used to configure the vector search:

- `GOOGLE_CLOUD_PROJECT`: The Google Cloud project ID
- `GOOGLE_CLOUD_REGION`: The Google Cloud region (e.g., us-central1)
- `VERTEX_AI_INDEX_ENDPOINT`: The Vertex AI index endpoint resource name
- `VERTEX_AI_INDEX`: The ID of the deployed index

### Index Creation and Deployment

The index is created and deployed using the following scripts:

1. `backend/create_768d_index.py`: Creates a new 768-dimensional index
2. `backend/deploy_768d_index.py`: Deploys the index to the index endpoint
3. `backend/update_env_for_768d.py`: Updates the .env file with the new index ID

For streaming updates, use these scripts:

1. `backend/create_streaming_index.py`: Creates a new index with streaming updates enabled
2. `backend/deploy_streaming_index.py`: Deploys the streaming index to the index endpoint
3. `backend/update_env_for_streaming_768d.py`: Updates the .env file with the new streaming index ID

## Testing

You can test the vector search functionality using the following scripts:

1. `backend/add_test_documents.py`: Adds test documents to the index
2. `backend/test_768d_search.py`: Tests the vector search with a sample query
3. `backend/test_popup_search.py`: Simulates the Chrome extension popup search

## Troubleshooting

If you encounter issues with vector search, check the following:

1. Ensure the correct index ID is set in the .env file
2. Verify that the index dimensions match the embedding dimensions (768)
3. Check that the index endpoint is correctly configured
4. Ensure the Google Cloud credentials are properly set up

## Future Improvements

Potential improvements to the vector search functionality:

1. Implement hybrid search (combining vector search with keyword search)
2. Add filtering capabilities (e.g., by date, category, tags)
3. Optimize embedding generation for better performance
4. Implement caching for frequently searched queries
