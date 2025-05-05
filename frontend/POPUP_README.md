# Marchiver Chrome Extension: Popup-Based Approach

This document explains the popup-based approach used in the Marchiver Chrome extension.

## Overview

The Marchiver Chrome extension now uses a popup-based approach for testing and interacting with the extension. This approach is more reliable than the previous bridge-based approach because it uses the standard Chrome extension messaging API directly, without trying to bridge between web pages and the extension.

## Key Components

1. **Popup UI (`popup.html` and `js/popup.js`)**
   - Provides a user interface for interacting with the extension
   - Allows testing of key extension functionality
   - Communicates directly with the background script using Chrome's messaging API

2. **Background Script (`js/background.js`)**
   - Handles messages from the popup
   - Implements the core extension functionality
   - Responds to context menu clicks

3. **Content Script (`js/content.js`)**
   - Injects into web pages
   - Can communicate with the background script

## How It Works

1. When the user clicks the extension icon in the Chrome toolbar, the popup opens
2. The popup provides buttons to test different extension features:
   - Check Extension Status: Tests if the extension is active
   - Save Current Page: Tests the save page functionality
   - Summarize Current Page: Tests the summarize page functionality
   - Check API Connection: Tests the connection to the backend API

3. When a button is clicked, the popup sends a message to the background script
4. The background script processes the message and sends a response
5. The popup displays the response

## Why This Approach Is Better

The popup-based approach is more reliable because:

1. It uses the standard Chrome extension messaging API
2. It doesn't rely on injecting code into web pages, which can be unreliable
3. It provides a simple, direct way to test the extension
4. It avoids the "Cannot read properties of undefined (reading 'sendMessage')" error that occurred with the bridge-based approach

## Testing the Extension

1. Load the extension in Chrome:
   - Go to `chrome://extensions/`
   - Enable "Developer mode" (toggle in the top-right corner)
   - Click "Load unpacked" and select the `frontend` directory

2. Click on the Marchiver extension icon in the Chrome toolbar to open the popup

3. Use the buttons in the popup to test the extension

## Context Menu Integration

The extension also adds context menu items:
- "Save page to Marchiver": Saves the current page to Marchiver
- "Summarize and save page": Summarizes and saves the current page

These context menu items provide a convenient way to use the extension without opening the popup.
