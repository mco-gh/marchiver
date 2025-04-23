#!/usr/bin/env python
"""
Test script for the Marchiver API.
This script tests the basic functionality of the API.
"""

import requests
import json
import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import from app
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Import config
from app.core.config import HOST, PORT, API_PREFIX

# Base URL for the API
BASE_URL = f"http://{HOST}:{PORT}"

def test_health():
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

def test_root():
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

def test_embedding():
    """Test the embedding endpoint."""
    url = f"{BASE_URL}{API_PREFIX}/embeddings"
    data = "This is a test text for embedding generation."
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            embedding = response.json()
            if isinstance(embedding, list) and len(embedding) > 0:
                print(f"✅ Embedding generation passed: {len(embedding)} dimensions")
                return True
            else:
                print(f"❌ Embedding generation failed: Invalid embedding format")
                return False
        else:
            print(f"❌ Embedding generation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Embedding generation failed: {e}")
        return False

def test_summarization():
    """Test the summarization endpoint."""
    url = f"{BASE_URL}{API_PREFIX}/summarize"
    data = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals.

    The term "artificial intelligence" had previously been used to describe machines that mimic and display "human" cognitive skills that are associated with the human mind, such as "learning" and "problem-solving". This definition has since been rejected by major AI researchers who now describe AI in terms of rationality and acting rationally, which does not limit how intelligence can be articulated.

    AI applications include advanced web search engines (e.g., Google), recommendation systems (used by YouTube, Amazon, and Netflix), understanding human speech (such as Siri and Alexa), self-driving cars (e.g., Waymo), generative or creative tools (ChatGPT and AI art), automated decision-making, and competing at the highest level in strategic game systems (such as chess and Go).

    As machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology.
    """
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            summary = response.json()
            print(f"✅ Summarization passed: {summary[:100]}...")
            return True
        else:
            print(f"❌ Summarization failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Summarization failed: {e}")
        return False

def test_web_fetch():
    """Test the web fetch endpoint."""
    url = f"{BASE_URL}{API_PREFIX}/web/fetch"
    data = {
        "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "save": False,
        "summarize": True
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Web fetch passed: {result['title']}")
            if result.get('summary'):
                print(f"  Summary: {result['summary'][:100]}...")
            return True
        else:
            print(f"❌ Web fetch failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Web fetch failed: {e}")
        return False

def run_tests():
    """Run all tests."""
    print("🔍 Testing Marchiver API...")
    print(f"🌐 Base URL: {BASE_URL}")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("Embedding Generation", test_embedding),
        ("Summarization", test_summarization),
        ("Web Fetch", test_web_fetch)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n🧪 Testing {name}...")
        result = test_func()
        results.append((name, result))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    passed = 0
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {name}")
        if result:
            passed += 1
    
    print(f"\n🏁 {passed}/{len(results)} tests passed")

if __name__ == "__main__":
    run_tests()
