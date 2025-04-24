# Marchiver

A personal knowledge archiving and retrieval system, inspired by the Memex, that allows users to save, organize, and intelligently access diverse digital information.

<img src="marchiver_logo.jpg" alt="Marchiver Logo" width="40%" />

## Architecture Documentation

Comprehensive architecture documentation is available in the [arch](./arch) directory:

- [Architecture Summary](./arch/marchiver_architecture_summary.md): A comprehensive overview of the entire system
- [Block Diagram](./arch/marchiver_architecture.md): High-level components and their relationships
- [Data Flow Diagram](./arch/marchiver_data_flow.md): Detailed illustration of how data moves through the system
- [Component Architecture](./arch/marchiver_component_architecture.md): Internal structure of each major component

See the [Architecture Documentation README](./arch/README.md) for information on viewing and modifying the diagrams.

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

## Installation and Usage

### 1. Set up the environment
First, create an environment file:
```
cp .env.sample .env
```

Edit the `.env` file to include your Google Cloud credentials. For testing purposes, you can use the dummy credentials:
```
GOOGLE_APPLICATION_CREDENTIALS=dummy-credentials.json
```

### 2. Start the backend
You have two options:

#### Option A: Run the real backend
This requires valid Google Cloud credentials:
```
./start_backend.sh
```

#### Option B: Run the mock backend (for testing)
This uses mock services and doesn't require real credentials:
```
./start_mock_backend.sh
```

The script will prompt you to install dependencies if needed. The backend server will run on http://localhost:8000 by default.

### 3. Test the frontend
Run the frontend test script:
```
./test_frontend.sh
```

This will open `frontend/test_extension.html` in your default browser, which provides a testing interface for the extension.

### 4. Chrome Extension
For full functionality, you need to load the extension into Chrome:

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in the top-right corner)
3. Click "Load unpacked" and select the `frontend` directory from this project
4. The Marchiver extension should now appear in your Chrome extensions
