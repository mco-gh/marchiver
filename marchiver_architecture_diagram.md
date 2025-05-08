# Marchiver Architecture Diagram

```mermaid
flowchart TD
    %% Define styles for components
    classDef chromeExt fill:#4285F4,stroke:#2A56C6,color:white,stroke-width:2px
    classDef backend fill:#34A853,stroke:#0F9D58,color:white,stroke-width:2px
    classDef googleServices fill:#FBBC05,stroke:#F9AB00,color:black,stroke-width:2px
    classDef externalWeb fill:#EA4335,stroke:#C5221F,color:white,stroke-width:2px
    
    %% Main components
    user([User])
    
    %% Chrome Extension components
    subgraph ChromeExtension["Chrome Extension"]
        direction TB
        popup[Popup UI]
        docViewer[Document Viewer]
        options[Options Page]
        background[Background Service]
        content[Content Scripts]
    end
    
    %% Backend components
    subgraph Backend["FastAPI Backend"]
        direction TB
        api[API Layer]
        docService[Document Service]
        embedService[Embedding Service]
        sumService[Summarization Service]
        webService[Web Service]
    end
    
    %% External services
    subgraph GoogleCloud["Google Cloud Services"]
        direction TB
        firestore[(Firestore DB)]
        vectorSearch[(Vertex AI Vector Search)]
        genAI[Generative AI]
    end
    
    externalWeb[External Websites]
    
    %% Connections
    user --> ChromeExtension
    ChromeExtension --> Backend
    Backend --> GoogleCloud
    webService --> externalWeb
    
    %% Apply styles
    class ChromeExtension chromeExt
    class Backend backend
    class GoogleCloud googleServices
    class externalWeb externalWeb
```

## Key Components

### Chrome Extension
- **Popup UI**: Main interface for searching and saving content
- **Document Viewer**: Displays archived content with tabs for content and summary
- **Options Page**: Configuration interface for user preferences
- **Background Service**: Handles background tasks and API communication
- **Content Scripts**: Extract content from web pages

### FastAPI Backend
- **API Layer**: RESTful endpoints for all core functionalities
- **Document Service**: Manages document operations and search
- **Embedding Service**: Generates vector embeddings for semantic search
- **Summarization Service**: Creates document summaries using AI
- **Web Service**: Fetches and processes web content

### Google Cloud Services
- **Firestore DB**: Document storage database
- **Vertex AI Vector Search**: Vector database for semantic search
- **Generative AI**: Provides embedding and summarization capabilities

### External Websites
- Sources of content to archive
