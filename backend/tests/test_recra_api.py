"""
RECRA Solutions CPQ Platform - Backend API Tests
Tests for products, projects, quotes, and AI recommendations
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://recra-config.preview.emergentagent.com').rstrip('/')

class TestProductsAPI:
    """Product catalog API tests"""
    
    def test_get_all_products_returns_22(self):
        """Verify exactly 22 products are returned (Muntautomaat removed)"""
        response = requests.get(f"{BASE_URL}/api/products")
        assert response.status_code == 200
        products = response.json()
        assert len(products) == 22, f"Expected 22 products, got {len(products)}"
        print(f"✅ GET /api/products returns {len(products)} products")
    
    def test_no_muntautomaat_in_products(self):
        """Verify Muntautomaat has been removed from product catalog"""
        response = requests.get(f"{BASE_URL}/api/products")
        assert response.status_code == 200
        products = response.json()
        product_names = [p['name'] for p in products]
        assert not any('Muntautomaat' in name for name in product_names), "Muntautomaat should be removed"
        print("✅ No Muntautomaat found in products")
    
    def test_sanitair_category_has_3_products(self):
        """Verify sanitair category has exactly 3 products"""
        response = requests.get(f"{BASE_URL}/api/products/category/sanitair")
        assert response.status_code == 200
        products = response.json()
        assert len(products) == 3, f"Expected 3 sanitair products, got {len(products)}"
        print(f"✅ Sanitair category has {len(products)} products")
    
    def test_douchelezer_category_has_3_products(self):
        """Verify douchelezer category has exactly 3 products"""
        response = requests.get(f"{BASE_URL}/api/products/category/douchelezer")
        assert response.status_code == 200
        products = response.json()
        assert len(products) == 3, f"Expected 3 douchelezer products, got {len(products)}"
        print(f"✅ Douchelezer category has {len(products)} products")
    
    def test_all_categories_exist(self):
        """Verify all expected categories exist"""
        response = requests.get(f"{BASE_URL}/api/products")
        assert response.status_code == 200
        products = response.json()
        categories = set(p['category'] for p in products)
        expected_categories = {'sanitair', 'slagboom', 'camera', 'wifi', 'verlichting', 'betaalsysteem', 'toegangscontrole', 'douchelezer'}
        assert expected_categories.issubset(categories), f"Missing categories: {expected_categories - categories}"
        print(f"✅ All {len(expected_categories)} categories exist")
    
    def test_product_has_required_fields(self):
        """Verify products have all required fields"""
        response = requests.get(f"{BASE_URL}/api/products")
        assert response.status_code == 200
        products = response.json()
        required_fields = ['id', 'name', 'category', 'description', 'price_purchase', 'price_lease_monthly', 'installation_cost', 'maintenance_yearly']
        for product in products[:3]:  # Check first 3 products
            for field in required_fields:
                assert field in product, f"Product missing field: {field}"
        print("✅ Products have all required fields")


class TestProjectsAPI:
    """Project CRUD API tests"""
    
    @pytest.fixture
    def test_project_data(self):
        return {
            "name": "TEST_Camping De Zonnehoek",
            "project_type": "camping",
            "num_spots": 30,
            "placed_products": [],
            "zones": []
        }
    
    def test_create_project(self, test_project_data):
        """Test creating a new project"""
        response = requests.post(f"{BASE_URL}/api/projects", json=test_project_data)
        assert response.status_code == 200
        project = response.json()
        assert project['name'] == test_project_data['name']
        assert project['project_type'] == test_project_data['project_type']
        assert 'id' in project
        print(f"✅ Created project: {project['id']}")
        return project['id']
    
    def test_get_project(self, test_project_data):
        """Test getting a project by ID"""
        # First create a project
        create_response = requests.post(f"{BASE_URL}/api/projects", json=test_project_data)
        project_id = create_response.json()['id']
        
        # Then get it
        response = requests.get(f"{BASE_URL}/api/projects/{project_id}")
        assert response.status_code == 200
        project = response.json()
        assert project['id'] == project_id
        assert project['name'] == test_project_data['name']
        print(f"✅ Retrieved project: {project_id}")
    
    def test_update_project_with_placed_products(self, test_project_data):
        """Test updating a project with placed products"""
        # Create project
        create_response = requests.post(f"{BASE_URL}/api/projects", json=test_project_data)
        project_id = create_response.json()['id']
        
        # Get a product ID
        products_response = requests.get(f"{BASE_URL}/api/products")
        product_id = products_response.json()[0]['id']
        
        # Update with placed product
        update_data = {
            "placed_products": [
                {"id": "placed-1", "product_id": product_id, "x": 100, "y": 100, "rotation": 0, "quantity": 1}
            ]
        }
        response = requests.put(f"{BASE_URL}/api/projects/{project_id}", json=update_data)
        assert response.status_code == 200
        updated = response.json()
        assert len(updated['placed_products']) == 1
        print(f"✅ Updated project with placed product")
    
    def test_delete_project(self, test_project_data):
        """Test deleting a project"""
        # Create project
        create_response = requests.post(f"{BASE_URL}/api/projects", json=test_project_data)
        project_id = create_response.json()['id']
        
        # Delete it
        response = requests.delete(f"{BASE_URL}/api/projects/{project_id}")
        assert response.status_code == 200
        
        # Verify it's gone
        get_response = requests.get(f"{BASE_URL}/api/projects/{project_id}")
        assert get_response.status_code == 404
        print(f"✅ Deleted project: {project_id}")


class TestQuoteAPI:
    """Quote calculation API tests"""
    
    def test_calculate_quote(self):
        """Test quote calculation with placed products"""
        # Create project
        project_data = {
            "name": "TEST_Quote Project",
            "project_type": "camping",
            "num_spots": 20,
            "placed_products": []
        }
        create_response = requests.post(f"{BASE_URL}/api/projects", json=project_data)
        project_id = create_response.json()['id']
        
        # Get a product
        products_response = requests.get(f"{BASE_URL}/api/products")
        product = products_response.json()[0]  # Compact Sanitair Unit
        
        # Update with placed product
        update_data = {
            "placed_products": [
                {"id": "placed-1", "product_id": product['id'], "x": 100, "y": 100, "rotation": 0, "quantity": 1}
            ]
        }
        requests.put(f"{BASE_URL}/api/projects/{project_id}", json=update_data)
        
        # Calculate quote
        response = requests.post(f"{BASE_URL}/api/quote/calculate?project_id={project_id}")
        assert response.status_code == 200
        quote = response.json()
        
        assert 'capex_total' in quote
        assert 'opex_monthly' in quote
        assert 'installation_total' in quote
        assert quote['capex_total'] == product['price_purchase']
        assert quote['opex_monthly'] == product['price_lease_monthly']
        print(f"✅ Quote calculated: CAPEX={quote['capex_total']}, OPEX/month={quote['opex_monthly']}")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/projects/{project_id}")


class TestAIRecommendationsAPI:
    """AI recommendations API tests"""
    
    def test_get_recommendations(self):
        """Test AI recommendations endpoint"""
        # Create project with products
        project_data = {
            "name": "TEST_AI Project",
            "project_type": "camping",
            "num_spots": 30,
            "placed_products": []
        }
        create_response = requests.post(f"{BASE_URL}/api/projects", json=project_data)
        project_id = create_response.json()['id']
        
        # Get recommendations
        response = requests.post(f"{BASE_URL}/api/ai/recommendations?project_id={project_id}")
        assert response.status_code == 200
        data = response.json()
        
        assert 'recommendations' in data
        assert isinstance(data['recommendations'], list)
        print(f"✅ Got {len(data['recommendations'])} AI recommendations")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/projects/{project_id}")


class TestPDFExportAPI:
    """PDF export API tests"""
    
    def test_generate_pdf(self):
        """Test PDF generation endpoint"""
        # Create project with products
        project_data = {
            "name": "TEST_PDF Project",
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
        
        assert 'html' in data
        assert 'RECRA' in data['html']
        assert 'Operational Lease' in data['html'], "PDF should contain 'Operational Lease' not 'OPEX'"
        print("✅ PDF generated with RECRA branding and Operational Lease")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/projects/{project_id}")


class TestHealthAndRoot:
    """Basic health check tests"""
    
    def test_api_root(self):
        """Test API root endpoint"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert 'message' in data
        assert 'RECRA' in data['message']
        print("✅ API root returns RECRA branding")


# Cleanup test data after all tests
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
                    print(f"Cleaned up test project: {project['name']}")
    except:
        pass
