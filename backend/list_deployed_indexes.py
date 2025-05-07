#!/usr/bin/env python3
"""
Script to list deployed indexes on the index endpoint.
"""

import os
import sys
from google.cloud import aiplatform

# Add the backend directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import (
    GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_REGION,
    VERTEX_AI_INDEX_ENDPOINT
)

def main():
    """List deployed indexes on the index endpoint."""
    print("Initializing Vertex AI...")
    aiplatform.init(
        project=GOOGLE_CLOUD_PROJECT,
        location=GOOGLE_CLOUD_REGION,
    )
    
    print(f"\nLoading the index endpoint: {VERTEX_AI_INDEX_ENDPOINT}")
    try:
        endpoint = aiplatform.MatchingEngineIndexEndpoint(index_endpoint_name=VERTEX_AI_INDEX_ENDPOINT)
        print(f"Successfully loaded index endpoint: {endpoint.name}")
        
        # List deployed indexes
        print("\nDeployed indexes:")
        if hasattr(endpoint, 'deployed_indexes') and endpoint.deployed_indexes:
            for i, deployed_index in enumerate(endpoint.deployed_indexes):
                print(f"\nDeployed Index {i+1}:")
                if isinstance(deployed_index, dict):
                    for key, value in deployed_index.items():
                        print(f"  {key}: {value}")
                else:
                    print(f"  {deployed_index}")
        else:
            print("No deployed indexes found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
