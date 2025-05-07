# Vector Search Implementation

This document describes the implementation of vector search in the Marchiver application using Google Vertex AI Vector Search.

## Overview

Vector search allows for semantic search capabilities, finding documents that are conceptually similar to a query even if they don't share the exact same keywords. This is achieved by:

1. Converting text into high-dimensional vectors (embeddings) that capture semantic meaning
2. Storing these vectors in a specialized index optimized for nearest-neighbor search
3. Finding the closest vectors to a query vector when performing a search

## Implementation Details

### Index Configuration

The application uses a 768-dimensional vector index with the following configuration:

- Dimensions: 768
- Distance measure: DOT_PRODUCT_DISTANCE
- Approximate neighbors count: 5
- Leaf node embedding count: 1000
- Leaf nodes to search percent: 5
- Streaming updates enabled

### Embedding Generation

Embeddings are generated using one of the following methods (in order of preference):

1. Google Generative AI API (if API key is provided and text is within size limits)
2. Vertex AI Text Embedding Model (text-embedding-004)
3. Deterministic embedding generation (fallback)

All embeddings are resized to 768 dimensions to match the index configuration.

### Search Process

When a user performs a search with semantic search enabled:

1. The search query is converted to a 768-dimensional embedding
2. The embedding is used to find the nearest neighbors in the vector index
3. The corresponding documents are retrieved from Firestore
4. The results are returned to the user

## Setup and Test Scripts

The following scripts are provided to set up and test vector search:

### Setup Scripts

- `create_streaming_index.py`: Creates a new 768-dimensional index with streaming updates enabled
- `deploy_streaming_index.py`: Deploys the index to the index endpoint
- `update_env_for_streaming_768d.py`: Updates the .env file to use the new index

### Test Scripts

- `test_768d_search.py`: Tests the vector search functionality with the new 768-dimensional index
  - Initializes the document and embedding services
  - Generates an embedding for a test query
  - Performs semantic search using the query embedding
  - Displays the search results

- `add_test_documents.py`: Adds test documents to the index
  - Creates sample documents with relevant content for testing
  - Generates embeddings for each document
  - Adds the documents and their embeddings to Firestore and the vector index

### Other Test Files in the Project

- `test_all_services.py`: Tests all services in the application (not specific to vector search)
- `test_api.py`: Tests the API endpoints
- `test_api_mock.py`: Tests the API endpoints with mock services
- `test_embedding.py`: Tests the embedding service
- `test_vector_search.py`: Tests the vector search functionality (general test, not specific to 768d)

## Usage

To set up vector search:

1. Create the index:
   ```
   python backend/create_streaming_index.py
   ```

2. Deploy the index:
   ```
   python backend/deploy_streaming_index.py
   ```

3. Update the .env file:
   ```
   python backend/update_env_for_streaming_768d.py
   ```

4. Add test documents:
   ```
   python backend/add_test_documents.py
   ```

5. Test the search functionality:
   ```
   python backend/test_768d_search.py
   ```

## Frontend Integration

The Chrome extension popup already supports vector search. When a user enters a search query and clicks the search button, the application performs a semantic search by default.

## API Endpoints

The following API endpoints support vector search:

- `GET /api/documents?query={query}&semantic=true`: Performs a semantic search using the provided query
- `GET /api/documents/{document_id}/similar`: Finds documents similar to the specified document

## Troubleshooting

If vector search is not working as expected:

1. Check that the index is created and deployed correctly
2. Verify that the VERTEX_AI_INDEX environment variable is set to the correct index ID
3. Ensure that the embeddings are being generated with the correct dimensions (768)
4. Check the logs for any errors related to vector search
