#!/bin/bash

# Start the Marchiver simple backend server for testing

echo "Starting Marchiver simple backend server..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if the backend directory exists
if [ ! -d "backend" ]; then
    echo "Error: backend directory not found"
    exit 1
fi

# Check if the simple server script exists
if [ ! -f "backend/simple_server.py" ]; then
    echo "Error: simple_server.py not found"
    exit 1
fi

# Make the script executable
chmod +x backend/simple_server.py

# Check for environment variables
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Using default configuration."
    echo "For testing, this is fine as the simple server doesn't need real credentials."
else
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
fi

# Start the server
echo "Starting simple server..."
cd backend && python3 simple_server.py

echo "Server stopped."
