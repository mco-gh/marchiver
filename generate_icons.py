#!/usr/bin/env python3
"""
Script to generate icons for the Marchiver Chrome extension.
This script takes the marchiver_logo.jpg file and creates icons in different sizes.
"""

import os
from PIL import Image

def generate_icons():
    """Generate icons in different sizes from the logo."""
    # Create the images directory if it doesn't exist
    if not os.path.exists("frontend/images"):
        os.makedirs("frontend/images")
    
    # Load the logo
    try:
        logo = Image.open("marchiver_logo.jpg")
    except IOError:
        print("Error: marchiver_logo.jpg not found.")
        return
    
    # Generate icons in different sizes
    sizes = [16, 48, 128]
    for size in sizes:
        # Resize the logo
        resized_logo = logo.resize((size, size), Image.ANTIALIAS)
        
        # Save the resized logo
        output_path = "frontend/images/icon{}.png".format(size)
        resized_logo.save(output_path, "PNG")
        print("Generated {}".format(output_path))
    
    print("Icon generation complete.")

if __name__ == "__main__":
    generate_icons()
