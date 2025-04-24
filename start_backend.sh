#!/bin/bash

# Start the Marchiver backend server

echo "Starting Marchiver backend server..."

# Check if Python 3 is installed
if ! command -v uv run python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if the backend directory exists
if [ ! -d "backend" ]; then
    echo "Error: backend directory not found"
    exit 1
fi

# Check if requirements are installed
echo "Checking dependencies..."
if [ ! -f "backend/requirements.txt" ]; then
    echo "Error: requirements.txt not found"
    exit 1
fi

# Remove old virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Removing old virtual environment..."
    rm -rf .venv
fi

# Create a new virtual environment with Python 3
echo "Creating virtual environment with Python 3..."
uv run python3 -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Verify we're using Python 3
python --version

# Prompt to install requirements if needed
read -p "Do you want to install/update dependencies? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing dependencies..."
    # Install packages one by one to avoid dependency issues
    uv run python3 -m pip install --upgrade pip
    
    # Install core packages needed for the server to run
    echo "Installing uvicorn..."
    uv run python3 -m pip install uvicorn==0.23.2
    
    echo "Installing starlette (FastAPI dependency)..."
    uv run python3 -m pip install starlette==0.27.0
    
    echo "Installing typing-extensions (FastAPI dependency)..."
    uv run python3 -m pip install typing-extensions==4.8.0
    
    echo "Installing anyio (FastAPI dependency)..."
    uv run python3 -m pip install anyio==3.7.1
    
    echo "Installing pydantic (FastAPI dependency)..."
    uv run python3 -m pip install pydantic==1.10.13
    
    echo "Installing fastapi..."
    uv run python3 -m pip install fastapi==0.104.1 --no-deps
    
    echo "Installing python-dotenv..."
    uv run python3 -m pip install python-dotenv==1.0.0
    
    echo "Installing requests..."
    uv run python3 -m pip install requests==2.31.0
    
    echo "Installing other dependencies..."
    uv run python3 -m pip install httpx==0.25.0 beautifulsoup4==4.12.2
    
    # Skip problematic packages: pydantic, google-cloud-aiplatform, lxml
    echo "Note: Some packages were skipped due to compatibility issues."
fi

# Check for environment variables
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Using default configuration."
    echo "For production use, please create a .env file with your configuration."
else
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
fi

# Start the server
echo "Starting server..."
cd backend && uv run python3 main.py

echo "Server stopped."
