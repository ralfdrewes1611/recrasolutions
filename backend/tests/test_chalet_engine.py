"""
Test suite for Chalet & Stay Engine API endpoints
Tests: models listing, filtering, pricing calculations, and filter options
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://recra-config.preview.emergentagent.com').rstrip('/')


class TestChaletModels:
    """Tests for GET /api/chalet/models endpoint"""
    
    def test_get_all_models_returns_10(self):
        """Should return exactly 10 chalet models"""
        response = requests.get(f"{BASE_URL}/api/chalet/models")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10, f"Expected 10 models, got {len(data)}"
    
    def test_models_have_required_fields(self):
        """Each model should have all required fields"""
        response = requests.get(f"{BASE_URL}/api/chalet/models")
        assert response.status_code == 200
        data = response.json()
        
        required_fields = ['id', 'name', 'supplier_id', 'supplier_name', 'oppervlakte_m2',
                          'model_vorm', 'dak_vorm', 'bestemmingen', 'slaapkamers', 'badkamers',
                          'max_personen', 'basisprijs', 'stijlen', 'pricing']
        
        for model in data:
            for field in required_fields:
                assert field in model, f"Model {model.get('name', 'unknown')} missing field: {field}"
    
    def test_models_have_pricing_structure(self):
        """Each model should have complete pricing structure"""
        response = requests.get(f"{BASE_URL}/api/chalet/models")
        assert response.status_code == 200
        data = response.json()
        
        pricing_fields = ['basisprijs', 'totaal_excl_btw', 'btw_percentage', 'btw_bedrag',
                         'totaal_incl_btw', 'lease_monthly', 'lease_months']
        
        for model in data:
            pricing = model.get('pricing', {})
            for field in pricing_fields:
                assert field in pricing, f"Model {model['name']} pricing missing: {field}"


class TestChaletFilters:
    """Tests for filtering chalet models"""
    
    def test_filter_by_bestemming_pre_mantelzorg(self):
        """Filter by bestemming=pre-mantelzorg should return fewer models"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?bestemming=pre-mantelzorg")
        assert response.status_code == 200
        data = response.json()
        assert len(data) < 10, "Pre-mantelzorg filter should return fewer than 10 models"
        assert len(data) == 5, f"Expected 5 pre-mantelzorg models, got {len(data)}"
        
        # Verify all returned models support pre-mantelzorg
        for model in data:
            assert 'pre-mantelzorg' in model['bestemmingen'], f"{model['name']} doesn't support pre-mantelzorg"
    
    def test_filter_by_dak_vorm_zadeldak(self):
        """Filter by dak_vorm=zadeldak should return only zadeldak models"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?dak_vorm=zadeldak")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3, f"Expected 3 zadeldak models, got {len(data)}"
        
        for model in data:
            assert model['dak_vorm'] == 'zadeldak', f"{model['name']} has dak_vorm {model['dak_vorm']}"
    
    def test_filter_by_model_vorm_l_vorm(self):
        """Filter by model_vorm=l-vorm should return only L-vorm models"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?model_vorm=l-vorm")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1, f"Expected 1 L-vorm model, got {len(data)}"
        assert data[0]['model_vorm'] == 'l-vorm'
        assert data[0]['name'] == 'L-Plat 16'
    
    def test_filter_by_area_range(self):
        """Filter by min_m2=50&max_m2=80 should return models in range"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?min_m2=50&max_m2=80")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5, f"Expected 5 models in 50-80 m² range, got {len(data)}"
        
        for model in data:
            assert 50 <= model['oppervlakte_m2'] <= 80, f"{model['name']} has {model['oppervlakte_m2']} m²"
    
    def test_combined_filters(self):
        """Test combining multiple filters"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?dak_vorm=platdak&model_vorm=rechthoek")
        assert response.status_code == 200
        data = response.json()
        
        for model in data:
            assert model['dak_vorm'] == 'platdak'
            assert model['model_vorm'] == 'rechthoek'


class TestChaletPricing:
    """Tests for specific model pricing"""
    
    def test_plat_12_pricing(self):
        """Plat 12 should have correct pricing: €74.950 basis, €90.690 incl BTW, €1.349 lease"""
        response = requests.get(f"{BASE_URL}/api/chalet/models/plat-12")
        assert response.status_code == 200
        data = response.json()
        
        assert data['name'] == 'Plat 12'
        assert data['basisprijs'] == 74950
        
        pricing = data['pricing']
        assert pricing['basisprijs'] == 74950
        assert pricing['totaal_incl_btw'] == 90690
        assert pricing['lease_monthly'] == 1349
        assert pricing['btw_percentage'] == 21
    
    def test_zadel_18_pricing(self):
        """Zadel 18 should have correct pricing: €128.700 basis, €155.727 incl BTW, €2.317 lease"""
        response = requests.get(f"{BASE_URL}/api/chalet/models/zadel-18")
        assert response.status_code == 200
        data = response.json()
        
        assert data['name'] == 'Zadel 18'
        assert data['basisprijs'] == 128700
        
        pricing = data['pricing']
        assert pricing['basisprijs'] == 128700
        assert pricing['totaal_incl_btw'] == 155727
        assert pricing['lease_monthly'] == 2317
    
    def test_btw_calculation(self):
        """BTW should be calculated as 21% of basisprijs"""
        response = requests.get(f"{BASE_URL}/api/chalet/models")
        assert response.status_code == 200
        data = response.json()
        
        for model in data:
            pricing = model['pricing']
            expected_btw = round(pricing['basisprijs'] * 0.21)
            assert pricing['btw_bedrag'] == expected_btw, f"{model['name']} BTW mismatch"
            assert pricing['totaal_incl_btw'] == pricing['basisprijs'] + pricing['btw_bedrag']


class TestChaletFilterOptions:
    """Tests for GET /api/chalet/filters endpoint"""
    
    def test_get_filters(self):
        """Should return all filter options"""
        response = requests.get(f"{BASE_URL}/api/chalet/filters")
        assert response.status_code == 200
        data = response.json()
        
        assert 'bestemmingen' in data
        assert 'model_vormen' in data
        assert 'dak_vormen' in data
        assert 'stijlen' in data
        assert 'oppervlakte_range' in data
        assert 'suppliers' in data
    
    def test_bestemmingen_options(self):
        """Should have recreatie and pre-mantelzorg options"""
        response = requests.get(f"{BASE_URL}/api/chalet/filters")
        assert response.status_code == 200
        data = response.json()
        
        bestemming_ids = [b['id'] for b in data['bestemmingen']]
        assert 'recreatie' in bestemming_ids
        assert 'pre-mantelzorg' in bestemming_ids
    
    def test_dak_vormen_options(self):
        """Should have all dak vorm options"""
        response = requests.get(f"{BASE_URL}/api/chalet/filters")
        assert response.status_code == 200
        data = response.json()
        
        dak_ids = [d['id'] for d in data['dak_vormen']]
        expected = ['alles', 'platdak', 'zadeldak', 'lessenaars', 'mansarde', 'schilddak']
        for dak in expected:
            assert dak in dak_ids, f"Missing dak vorm: {dak}"
    
    def test_suppliers(self):
        """Should have 2 suppliers: Kunert Group and Arcabo"""
        response = requests.get(f"{BASE_URL}/api/chalet/filters")
        assert response.status_code == 200
        data = response.json()
        
        assert len(data['suppliers']) == 2
        supplier_names = [s['name'] for s in data['suppliers']]
        assert 'Kunert Group' in supplier_names
        assert 'Arcabo' in supplier_names


class TestChaletModelDetails:
    """Tests for GET /api/chalet/models/{model_id} endpoint"""
    
    def test_get_model_by_id(self):
        """Should return single model with full details"""
        response = requests.get(f"{BASE_URL}/api/chalet/models/plat-12")
        assert response.status_code == 200
        data = response.json()
        
        assert data['id'] == 'plat-12'
        assert data['name'] == 'Plat 12'
        assert data['supplier_name'] == 'Kunert Group'
    
    def test_get_nonexistent_model(self):
        """Should return error for nonexistent model"""
        response = requests.get(f"{BASE_URL}/api/chalet/models/nonexistent-model")
        assert response.status_code == 200  # API returns 200 with error object
        data = response.json()
        assert 'error' in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
