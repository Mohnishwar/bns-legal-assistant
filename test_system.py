#!/usr/bin/env python3
"""
Test script for BNS Legal Assistant
Tests all major components of the system
"""

import requests
import json
import time
from typing import Dict, Any

class BNSSystemTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []
    
    def test_health_endpoint(self) -> bool:
        """Test the health endpoint"""
        print("🔍 Testing health endpoint...")
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed: {data['status']}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def test_chapters_endpoint(self) -> bool:
        """Test the chapters endpoint"""
        print("🔍 Testing chapters endpoint...")
        try:
            response = requests.get(f"{self.base_url}/chapters")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Chapters endpoint passed: {len(data.get('chapters', []))} chapters found")
                return True
            else:
                print(f"❌ Chapters endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Chapters endpoint error: {e}")
            return False
    
    def test_ask_endpoint(self, question: str) -> bool:
        """Test the ask endpoint with a sample question"""
        print(f"🔍 Testing ask endpoint with: '{question}'")
        try:
            response = requests.post(
                f"{self.base_url}/ask",
                json={"question": question, "language": "English"}
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Ask endpoint passed: {data['status']}")
                print(f"📝 Answer: {data['answer'][:100]}...")
                return True
            else:
                print(f"❌ Ask endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Ask endpoint error: {e}")
            return False
    
    def test_process_data_endpoint(self) -> bool:
        """Test the process data endpoint"""
        print("🔍 Testing process data endpoint...")
        try:
            response = requests.post(f"{self.base_url}/process-data")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Process data endpoint passed: {data['status']}")
                return True
            else:
                print(f"❌ Process data endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Process data endpoint error: {e}")
            return False
    
    def test_section_endpoint(self, section_number: str = "1") -> bool:
        """Test the section endpoint"""
        print(f"🔍 Testing section endpoint for section {section_number}...")
        try:
            response = requests.get(f"{self.base_url}/sections/{section_number}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Section endpoint passed: {len(data.get('sections', []))} sections found")
                return True
            else:
                print(f"❌ Section endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Section endpoint error: {e}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return results"""
        print("🚀 Starting BNS Legal Assistant System Tests")
        print("=" * 50)
        
        tests = [
            ("Health Endpoint", self.test_health_endpoint),
            ("Chapters Endpoint", self.test_chapters_endpoint),
            ("Ask Endpoint (Murder)", lambda: self.test_ask_endpoint("What is the punishment for murder under BNS?")),
            ("Ask Endpoint (Private Defence)", lambda: self.test_ask_endpoint("Explain the right of private defence")),
            ("Process Data Endpoint", self.test_process_data_endpoint),
            ("Section Endpoint", lambda: self.test_section_endpoint("1")),
        ]
        
        results = {}
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n{'='*20} {test_name} {'='*20}")
            try:
                success = test_func()
                results[test_name] = success
                if success:
                    passed += 1
                time.sleep(1)  # Small delay between tests
            except Exception as e:
                print(f"❌ Test error: {e}")
                results[test_name] = False
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 50)
        
        for test_name, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} - {test_name}")
        
        print(f"\n🎯 Overall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! System is working correctly.")
        else:
            print("⚠️ Some tests failed. Please check the system configuration.")
        
        return {
            "total_tests": total,
            "passed_tests": passed,
            "failed_tests": total - passed,
            "success_rate": (passed / total) * 100,
            "results": results
        }

def main():
    """Main test function"""
    tester = BNSSystemTester()
    results = tester.run_all_tests()
    
    # Save results to file
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Test results saved to test_results.json")
    
    # Exit with appropriate code
    if results["passed_tests"] == results["total_tests"]:
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main() 