"""
Iteration 11 Tests: Paywall, Rule-based AI, Travel Costs Filtering, New Products
Tests:
- Paywall tiers (Free/Pro/Enterprise) - frontend state management
- Rule-based AI recommendations (no GPT calls)
- Travel costs filtered by placed product categories
- 27 total products including new UniFi USW-Lite-8-PoE and UNVR Pro
- Flow filtering: Recreatie=all, Chalet=no slagboom, FEC=no sanitair/douchelezer
"""

import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://pleasure-engine.preview.emergentagent.com')

class TestProductsAndFlows:
    """Test product database and flow filtering"""
    
    def test_total_products_count(self):
        """Should have 27 total products"""
        response = requests.get(f"{BASE_URL}/api/products")
        assert response.status_code == 200
        products = response.json()
        assert len(products) == 27, f"Expected 27 products, got {len(products)}"
    
    def test_new_unifi_products_exist(self):
        """Should include new UniFi USW-Lite-8-PoE and UNVR Pro"""
        response = requests.get(f"{BASE_URL}/api/products")
        assert response.status_code == 200
        products = response.json()
        product_names = [p['name'] for p in products]
        
        assert 'UniFi USW-Lite-8-PoE' in product_names, "Missing UniFi USW-Lite-8-PoE"
        assert 'UniFi UNVR Pro' in product_names, "Missing UniFi UNVR Pro"
    
    def test_recreatie_flow_all_categories(self):
        """Recreatie flow should include all 8 categories"""
        response = requests.get(f"{BASE_URL}/api/products?flow=recreatie")
        assert response.status_code == 200
        products = response.json()
        categories = set(p['category'] for p in products)
        
        expected_categories = {'sanitair', 'slagboom', 'camera', 'wifi', 'verlichting', 
                              'betaalsysteem', 'toegangscontrole', 'douchelezer'}
        assert categories == expected_categories, f"Expected {expected_categories}, got {categories}"
        assert len(products) == 27, f"Recreatie should have 27 products, got {len(products)}"
    
    def test_chalet_flow_no_slagboom(self):
        """Chalet flow should exclude slagboom category"""
        response = requests.get(f"{BASE_URL}/api/products?flow=chalet")
        assert response.status_code == 200
        products = response.json()
        categories = set(p['category'] for p in products)
        
        assert 'slagboom' not in categories, "Chalet flow should not include slagboom"
        assert len(products) == 24, f"Chalet should have 24 products, got {len(products)}"
    
    def test_fec_flow_no_sanitair_douchelezer(self):
        """FEC flow should exclude sanitair and douchelezer categories"""
        response = requests.get(f"{BASE_URL}/api/products?flow=fec")
        assert response.status_code == 200
        products = response.json()
        categories = set(p['category'] for p in products)
        
        assert 'sanitair' not in categories, "FEC flow should not include sanitair"
        assert 'douchelezer' not in categories, "FEC flow should not include douchelezer"
        assert len(products) == 21, f"FEC should have 21 products, got {len(products)}"


class TestRuleBasedAI:
    """Test rule-based AI recommendations (no GPT calls)"""
    
    @pytest.fixture
    def test_project(self):
        """Create a test project for AI recommendations"""
        response = requests.post(f"{BASE_URL}/api/projects", json={
            "name": "TEST_AI_Iteration11",
            "project_type": "camping",
            "project_flow": "recreatie",
            "num_spots": 30,
            "placed_products": []
        })
        assert response.status_code == 200
        project = response.json()
        yield project
        # Cleanup
        requests.delete(f"{BASE_URL}/api/projects/{project['id']}")
    
    def test_ai_recommendations_returns_rules(self, test_project):
        """AI recommendations should return rule-based suggestions"""
        response = requests.post(
            f"{BASE_URL}/api/ai/recommendations?project_id={test_project['id']}"
        )
        assert response.status_code == 200
        data = response.json()
        
        assert 'recommendations' in data
        assert len(data['recommendations']) > 0
        
        # Check recommendation structure
        rec = data['recommendations'][0]
        assert 'type' in rec
        assert 'title' in rec
        assert 'description' in rec
    
    def test_ai_sanitair_rule(self, test_project):
        """Should recommend sanitair for 30 spots with none placed"""
        response = requests.post(
            f"{BASE_URL}/api/ai/recommendations?project_id={test_project['id']}"
        )
        assert response.status_code == 200
        data = response.json()
        
        # Find sanitair recommendation
        sanitair_rec = next(
            (r for r in data['recommendations'] if 'sanitair' in r['title'].lower()),
            None
        )
        assert sanitair_rec is not None, "Should have sanitair recommendation"
        assert sanitair_rec['type'] == 'warning'
    
    def test_ai_wifi_rule(self, test_project):
        """Should recommend WiFi for 30 spots with none placed"""
        response = requests.post(
            f"{BASE_URL}/api/ai/recommendations?project_id={test_project['id']}"
        )
        assert response.status_code == 200
        data = response.json()
        
        # Find wifi recommendation
        wifi_rec = next(
            (r for r in data['recommendations'] if 'wifi' in r['title'].lower()),
            None
        )
        assert wifi_rec is not None, "Should have WiFi recommendation"
    
    def test_ai_camera_rule(self, test_project):
        """Should recommend cameras when none placed"""
        response = requests.post(
            f"{BASE_URL}/api/ai/recommendations?project_id={test_project['id']}"
        )
        assert response.status_code == 200
        data = response.json()
        
        # Find camera recommendation
        camera_rec = next(
            (r for r in data['recommendations'] if 'camera' in r['title'].lower()),
            None
        )
        assert camera_rec is not None, "Should have camera recommendation"
    
    def test_ai_slagboom_rule(self, test_project):
        """Should recommend slagboom for parks with >10 spots"""
        response = requests.post(
            f"{BASE_URL}/api/ai/recommendations?project_id={test_project['id']}"
        )
        assert response.status_code == 200
        data = response.json()
        
        # Find slagboom/toegangscontrole recommendation
        slagboom_rec = next(
            (r for r in data['recommendations'] if 'toegangscontrole' in r['title'].lower() or 'slagboom' in r['description'].lower()),
            None
        )
        assert slagboom_rec is not None, "Should have slagboom/toegangscontrole recommendation"
    
    def test_ai_verlichting_rule(self, test_project):
        """Should recommend verlichting when none placed"""
        response = requests.post(
            f"{BASE_URL}/api/ai/recommendations?project_id={test_project['id']}"
        )
        assert response.status_code == 200
        data = response.json()
        
        # Find verlichting recommendation
        verlichting_rec = next(
            (r for r in data['recommendations'] if 'verlichting' in r['title'].lower()),
            None
        )
        assert verlichting_rec is not None, "Should have verlichting recommendation"


class TestTravelCostsFiltering:
    """Test that travel costs only show for categories with placed products"""
    
    @pytest.fixture
    def test_project_with_wifi(self):
        """Create a test project with only wifi product placed"""
        # Get a wifi product ID
        products_response = requests.get(f"{BASE_URL}/api/products")
        products = products_response.json()
        wifi_product = next(p for p in products if p['category'] == 'wifi')
        
        # Create project with wifi product
        response = requests.post(f"{BASE_URL}/api/projects", json={
            "name": "TEST_TravelCosts_Iteration11",
            "project_type": "camping",
            "project_flow": "recreatie",
            "num_spots": 30,
            "lat": 52.0,
            "lng": 5.0,
            "placed_products": [
                {"id": "placed-wifi-1", "product_id": wifi_product['id'], "x": 100, "y": 100, "rotation": 0, "quantity": 1}
            ]
        })
        assert response.status_code == 200
        project = response.json()
        yield project, wifi_product
        # Cleanup
        requests.delete(f"{BASE_URL}/api/projects/{project['id']}")
    
    def test_travel_costs_only_for_placed_categories(self, test_project_with_wifi):
        """Travel costs should only include wifi category"""
        project, wifi_product = test_project_with_wifi
        
        response = requests.post(
            f"{BASE_URL}/api/quote/calculate?project_id={project['id']}"
        )
        assert response.status_code == 200
        quote = response.json()
        
        # Should have travel_costs array
        assert 'travel_costs' in quote
        assert len(quote['travel_costs']) == 1, f"Expected 1 travel cost entry, got {len(quote['travel_costs'])}"
        
        # Should only be for wifi category
        assert quote['travel_costs'][0]['category'] == 'wifi'
    
    def test_travel_costs_multiple_categories(self):
        """Travel costs should include all placed product categories"""
        # Get products from different categories
        products_response = requests.get(f"{BASE_URL}/api/products")
        products = products_response.json()
        wifi_product = next(p for p in products if p['category'] == 'wifi')
        camera_product = next(p for p in products if p['category'] == 'camera')
        
        # Create project with both wifi and camera
        response = requests.post(f"{BASE_URL}/api/projects", json={
            "name": "TEST_MultiCategory_Iteration11",
            "project_type": "camping",
            "project_flow": "recreatie",
            "num_spots": 30,
            "lat": 52.0,
            "lng": 5.0,
            "placed_products": [
                {"id": "placed-wifi-1", "product_id": wifi_product['id'], "x": 100, "y": 100, "rotation": 0, "quantity": 1},
                {"id": "placed-camera-1", "product_id": camera_product['id'], "x": 200, "y": 200, "rotation": 0, "quantity": 1}
            ]
        })
        assert response.status_code == 200
        project = response.json()
        
        try:
            quote_response = requests.post(
                f"{BASE_URL}/api/quote/calculate?project_id={project['id']}"
            )
            assert quote_response.status_code == 200
            quote = quote_response.json()
            
            # Should have travel costs for both categories
            categories_in_travel = [tc['category'] for tc in quote['travel_costs']]
            assert 'wifi' in categories_in_travel, "Should have wifi travel cost"
            assert 'camera' in categories_in_travel, "Should have camera travel cost"
        finally:
            requests.delete(f"{BASE_URL}/api/projects/{project['id']}")
    
    def test_no_travel_costs_for_empty_project(self):
        """Empty project should have no travel costs"""
        response = requests.post(f"{BASE_URL}/api/projects", json={
            "name": "TEST_Empty_Iteration11",
            "project_type": "camping",
            "project_flow": "recreatie",
            "num_spots": 30,
            "placed_products": []
        })
        assert response.status_code == 200
        project = response.json()
        
        try:
            quote_response = requests.post(
                f"{BASE_URL}/api/quote/calculate?project_id={project['id']}"
            )
            assert quote_response.status_code == 200
            quote = quote_response.json()
            
            # Should have empty travel_costs
            assert quote['travel_costs'] == [], f"Expected empty travel_costs, got {quote['travel_costs']}"
            assert quote['travel_total'] == 0
        finally:
            requests.delete(f"{BASE_URL}/api/projects/{project['id']}")


class TestSupplierMatching:
    """Test supplier matching API"""
    
    def test_supplier_match_returns_data(self):
        """Supplier match should return suppliers with travel info"""
        response = requests.post(f"{BASE_URL}/api/suppliers/match", json={
            "project_lat": 52.0,
            "project_lng": 5.0
        })
        assert response.status_code == 200
        suppliers = response.json()
        
        assert len(suppliers) > 0, "Should return at least one supplier"
        
        # Check structure
        supplier = suppliers[0]
        assert 'supplier' in supplier
        assert 'travel' in supplier
        assert 'distance_km' in supplier['travel']
        assert 'total_travel_cost' in supplier['travel']


class TestHealthAndBasics:
    """Basic health checks"""
    
    def test_api_health(self):
        """API should be healthy"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert 'message' in data
    
    def test_products_endpoint(self):
        """Products endpoint should return data"""
        response = requests.get(f"{BASE_URL}/api/products")
        assert response.status_code == 200
        products = response.json()
        assert isinstance(products, list)
        assert len(products) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
