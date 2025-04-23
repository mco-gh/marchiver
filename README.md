# Marchiver

A personal knowledge archiving and retrieval system, inspired by the Memex, that allows users to save, organize, and intelligently access diverse digital information.

![Marchiver Logo](marchiver_logo.jpg)

## Overview

Marchiver is a comprehensive system for archiving and retrieving digital content. It allows users to save web pages, documents, and other digital content, and then search and retrieve them using both traditional and semantic search methods.

The system consists of two main components:
1. A backend API built with FastAPI and Python
2. A Chrome extension for easy content saving and retrieval

## Features

- **Data Acquisition & Storage**: Store web pages, documents, images, and other digital content
- **Content Embedding**: Generate vector embeddings for semantic search and similarity analysis
- **Semantic Search**: Search for content based on meaning and context
- **Summarization**: Automatically summarize content using Google Gemini Pro 2.5
- **Data Management**: Edit metadata, track versions, and manage stored content
- **Chrome Extension**: Easily save and search content from your browser

## System Architecture

### Backend

- **FastAPI**: RESTful API for all core functionalities
- **Firestore**: Document storage
- **Google Vertex AI Vector Search**: Vector storage for embeddings
- **Google Gemini**: For embeddings and summarization

### Frontend

- **Chrome Extension**: JavaScript-based extension for easy content saving and retrieval

## Setup Instructions

### Backend Setup

1. Install Python dependencies:
   ```
   cd backend
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/firebase-credentials.json"
   export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
   export GOOGLE_CLOUD_REGION="your-gcp-region"
   export GOOGLE_API_KEY="your-google-api-key"
   export VERTEX_AI_INDEX_ENDPOINT="your-vertex-ai-index-endpoint"
   export VERTEX_AI_INDEX="your-vertex-ai-index"
   export VERTEX_AI_EMBEDDING_ENDPOINT="your-vertex-ai-embedding-endpoint"
   ```

3. Run the backend server:
   ```
   cd backend
   python main.py
   ```

### Chrome Extension Setup

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in the top-right corner)
3. Click "Load unpacked" and select the `frontend` directory
4. The Marchiver extension should now be installed and visible in your browser toolbar

## Usage

### Saving Content

- Click the Marchiver extension icon in your browser toolbar
- Click "Save Current Page" to save the current page
- Click "Summarize & Save" to generate a summary and save the page

### Searching Content

- Click the Marchiver extension icon in your browser toolbar
- Enter your search query in the search box
- Toggle "Semantic Search" to enable or disable semantic search
- Click "Search" to search your archived content

### Viewing and Managing Content

- Click on a search result to view the full content
- Use the tabs to switch between the original content and the summary
- Click "Edit" to modify metadata such as title, tags, and summary

## API Documentation

The backend API provides the following endpoints:

- `GET /api/documents`: Search for documents
- `POST /api/documents`: Create a new document
- `GET /api/documents/{document_id}`: Get a document by ID
- `PUT /api/documents/{document_id}`: Update a document
- `DELETE /api/documents/{document_id}`: Delete a document
- `GET /api/documents/{document_id}/similar`: Get similar documents
- `POST /api/web/fetch`: Fetch and optionally save a web page
- `POST /api/embeddings`: Generate an embedding for text
- `POST /api/summarize`: Summarize text

## Development

### Backend Development

The backend is structured as follows:
- `main.py`: Entry point for the FastAPI application
- `app/api/routes.py`: API route definitions
- `app/models/`: Data models
- `app/services/`: Business logic services

### Frontend Development

The Chrome extension is structured as follows:
- `manifest.json`: Extension manifest
- `popup.html`: Main extension popup
- `options.html`: Settings page
- `document.html`: Document viewer
- `js/`: JavaScript files
- `css/`: CSS stylesheets
- `images/`: Extension icons and images

## License

This project is licensed under the terms of the license included in the repository.
