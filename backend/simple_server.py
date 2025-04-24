#!/usr/bin/env python3
"""
Simple HTTP server for testing the Marchiver backend.
This is a temporary solution until the compatibility issues with FastAPI and pydantic are resolved.
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# Load environment variables from .env file if it exists
if os.path.exists('../.env'):
    print("Loading environment variables from .env file...")
    with open('../.env', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key] = value

# Server configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "t")

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200, content_type="application/json"):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()
        
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == "/":
            self._set_headers()
            response = {"message": "Welcome to Marchiver API (Simple Server)"}
            self.wfile.write(json.dumps(response).encode())
        elif path == "/health":
            self._set_headers()
            response = {"status": "healthy", "mode": "simple"}
            self.wfile.write(json.dumps(response).encode())
        elif path == "/api/documents":
            self._set_headers()
            response = {"documents": [
                {"id": "1", "title": "Sample Document 1", "content": "This is a sample document."},
                {"id": "2", "title": "Sample Document 2", "content": "This is another sample document."}
            ]}
            self.wfile.write(json.dumps(response).encode())
        else:
            self._set_headers(404)
            response = {"error": "Not found"}
            self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        content_length = int(self.headers['Content-Length']) if 'Content-Length' in self.headers else 0
        post_data = self.rfile.read(content_length)
        
        if path == "/api/documents":
            self._set_headers(201)
            response = {"message": "Document created successfully", "document_id": "3"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self._set_headers(404)
            response = {"error": "Not found"}
            self.wfile.write(json.dumps(response).encode())

def run_server():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Starting Marchiver Simple Server at http://{HOST}:{PORT}")
    print("This is a temporary server for testing purposes.")
    print("Press Ctrl+C to stop the server.")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
