#!/usr/bin/env python
"""
Comprehensive test script for the Marchiver API.
This script tests all backend services by calling the API endpoints and verifying the expected responses.
"""

import requests
import json
import sys
import os
import uuid
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import time

# Add the parent directory to the path so we can import from app
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Import config
from app.core.config import HOST, PORT, API_PREFIX

# Base URL for the API
BASE_URL = f"http://{HOST}:{PORT}"
API_URL = f"{BASE_URL}{API_PREFIX}"

# Test data
TEST_DOCUMENT = {
    "content": "This is a test document for the Marchiver API. It contains information about artificial intelligence and machine learning.",
    "title": "Test Document",
    "url": "https://example.com/test",
    "metadata": {
        "source": "test",
        "importance": "high"
    },
    "tags": ["test", "api", "marchiver"],
    "category": "testing"
}

TEST_DOCUMENT_UPDATE = {
    "title": "Updated Test Document",
    "tags": ["test", "api", "marchiver", "updated"],
    "metadata": {
        "source": "test",
        "importance": "critical",
        "updated": True
    }
}

TEST_SEARCH_QUERY = "artificial intelligence"
TEST_WEB_URL = "https://en.wikipedia.org/wiki/Artificial_intelligence"
TEST_TEXT_FOR_SUMMARIZATION = """
Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals.

The term "artificial intelligence" had previously been used to describe machines that mimic and display "human" cognitive skills that are associated with the human mind, such as "learning" and "problem-solving". This definition has since been rejected by major AI researchers who now describe AI in terms of rationality and acting rationally, which does not limit how intelligence can be articulated.

AI applications include advanced web search engines (e.g., Google), recommendation systems (used by YouTube, Amazon, and Netflix), understanding human speech (such as Siri and Alexa), self-driving cars (e.g., Waymo), generative or creative tools (ChatGPT and AI art), automated decision-making, and competing at the highest level in strategic game systems (such as chess and Go).

As machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology.
"""

# Global variables to store test data
created_document_id = None
created_document = None
embedding_result = None

def print_separator(title: str = None):
    """Print a separator line with an optional title."""
    if title:
        print(f"\n{'=' * 20} {title} {'=' * 20}")
    else:
        print("\n" + "=" * 60)

def test_health() -> bool:
    """Test the health endpoint."""
    url = f"{BASE_URL}/health"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"✅ Health check passed: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_api_health() -> bool:
    """Test the API health endpoint."""
    url = f"{API_URL}/health"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"✅ API health check passed: {response.json()}")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API health check failed: {e}")
        return False

def test_root() -> bool:
    """Test the root endpoint."""
    url = f"{BASE_URL}/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"✅ Root endpoint passed: {response.json()}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return False

def test_embedding_service() -> bool:
    """Test the embedding service."""
    global embedding_result
    url = f"{API_URL}/embeddings"
    params = {"text": TEST_DOCUMENT["content"]}
    try:
        response = requests.post(url, params=params)
        if response.status_code == 200:
            embedding = response.json()
            if isinstance(embedding, list) and len(embedding) > 0:
                print(f"✅ Embedding generation passed: {len(embedding)} dimensions")
                embedding_result = embedding
                return True
            else:
                print(f"❌ Embedding generation failed: Invalid embedding format")
                return False
        else:
            print(f"❌ Embedding generation failed: Status code {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Embedding generation failed: {e}")
        return False

def test_summarization_service() -> bool:
    """Test the summarization service."""
    url = f"{API_URL}/summarize"
    params = {"text": TEST_TEXT_FOR_SUMMARIZATION}
    try:
        response = requests.post(url, params=params)
        if response.status_code == 200:
            summary = response.json()
            print(f"✅ Summarization passed: {summary[:100]}...")
            return True
        else:
            print(f"❌ Summarization failed: Status code {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Summarization failed: {e}")
        return False

def test_web_service() -> bool:
    """Test the web service."""
    url = f"{API_URL}/web/fetch"
    params = {
        "url": TEST_WEB_URL,
        "save": "false",
        "summarize": "true"
    }
    try:
        response = requests.post(url, params=params)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Web fetch passed: {result['title']}")
            if result.get('summary'):
                print(f"  Summary: {result['summary'][:100]}...")
            return True
        else:
            print(f"❌ Web fetch failed: Status code {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Web fetch failed: {e}")
        return False

def test_document_service_create() -> bool:
    """Test creating a document."""
    global created_document_id, created_document
    url = f"{API_URL}/documents"
    try:
        response = requests.post(url, json=TEST_DOCUMENT)
        if response.status_code == 201:
            result = response.json()
            created_document_id = result["id"]
            created_document = result
            print(f"✅ Document creation passed: ID {created_document_id}")
            return True
        else:
            print(f"❌ Document creation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Document creation failed: {e}")
        return False

def test_document_service_get() -> bool:
    """Test getting a document."""
    if not created_document_id:
        print("❌ Document get failed: No document ID available")
        return False
    
    url = f"{API_URL}/documents/{created_document_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Document get passed: {result['title']}")
            return True
        else:
            print(f"❌ Document get failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Document get failed: {e}")
        return False

def test_document_service_update() -> bool:
    """Test updating a document."""
    if not created_document_id:
        print("❌ Document update failed: No document ID available")
        return False
    
    url = f"{API_URL}/documents/{created_document_id}"
    try:
        response = requests.put(url, json=TEST_DOCUMENT_UPDATE)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Document update passed: {result['title']}")
            # Verify the update was applied
            if result["title"] == TEST_DOCUMENT_UPDATE["title"]:
                print("  ✅ Title update verified")
            else:
                print("  ❌ Title update failed")
            
            if "updated" in result["metadata"] and result["metadata"]["updated"] == True:
                print("  ✅ Metadata update verified")
            else:
                print("  ❌ Metadata update failed")
            
            if "updated" in result["tags"]:
                print("  ✅ Tags update verified")
            else:
                print("  ❌ Tags update failed")
            
            return True
        else:
            print(f"❌ Document update failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Document update failed: {e}")
        return False

def test_document_service_search() -> bool:
    """Test searching for documents."""
    url = f"{API_URL}/documents"
    params = {
        "query": TEST_SEARCH_QUERY,
        "semantic": False,
        "limit": 10,
        "offset": 0
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Document search passed: {len(results)} results")
            return True
        else:
            print(f"❌ Document search failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Document search failed: {e}")
        return False

def test_document_service_semantic_search() -> bool:
    """Test semantic search for documents."""
    url = f"{API_URL}/documents"
    params = {
        "query": TEST_SEARCH_QUERY,
        "semantic": True,
        "limit": 10,
        "offset": 0
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Document semantic search passed: {len(results)} results")
            return True
        else:
            print(f"❌ Document semantic search failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Document semantic search failed: {e}")
        return False

def test_document_service_similar() -> bool:
    """Test finding similar documents."""
    if not created_document_id:
        print("❌ Similar documents failed: No document ID available")
        return False
    
    url = f"{API_URL}/documents/{created_document_id}/similar"
    params = {
        "limit": 10
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Similar documents passed: {len(results)} results")
            return True
        else:
            print(f"❌ Similar documents failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Similar documents failed: {e}")
        return False

def test_document_service_delete() -> bool:
    """Test deleting a document."""
    if not created_document_id:
        print("❌ Document delete failed: No document ID available")
        return False
    
    url = f"{API_URL}/documents/{created_document_id}"
    try:
        response = requests.delete(url)
        if response.status_code == 204:
            print(f"✅ Document delete passed")
            
            # Verify the document was deleted
            verify_response = requests.get(url)
            if verify_response.status_code == 404:
                print("  ✅ Document deletion verified")
                return True
            else:
                print("  ❌ Document deletion verification failed")
                return False
        else:
            print(f"❌ Document delete failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Document delete failed: {e}")
        return False

def test_web_fetch_and_save() -> bool:
    """Test fetching a web page and saving it as a document."""
    url = f"{API_URL}/web/fetch"
    params = {
        "url": TEST_WEB_URL,
        "save": "true",
        "summarize": "true"
    }
    try:
        response = requests.post(url, params=params)
        if response.status_code == 200:
            result = response.json()
            document_id = result["id"]
            print(f"✅ Web fetch and save passed: ID {document_id}")
            
            # Clean up by deleting the document
            delete_url = f"{API_URL}/documents/{document_id}"
            delete_response = requests.delete(delete_url)
            if delete_response.status_code == 204:
                print("  ✅ Cleanup successful")
            else:
                print("  ❌ Cleanup failed")
            
            return True
        else:
            print(f"❌ Web fetch and save failed: Status code {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Web fetch and save failed: {e}")
        return False

def run_tests():
    """Run all tests."""
    print_separator("MARCHIVER API COMPREHENSIVE TEST SUITE")
    print(f"🌐 Base URL: {BASE_URL}")
    print(f"🌐 API URL: {API_URL}")
    print_separator()
    
    # Basic health checks
    print_separator("Basic Health Checks")
    basic_tests = [
        ("Root Endpoint", test_root),
        ("Health Check", test_health),
        ("API Health Check", test_api_health),
    ]
    
    # Service tests
    print_separator("Service Tests")
    service_tests = [
        ("Embedding Service", test_embedding_service),
        ("Summarization Service", test_summarization_service),
        ("Web Service", test_web_service),
    ]
    
    # Document service tests
    print_separator("Document Service Tests")
    document_tests = [
        ("Document Creation", test_document_service_create),
        ("Document Retrieval", test_document_service_get),
        ("Document Update", test_document_service_update),
        ("Document Search", test_document_service_search),
        ("Document Semantic Search", test_document_service_semantic_search),
        ("Similar Documents", test_document_service_similar),
        ("Document Deletion", test_document_service_delete),
    ]
    
    # Integration tests
    print_separator("Integration Tests")
    integration_tests = [
        ("Web Fetch and Save", test_web_fetch_and_save),
    ]
    
    # Run all tests
    all_tests = basic_tests + service_tests + document_tests + integration_tests
    results = []
    
    for name, test_func in all_tests:
        print(f"\n🧪 Testing {name}...")
        start_time = time.time()
        result = test_func()
        end_time = time.time()
        duration = end_time - start_time
        results.append((name, result, duration))
    
    # Print results
    print_separator("Test Results")
    
    passed = 0
    total_duration = 0
    
    for name, result, duration in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {name} ({duration:.2f}s)")
        if result:
            passed += 1
        total_duration += duration
    
    success_rate = (passed / len(results)) * 100
    print_separator("Summary")
    print(f"🏁 {passed}/{len(results)} tests passed ({success_rate:.1f}%)")
    print(f"⏱️ Total duration: {total_duration:.2f}s")
    
    # Return success if all tests passed
    return passed == len(results)

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
