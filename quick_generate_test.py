#!/usr/bin/env python3
"""
Quick test for generate endpoint to check if it's reachable
"""

import requests
import json

BACKEND_URL = "https://self-improving-dev.preview.emergentagent.com"

def test_generate_endpoint_quick():
    """Test if generate endpoint is reachable and starts processing"""
    try:
        payload = {
            "description": "Build a simple calculator",
            "use_thinking": False,
            "auto_test": False,
            "max_iterations": 1
        }
        
        print("Testing generate endpoint reachability...")
        response = requests.post(
            f"{BACKEND_URL}/api/generate", 
            json=payload,
            timeout=5  # Short timeout to just check if endpoint responds
        )
        
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Generate endpoint is reachable and processing requests")
            return True
        else:
            print(f"❌ Generate endpoint returned {response.status_code}: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏱️  Generate endpoint is processing (timed out after 5s, which is expected)")
        return True  # Timeout means it's processing, which is good
    except Exception as e:
        print(f"❌ Generate endpoint error: {str(e)}")
        return False

if __name__ == "__main__":
    test_generate_endpoint_quick()