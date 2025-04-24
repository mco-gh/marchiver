# Marchiver Data Flow Diagram

```mermaid
sequenceDiagram
    participant User
    participant Extension as Chrome Extension
    participant API as FastAPI Backend
    participant DocService as Document Service
    participant EmbedService as Embedding Service
    participant SumService as Summarization Service
    participant WebService as Web Service
    participant Firestore
    participant VectorSearch as Vertex AI Vector Search
    participant GenAI as Google Generative AI
    participant Web as External Websites

    %% Save Page Flow
    User->>Extension: Click "Save Page"
    Extension->>API: POST /api/web/fetch
    API->>WebService: fetch_web_page(url)
    WebService->>Web: HTTP GET request
    Web-->>WebService: HTML content
    WebService-->>API: content, title
    API->>EmbedService: generate_embedding(content)
    EmbedService->>GenAI: Embedding request
    GenAI-->>EmbedService: Vector embedding
    EmbedService-->>API: embedding
    API->>DocService: create_document(doc, embedding)
    DocService->>Firestore: Store document
    DocService->>VectorSearch: Store embedding
    DocService-->>API: document
    API-->>Extension: document
    Extension-->>User: Show document view

    %% Summarize Page Flow
    User->>Extension: Click "Summarize & Save"
    Extension->>API: POST /api/web/fetch (summarize=true)
    API->>WebService: fetch_web_page(url)
    WebService->>Web: HTTP GET request
    Web-->>WebService: HTML content
    WebService-->>API: content, title
    API->>SumService: summarize(content)
    SumService->>GenAI: Summarization request
    GenAI-->>SumService: Summary text
    SumService-->>API: summary
    API->>EmbedService: generate_embedding(content)
    EmbedService->>GenAI: Embedding request
    GenAI-->>EmbedService: Vector embedding
    EmbedService-->>API: embedding
    API->>DocService: create_document(doc, embedding)
    DocService->>Firestore: Store document
    DocService->>VectorSearch: Store embedding
    DocService-->>API: document
    API-->>Extension: document
    Extension-->>User: Show document view

    %% Search Flow
    User->>Extension: Enter search query
    Extension->>API: GET /api/documents?query=...
    
    alt Semantic Search
        API->>EmbedService: generate_embedding(query)
        EmbedService->>GenAI: Embedding request
        GenAI-->>EmbedService: Query embedding
        EmbedService-->>API: query_embedding
        API->>DocService: semantic_search(query_embedding)
        DocService->>VectorSearch: Find similar vectors
        VectorSearch-->>DocService: Similar document IDs
        DocService->>Firestore: Get documents by IDs
        Firestore-->>DocService: Documents
    else Full-text Search
        API->>DocService: full_text_search(query)
        DocService->>Firestore: Query documents
        Firestore-->>DocService: Matching documents
    end
    
    DocService-->>API: search results
    API-->>Extension: search results
    Extension-->>User: Display search results

    %% View Document Flow
    User->>Extension: Click on search result
    Extension->>API: GET /api/documents/{id}
    API->>DocService: get_document(id)
    DocService->>Firestore: Get document
    Firestore-->>DocService: Document
    DocService-->>API: document
    API-->>Extension: document
    Extension-->>User: Display document

    %% Get Similar Documents Flow
    Extension->>API: GET /api/documents/{id}/similar
    API->>DocService: find_similar_documents(embedding)
    DocService->>VectorSearch: Find similar vectors
    VectorSearch-->>DocService: Similar document IDs
    DocService->>Firestore: Get documents by IDs
    Firestore-->>DocService: Similar documents
    DocService-->>API: similar documents
    API-->>Extension: similar documents
    Extension-->>User: Display similar documents
```

## Key Data Flows

### 1. Save Page Flow
- User clicks "Save Page" in the extension
- Extension sends the URL to the backend
- Web Service fetches the page content
- Embedding Service generates a vector embedding
- Document Service stores the document and embedding
- Document is displayed to the user

### 2. Summarize Page Flow
- User clicks "Summarize & Save" in the extension
- Extension sends the URL to the backend
- Web Service fetches the page content
- Summarization Service generates a summary
- Embedding Service generates a vector embedding
- Document Service stores the document, summary, and embedding
- Document with summary is displayed to the user

### 3. Search Flow
- User enters a search query in the extension
- For semantic search:
  - Embedding Service generates a vector embedding for the query
  - Document Service finds similar documents using vector search
- For full-text search:
  - Document Service performs a text-based search
- Search results are displayed to the user

### 4. View Document Flow
- User clicks on a search result
- Document Service retrieves the document
- Document is displayed to the user with content and summary
- Similar documents are fetched and displayed

## Data Storage

### Document Structure
- Content: The full text of the document
- Title: Document title
- URL: Source URL (if applicable)
- Summary: AI-generated summary (if available)
- Metadata: Additional information about the document
- Tags: User-defined tags for categorization
- Embedding: Vector representation for semantic search
- Version: Document version for tracking changes

### Storage Systems
- **Firestore**: Stores document content, metadata, and other attributes
- **Vertex AI Vector Search**: Stores vector embeddings for semantic search
