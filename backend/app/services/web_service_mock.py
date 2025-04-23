"""
Mock web service for testing purposes.
Returns predefined content instead of fetching real web pages.
"""

from typing import Tuple

class WebServiceMock:
    """Mock service for fetching web pages."""
    
    def __init__(self):
        """Initialize the mock web service."""
        print("Initialized Mock Web Service")
        
        # Predefined responses for common URLs
        self.predefined_responses = {
            "https://en.wikipedia.org/wiki/Memex": (
                "The Memex is the name of the hypothetical electromechanical device that Vannevar Bush described in his 1945 article \"As We May Think\". Bush envisioned the Memex as a device in which individuals would compress and store all of their books, records, and communications, mechanized so that it may be consulted with exceeding speed and flexibility. The Memex would provide an \"enlarged intimate supplement to one's memory\". The concept of the Memex influenced the development of early hypertext systems, eventually leading to the creation of the World Wide Web, and personal knowledge base software.",
                "Memex - Wikipedia"
            ),
            "https://en.wikipedia.org/wiki/Artificial_intelligence": (
                "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals. The term \"artificial intelligence\" had previously been used to describe machines that mimic and display \"human\" cognitive skills that are associated with the human mind, such as \"learning\" and \"problem-solving\". This definition has since been rejected by major AI researchers who now describe AI in terms of rationality and acting rationally, which does not limit how intelligence can be articulated.",
                "Artificial intelligence - Wikipedia"
            ),
            "https://example.com": (
                "This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission. More information...",
                "Example Domain"
            )
        }
    
    async def fetch_web_page(self, url: str) -> Tuple[str, str]:
        """
        Return predefined content for the given URL.
        
        Args:
            url: The URL of the web page to fetch.
            
        Returns:
            A tuple of (content, title).
        """
        # Check if we have a predefined response for this URL
        if url in self.predefined_responses:
            content, title = self.predefined_responses[url]
            print(f"Returning predefined content for URL: {url}")
            return content, title
        
        # For unknown URLs, generate a mock response
        print(f"Generating mock content for URL: {url}")
        return f"This is mock content for {url}", f"Mock Page: {url}"
    
    async def close(self):
        """Close the mock service."""
        print("Closing Mock Web Service")
