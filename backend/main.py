import uvicorn
import firebase_admin
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.routes import router as api_router
from app.core.config import (
    API_TITLE, API_DESCRIPTION, API_VERSION, API_PREFIX,
    HOST, PORT, DEBUG, CORS_ORIGINS, CORS_METHODS, CORS_HEADERS
)

# Custom middleware to log requests
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log the request as soon as it arrives
        path = request.url.path
        method = request.method
        query_params = dict(request.query_params)
        
        # Print a brief summary of the request
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Request received: {method} {path}")
        if query_params:
            print(f"Query parameters: {query_params}")
        
        # Process the request
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log additional information after the request is completed
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Request completed: {method} {path}")
        print(f"Status code: {response.status_code}")
        print(f"Processing time: {process_time:.4f} seconds")
        
        return response

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
)

# Add request logging middleware
app.add_middleware(RequestLoggingMiddleware)

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
    return {"message": "Welcome to Marchiver API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get(f"{API_PREFIX}/health")
async def api_health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=DEBUG)
