#!/usr/bin/env python3
"""
Script to generate a PNG image from the architecture diagram HTML file.
Requires playwright to be installed: pip install playwright
After installation, you need to install the browser: playwright install
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def generate_image():
    # Get the current directory
    current_dir = Path.cwd()
    
    # HTML file path
    html_path = current_dir / "marchiver_architecture_diagram.html"
    
    # Output PNG path
    output_path = current_dir / "marchiver_architecture.png"
    
    print(f"Generating image from {html_path}")
    print(f"Output will be saved to {output_path}")
    
    async with async_playwright() as p:
        # Launch a browser
        browser = await p.chromium.launch()
        
        # Create a new page
        page = await browser.new_page()
        
        # Go to the HTML file
        await page.goto(f"file://{html_path}")
        
        # Wait for the mermaid diagram to render
        await page.wait_for_selector(".mermaid svg", state="visible", timeout=10000)
        
        # Wait a bit more to ensure complete rendering
        await asyncio.sleep(2)
        
        # Take a screenshot of the diagram
        diagram = await page.query_selector(".mermaid")
        if diagram:
            await diagram.screenshot(path=str(output_path))
            print(f"Screenshot saved to {output_path}")
        else:
            print("Could not find the diagram element")
        
        # Close the browser
        await browser.close()

if __name__ == "__main__":
    asyncio.run(generate_image())
