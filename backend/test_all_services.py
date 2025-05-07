#!/usr/bin/env python3
"""
Comprehensive test script for the Marchiver backend services.
This script tests all the backend services by calling their APIs and verifying the responses.
"""

import os
import sys
import json
import asyncio
import httpx
import time
from typing import Dict, Any, List, Optional

# Add the backend directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.embedding_service import EmbeddingService
from app.services.summarization_service import SummarizationService
from app.services.web_service import WebService

# Try to import DocumentService, but don't fail if it's not available
try:
    from app.services.document_service import DocumentService
    DOCUMENT_SERVICE_AVAILABLE = True
except ImportError:
    print("Warning: DocumentService could not be imported. Document tests will be skipped.")
    DOCUMENT_SERVICE_AVAILABLE = False

# Constants
API_BASE_URL = "http://localhost:8000/api"
TEST_URL = "https://en.wikipedia.org/wiki/Artificial_intelligence"
TEST_DOCUMENT_ID = "test_document_" + str(int(time.time()))

class BackendTester:
    """Test all backend services."""
    
    def __init__(self):
        """Initialize the tester."""
        self.client = httpx.AsyncClient(timeout=60.0)  # Longer timeout for API calls
        self.embedding_service = EmbeddingService()
        self.summarization_service = SummarizationService()
        self.web_service = WebService()
        
        # Initialize document service if available
        if DOCUMENT_SERVICE_AVAILABLE:
            try:
                self.document_service = DocumentService()
            except Exception as e:
                print(f"Warning: Failed to initialize DocumentService: {e}")
                self.document_service = None
        else:
            self.document_service = None
        
        # Track test results
        self.results = {
            "embedding_service": {"success": False, "details": ""},
            "summarization_service": {"success": False, "details": ""},
            "web_service": {"success": False, "details": ""},
            "api_health": {"success": False, "details": ""},
            "api_fetch": {"success": False, "details": ""},
            "api_summarize": {"success": False, "details": ""},
            "api_search": {"success": False, "details": ""},
        }
        
        # Add document service test result only if available
        if DOCUMENT_SERVICE_AVAILABLE:
            self.results["document_service"] = {"success": False, "details": ""}
    
    async def test_embedding_service(self):
        """Test the embedding service."""
        print("\n=== Testing Embedding Service ===")
        try:
            text = "This is a test of the embedding service. It should generate an embedding vector for this text."
            print(f"Generating embedding for text: '{text}'")
            
            embedding = await self.embedding_service.generate_embedding(text)
            
            if embedding and len(embedding) > 0:
                print("Embedding generated successfully!")
                print(f"Embedding length: {len(embedding)}")
                print(f"First 5 values: {embedding[:5]}")
                self.results["embedding_service"]["success"] = True
                self.results["embedding_service"]["details"] = f"Generated embedding of length {len(embedding)}"
                return True
            else:
                print("Failed to generate embedding: Empty result")
                self.results["embedding_service"]["details"] = "Empty embedding result"
                return False
        except Exception as e:
            print(f"Error testing embedding service: {e}")
            self.results["embedding_service"]["details"] = f"Error: {str(e)}"
            return False
    
    async def test_summarization_service(self):
        """Test the summarization service."""
        print("\n=== Testing Summarization Service ===")
        try:
            text = """
            Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to intelligence of humans and other animals. 
            Example tasks in which this is done include speech recognition, computer vision, translation between (natural) languages, 
            as well as other mappings of inputs. AI applications include advanced web search engines, recommendation systems, 
            understanding human speech, self-driving cars, automated decision-making and competing at the highest level in strategic game systems.
            
            As machines become increasingly capable, along with tasks considered to require "intelligence", tasks considered to require "intelligence" 
            are often removed from the definition of AI, a phenomenon known as the AI effect.
            """
            
            print(f"Generating summary for text of length {len(text)}")
            
            summary = await self.summarization_service.summarize(text)
            
            if summary and len(summary) > 0:
                print("Summary generated successfully!")
                print(f"Summary: {summary}")
                self.results["summarization_service"]["success"] = True
                self.results["summarization_service"]["details"] = f"Generated summary of length {len(summary)}"
                return True
            else:
                print("Failed to generate summary: Empty result")
                self.results["summarization_service"]["details"] = "Empty summary result"
                return False
        except Exception as e:
            print(f"Error testing summarization service: {e}")
            self.results["summarization_service"]["details"] = f"Error: {str(e)}"
            return False
    
    async def test_web_service(self):
        """Test the web service."""
        print("\n=== Testing Web Service ===")
        try:
            print(f"Fetching content from URL: {TEST_URL}")
            
            content, title = await self.web_service.fetch_web_page(TEST_URL)
            
            if content and len(content) > 0:
                print("Content fetched successfully!")
                print(f"Content length: {len(content)}")
                print(f"First 100 characters: {content[:100]}...")
                self.results["web_service"]["success"] = True
                self.results["web_service"]["details"] = f"Fetched content of length {len(content)}"
                return True
            else:
                print("Failed to fetch content: Empty result")
                self.results["web_service"]["details"] = "Empty content result"
                return False
        except Exception as e:
            print(f"Error testing web service: {e}")
            self.results["web_service"]["details"] = f"Error: {str(e)}"
            return False
    
    async def test_api_health(self):
        """Test the API health endpoint."""
        print("\n=== Testing API Health Endpoint ===")
        try:
            url = f"{API_BASE_URL}/health"
            print(f"Sending GET request to {url}")
            
            response = await self.client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                print(f"API health check successful: {data}")
                self.results["api_health"]["success"] = True
                self.results["api_health"]["details"] = f"Status: {data.get('status', 'unknown')}"
                return True
            else:
                print(f"API health check failed: {response.status_code} {response.text}")
                self.results["api_health"]["details"] = f"Status code: {response.status_code}"
                return False
        except Exception as e:
            print(f"Error testing API health: {e}")
            self.results["api_health"]["details"] = f"Error: {str(e)}"
            return False
    
    async def test_api_fetch(self):
        """Test the API fetch endpoint."""
        print("\n=== Testing API Fetch Endpoint ===")
        try:
            url = f"{API_BASE_URL}/web/fetch"
            params = {"url": TEST_URL}
            print(f"Sending POST request to {url} with params: {params}")
            
            response = await self.client.post(url, params=params)
            
            if response.status_code == 200:
                result = response.json()
                print(f"API fetch successful: {result.keys()}")
                if "content" in result and result["content"]:
                    content_length = len(result["content"])
                    print(f"Content length: {content_length}")
                    self.results["api_fetch"]["success"] = True
                    self.results["api_fetch"]["details"] = f"Fetched content of length {content_length}"
                    return True
                else:
                    print("API fetch returned empty content")
                    self.results["api_fetch"]["details"] = "Empty content in response"
                    return False
            else:
                print(f"API fetch failed: {response.status_code} {response.text}")
                self.results["api_fetch"]["details"] = f"Status code: {response.status_code}"
                return False
        except Exception as e:
            print(f"Error testing API fetch: {e}")
            self.results["api_fetch"]["details"] = f"Error: {str(e)}"
            return False
    
    async def test_api_summarize(self):
        """Test the API summarize endpoint."""
        print("\n=== Testing API Summarize Endpoint ===")
        try:
            url = f"{API_BASE_URL}/summarize"
            text = "This is a test of the summarization API. It should generate a summary of this text."
            params = {"text": text}
            print(f"Sending POST request to {url} with text of length {len(text)}")
            
            response = await self.client.post(url, params=params)
            
            if response.status_code == 200:
                try:
                    # Try to parse as JSON
                    result = response.json()
                    print(f"API summarize successful: {result}")
                    if "summary" in result and result["summary"]:
                        summary_length = len(result["summary"])
                        print(f"Summary: {result['summary']}")
                        self.results["api_summarize"]["success"] = True
                        self.results["api_summarize"]["details"] = f"Generated summary of length {summary_length}"
                        return True
                    else:
                        print("API summarize returned empty summary")
                        self.results["api_summarize"]["details"] = "Empty summary in response"
                        return False
                except:
                    # Handle case where response is a string
                    summary = response.text
                    print(f"API summarize successful (string response): {summary}")
                    if summary:
                        summary_length = len(summary)
                        self.results["api_summarize"]["success"] = True
                        self.results["api_summarize"]["details"] = f"Generated summary of length {summary_length}"
                        return True
                    else:
                        print("API summarize returned empty summary")
                        self.results["api_summarize"]["details"] = "Empty summary in response"
                        return False
            else:
                print(f"API summarize failed: {response.status_code} {response.text}")
                self.results["api_summarize"]["details"] = f"Status code: {response.status_code}"
                return False
        except Exception as e:
            print(f"Error testing API summarize: {e}")
            self.results["api_summarize"]["details"] = f"Error: {str(e)}"
            return False
    
    async def test_api_search(self):
        """Test the API search endpoint."""
        print("\n=== Testing API Search Endpoint ===")
        try:
            url = f"{API_BASE_URL}/documents"
            query = "artificial intelligence"
            params = {"query": query, "semantic": "true", "limit": 5}
            print(f"Sending GET request to {url} with params: {params}")
            
            response = await self.client.get(url, params=params)
            
            if response.status_code == 200:
                results = response.json()
                print(f"API search successful: {len(results)} results")
                if results:
                    print(f"First result title: {results[0].get('title', 'No title')}")
                    self.results["api_search"]["success"] = True
                    self.results["api_search"]["details"] = f"Found {len(results)} documents"
                    return True
                else:
                    print("API search returned no results")
                    self.results["api_search"]["details"] = "No search results"
                    # Still mark as success if the API works but returns no results
                    self.results["api_search"]["success"] = True
                    return True
            else:
                print(f"API search failed: {response.status_code} {response.text}")
                self.results["api_search"]["details"] = f"Status code: {response.status_code}"
                return False
        except Exception as e:
            print(f"Error testing API search: {e}")
            self.results["api_search"]["details"] = f"Error: {str(e)}"
            return False
    
    async def run_all_tests(self):
        """Run all tests."""
        print("=== Starting Backend Tests ===")
        
        # Test direct service calls
        await self.test_embedding_service()
        await self.test_summarization_service()
        await self.test_web_service()
        
        # Test API endpoints
        try:
            print("\n=== Testing if API server is running ===")
            response = await self.client.get(f"{API_BASE_URL}/health", timeout=2.0)
            print(f"API server is running: {response.status_code}")
            
            # Run API tests
            await self.test_api_health()
            await self.test_api_fetch()
            await self.test_api_summarize()
            await self.test_api_search()
        except Exception as e:
            print(f"Error connecting to API server: {e}")
            print("Skipping API tests. Make sure the backend server is running.")
        
        # Print summary
        print("\n=== Test Results Summary ===")
        for test_name, result in self.results.items():
            status = "✅ PASSED" if result["success"] else "❌ FAILED"
            print(f"{test_name}: {status} - {result['details']}")
        
        # Calculate overall success
        success_count = sum(1 for result in self.results.values() if result["success"])
        total_count = len(self.results)
        print(f"\nOverall: {success_count}/{total_count} tests passed")
        
        return success_count == total_count

async def main():
    """Run the tests."""
    tester = BackendTester()
    success = await tester.run_all_tests()
    await tester.client.aclose()
    
    if success:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n⚠️ Some tests failed. See details above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
