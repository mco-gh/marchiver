import httpx
from bs4 import BeautifulSoup
from typing import Tuple

class WebService:
    """Service for fetching web pages."""
    
    def __init__(self):
        """Initialize the web service."""
        self.client = httpx.AsyncClient(
            follow_redirects=True,
            timeout=30.0,
        )
    
    async def fetch_web_page(self, url: str) -> Tuple[str, str]:
        """
        Fetch a web page and extract its content and title.
        
        Args:
            url: The URL of the web page to fetch.
            
        Returns:
            A tuple of (content, title).
        """
        try:
            # Fetch the web page
            response = await self.client.get(url)
            response.raise_for_status()
            
            # Parse the HTML
            soup = BeautifulSoup(response.text, "lxml")
            
            # Extract the title
            title = soup.title.string if soup.title else url
            
            # Extract the main content
            # This is a simple implementation that just gets the text
            # In a real implementation, you might want to use a more sophisticated
            # approach to extract the main content
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()
            
            # Get the text
            content = soup.get_text(separator="\n", strip=True)
            
            return content, title
        except Exception as e:
            print(f"Failed to fetch web page: {e}")
            return f"Failed to fetch web page: {e}", url
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
