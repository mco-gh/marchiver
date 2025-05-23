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
    uv run python3 -m pip install --trusted-host pypi.org --upgrade pip -r backend/requirements.txt
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
