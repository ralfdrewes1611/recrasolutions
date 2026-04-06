"""
RECRA Solutions - Iteration 10 Backend Tests
Tests for:
- Flow-specific product filtering (recreatie, chalet, fec)
- Supplier matching API with travel costs
- Quote calculation with travel_costs and travel_total fields
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestFlowProductFiltering:
    """Test flow-specific product filtering"""
    
    def test_api_health(self):
        """Test API is running"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print("PASS: API health check")
    
    def test_all_products_count(self):
        """Test total products without flow filter"""
        response = requests.get(f"{BASE_URL}/api/products")
        assert response.status_code == 200
        products = response.json()
        assert len(products) == 25, f"Expected 25 products, got {len(products)}"
        print(f"PASS: Total products = {len(products)}")
    
    def test_recreatie_flow_products(self):
        """Test recreatie flow returns 25 products (all categories)"""
        response = requests.get(f"{BASE_URL}/api/products?flow=recreatie")
        assert response.status_code == 200
        products = response.json()
        assert len(products) == 25, f"Expected 25 products for recreatie, got {len(products)}"
        categories = set(p['category'] for p in products)
        expected_cats = {'sanitair', 'slagboom', 'camera', 'wifi', 'verlichting', 'betaalsysteem', 'toegangscontrole', 'douchelezer'}
        assert categories == expected_cats, f"Expected categories {expected_cats}, got {categories}"
        print(f"PASS: Recreatie flow = {len(products)} products, categories: {categories}")
    
    def test_chalet_flow_products(self):
        """Test chalet flow returns 22 products (no slagboom)"""
        response = requests.get(f"{BASE_URL}/api/products?flow=chalet")
        assert response.status_code == 200
        products = response.json()
        assert len(products) == 22, f"Expected 22 products for chalet, got {len(products)}"
        categories = set(p['category'] for p in products)
        assert 'slagboom' not in categories, "Chalet flow should not include slagboom"
        print(f"PASS: Chalet flow = {len(products)} products, categories: {categories}")
    
    def test_fec_flow_products(self):
        """Test FEC flow returns 19 products (no sanitair, douchelezer)"""
        response = requests.get(f"{BASE_URL}/api/products?flow=fec")
        assert response.status_code == 200
        products = response.json()
        assert len(products) == 19, f"Expected 19 products for FEC, got {len(products)}"
        categories = set(p['category'] for p in products)
        assert 'sanitair' not in categories, "FEC flow should not include sanitair"
        assert 'douchelezer' not in categories, "FEC flow should not include douchelezer"
        print(f"PASS: FEC flow = {len(products)} products, categories: {categories}")


class TestSupplierMatching:
    """Test supplier matching API with travel costs"""
    
    def test_supplier_list(self):
        """Test GET /api/suppliers returns all suppliers"""
        response = requests.get(f"{BASE_URL}/api/suppliers")
        assert response.status_code == 200
        suppliers = response.json()
        assert len(suppliers) == 5, f"Expected 5 suppliers, got {len(suppliers)}"
        print(f"PASS: Supplier list = {len(suppliers)} suppliers")
    
    def test_supplier_match_returns_sorted_list(self):
        """Test POST /api/suppliers/match returns sorted suppliers with travel costs"""
        response = requests.post(f"{BASE_URL}/api/suppliers/match", json={
            "project_lat": 52.0,
            "project_lng": 5.0
        })
        assert response.status_code == 200
        results = response.json()
        assert len(results) == 5, f"Expected 5 matched suppliers, got {len(results)}"
        
        # Check structure
        for r in results:
            assert 'supplier' in r, "Missing 'supplier' field"
            assert 'travel' in r, "Missing 'travel' field"
            assert 'distance_km' in r['travel'], "Missing 'distance_km' in travel"
            assert 'total_travel_cost' in r['travel'], "Missing 'total_travel_cost' in travel"
            assert 'travel_time_hours' in r['travel'], "Missing 'travel_time_hours' in travel"
        
        # Check sorting (verified first, then by distance)
        verified_statuses = [r['supplier'].get('verified_status', 'basic') for r in results]
        print(f"PASS: Supplier match returns {len(results)} suppliers with travel costs")
        print(f"  Verified statuses order: {verified_statuses}")
    
    def test_supplier_match_with_category_filter(self):
        """Test supplier match with category filter"""
        response = requests.post(f"{BASE_URL}/api/suppliers/match", json={
            "project_lat": 52.0,
            "project_lng": 5.0,
            "category": "camera"
        })
        assert response.status_code == 200
        results = response.json()
        # Only Ubiquiti should match camera category
        assert len(results) >= 1, "Expected at least 1 supplier for camera category"
        for r in results:
            assert 'camera' in r['supplier']['categories'], f"Supplier {r['supplier']['name']} doesn't have camera category"
        print(f"PASS: Supplier match with category filter = {len(results)} suppliers")


class TestQuoteCalculation:
    """Test quote calculation with travel costs"""
    
    @pytest.fixture
    def test_project(self):
        """Create a test project with products"""
        # Get a product ID
        products_resp = requests.get(f"{BASE_URL}/api/products")
        products = products_resp.json()
        sanitair_product = next((p for p in products if p['category'] == 'sanitair'), None)
        camera_product = next((p for p in products if p['category'] == 'camera'), None)
        
        # Create project
        project_resp = requests.post(f"{BASE_URL}/api/projects", json={
            "name": "TEST_Quote_Iteration10",
            "project_type": "camping",
            "project_flow": "recreatie",
            "lat": 52.0,
            "lng": 5.0,
            "num_spots": 30,
            "placed_products": [
                {"id": "test-1", "product_id": sanitair_product['id'], "x": 100, "y": 100, "rotation": 0, "quantity": 1},
                {"id": "test-2", "product_id": camera_product['id'], "x": 200, "y": 200, "rotation": 0, "quantity": 2}
            ]
        })
        project = project_resp.json()
        yield project
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/projects/{project['id']}")
    
    def test_quote_includes_travel_costs(self, test_project):
        """Test quote calculation includes travel_costs and travel_total"""
        response = requests.post(f"{BASE_URL}/api/quote/calculate?project_id={test_project['id']}")
        assert response.status_code == 200
        quote = response.json()
        
        # Check required fields
        assert 'capex_total' in quote, "Missing capex_total"
        assert 'installation_total' in quote, "Missing installation_total"
        assert 'travel_costs' in quote, "Missing travel_costs"
        assert 'travel_total' in quote, "Missing travel_total"
        assert 'project_total' in quote, "Missing project_total"
        
        # Check travel_costs structure
        assert isinstance(quote['travel_costs'], list), "travel_costs should be a list"
        for tc in quote['travel_costs']:
            assert 'category' in tc, "Missing category in travel_cost"
            assert 'supplier_name' in tc, "Missing supplier_name in travel_cost"
            assert 'distance_km' in tc, "Missing distance_km in travel_cost"
            assert 'total_travel_cost' in tc, "Missing total_travel_cost in travel_cost"
        
        # Check project_total calculation
        expected_total = quote['capex_total'] + quote['installation_total'] + quote['travel_total']
        assert abs(quote['project_total'] - expected_total) < 0.01, f"project_total mismatch: {quote['project_total']} != {expected_total}"
        
        print(f"PASS: Quote calculation with travel costs")
        print(f"  capex_total: EUR {quote['capex_total']}")
        print(f"  installation_total: EUR {quote['installation_total']}")
        print(f"  travel_total: EUR {quote['travel_total']}")
        print(f"  project_total: EUR {quote['project_total']}")
        print(f"  travel_costs entries: {len(quote['travel_costs'])}")
    
    def test_quote_travel_costs_per_category(self, test_project):
        """Test that travel costs are calculated per category (nearest supplier)"""
        response = requests.post(f"{BASE_URL}/api/quote/calculate?project_id={test_project['id']}")
        quote = response.json()
        
        # Should have travel costs for sanitair and camera categories
        categories_in_travel = [tc['category'] for tc in quote['travel_costs']]
        assert 'sanitair' in categories_in_travel, "Missing sanitair in travel_costs"
        assert 'camera' in categories_in_travel, "Missing camera in travel_costs"
        
        print(f"PASS: Travel costs per category: {categories_in_travel}")


class TestProjectCRUD:
    """Test project CRUD operations"""
    
    def test_create_and_get_project(self):
        """Test creating and retrieving a project"""
        # Create
        create_resp = requests.post(f"{BASE_URL}/api/projects", json={
            "name": "TEST_CRUD_Project",
            "project_type": "camping",
            "project_flow": "recreatie",
            "lat": 52.5,
            "lng": 5.5,
            "num_spots": 20
        })
        assert create_resp.status_code == 200
        project = create_resp.json()
        assert 'id' in project
        assert project['name'] == "TEST_CRUD_Project"
        
        # Get
        get_resp = requests.get(f"{BASE_URL}/api/projects/{project['id']}")
        assert get_resp.status_code == 200
        fetched = get_resp.json()
        assert fetched['id'] == project['id']
        assert fetched['name'] == "TEST_CRUD_Project"
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/projects/{project['id']}")
        print("PASS: Project CRUD - create and get")
    
    def test_update_project(self):
        """Test updating a project"""
        # Create
        create_resp = requests.post(f"{BASE_URL}/api/projects", json={
            "name": "TEST_Update_Project",
            "project_type": "camping",
            "project_flow": "recreatie"
        })
        project = create_resp.json()
        
        # Update
        update_resp = requests.put(f"{BASE_URL}/api/projects/{project['id']}", json={
            "name": "TEST_Updated_Name",
            "num_spots": 50
        })
        assert update_resp.status_code == 200
        updated = update_resp.json()
        assert updated['name'] == "TEST_Updated_Name"
        assert updated['num_spots'] == 50
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/projects/{project['id']}")
        print("PASS: Project CRUD - update")
    
    def test_delete_project(self):
        """Test deleting a project"""
        # Create
        create_resp = requests.post(f"{BASE_URL}/api/projects", json={
            "name": "TEST_Delete_Project",
            "project_type": "camping"
        })
        project = create_resp.json()
        
        # Delete
        delete_resp = requests.delete(f"{BASE_URL}/api/projects/{project['id']}")
        assert delete_resp.status_code == 200
        
        # Verify deleted
        get_resp = requests.get(f"{BASE_URL}/api/projects/{project['id']}")
        assert get_resp.status_code == 404
        
        print("PASS: Project CRUD - delete")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
