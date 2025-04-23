"""
Mock version of the main application for testing purposes.
Uses mock services instead of real ones.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_mock import router as api_router
from app.core.config import (
    API_TITLE, API_DESCRIPTION, API_VERSION, API_PREFIX,
    HOST, PORT, DEBUG, CORS_ORIGINS, CORS_METHODS, CORS_HEADERS
)

app = FastAPI(
    title=f"{API_TITLE} (Mock)",
    description=f"{API_DESCRIPTION} (Mock Version for Testing)",
    version=API_VERSION,
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

# Include API routes
app.include_router(api_router, prefix=API_PREFIX)

@app.get("/")
async def root():
    return {"message": "Welcome to Marchiver API (Mock Version)"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "mode": "mock"}

if __name__ == "__main__":
    print(f"Starting Marchiver API Mock Server at http://{HOST}:{PORT}")
    print(f"API documentation available at http://{HOST}:{PORT}/docs")
    print("WARNING: This is a mock version of the API for testing purposes.")
    print("It uses mock services instead of real ones and does not connect to Google Cloud.")
    uvicorn.run("main_mock:app", host=HOST, port=PORT, reload=DEBUG)
