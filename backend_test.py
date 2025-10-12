#!/usr/bin/env python3
"""
Backend API Testing for CodeForge
Tests the core API endpoints to verify functionality
"""

import requests
import json
import time
import sys
from typing import Dict, Any

# Backend URL from environment
BACKEND_URL = "https://self-improving-dev.preview.emergentagent.com"

class CodeForgeAPITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 30
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str, response_data: Any = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "response_data": response_data,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        
        if response_data and not success:
            print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
    
    def test_root_endpoint(self):
        """Test GET /api/ - Root endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/")
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required fields
                required_fields = ["message", "status", "version", "features"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test(
                        "Root Endpoint Structure", 
                        False, 
                        f"Missing required fields: {missing_fields}",
                        data
                    )
                    return False
                
                # Check if features list contains expected items
                expected_features = ["multi-agent", "a2a-protocol", "copilotkit-ready", "self-learning"]
                features = data.get("features", [])
                missing_features = [f for f in expected_features if f not in features]
                
                if missing_features:
                    self.log_test(
                        "Root Endpoint Features", 
                        False, 
                        f"Missing expected features: {missing_features}",
                        data
                    )
                else:
                    self.log_test(
                        "Root Endpoint Features", 
                        True, 
                        f"All expected features present: {features}"
                    )
                
                self.log_test(
                    "Root Endpoint", 
                    True, 
                    f"Status: {data.get('status')}, Version: {data.get('version')}"
                )
                return True
            else:
                self.log_test(
                    "Root Endpoint", 
                    False, 
                    f"HTTP {response.status_code}: {response.text[:100]}"
                )
                return False
                
        except Exception as e:
            self.log_test("Root Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def test_metrics_endpoint(self):
        """Test GET /api/metrics - Performance metrics"""
        try:
            response = self.session.get(f"{self.base_url}/api/metrics")
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required metrics fields
                required_fields = ["total_apps", "successful_apps", "success_rate", "pattern_count", "failed_attempts", "success_history"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test(
                        "Metrics Endpoint Structure", 
                        False, 
                        f"Missing required fields: {missing_fields}",
                        data
                    )
                    return False
                
                # Validate data types
                if not isinstance(data.get("total_apps"), int):
                    self.log_test("Metrics Data Types", False, "total_apps should be integer")
                    return False
                
                if not isinstance(data.get("success_rate"), (int, float)):
                    self.log_test("Metrics Data Types", False, "success_rate should be number")
                    return False
                
                if not isinstance(data.get("success_history"), list):
                    self.log_test("Metrics Data Types", False, "success_history should be list")
                    return False
                
                self.log_test(
                    "Metrics Endpoint", 
                    True, 
                    f"Total apps: {data.get('total_apps')}, Success rate: {data.get('success_rate'):.2%}, Patterns: {data.get('pattern_count')}"
                )
                return True
            else:
                self.log_test(
                    "Metrics Endpoint", 
                    False, 
                    f"HTTP {response.status_code}: {response.text[:100]}"
                )
                return False
                
        except Exception as e:
            self.log_test("Metrics Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def test_patterns_endpoint(self):
        """Test GET /api/patterns - Learned patterns"""
        try:
            response = self.session.get(f"{self.base_url}/api/patterns")
            
            if response.status_code == 200:
                data = response.json()
                
                if not isinstance(data, list):
                    self.log_test(
                        "Patterns Endpoint", 
                        False, 
                        "Response should be a list of patterns",
                        data
                    )
                    return False
                
                # If patterns exist, validate structure
                if data:
                    pattern = data[0]
                    required_fields = ["id", "description", "code_snippet", "tech_stack", "features", "success_rate", "usage_count", "timestamp"]
                    missing_fields = [field for field in required_fields if field not in pattern]
                    
                    if missing_fields:
                        self.log_test(
                            "Patterns Structure", 
                            False, 
                            f"Pattern missing fields: {missing_fields}",
                            pattern
                        )
                        return False
                
                self.log_test(
                    "Patterns Endpoint", 
                    True, 
                    f"Retrieved {len(data)} patterns successfully"
                )
                return True
            else:
                self.log_test(
                    "Patterns Endpoint", 
                    False, 
                    f"HTTP {response.status_code}: {response.text[:100]}"
                )
                return False
                
        except Exception as e:
            self.log_test("Patterns Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def test_generate_endpoint(self):
        """Test POST /api/generate - App generation"""
        try:
            # Test payload as specified in review request
            payload = {
                "description": "Build a simple calculator",
                "use_thinking": False,
                "auto_test": False,
                "max_iterations": 1
            }
            
            print("   Sending generation request (may take 10-20 seconds)...")
            response = self.session.post(
                f"{self.base_url}/api/generate", 
                json=payload,
                timeout=60  # Extended timeout for generation
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required response fields
                required_fields = ["success", "files", "metadata", "time_taken"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test(
                        "Generate Response Structure", 
                        False, 
                        f"Missing required fields: {missing_fields}",
                        data
                    )
                    return False
                
                # Check if generation was successful
                if not data.get("success"):
                    self.log_test(
                        "Generate Endpoint", 
                        False, 
                        f"Generation failed: {data.get('error', 'Unknown error')}",
                        data
                    )
                    return False
                
                # Validate files structure
                files = data.get("files", {})
                if not isinstance(files, dict):
                    self.log_test(
                        "Generate Files Structure", 
                        False, 
                        "Files should be a dictionary"
                    )
                    return False
                
                # Check for expected files
                expected_files = ["index.html", "styles.css", "script.js"]
                present_files = [f for f in expected_files if f in files]
                
                self.log_test(
                    "Generate Endpoint", 
                    True, 
                    f"Generated calculator app with {len(files)} files ({', '.join(present_files)}), took {data.get('time_taken', 0):.2f}s"
                )
                return True
            else:
                self.log_test(
                    "Generate Endpoint", 
                    False, 
                    f"HTTP {response.status_code}: {response.text[:200]}"
                )
                return False
                
        except requests.exceptions.Timeout:
            self.log_test("Generate Endpoint", False, "Request timed out (>60s)")
            return False
        except Exception as e:
            self.log_test("Generate Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all API tests"""
        print(f"🧪 Testing CodeForge Backend APIs at {self.base_url}")
        print("=" * 60)
        
        tests = [
            ("Root Endpoint", self.test_root_endpoint),
            ("Metrics Endpoint", self.test_metrics_endpoint), 
            ("Patterns Endpoint", self.test_patterns_endpoint),
            ("Generate Endpoint", self.test_generate_endpoint)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🔍 Testing {test_name}...")
            if test_func():
                passed += 1
        
        print("\n" + "=" * 60)
        print(f"📊 Test Summary: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed!")
            return True
        else:
            print(f"⚠️  {total - passed} tests failed")
            return False
    
    def get_summary(self):
        """Get test summary for reporting"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": passed_tests / total_tests if total_tests > 0 else 0,
            "results": self.test_results
        }

def main():
    """Main test execution"""
    tester = CodeForgeAPITester(BACKEND_URL)
    
    try:
        success = tester.run_all_tests()
        summary = tester.get_summary()
        
        # Print detailed results for failed tests
        failed_tests = [r for r in summary["results"] if not r["success"]]
        if failed_tests:
            print("\n❌ Failed Test Details:")
            for test in failed_tests:
                print(f"  • {test['test']}: {test['details']}")
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)