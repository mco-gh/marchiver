#!/usr/bin/env python3
"""
Script to deploy the streaming index to the index endpoint.
"""

import os
import sys
from google.cloud import aiplatform

# Add the backend directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import (
    GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_REGION,
    VERTEX_AI_INDEX_ENDPOINT, VERTEX_AI_INDEX
)

def main():
    """Deploy the streaming index to the index endpoint."""
    print("Initializing Vertex AI...")
    aiplatform.init(
        project=GOOGLE_CLOUD_PROJECT,
        location=GOOGLE_CLOUD_REGION,
    )
    
    # The resource name of the new index
    new_index_resource_name = "projects/1082996892307/locations/us-central1/indexes/5627179564678512640"
    
    print(f"\nLoading the new index: {new_index_resource_name}")
    try:
        new_index = aiplatform.MatchingEngineIndex(index_name=new_index_resource_name)
        print(f"Successfully loaded index: {new_index.name}")
        
        print(f"\nLoading the index endpoint: {VERTEX_AI_INDEX_ENDPOINT}")
        endpoint = aiplatform.MatchingEngineIndexEndpoint(index_endpoint_name=VERTEX_AI_INDEX_ENDPOINT)
        print(f"Successfully loaded index endpoint: {endpoint.name}")
        
        # Deploy the new index to the index endpoint
        print("\nDeploying the new index to the index endpoint...")
        deployed_index = endpoint.deploy_index(
            index=new_index,
                deployed_index_id="marchiver_streaming_768d",
            display_name="marchiver_streaming_768d",
        )
        
        print(f"\nSuccessfully deployed index to endpoint:")
        print(f"Deployed index ID: {deployed_index.id}")
        
        print("\nNext steps:")
        print("1. Update your application to use the new index")
        print("2. Update the VERTEX_AI_INDEX value in .env to 'marchiver_streaming_768d'")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
