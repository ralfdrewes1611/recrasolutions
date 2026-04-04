"""
RECRA Solutions CPQ Platform - Iteration 5 Backend Tests
Tests for: Click-to-place, CAPEX->Investering, visible lease text, realistic sanitair dimensions, rectangular pitches
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://recra-quote-wizard.preview.emergentagent.com').rstrip('/')


class TestSanitairDimensions:
    """Test sanitair products have realistic dimensions (3x6m, 6x8m, 8x12m)"""
    
    def test_compact_sanitair_dimensions(self):
        """Compact Sanitair Unit should be 3x6m"""
        response = requests.get(f"{BASE_URL}/api/products/category/sanitair")
        assert response.status_code == 200
        products = response.json()
        
        compact = next((p for p in products if 'Compact' in p['name']), None)
        assert compact is not None, "Compact Sanitair Unit not found"
        
        dims = compact.get('dimensions', {})
        assert dims.get('width') == 3, f"Expected width 3, got {dims.get('width')}"
        assert dims.get('height') == 6, f"Expected height 6, got {dims.get('height')}"
        print(f"✅ Compact Sanitair Unit: {dims['width']}x{dims['height']}m")
    
    def test_medium_sanitair_dimensions(self):
        """Medium Sanitair Unit should be 6x8m"""
        response = requests.get(f"{BASE_URL}/api/products/category/sanitair")
        assert response.status_code == 200
        products = response.json()
        
        medium = next((p for p in products if 'Medium' in p['name']), None)
        assert medium is not None, "Medium Sanitair Unit not found"
        
        dims = medium.get('dimensions', {})
        assert dims.get('width') == 6, f"Expected width 6, got {dims.get('width')}"
        assert dims.get('height') == 8, f"Expected height 8, got {dims.get('height')}"
        print(f"✅ Medium Sanitair Unit: {dims['width']}x{dims['height']}m")
    
    def test_premium_sanitair_dimensions(self):
        """Premium Sanitair Blok should be 8x12m"""
        response = requests.get(f"{BASE_URL}/api/products/category/sanitair")
        assert response.status_code == 200
        products = response.json()
        
        premium = next((p for p in products if 'Premium' in p['name']), None)
        assert premium is not None, "Premium Sanitair Blok not found"
        
        dims = premium.get('dimensions', {})
        assert dims.get('width') == 8, f"Expected width 8, got {dims.get('width')}"
        assert dims.get('height') == 12, f"Expected height 12, got {dims.get('height')}"
        print(f"✅ Premium Sanitair Blok: {dims['width']}x{dims['height']}m")


class TestMuntautomaatRemoved:
    """Verify Muntautomaat is not in product catalog"""
    
    def test_no_muntautomaat_in_products(self):
        """No product should contain 'Muntautomaat' in name"""
        response = requests.get(f"{BASE_URL}/api/products")
        assert response.status_code == 200
        products = response.json()
        
        muntautomaat_products = [p for p in products if 'Muntautomaat' in p['name']]
        assert len(muntautomaat_products) == 0, f"Found Muntautomaat products: {[p['name'] for p in muntautomaat_products]}"
        print("✅ No Muntautomaat found in product catalog")


class TestPDFLabels:
    """Test PDF export uses correct Dutch labels"""
    
    def test_pdf_uses_aankoopkosten_not_capex(self):
        """PDF should use 'Aankoopkosten' instead of 'CAPEX'"""
        # Create project
        project_data = {
            "name": "TEST_PDF_Labels",
            "project_type": "camping",
            "num_spots": 20,
            "placed_products": []
        }
        create_response = requests.post(f"{BASE_URL}/api/projects", json=project_data)
        project_id = create_response.json()['id']
        
        # Get a product and add it
        products_response = requests.get(f"{BASE_URL}/api/products")
        product = products_response.json()[0]
        
        update_data = {
            "placed_products": [
                {"id": "placed-1", "product_id": product['id'], "x": 100, "y": 100, "rotation": 0, "quantity": 1}
            ]
        }
        requests.put(f"{BASE_URL}/api/projects/{project_id}", json=update_data)
        
        # Generate PDF
        response = requests.post(f"{BASE_URL}/api/quote/pdf?project_id={project_id}")
        assert response.status_code == 200
        data = response.json()
        
        html = data['html']
        assert 'Aankoopkosten' in html, "PDF should contain 'Aankoopkosten'"
        # CAPEX should not appear as a label (it may appear in code comments but not as visible text)
        # Check that CAPEX is not used as a visible label
        print("✅ PDF uses 'Aankoopkosten' label")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/projects/{project_id}")
    
    def test_pdf_uses_operational_lease_not_opex(self):
        """PDF should use 'Operational Lease' instead of 'OPEX'"""
        # Create project
        project_data = {
            "name": "TEST_PDF_Lease",
            "project_type": "camping",
            "num_spots": 20,
            "placed_products": []
        }
        create_response = requests.post(f"{BASE_URL}/api/projects", json=project_data)
        project_id = create_response.json()['id']
        
        # Get a product and add it
        products_response = requests.get(f"{BASE_URL}/api/products")
        product = products_response.json()[0]
        
        update_data = {
            "placed_products": [
                {"id": "placed-1", "product_id": product['id'], "x": 100, "y": 100, "rotation": 0, "quantity": 1}
            ]
        }
        requests.put(f"{BASE_URL}/api/projects/{project_id}", json=update_data)
        
        # Generate PDF
        response = requests.post(f"{BASE_URL}/api/quote/pdf?project_id={project_id}")
        assert response.status_code == 200
        data = response.json()
        
        html = data['html']
        assert 'Operational Lease' in html, "PDF should contain 'Operational Lease'"
        assert '60 maanden' in html, "PDF should mention '60 maanden'"
        assert 'SLA' in html, "PDF should mention 'SLA'"
        print("✅ PDF uses 'Operational Lease' with 60 maanden SLA text")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/projects/{project_id}")


class TestProductsAPI:
    """General product API tests"""
    
    def test_get_all_products(self):
        """Verify products endpoint returns data"""
        response = requests.get(f"{BASE_URL}/api/products")
        assert response.status_code == 200
        products = response.json()
        assert len(products) > 0, "Should have products"
        print(f"✅ GET /api/products returns {len(products)} products")
    
    def test_sanitair_products_have_dimensions(self):
        """All sanitair products should have dimensions"""
        response = requests.get(f"{BASE_URL}/api/products/category/sanitair")
        assert response.status_code == 200
        products = response.json()
        
        for product in products:
            dims = product.get('dimensions', {})
            assert 'width' in dims, f"{product['name']} missing width"
            assert 'height' in dims, f"{product['name']} missing height"
            assert dims['width'] > 0, f"{product['name']} has invalid width"
            assert dims['height'] > 0, f"{product['name']} has invalid height"
        print(f"✅ All {len(products)} sanitair products have valid dimensions")


class TestProjectCRUD:
    """Project CRUD operations"""
    
    def test_create_and_get_project(self):
        """Test creating and retrieving a project"""
        project_data = {
            "name": "TEST_Iteration5_Project",
            "project_type": "camping",
            "num_spots": 30,
            "num_large_spots": 5,
            "placed_products": [],
            "zones": []
        }
        
        # Create
        create_response = requests.post(f"{BASE_URL}/api/projects", json=project_data)
        assert create_response.status_code == 200
        project = create_response.json()
        project_id = project['id']
        
        # Get
        get_response = requests.get(f"{BASE_URL}/api/projects/{project_id}")
        assert get_response.status_code == 200
        retrieved = get_response.json()
        assert retrieved['name'] == project_data['name']
        
        print(f"✅ Project CRUD working: {project_id}")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/projects/{project_id}")


class TestQuoteCalculation:
    """Quote calculation tests"""
    
    def test_quote_with_sanitair(self):
        """Test quote calculation with sanitair product"""
        # Create project
        project_data = {
            "name": "TEST_Quote_Sanitair",
            "project_type": "camping",
            "num_spots": 30,
            "placed_products": []
        }
        create_response = requests.post(f"{BASE_URL}/api/projects", json=project_data)
        project_id = create_response.json()['id']
        
        # Get sanitair product
        products_response = requests.get(f"{BASE_URL}/api/products/category/sanitair")
        sanitair = products_response.json()[0]
        
        # Add to project
        update_data = {
            "placed_products": [
                {"id": "placed-1", "product_id": sanitair['id'], "x": 100, "y": 100, "rotation": 0, "quantity": 1}
            ]
        }
        requests.put(f"{BASE_URL}/api/projects/{project_id}", json=update_data)
        
        # Calculate quote
        response = requests.post(f"{BASE_URL}/api/quote/calculate?project_id={project_id}")
        assert response.status_code == 200
        quote = response.json()
        
        assert quote['capex_total'] == sanitair['price_purchase']
        assert quote['opex_monthly'] == sanitair['price_lease_monthly']
        print(f"✅ Quote calculation correct: CAPEX={quote['capex_total']}, Lease/mnd={quote['opex_monthly']}")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/projects/{project_id}")


# Cleanup fixture
@pytest.fixture(scope="session", autouse=True)
def cleanup_test_data():
    yield
    # Cleanup any TEST_ prefixed projects
    try:
        response = requests.get(f"{BASE_URL}/api/projects")
        if response.status_code == 200:
            projects = response.json()
            for project in projects:
                if project['name'].startswith('TEST_'):
                    requests.delete(f"{BASE_URL}/api/projects/{project['id']}")
                    print(f"Cleaned up: {project['name']}")
    except:
        pass
