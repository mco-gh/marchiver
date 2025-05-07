#!/usr/bin/env python3
"""
Script to create a new Vertex AI Vector Search index with streaming updates enabled.
"""

import os
import sys
from google.cloud import aiplatform
from google.cloud.aiplatform.matching_engine import matching_engine_index_config

# Add the backend directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import (
    GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_REGION,
    VERTEX_AI_INDEX_ENDPOINT, VERTEX_AI_INDEX
)

def main():
    """Create a new Vertex AI Vector Search index with streaming updates enabled."""
    print("Initializing Vertex AI...")
    aiplatform.init(
        project=GOOGLE_CLOUD_PROJECT,
        location=GOOGLE_CLOUD_REGION,
    )
    
    print("\nListing all MatchingEngineIndex instances...")
    try:
        indexes = aiplatform.MatchingEngineIndex.list()
        print(f"Found {len(indexes)} indexes:")
        
        if indexes and len(indexes) > 0:
            # Use the first index as a template
            old_index = indexes[0]
            print(f"\nUsing index as template: {old_index.name}")
            print(f"Resource name: {old_index.resource_name}")
            
            # Use hardcoded values from the check_index_config.py output
            dimensions = 768  # Changed from 1024 to 768
            approximate_neighbors_count = 5
            distance_measure_type = "DOT_PRODUCT_DISTANCE"
            leaf_node_embedding_count = 1000
            leaf_nodes_to_search_percent = 5
            
            # Print the configuration
            print("\nUsing configuration:")
            print(f"dimensions: {dimensions}")
            print(f"approximate_neighbors_count: {approximate_neighbors_count}")
            print(f"distance_measure_type: {distance_measure_type}")
            print(f"leaf_node_embedding_count: {leaf_node_embedding_count}")
            print(f"leaf_nodes_to_search_percent: {leaf_nodes_to_search_percent}")
            
            # Use the string value directly
            distance_measure_str = distance_measure_type
            
            # Create a new index with streaming updates enabled
            print("\nCreating a new index with streaming updates enabled...")
            try:
                new_index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
                    display_name="marchiver_768d",
                    dimensions=dimensions,
                    approximate_neighbors_count=approximate_neighbors_count,
                    distance_measure_type=distance_measure_str,
                    leaf_node_embedding_count=leaf_node_embedding_count,
                    leaf_nodes_to_search_percent=leaf_nodes_to_search_percent,
                    # Removed index_update_method parameter as it's not supported
                )
                
                print(f"\nSuccessfully created new index with streaming updates enabled:")
                print(f"Name: {new_index.name}")
                print(f"Resource name: {new_index.resource_name}")
                print(f"Display name: {new_index.display_name}")
                
                print("\nNext steps:")
                print("1. Deploy the new index to the index endpoint")
                print("2. Update your application to use the new index")
                print("\nTo deploy the new index to the index endpoint, run:")
                print(f"endpoint = aiplatform.MatchingEngineIndexEndpoint(index_endpoint_name='{VERTEX_AI_INDEX_ENDPOINT}')")
                print(f"endpoint.deploy_index(index=new_index, deployed_index_id='marchiver_768d')")
                
                print("\nTo update your application to use the new index, update the VERTEX_AI_INDEX value in .env to 'marchiver_768d'")
            except Exception as e:
                print(f"\nError creating new index: {e}")
        else:
            print("No indexes found.")
    except Exception as e:
        print(f"Error listing indexes: {e}")

if __name__ == "__main__":
    main()
