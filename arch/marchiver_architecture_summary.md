# Marchiver Architecture Summary

This document provides a comprehensive overview of the Marchiver application architecture, a personal knowledge archiving and retrieval system that allows users to save, organize, and intelligently access diverse digital information.

## System Overview

Marchiver consists of two main components:

1. **Backend API**: A FastAPI-based Python application that provides core functionality for document management, embedding generation, summarization, and web content fetching.

2. **Frontend Chrome Extension**: A browser extension that allows users to interact with the system, save web pages, search for content, and manage their archived information.

The system leverages several external services:
- **Google Cloud Firestore**: For document storage
- **Google Vertex AI Vector Search**: For vector embedding storage and similarity search
- **Google Generative AI**: For embedding generation and content summarization

## Architecture Diagrams

Three complementary diagrams are provided to illustrate different aspects of the system architecture:

1. [**Block Diagram**](marchiver_architecture.md): Shows the high-level components and their relationships
2. [**Data Flow Diagram**](marchiver_data_flow.md): Illustrates how data moves through the system
3. [**Component Architecture**](marchiver_component_architecture.md): Details the internal structure of each component

## Key Components

### Backend Components

#### API Layer
- **FastAPI Application**: Main application entry point
- **API Router**: Defines all API endpoints and routes requests to appropriate services

#### Service Layer
- **Document Service**: Core service for document operations
- **Embedding Service**: Generates vector embeddings for semantic search
- **Summarization Service**: Creates document summaries using AI
- **Web Service**: Fetches and processes web content

#### Data Layer
- **Document Models**: Define document structure and validation rules
- **Configuration**: Manages application settings and environment variables

### Frontend Components

#### User Interface
- **Popup UI**: Main extension interface for searching and saving
- **Document Viewer**: Displays archived content with tabs for content and summary
- **Options Page**: Configuration interface for user preferences

#### Background Processing
- **Background Service Worker**: Handles background tasks and API communication
- **Content Scripts**: Interact with web pages for content extraction

#### Storage
- **Chrome Storage**: Manages user preferences and settings

### External Services

- **Firestore**: Document database for content and metadata
- **Vertex AI Vector Search**: Vector database for semantic search
- **Google Generative AI**: AI services for embeddings and summarization

## Key Features

- **Data Acquisition & Storage**: Store web pages, documents, and other digital content
- **Content Embedding**: Generate vector embeddings for semantic search
- **Semantic Search**: Search for content based on meaning and context
- **Summarization**: Automatically summarize content using Google Gemini Pro
- **Data Management**: Edit metadata, track versions, and manage stored content

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

## Technical Implementation

### Backend (Python/FastAPI)
- **Language**: Python 3.8+
- **Framework**: FastAPI
- **Database**: Google Cloud Firestore
- **Vector Database**: Google Vertex AI Vector Search
- **AI Services**: Google Generative AI (Gemini Pro)
- **HTTP Client**: httpx for asynchronous requests
- **HTML Parsing**: BeautifulSoup for content extraction

### Frontend (Chrome Extension)
- **Manifest Version**: 3
- **Languages**: HTML, CSS, JavaScript
- **Storage**: Chrome Storage API
- **Browser APIs**: Tabs, Context Menus, Runtime

## Deployment Requirements

- Google Cloud Project with Firestore and Vertex AI enabled
- Google API Key for Generative AI access
- Environment variables for configuration
- Chrome browser for extension installation

## Conclusion

The Marchiver architecture provides a robust foundation for personal knowledge management, combining modern web technologies with advanced AI capabilities. The system's modular design allows for easy extension and maintenance, while the use of vector embeddings enables powerful semantic search functionality.
