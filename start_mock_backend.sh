#!/bin/bash

# Start the Marchiver mock backend server for testing

echo "Starting Marchiver mock backend server..."

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
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

# Prompt to install requirements if needed
read -p "Do you want to install/update dependencies? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing dependencies..."
    uv pip install -r backend/requirements.txt
fi

# Check for environment variables
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Using default configuration."
    echo "For testing, this is fine as the mock server doesn't need real credentials."
else
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
fi

# Make the script executable
chmod +x backend/main_mock.py

# Start the server
echo "Starting mock server..."
cd backend && python main_mock.py

echo "Server stopped."
