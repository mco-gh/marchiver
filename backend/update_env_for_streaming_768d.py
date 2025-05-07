#!/usr/bin/env python3
"""
Script to update the .env file to use the new 768-dimensional streaming index.
"""

import os
import sys
import re

# Add the backend directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Update the .env file to use the new 768-dimensional streaming index."""
    # Path to the .env file
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    
    # Check if the .env file exists
    if not os.path.exists(env_path):
        print(f"ERROR: .env file not found at {env_path}")
        print("Creating a new .env file from .env.sample")
        
        # Path to the .env.sample file
        env_sample_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env.sample')
        
        # Check if the .env.sample file exists
        if not os.path.exists(env_sample_path):
            print(f"ERROR: .env.sample file not found at {env_sample_path}")
            return
        
        # Copy the .env.sample file to .env
        with open(env_sample_path, 'r') as f:
            env_sample_content = f.read()
        
        with open(env_path, 'w') as f:
            f.write(env_sample_content)
        
        print(f"Created new .env file at {env_path}")
    
    # Read the .env file
    with open(env_path, 'r') as f:
        env_content = f.read()
    
    # Update the VERTEX_AI_INDEX value
    new_env_content = re.sub(
        r'VERTEX_AI_INDEX=.*',
        'VERTEX_AI_INDEX=marchiver_streaming_768d_1746631997838',
        env_content
    )
    
    # Write the updated content back to the .env file
    with open(env_path, 'w') as f:
        f.write(new_env_content)
    
    print(f"Updated .env file at {env_path}")
    print("VERTEX_AI_INDEX is now set to 'marchiver_streaming_768d_1746631997838'")

if __name__ == "__main__":
    main()
