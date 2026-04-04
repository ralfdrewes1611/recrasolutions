"""
Test suite for RECRA AI Services - Iteration 8
Tests: Excel/CSV import, Website scraper, Floor plan analysis, Quote text generation
"""
import pytest
import requests
import os
import io
import csv

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestAIQuoteTextGeneration:
    """Test POST /api/ai/generate-quote-text - generates Dutch professional quote text"""
    
    def test_generate_quote_text_success(self):
        """Test quote text generation with valid project data"""
        payload = {
            "project_name": "Camping De Zonnehoek",
            "project_type": "camping",
            "num_spots": 30,
            "products": [
                {"name": "Compact Sanitair Unit", "quantity": 2, "price": 18500},
                {"name": "UniFi Access Point Outdoor", "quantity": 3, "price": 450}
            ],
            "total_investment": 38350,
            "lease_monthly": 945
        }
        
        response = requests.post(f"{BASE_URL}/api/ai/generate-quote-text", json=payload, timeout=30)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "intro" in data, "Response should contain 'intro' field"
        assert "body" in data, "Response should contain 'body' field"
        assert "closing" in data, "Response should contain 'closing' field"
        
        # Verify content is not empty
        assert len(data["intro"]) > 10, "Intro should have meaningful content"
        assert len(data["body"]) > 50, "Body should have meaningful content"
        assert len(data["closing"]) > 10, "Closing should have meaningful content"
        
        print(f"✓ Quote text generated successfully")
        print(f"  Intro: {data['intro'][:100]}...")
        print(f"  Body length: {len(data['body'])} chars")
        print(f"  Closing: {data['closing'][:100]}...")

    def test_generate_quote_text_empty_products(self):
        """Test quote text generation with empty products list"""
        payload = {
            "project_name": "Empty Project",
            "project_type": "camping",
            "num_spots": 10,
            "products": [],
            "total_investment": 0,
            "lease_monthly": 0
        }
        
        response = requests.post(f"{BASE_URL}/api/ai/generate-quote-text", json=payload, timeout=30)
        
        # Should still return 200 with fallback text
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "intro" in data
        assert "body" in data
        assert "closing" in data
        print(f"✓ Quote text generated for empty products (fallback)")


class TestWebsiteScraper:
    """Test POST /api/ai/scrape-products - takes URL, returns scraped products"""
    
    def test_scrape_products_valid_url(self):
        """Test scraping products from a valid URL"""
        payload = {"url": "https://example.com"}
        
        response = requests.post(f"{BASE_URL}/api/ai/scrape-products", json=payload, timeout=30)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "products" in data, "Response should contain 'products' field"
        assert "page_title" in data, "Response should contain 'page_title' field"
        assert "source_url" in data, "Response should contain 'source_url' field"
        assert isinstance(data["products"], list), "Products should be a list"
        
        print(f"✓ Scrape endpoint returned successfully")
        print(f"  Page title: {data['page_title']}")
        print(f"  Products found: {len(data['products'])}")

    def test_scrape_products_invalid_url(self):
        """Test scraping with invalid URL returns error"""
        payload = {"url": "not-a-valid-url-12345.invalid"}
        
        response = requests.post(f"{BASE_URL}/api/ai/scrape-products", json=payload, timeout=30)
        
        # Should return 400 for invalid URL
        assert response.status_code == 400, f"Expected 400 for invalid URL, got {response.status_code}"
        print(f"✓ Invalid URL correctly returns 400 error")

    def test_scrape_products_url_without_protocol(self):
        """Test scraping URL without http:// prefix"""
        payload = {"url": "example.com"}
        
        response = requests.post(f"{BASE_URL}/api/ai/scrape-products", json=payload, timeout=30)
        
        # Should auto-add https:// and work
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "products" in data
        print(f"✓ URL without protocol handled correctly")


class TestExcelCSVImport:
    """Test POST /api/ai/import-products - takes Excel/CSV file, returns mapped products"""
    
    def test_import_csv_file(self):
        """Test importing a CSV file with product data"""
        # Create a simple CSV in memory
        csv_content = "naam;prijs;breedte;hoogte;categorie\n"
        csv_content += "Test Camera;350;0.3;0.3;camera\n"
        csv_content += "Test WiFi AP;450;0.3;0.3;wifi\n"
        csv_content += "Test Slagboom;1800;0.5;4;slagboom\n"
        
        files = {
            'file': ('test_products.csv', csv_content.encode('utf-8'), 'text/csv')
        }
        
        response = requests.post(f"{BASE_URL}/api/ai/import-products", files=files, timeout=60)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "products" in data, "Response should contain 'products' field"
        assert "column_mapping" in data, "Response should contain 'column_mapping' field"
        assert "raw_headers" in data, "Response should contain 'raw_headers' field"
        assert "total_rows" in data, "Response should contain 'total_rows' field"
        
        assert len(data["products"]) >= 1, "Should have at least 1 product"
        assert data["total_rows"] == 3, f"Expected 3 rows, got {data['total_rows']}"
        
        print(f"✓ CSV import successful")
        print(f"  Products found: {len(data['products'])}")
        print(f"  Column mapping: {data['column_mapping']}")
        print(f"  Headers: {data['raw_headers']}")

    def test_import_empty_file(self):
        """Test importing an empty file returns error"""
        files = {
            'file': ('empty.csv', b'', 'text/csv')
        }
        
        response = requests.post(f"{BASE_URL}/api/ai/import-products", files=files, timeout=30)
        
        assert response.status_code == 400, f"Expected 400 for empty file, got {response.status_code}"
        print(f"✓ Empty file correctly returns 400 error")

    def test_import_unsupported_format(self):
        """Test importing unsupported file format returns error"""
        files = {
            'file': ('test.txt', b'some text content', 'text/plain')
        }
        
        response = requests.post(f"{BASE_URL}/api/ai/import-products", files=files, timeout=30)
        
        assert response.status_code == 400, f"Expected 400 for unsupported format, got {response.status_code}"
        print(f"✓ Unsupported format correctly returns 400 error")


class TestImportConfirm:
    """Test POST /api/ai/import-products/confirm - saves products to DB"""
    
    def test_confirm_import_products(self):
        """Test confirming and saving imported products"""
        payload = {
            "products": [
                {
                    "name": "TEST_Import_Camera",
                    "category": "camera",
                    "description": "Test imported camera",
                    "price_purchase": 350,
                    "price_lease_monthly": 12,
                    "installation_cost": 150,
                    "maintenance_yearly": 50,
                    "dimensions_width": 0.3,
                    "dimensions_height": 0.3,
                    "confidence": 0.9
                }
            ]
        }
        
        response = requests.post(f"{BASE_URL}/api/ai/import-products/confirm", json=payload, timeout=30)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "saved" in data, "Response should contain 'saved' count"
        assert data["saved"] == 1, f"Expected 1 saved, got {data['saved']}"
        
        print(f"✓ Import confirm successful: {data['saved']} products saved")
        
        # Verify product was actually saved by fetching products
        products_response = requests.get(f"{BASE_URL}/api/products", timeout=10)
        assert products_response.status_code == 200
        products = products_response.json()
        
        # Find our test product
        test_product = next((p for p in products if p["name"] == "TEST_Import_Camera"), None)
        assert test_product is not None, "Imported product should be in database"
        print(f"✓ Verified product exists in database with id: {test_product['id']}")

    def test_confirm_import_empty_list(self):
        """Test confirming with empty products list"""
        payload = {"products": []}
        
        response = requests.post(f"{BASE_URL}/api/ai/import-products/confirm", json=payload, timeout=30)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["saved"] == 0
        print(f"✓ Empty import list handled correctly")


class TestFloorPlanAnalysis:
    """Test POST /api/ai/analyze-floorplan-smart - analyzes floor plan image with Vision AI"""
    
    def test_analyze_floorplan_basic(self):
        """Test floor plan analysis with a simple base64 image"""
        # Create a minimal valid PNG (1x1 pixel white)
        # This is a valid 1x1 white PNG in base64
        minimal_png_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        
        payload = {
            "image_base64": minimal_png_b64,
            "project_type": "camping",
            "canvas_width": 1000,
            "canvas_height": 700
        }
        
        response = requests.post(f"{BASE_URL}/api/ai/analyze-floorplan-smart", json=payload, timeout=60)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "zones" in data, "Response should contain 'zones' field"
        assert "estimated_spots" in data, "Response should contain 'estimated_spots' field"
        assert "suggested_scale" in data, "Response should contain 'suggested_scale' field"
        assert "suggestions" in data, "Response should contain 'suggestions' field"
        
        assert isinstance(data["zones"], list), "Zones should be a list"
        assert isinstance(data["suggestions"], list), "Suggestions should be a list"
        
        print(f"✓ Floor plan analysis successful")
        print(f"  Zones detected: {len(data['zones'])}")
        print(f"  Estimated spots: {data['estimated_spots']}")
        print(f"  Suggested scale: {data['suggested_scale']}")

    def test_analyze_floorplan_with_data_url_prefix(self):
        """Test floor plan analysis with data URL prefix in base64"""
        minimal_png_b64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        
        payload = {
            "image_base64": minimal_png_b64,
            "project_type": "camping",
            "canvas_width": 800,
            "canvas_height": 600
        }
        
        response = requests.post(f"{BASE_URL}/api/ai/analyze-floorplan-smart", json=payload, timeout=60)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "zones" in data
        print(f"✓ Floor plan analysis with data URL prefix handled correctly")


class TestExistingEndpoints:
    """Verify existing endpoints still work after AI services addition"""
    
    def test_health_check(self):
        """Test API root endpoint"""
        response = requests.get(f"{BASE_URL}/api/", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print(f"✓ API health check passed: {data['message']}")

    def test_get_products(self):
        """Test products endpoint"""
        response = requests.get(f"{BASE_URL}/api/products", timeout=10)
        assert response.status_code == 200
        products = response.json()
        assert isinstance(products, list)
        assert len(products) > 0, "Should have seeded products"
        print(f"✓ Products endpoint working: {len(products)} products")

    def test_get_projects(self):
        """Test projects endpoint"""
        response = requests.get(f"{BASE_URL}/api/projects", timeout=10)
        assert response.status_code == 200
        projects = response.json()
        assert isinstance(projects, list)
        print(f"✓ Projects endpoint working: {len(projects)} projects")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
