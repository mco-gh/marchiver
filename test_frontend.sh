#!/bin/bash

# Test the Marchiver frontend extension

echo "Opening Marchiver extension test page..."

# Check if the frontend directory exists
if [ ! -d "frontend" ]; then
    echo "Error: frontend directory not found"
    exit 1
fi

# Check if the test extension HTML file exists
if [ ! -f "frontend/test_extension.html" ]; then
    echo "Error: test_extension.html not found"
    exit 1
fi

# Get the absolute path to the test extension HTML file
TEST_PAGE_PATH=$(realpath frontend/test_extension.html)

# Detect the operating system
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Opening test page in default browser..."
    open "$TEST_PAGE_PATH"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "Opening test page in default browser..."
    xdg-open "$TEST_PAGE_PATH"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    echo "Opening test page in default browser..."
    start "$TEST_PAGE_PATH"
else
    echo "Unsupported operating system: $OSTYPE"
    echo "Please open the test page manually: $TEST_PAGE_PATH"
fi

echo "Test page opened. Make sure the mock backend server is running."
echo "You can start the mock backend server with: ./start_mock_backend.sh"
