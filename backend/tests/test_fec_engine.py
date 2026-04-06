"""
FEC Revenue Engine API Tests
Tests for FEC-specific endpoints: products, suppliers, zone-types, top5, calculate-revenue
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestFecProducts:
    """Tests for GET /api/fec/products endpoint"""
    
    def test_get_fec_products_returns_200(self):
        """Verify FEC products endpoint returns 200"""
        response = requests.get(f"{BASE_URL}/api/fec/products")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print("✓ GET /api/fec/products returns 200")
    
    def test_get_fec_products_returns_14_products(self):
        """Verify FEC products endpoint returns exactly 14 products"""
        response = requests.get(f"{BASE_URL}/api/fec/products")
        data = response.json()
        assert len(data) == 14, f"Expected 14 products, got {len(data)}"
        print(f"✓ GET /api/fec/products returns 14 products")
    
    def test_fec_products_have_required_fields(self):
        """Verify each FEC product has revenue_per_hour, footprint_m2, roi_months"""
        response = requests.get(f"{BASE_URL}/api/fec/products")
        data = response.json()
        
        required_fields = ['id', 'name', 'category', 'supplier', 'footprint_m2', 
                          'price_purchase', 'revenue_per_hour', 'roi_months']
        
        for product in data:
            for field in required_fields:
                assert field in product, f"Product {product.get('name', 'unknown')} missing field: {field}"
            
            # Verify numeric fields are positive
            assert product['revenue_per_hour'] > 0, f"Product {product['name']} has invalid revenue_per_hour"
            assert product['footprint_m2'] > 0, f"Product {product['name']} has invalid footprint_m2"
            assert product['roi_months'] > 0, f"Product {product['name']} has invalid roi_months"
        
        print(f"✓ All 14 FEC products have required fields with valid values")
    
    def test_fec_products_categories(self):
        """Verify FEC products span 5 categories: arcade, karting, interactive, indoor_play, horeca"""
        response = requests.get(f"{BASE_URL}/api/fec/products")
        data = response.json()
        
        categories = set(p['category'] for p in data)
        expected_categories = {'arcade', 'karting', 'interactive', 'indoor_play', 'horeca'}
        
        assert categories == expected_categories, f"Expected categories {expected_categories}, got {categories}"
        print(f"✓ FEC products span all 5 expected categories: {categories}")


class TestFecTop5:
    """Tests for GET /api/fec/top5 endpoint"""
    
    def test_get_top5_returns_200(self):
        """Verify top5 endpoint returns 200"""
        response = requests.get(f"{BASE_URL}/api/fec/top5")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print("✓ GET /api/fec/top5 returns 200")
    
    def test_get_top5_returns_5_products(self):
        """Verify top5 endpoint returns exactly 5 products"""
        response = requests.get(f"{BASE_URL}/api/fec/top5")
        data = response.json()
        assert len(data) == 5, f"Expected 5 products, got {len(data)}"
        print("✓ GET /api/fec/top5 returns 5 products")
    
    def test_top5_sorted_by_revenue_per_m2(self):
        """Verify top5 is sorted by revenue_per_m2 descending"""
        response = requests.get(f"{BASE_URL}/api/fec/top5")
        data = response.json()
        
        revenue_values = [p['revenue_per_m2'] for p in data]
        assert revenue_values == sorted(revenue_values, reverse=True), \
            f"Top5 not sorted by revenue_per_m2: {revenue_values}"
        
        # First item should have highest revenue per m2
        assert data[0]['revenue_per_m2'] >= data[-1]['revenue_per_m2'], \
            "First item should have highest revenue_per_m2"
        
        print(f"✓ Top5 correctly sorted by revenue_per_m2: {revenue_values}")
    
    def test_top5_has_required_fields(self):
        """Verify top5 products have all required fields"""
        response = requests.get(f"{BASE_URL}/api/fec/top5")
        data = response.json()
        
        required_fields = ['id', 'name', 'category', 'supplier', 'investment', 
                          'monthly_revenue', 'roi_months', 'revenue_per_m2', 'revenue_per_hour']
        
        for product in data:
            for field in required_fields:
                assert field in product, f"Top5 product {product.get('name', 'unknown')} missing field: {field}"
        
        print("✓ All top5 products have required fields")


class TestFecZoneTypes:
    """Tests for GET /api/fec/zone-types endpoint"""
    
    def test_get_zone_types_returns_200(self):
        """Verify zone-types endpoint returns 200"""
        response = requests.get(f"{BASE_URL}/api/fec/zone-types")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print("✓ GET /api/fec/zone-types returns 200")
    
    def test_zone_types_returns_7_types(self):
        """Verify zone-types returns 7 zone types"""
        response = requests.get(f"{BASE_URL}/api/fec/zone-types")
        data = response.json()
        assert len(data) == 7, f"Expected 7 zone types, got {len(data)}"
        print(f"✓ GET /api/fec/zone-types returns 7 zone types")
    
    def test_zone_types_have_required_fields(self):
        """Verify each zone type has id, name, color, min_m2, revenue_factor"""
        response = requests.get(f"{BASE_URL}/api/fec/zone-types")
        data = response.json()
        
        required_fields = ['id', 'name', 'color', 'min_m2', 'revenue_factor']
        expected_ids = {'entree', 'arcade', 'karting', 'interactive', 'indoor_play', 'horeca', 'routing'}
        
        actual_ids = set()
        for zone in data:
            for field in required_fields:
                assert field in zone, f"Zone {zone.get('id', 'unknown')} missing field: {field}"
            actual_ids.add(zone['id'])
        
        assert actual_ids == expected_ids, f"Expected zone IDs {expected_ids}, got {actual_ids}"
        print(f"✓ All zone types have required fields and correct IDs")


class TestFecSuppliers:
    """Tests for GET /api/fec/suppliers endpoint"""
    
    def test_get_suppliers_returns_200(self):
        """Verify suppliers endpoint returns 200"""
        response = requests.get(f"{BASE_URL}/api/fec/suppliers")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print("✓ GET /api/fec/suppliers returns 200")
    
    def test_suppliers_returns_5_suppliers(self):
        """Verify suppliers endpoint returns exactly 5 FEC suppliers"""
        response = requests.get(f"{BASE_URL}/api/fec/suppliers")
        data = response.json()
        assert len(data) == 5, f"Expected 5 suppliers, got {len(data)}"
        print(f"✓ GET /api/fec/suppliers returns 5 suppliers")
    
    def test_suppliers_have_required_fields(self):
        """Verify each supplier has required fields"""
        response = requests.get(f"{BASE_URL}/api/fec/suppliers")
        data = response.json()
        
        required_fields = ['id', 'name', 'address', 'lat', 'lng', 'categories', 'specialization']
        expected_names = {'X-Wall', 'Shuffly', 'Heemskerk Play', 'Pro Karting', 'Time Mission'}
        
        actual_names = set()
        for supplier in data:
            for field in required_fields:
                assert field in supplier, f"Supplier {supplier.get('name', 'unknown')} missing field: {field}"
            actual_names.add(supplier['name'])
        
        assert actual_names == expected_names, f"Expected suppliers {expected_names}, got {actual_names}"
        print(f"✓ All 5 FEC suppliers present: {actual_names}")


class TestFecCalculateRevenue:
    """Tests for POST /api/fec/calculate-revenue endpoint"""
    
    def test_calculate_revenue_returns_200(self):
        """Verify calculate-revenue endpoint returns 200"""
        payload = {
            "products": [{"product_id": "fec-0", "quantity": 1}],
            "operating_hours": 10,
            "operating_days": 30,
            "project": {"total_area_m2": 500, "ceiling_height_m": 5, "zones": []}
        }
        response = requests.post(f"{BASE_URL}/api/fec/calculate-revenue", json=payload)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print("✓ POST /api/fec/calculate-revenue returns 200")
    
    def test_calculate_revenue_response_structure(self):
        """Verify calculate-revenue returns all required fields"""
        payload = {
            "products": [{"product_id": "fec-0", "quantity": 1}],
            "operating_hours": 10,
            "operating_days": 30,
            "project": {"total_area_m2": 500, "ceiling_height_m": 5, "zones": []}
        }
        response = requests.post(f"{BASE_URL}/api/fec/calculate-revenue", json=payload)
        data = response.json()
        
        required_fields = ['total_investment', 'total_monthly_revenue', 'break_even_months', 
                          'top_performers', 'suggestions']
        
        for field in required_fields:
            assert field in data, f"Response missing required field: {field}"
        
        print(f"✓ calculate-revenue response has all required fields")
    
    def test_calculate_revenue_correct_calculation(self):
        """Verify revenue calculation is correct for known product"""
        # fec-0 is Shuffleboard Pro Table: price_purchase=4500, installation_cost=500, revenue_per_hour=25
        payload = {
            "products": [{"product_id": "fec-0", "quantity": 1}],
            "operating_hours": 10,
            "operating_days": 30,
            "project": {"total_area_m2": 500, "ceiling_height_m": 5, "zones": []}
        }
        response = requests.post(f"{BASE_URL}/api/fec/calculate-revenue", json=payload)
        data = response.json()
        
        # Expected: investment = 4500 + 500 = 5000
        # Expected: monthly_revenue = 25 * 10 * 30 = 7500
        # Expected: break_even = 5000 / 7500 = 0.67 (rounded to 0.7)
        
        assert data['total_investment'] == 5000, f"Expected investment 5000, got {data['total_investment']}"
        assert data['total_monthly_revenue'] == 7500, f"Expected monthly revenue 7500, got {data['total_monthly_revenue']}"
        assert 0.6 <= data['break_even_months'] <= 0.8, f"Expected break_even ~0.7, got {data['break_even_months']}"
        
        print(f"✓ Revenue calculation correct: investment={data['total_investment']}, monthly={data['total_monthly_revenue']}, break_even={data['break_even_months']}")
    
    def test_calculate_revenue_multiple_products(self):
        """Verify revenue calculation with multiple products and quantities"""
        payload = {
            "products": [
                {"product_id": "fec-0", "quantity": 2},  # 2x Shuffleboard
                {"product_id": "fec-12", "quantity": 1}  # 1x Self-Service Drinks
            ],
            "operating_hours": 10,
            "operating_days": 30,
            "project": {"total_area_m2": 500, "ceiling_height_m": 5, "zones": []}
        }
        response = requests.post(f"{BASE_URL}/api/fec/calculate-revenue", json=payload)
        data = response.json()
        
        # fec-0: (4500+500)*2 = 10000 investment, 25*10*30*2 = 15000 monthly
        # fec-12: (8500+1500)*1 = 10000 investment, 35*10*30*1 = 10500 monthly
        # Total: 20000 investment, 25500 monthly
        
        assert data['total_investment'] == 20000, f"Expected investment 20000, got {data['total_investment']}"
        assert data['total_monthly_revenue'] == 25500, f"Expected monthly revenue 25500, got {data['total_monthly_revenue']}"
        
        print(f"✓ Multi-product calculation correct: investment={data['total_investment']}, monthly={data['total_monthly_revenue']}")
    
    def test_calculate_revenue_returns_suggestions(self):
        """Verify calculate-revenue returns AI suggestions"""
        payload = {
            "products": [{"product_id": "fec-0", "quantity": 1}],  # Only arcade, no horeca
            "operating_hours": 10,
            "operating_days": 30,
            "project": {"total_area_m2": 500, "ceiling_height_m": 5, "zones": []}
        }
        response = requests.post(f"{BASE_URL}/api/fec/calculate-revenue", json=payload)
        data = response.json()
        
        assert 'suggestions' in data, "Response missing suggestions"
        assert len(data['suggestions']) > 0, "Expected at least one suggestion"
        
        # Should suggest adding horeca since we only have arcade
        suggestion_titles = [s['title'] for s in data['suggestions']]
        print(f"✓ AI suggestions returned: {suggestion_titles}")
    
    def test_calculate_revenue_top_performers(self):
        """Verify top_performers is sorted by monthly_revenue"""
        payload = {
            "products": [
                {"product_id": "fec-0", "quantity": 1},
                {"product_id": "fec-12", "quantity": 1},
                {"product_id": "fec-3", "quantity": 1}  # Karting - highest revenue
            ],
            "operating_hours": 10,
            "operating_days": 30,
            "project": {"total_area_m2": 500, "ceiling_height_m": 5, "zones": []}
        }
        response = requests.post(f"{BASE_URL}/api/fec/calculate-revenue", json=payload)
        data = response.json()
        
        top_performers = data['top_performers']
        assert len(top_performers) > 0, "Expected top_performers"
        
        # Verify sorted by monthly_revenue descending
        revenues = [p['monthly_revenue'] for p in top_performers]
        assert revenues == sorted(revenues, reverse=True), f"Top performers not sorted: {revenues}"
        
        print(f"✓ Top performers sorted correctly: {[p['product_name'] for p in top_performers]}")


class TestRecreatieChaletFlowsStillWork:
    """Verify existing Recreatie/Chalet flows are not broken by FEC changes"""
    
    def test_products_endpoint_still_works(self):
        """Verify main products endpoint still works"""
        response = requests.get(f"{BASE_URL}/api/products")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert len(data) > 0, "Expected products"
        print(f"✓ GET /api/products still works, returns {len(data)} products")
    
    def test_products_filter_by_recreatie_flow(self):
        """Verify products can be filtered by recreatie flow"""
        response = requests.get(f"{BASE_URL}/api/products?flow=recreatie")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert len(data) > 0, "Expected recreatie products"
        
        # Verify categories are recreatie-specific
        categories = set(p['category'] for p in data)
        expected_categories = {'sanitair', 'slagboom', 'camera', 'wifi', 'verlichting', 
                              'betaalsysteem', 'toegangscontrole', 'douchelezer'}
        assert categories.issubset(expected_categories), f"Unexpected categories: {categories - expected_categories}"
        
        print(f"✓ Recreatie flow products filter works, {len(data)} products in categories: {categories}")
    
    def test_products_filter_by_chalet_flow(self):
        """Verify products can be filtered by chalet flow"""
        response = requests.get(f"{BASE_URL}/api/products?flow=chalet")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert len(data) > 0, "Expected chalet products"
        print(f"✓ Chalet flow products filter works, returns {len(data)} products")
    
    def test_projects_crud_still_works(self):
        """Verify projects CRUD still works"""
        # Create
        project_data = {
            "name": "TEST_FEC_Iteration_Project",
            "project_type": "camping",
            "project_flow": "recreatie",
            "num_spots": 30
        }
        create_response = requests.post(f"{BASE_URL}/api/projects", json=project_data)
        assert create_response.status_code == 200, f"Create failed: {create_response.status_code}"
        created = create_response.json()
        project_id = created['id']
        
        # Read
        get_response = requests.get(f"{BASE_URL}/api/projects/{project_id}")
        assert get_response.status_code == 200, f"Get failed: {get_response.status_code}"
        
        # Delete
        delete_response = requests.delete(f"{BASE_URL}/api/projects/{project_id}")
        assert delete_response.status_code == 200, f"Delete failed: {delete_response.status_code}"
        
        print("✓ Projects CRUD still works (create, read, delete)")
    
    def test_ai_recommendations_still_works(self):
        """Verify AI recommendations endpoint still works"""
        # Create a project first
        project_data = {
            "name": "TEST_AI_Rec_Project",
            "project_type": "camping",
            "project_flow": "recreatie",
            "num_spots": 30,
            "placed_products": []
        }
        create_response = requests.post(f"{BASE_URL}/api/projects", json=project_data)
        created = create_response.json()
        project_id = created['id']
        
        # Get recommendations
        rec_response = requests.post(f"{BASE_URL}/api/ai/recommendations?project_id={project_id}")
        assert rec_response.status_code == 200, f"AI recommendations failed: {rec_response.status_code}"
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/projects/{project_id}")
        
        print("✓ AI recommendations endpoint still works")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
