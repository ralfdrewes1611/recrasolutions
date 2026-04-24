#!/usr/bin/env python3
"""
RECRA Solutions Configurator Platform - Backend API Testing
Tests all backend endpoints for functionality and integration
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any, List

class RECRABackendTester:
    def __init__(self, base_url: str = "https://lease-simulator.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.project_id = None
        self.products = []
        
    def log(self, message: str, level: str = "INFO"):
        """Log test messages with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def run_test(self, name: str, method: str, endpoint: str, expected_status: int = 200, 
                 data: Dict = None, params: Dict = None) -> tuple[bool, Any]:
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if not endpoint.startswith('http') else endpoint
        headers = {'Content-Type': 'application/json'}
        
        self.tests_run += 1
        self.log(f"Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, params=params, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                self.log(f"✅ {name} - Status: {response.status_code}", "PASS")
                try:
                    return True, response.json()
                except:
                    return True, response.text
            else:
                self.log(f"❌ {name} - Expected {expected_status}, got {response.status_code}", "FAIL")
                self.log(f"   Response: {response.text[:200]}", "ERROR")
                return False, {}
                
        except Exception as e:
            self.log(f"❌ {name} - Error: {str(e)}", "ERROR")
            return False, {}
    
    def test_welcome_endpoint(self) -> bool:
        """Test /api/ returns welcome message"""
        success, response = self.run_test(
            "Welcome endpoint",
            "GET", 
            "",
            200
        )
        
        if success and isinstance(response, dict):
            if "message" in response and "RECRA" in response["message"]:
                self.log("✅ Welcome message contains RECRA branding")
                return True
            else:
                self.log("❌ Welcome message missing or incorrect")
                return False
        return success
    
    def test_products_endpoint(self) -> bool:
        """Test /api/products returns 19 seeded products"""
        success, response = self.run_test(
            "Get all products",
            "GET",
            "products",
            200
        )
        
        if success and isinstance(response, list):
            self.products = response
            product_count = len(response)
            
            if product_count == 23:
                self.log(f"✅ Found exactly 23 products as expected")
            else:
                self.log(f"❌ Expected 23 products, found {product_count}")
                return False
            
            # Verify product structure
            if response:
                product = response[0]
                required_fields = ['id', 'name', 'category', 'description', 'price_purchase', 
                                 'price_lease_monthly', 'installation_cost', 'maintenance_yearly']
                
                missing_fields = [field for field in required_fields if field not in product]
                if missing_fields:
                    self.log(f"❌ Product missing fields: {missing_fields}")
                    return False
                else:
                    self.log("✅ Product structure is correct")
            
            # Check categories
            categories = set(p['category'] for p in response)
            expected_categories = {'sanitair', 'slagboom', 'camera', 'wifi', 'verlichting', 'betaalsysteem', 'toegangscontrole', 'douchelezer'}
            
            if expected_categories.issubset(categories):
                self.log(f"✅ All 8 expected categories found: {categories}")
            else:
                missing = expected_categories - categories
                self.log(f"❌ Missing categories: {missing}")
                return False
                
            return True
        
        return success
    
    def test_products_by_category(self) -> bool:
        """Test /api/products/category/{category} filters correctly"""
        if not self.products:
            self.log("❌ No products available for category testing")
            return False
        
        # Test each category
        categories = set(p['category'] for p in self.products)
        all_passed = True
        
        for category in categories:
            success, response = self.run_test(
                f"Get products by category: {category}",
                "GET",
                f"products/category/{category}",
                200
            )
            
            if success and isinstance(response, list):
                # Verify all returned products are from the requested category
                wrong_category = [p for p in response if p['category'] != category]
                if wrong_category:
                    self.log(f"❌ Category {category} returned products from other categories")
                    all_passed = False
                else:
                    self.log(f"✅ Category {category} filter working correctly ({len(response)} products)")
            else:
                all_passed = False
        
        return all_passed
    
    def test_create_project(self) -> bool:
        """Test POST /api/projects creates a new project"""
        project_data = {
            "name": "Test RECRA Project",
            "project_type": "camping",
            "num_spots": 50,
            "canvas_width": 800,
            "canvas_height": 600,
            "scale_meters_per_pixel": 0.1,
            "placed_products": [],
            "zones": []
        }
        
        success, response = self.run_test(
            "Create new project",
            "POST",
            "projects",
            200,
            data=project_data
        )
        
        if success and isinstance(response, dict):
            if 'id' in response:
                self.project_id = response['id']
                self.log(f"✅ Project created with ID: {self.project_id}")
                
                # Verify project data
                if response['name'] == project_data['name'] and response['project_type'] == project_data['project_type']:
                    self.log("✅ Project data saved correctly")
                    return True
                else:
                    self.log("❌ Project data not saved correctly")
                    return False
            else:
                self.log("❌ Project creation response missing ID")
                return False
        
        return success
    
    def test_update_project(self) -> bool:
        """Test PUT /api/projects/{id} updates project"""
        if not self.project_id:
            self.log("❌ No project ID available for update test")
            return False
        
        # Add some placed products for quote testing
        if self.products:
            update_data = {
                "name": "Updated Test Project",
                "num_spots": 75,
                "placed_products": [
                    {
                        "id": "placed-1",
                        "product_id": self.products[0]['id'],
                        "x": 100,
                        "y": 100,
                        "rotation": 0,
                        "quantity": 1
                    },
                    {
                        "id": "placed-2", 
                        "product_id": self.products[1]['id'],
                        "x": 200,
                        "y": 200,
                        "rotation": 45,
                        "quantity": 2
                    }
                ]
            }
        else:
            update_data = {
                "name": "Updated Test Project",
                "num_spots": 75
            }
        
        success, response = self.run_test(
            "Update project",
            "PUT",
            f"projects/{self.project_id}",
            200,
            data=update_data
        )
        
        if success and isinstance(response, dict):
            if response.get('name') == update_data['name'] and response.get('num_spots') == update_data['num_spots']:
                self.log("✅ Project updated successfully")
                return True
            else:
                self.log("❌ Project update data not saved correctly")
                return False
        
        return success
    
    def test_calculate_quote(self) -> bool:
        """Test POST /api/quote/calculate calculates quote from placed products"""
        if not self.project_id:
            self.log("❌ No project ID available for quote calculation")
            return False
        
        success, response = self.run_test(
            "Calculate project quote",
            "POST",
            f"quote/calculate",
            200,
            params={"project_id": self.project_id}
        )
        
        if success and isinstance(response, dict):
            required_fields = ['capex_total', 'opex_monthly', 'opex_yearly', 'installation_total', 'maintenance_yearly', 'items']
            missing_fields = [field for field in required_fields if field not in response]
            
            if missing_fields:
                self.log(f"❌ Quote response missing fields: {missing_fields}")
                return False
            
            # Verify calculations make sense
            if response['opex_yearly'] == response['opex_monthly'] * 12:
                self.log("✅ OPEX calculations are consistent")
            else:
                self.log("❌ OPEX yearly calculation incorrect")
                return False
            
            if isinstance(response['items'], list):
                self.log(f"✅ Quote calculated with {len(response['items'])} items")
                self.log(f"   CAPEX: €{response['capex_total']:,.2f}")
                self.log(f"   OPEX Monthly: €{response['opex_monthly']:,.2f}")
                self.log(f"   Installation: €{response['installation_total']:,.2f}")
                return True
            else:
                self.log("❌ Quote items not returned as list")
                return False
        
        return success
    
    def test_ai_recommendations(self) -> bool:
        """Test POST /api/ai/recommendations returns AI recommendations"""
        if not self.project_id:
            self.log("❌ No project ID available for AI recommendations")
            return False
        
        success, response = self.run_test(
            "Get AI recommendations",
            "POST",
            f"ai/recommendations",
            200,
            params={"project_id": self.project_id}
        )
        
        if success and isinstance(response, dict):
            if 'recommendations' in response and isinstance(response['recommendations'], list):
                recommendations = response['recommendations']
                self.log(f"✅ AI returned {len(recommendations)} recommendations")
                
                # Verify recommendation structure
                if recommendations:
                    rec = recommendations[0]
                    required_fields = ['type', 'title', 'description']
                    missing_fields = [field for field in required_fields if field not in rec]
                    
                    if missing_fields:
                        self.log(f"❌ Recommendation missing fields: {missing_fields}")
                        return False
                    
                    valid_types = ['warning', 'suggestion', 'optimization']
                    if rec['type'] in valid_types:
                        self.log(f"✅ Recommendation type '{rec['type']}' is valid")
                        self.log(f"   Title: {rec['title']}")
                        return True
                    else:
                        self.log(f"❌ Invalid recommendation type: {rec['type']}")
                        return False
                else:
                    self.log("✅ AI recommendations endpoint working (empty list)")
                    return True
            else:
                self.log("❌ AI response missing recommendations field")
                return False
        
        return success
    
    def test_pdf_generation(self) -> bool:
        """Test POST /api/quote/pdf generates quote PDF"""
        if not self.project_id:
            self.log("❌ No project ID available for PDF generation")
            return False
        
        success, response = self.run_test(
            "Generate quote PDF",
            "POST",
            f"quote/pdf",
            200,
            params={"project_id": self.project_id}
        )
        
        if success and isinstance(response, dict):
            if 'html' in response and 'project_name' in response and 'quote' in response:
                html_content = response['html']
                if 'RECRA Solutions' in html_content and 'Offerte' in html_content:
                    self.log("✅ PDF HTML generated with RECRA branding")
                    return True
                else:
                    self.log("❌ PDF HTML missing expected content")
                    return False
            else:
                self.log("❌ PDF response missing required fields")
                return False
        
        return success
    
    def test_seed_products(self) -> bool:
        """Test POST /api/seed-products (should indicate products already exist)"""
        success, response = self.run_test(
            "Seed products endpoint",
            "POST",
            "seed-products",
            200
        )
        
        if success and isinstance(response, dict):
            if 'message' in response:
                self.log(f"✅ Seed endpoint response: {response['message']}")
                return True
            else:
                self.log("❌ Seed response missing message")
                return False
        
        return success
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all backend tests"""
        self.log("🚀 Starting RECRA Backend API Tests")
        self.log(f"Testing against: {self.base_url}")
        
        test_results = {
            "welcome_endpoint": self.test_welcome_endpoint(),
            "products_endpoint": self.test_products_endpoint(),
            "products_by_category": self.test_products_by_category(),
            "create_project": self.test_create_project(),
            "update_project": self.test_update_project(),
            "calculate_quote": self.test_calculate_quote(),
            "ai_recommendations": self.test_ai_recommendations(),
            "pdf_generation": self.test_pdf_generation(),
            "seed_products": self.test_seed_products(),
        }
        
        # Summary
        passed_tests = sum(test_results.values())
        total_tests = len(test_results)
        success_rate = (passed_tests / total_tests) * 100
        
        self.log("\n" + "="*60)
        self.log("📊 BACKEND TEST SUMMARY")
        self.log("="*60)
        
        for test_name, passed in test_results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            self.log(f"{test_name.replace('_', ' ').title()}: {status}")
        
        self.log(f"\nOverall: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
        
        if passed_tests == total_tests:
            self.log("🎉 All backend tests passed!")
            return {"success": True, "results": test_results, "summary": f"{passed_tests}/{total_tests} passed"}
        else:
            failed_tests = [name for name, passed in test_results.items() if not passed]
            self.log(f"❌ Failed tests: {', '.join(failed_tests)}")
            return {"success": False, "results": test_results, "summary": f"{passed_tests}/{total_tests} passed", "failed": failed_tests}

def main():
    """Main test execution"""
    tester = RECRABackendTester()
    results = tester.run_all_tests()
    
    # Return appropriate exit code
    return 0 if results["success"] else 1

if __name__ == "__main__":
    sys.exit(main())