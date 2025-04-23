"""
Configuration module for the Marchiver application.
Loads environment variables from .env file if available.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).resolve().parents[3] / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=str(env_path))

# API Configuration
API_TITLE = "Marchiver API"
API_DESCRIPTION = "API for the Marchiver personal knowledge archiving and retrieval system"
API_VERSION = "0.1.0"
API_PREFIX = "/api"

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "t")

# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Vertex AI Configuration
VERTEX_AI_INDEX_ENDPOINT = os.getenv("VERTEX_AI_INDEX_ENDPOINT")
VERTEX_AI_INDEX = os.getenv("VERTEX_AI_INDEX")
VERTEX_AI_EMBEDDING_ENDPOINT = os.getenv("VERTEX_AI_EMBEDDING_ENDPOINT")

# Embedding Model Configuration
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/embedding-001")
SUMMARIZATION_MODEL = os.getenv("SUMMARIZATION_MODEL", "gemini-pro-2.5")

# Firestore Configuration
FIRESTORE_COLLECTION = os.getenv("FIRESTORE_COLLECTION", "documents")

# CORS Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_METHODS = os.getenv("CORS_METHODS", "*").split(",")
CORS_HEADERS = os.getenv("CORS_HEADERS", "*").split(",")
