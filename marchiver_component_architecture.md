# Marchiver Component Architecture

```mermaid
classDiagram
    %% Backend Classes
    class FastAPIApp {
        +include_router()
        +add_middleware()
    }
    
    class APIRouter {
        +create_document()
        +get_document()
        +update_document()
        +delete_document()
        +search_documents()
        +fetch_web_page()
        +generate_embedding()
        +summarize_text()
        +get_similar_documents()
    }
    
    class DocumentService {
        -db: FirestoreClient
        -collection: FirestoreCollection
        -vector_search_initialized: bool
        +create_document()
        +get_document()
        +update_document()
        +delete_document()
        +semantic_search()
        +full_text_search()
        +get_recent_documents()
        +find_similar_documents()
        -_add_embedding_to_vector_search()
        -_update_embedding_in_vector_search()
        -_delete_embedding_from_vector_search()
        -_find_similar_embeddings()
    }
    
    class EmbeddingService {
        -embedding_model: string
        -vertex_ai_initialized: bool
        +generate_embedding()
    }
    
    class SummarizationService {
        -model_name: string
        -model: GenerativeModel
        -model_initialized: bool
        +summarize()
    }
    
    class WebService {
        -client: AsyncClient
        +fetch_web_page()
        +close()
    }
    
    class Document {
        +id: string
        +content: string
        +title: string
        +url: string
        +summary: string
        +metadata: Dict
        +tags: List
        +category: string
        +embedding: List[float]
        +version: int
        +author: string
        +date: string
    }
    
    class DocumentCreate {
        +content: string
        +title: string
        +url: string
        +summary: string
        +metadata: Dict
        +tags: List
        +category: string
        +author: string
        +date: string
    }
    
    class DocumentUpdate {
        +content: string
        +title: string
        +url: string
        +summary: string
        +metadata: Dict
        +tags: List
        +category: string
        +author: string
        +date: string
    }
    
    class Config {
        +API_TITLE: string
        +API_DESCRIPTION: string
        +API_VERSION: string
        +API_PREFIX: string
        +HOST: string
        +PORT: int
        +DEBUG: bool
        +GOOGLE_APPLICATION_CREDENTIALS: string
        +GOOGLE_CLOUD_PROJECT: string
        +GOOGLE_CLOUD_REGION: string
        +GOOGLE_API_KEY: string
        +VERTEX_AI_INDEX_ENDPOINT: string
        +VERTEX_AI_INDEX: string
        +VERTEX_AI_EMBEDDING_ENDPOINT: string
        +EMBEDDING_MODEL: string
        +SUMMARIZATION_MODEL: string
        +FIRESTORE_COLLECTION: string
        +CORS_ORIGINS: List
        +CORS_METHODS: List
        +CORS_HEADERS: List
    }
    
    %% Frontend Classes
    class ChromeExtension {
        +manifest.json
        +popup.html
        +options.html
        +document.html
    }
    
    class PopupJS {
        -API_BASE_URL: string
        +init()
        +savePage()
        +summarizePage()
        +performSearch()
        +displaySearchResults()
        +openOptions()
        +loadSettings()
        +showStatus()
    }
    
    class BackgroundJS {
        -API_BASE_URL: string
        +savePage()
        +summarizePage()
        +search()
        +loadSettings()
    }
    
    class DocumentJS {
        -API_BASE_URL: string
        -currentDocument: Document
        -documentId: string
        +init()
        +loadDocument()
        +displayDocument()
        +loadRelatedDocuments()
        +displayRelatedDocuments()
        +switchTab()
        +openEditModal()
        +closeEditModal()
        +saveDocumentChanges()
        +goBack()
        +loadSettings()
        +showStatus()
    }
    
    class ContentJS {
        +extractPageContent()
    }
    
    class OptionsJS {
        +loadSettings()
        +saveSettings()
    }
    
    %% External Services
    class FirestoreDB {
        +collection()
        +document()
        +get()
        +set()
        +update()
        +delete()
        +query()
    }
    
    class VertexAIVectorSearch {
        +index_endpoint
        +index
        +search_vectors()
        +add_vector()
        +update_vector()
        +delete_vector()
    }
    
    class GoogleGenerativeAI {
        +embed_content()
        +generate_content()
    }
    
    %% Relationships - Backend
    FastAPIApp --> APIRouter : includes
    APIRouter --> DocumentService : uses
    APIRouter --> EmbeddingService : uses
    APIRouter --> SummarizationService : uses
    APIRouter --> WebService : uses
    DocumentService --> Document : manages
    DocumentService --> DocumentCreate : accepts
    DocumentService --> DocumentUpdate : accepts
    DocumentService --> FirestoreDB : uses
    DocumentService --> VertexAIVectorSearch : uses
    EmbeddingService --> GoogleGenerativeAI : uses
    SummarizationService --> GoogleGenerativeAI : uses
    Config --> FastAPIApp : configures
    Config --> DocumentService : configures
    Config --> EmbeddingService : configures
    Config --> SummarizationService : configures
    
    %% Relationships - Frontend
    ChromeExtension --> PopupJS : contains
    ChromeExtension --> BackgroundJS : contains
    ChromeExtension --> DocumentJS : contains
    ChromeExtension --> ContentJS : contains
    ChromeExtension --> OptionsJS : contains
    
    %% Cross-Component Relationships
    BackgroundJS --> APIRouter : calls
    PopupJS --> APIRouter : calls
    DocumentJS --> APIRouter : calls
```

## Component Details

### Backend Components

#### API Layer
- **FastAPI Application**: Main application entry point
- **API Router**: Defines all API endpoints and routes requests to appropriate services

#### Service Layer
- **Document Service**: Core service for document operations
  - Manages CRUD operations for documents
  - Handles search functionality (both semantic and full-text)
  - Interfaces with Firestore for document storage
  - Interfaces with Vector Search for embedding storage
  
- **Embedding Service**: Generates vector embeddings
  - Uses Google Generative AI for embedding generation
  - Provides fallback mechanisms for embedding generation
  
- **Summarization Service**: Creates document summaries
  - Uses Google Generative AI for text summarization
  - Formats prompts for optimal summarization
  
- **Web Service**: Fetches and processes web content
  - Uses httpx for asynchronous HTTP requests
  - Extracts relevant content from web pages

#### Data Layer
- **Document Models**: Define document structure
  - Base document structure
  - Create/update operation models
  - Validation rules

- **Configuration**: Manages application settings
  - Environment variable handling
  - Service configuration
  - API settings

### Frontend Components

#### User Interface
- **Popup UI**: Main extension interface
  - Search functionality
  - Page saving controls
  - Results display
  
- **Document Viewer**: Displays archived content
  - Content/summary tabs
  - Related documents
  - Edit functionality
  
- **Options Page**: Configuration interface
  - API settings
  - Display preferences
  - Feature toggles

#### Background Processing
- **Background Service Worker**: Handles background tasks
  - API communication
  - Context menu functionality
  - Message handling
  
- **Content Scripts**: Interact with web pages
  - Content extraction
  - Page analysis

#### Storage
- **Chrome Storage**: Manages user preferences
  - API endpoint configuration
  - Feature toggles
  - UI preferences

### External Services

- **Firestore**: Document database
  - Stores document content and metadata
  - Provides basic query capabilities
  
- **Vertex AI Vector Search**: Vector database
  - Stores embeddings for semantic search
  - Performs similarity searches
  
- **Google Generative AI**: AI services
  - Generates embeddings for semantic search
  - Creates document summaries
