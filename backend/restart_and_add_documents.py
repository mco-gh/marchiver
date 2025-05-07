#!/usr/bin/env python3
"""
Script to restart the Python process and add test documents.
"""

import os
import sys
import subprocess

def main():
    """Restart the Python process and add test documents."""
    print("Restarting the Python process to pick up new environment variables...")
    
    # Get the current environment variables
    env = os.environ.copy()
    
    # Read the .env file
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env[key] = value
    
    # Print the VERTEX_AI_INDEX value
    print(f"VERTEX_AI_INDEX from .env: {env.get('VERTEX_AI_INDEX', 'Not found')}")
    
    # Run the add_test_documents.py script with the updated environment variables
    print("\nRunning add_test_documents.py with updated environment variables...")
    subprocess.run([sys.executable, "backend/add_test_documents.py"], env=env)

if __name__ == "__main__":
    main()
