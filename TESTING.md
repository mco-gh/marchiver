# Testing Marchiver

This document provides instructions for testing the Marchiver application. The testing setup includes mock services that don't require real Google Cloud credentials, making it easy to test the application without setting up a real backend.

## Prerequisites

- Python 3.8 or higher
- A modern web browser (Chrome, Firefox, Edge, etc.)

## Setup

1. Clone the repository and navigate to the project directory:
   ```
   git clone https://github.com/yourusername/marchiver.git
   cd marchiver
   ```

2. The testing environment has been set up with mock services that don't require real Google Cloud credentials. The following files have been created:
   - `.env` - Environment variables with dummy values
   - `dummy-credentials.json` - Dummy Google Cloud credentials
   - Mock service implementations in `backend/app/services/`
   - Mock API routes in `backend/app/api/routes_mock.py`
   - Mock main application in `backend/main_mock.py`

## Testing the Backend

1. Start the mock backend server:
   ```
   ./start_mock_backend.sh
   ```
   This will start a FastAPI server on http://0.0.0.0:8000 with mock implementations of all services.

2. Run the API tests:
   ```
   python backend/test_api_mock.py
   ```
   This will test the basic functionality of the API, including the health check and root endpoint.

3. You can also explore the API documentation at http://0.0.0.0:8000/docs to see all available endpoints and test them manually.

## Testing the Frontend

1. Make sure the mock backend server is running (see above).

2. Open the test extension page:
   ```
   ./test_frontend.sh
   ```
   This will open the `frontend/test_extension.html` file in your default browser.

3. On the test page, you can test various features of the extension:
   - Test 1: Save Current Page - Tests saving the current page to the archive
   - Test 2: Summarize Current Page - Tests summarizing the current page and saving it to the archive
   - Test 3: Search Archive - Tests searching the archive for the term "test"
   - Test 4: Check API Connection - Tests if the extension can connect to the Marchiver API
   - Test 5: Keyboard Shortcuts - Tests the keyboard shortcuts for saving and summarizing pages

## Testing the Chrome Extension

If you want to test the actual Chrome extension:

1. Make sure the mock backend server is running (see above).

2. Open Chrome and navigate to `chrome://extensions/`.

3. Enable "Developer mode" (toggle in the top-right corner).

4. Click "Load unpacked" and select the `frontend` directory.

5. The Marchiver extension should now be installed and visible in your browser toolbar.

6. Click on the extension icon to open the popup and test its functionality.

## Troubleshooting

- If you encounter issues with the mock backend server, check the terminal output for error messages.
- If the extension can't connect to the API, make sure the backend server is running and the API endpoint in the extension settings is correct (default: http://localhost:8000/api).
- If you need to modify the mock services, you can edit the files in `backend/app/services/` with the `_mock` suffix.

## Notes

- The mock services use in-memory storage instead of Firestore, so data will be lost when the server is restarted.
- The mock embedding service generates random embeddings instead of using Google Vertex AI.
- The mock summarization service creates simple summaries by taking the first and last few words of the text.
- The mock web service returns predefined content for common URLs and generates mock content for unknown URLs.
