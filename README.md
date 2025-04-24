# Marchiver

A personal knowledge archiving and retrieval system, inspired by the Memex, that allows users to save, organize, and intelligently access diverse digital information.

![Marchiver Logo](marchiver_logo.jpg)

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
