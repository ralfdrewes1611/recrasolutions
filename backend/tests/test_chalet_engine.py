"""
Test suite for Chalet & Stay Engine API endpoints - Iteration 17
Tests: 26 models, 4 suppliers (Kunert, Arcabo, BBS, Campsolutions), categorie/leverancier filters
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://recra-config.preview.emergentagent.com').rstrip('/')


class TestChaletModelsCount:
    """Tests for model counts - 26 total models"""
    
    def test_get_all_models_returns_26(self):
        """Should return exactly 26 chalet/glamping models"""
        response = requests.get(f"{BASE_URL}/api/chalet/models")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 26, f"Expected 26 models, got {len(data)}"
    
    def test_chalet_category_returns_17(self):
        """Categorie=chalet should return 17 models (Kunert 8 + Arcabo 6 + BBS 3)"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?categorie=chalet")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 17, f"Expected 17 chalet models, got {len(data)}"
        for model in data:
            assert model['categorie'] == 'chalet'
    
    def test_glamping_category_returns_9(self):
        """Categorie=glamping should return 9 Campsolutions models"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?categorie=glamping")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9, f"Expected 9 glamping models, got {len(data)}"
        for model in data:
            assert model['categorie'] == 'glamping'
            assert model['supplier_id'] == 'campsolutions'


class TestSupplierFilters:
    """Tests for supplier filtering - 4 suppliers"""
    
    def test_kunert_returns_8_models(self):
        """Kunert Group should have 8 chalet models"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?supplier_id=kunert")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 8, f"Expected 8 Kunert models, got {len(data)}"
        for model in data:
            assert model['supplier_id'] == 'kunert'
            assert model['supplier_name'] == 'Kunert Group'
    
    def test_arcabo_returns_6_models(self):
        """Arcabo should have 6 chalet models"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?supplier_id=arcabo")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 6, f"Expected 6 Arcabo models, got {len(data)}"
        for model in data:
            assert model['supplier_id'] == 'arcabo'
            assert model['supplier_name'] == 'Arcabo'
    
    def test_bbs_returns_3_models(self):
        """BBS Systeembouw should have 3 vakantiewoning models"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?supplier_id=bbs")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3, f"Expected 3 BBS models, got {len(data)}"
        for model in data:
            assert model['supplier_id'] == 'bbs'
            assert model['supplier_name'] == 'BBS Systeembouw'
    
    def test_campsolutions_returns_9_models(self):
        """Campsolutions should have 9 glamping models"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?supplier_id=campsolutions")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9, f"Expected 9 Campsolutions models, got {len(data)}"
        for model in data:
            assert model['supplier_id'] == 'campsolutions'
            assert model['supplier_name'] == 'Campsolutions'
            assert model['categorie'] == 'glamping'


class TestSuppliersEndpoint:
    """Tests for GET /api/chalet/suppliers endpoint"""
    
    def test_suppliers_returns_4(self):
        """Should return exactly 4 suppliers"""
        response = requests.get(f"{BASE_URL}/api/chalet/suppliers")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 4, f"Expected 4 suppliers, got {len(data)}"
    
    def test_suppliers_have_correct_names(self):
        """Should have Kunert, Arcabo, BBS, Campsolutions"""
        response = requests.get(f"{BASE_URL}/api/chalet/suppliers")
        assert response.status_code == 200
        data = response.json()
        
        supplier_names = [s['name'] for s in data]
        assert 'Kunert Group' in supplier_names
        assert 'Arcabo' in supplier_names
        assert 'BBS Systeembouw' in supplier_names
        assert 'Campsolutions' in supplier_names


class TestFiltersEndpoint:
    """Tests for GET /api/chalet/filters endpoint"""
    
    def test_filters_include_categorieen(self):
        """Should include categorieen filter with Alles/Chalets/Glamping"""
        response = requests.get(f"{BASE_URL}/api/chalet/filters")
        assert response.status_code == 200
        data = response.json()
        
        assert 'categorieen' in data
        cat_ids = [c['id'] for c in data['categorieen']]
        assert 'alles' in cat_ids
        assert 'chalet' in cat_ids
        assert 'glamping' in cat_ids
    
    def test_filters_include_4_suppliers(self):
        """Should include 4 suppliers in filters"""
        response = requests.get(f"{BASE_URL}/api/chalet/filters")
        assert response.status_code == 200
        data = response.json()
        
        assert 'suppliers' in data
        assert len(data['suppliers']) == 4


class TestBestemmingFilter:
    """Tests for bestemming filtering"""
    
    def test_filter_by_bestemming_pre_mantelzorg(self):
        """Filter by bestemming=pre-mantelzorg should return models supporting it"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?bestemming=pre-mantelzorg")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10, f"Expected 10 pre-mantelzorg models, got {len(data)}"
        
        for model in data:
            assert 'pre-mantelzorg' in model['bestemmingen']


class TestDakVormFilter:
    """Tests for dak_vorm filtering"""
    
    def test_filter_by_dak_vorm_zadeldak(self):
        """Filter by dak_vorm=zadeldak should return zadeldak models"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?dak_vorm=zadeldak")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 8, f"Expected 8 zadeldak models, got {len(data)}"
        
        for model in data:
            assert model['dak_vorm'] == 'zadeldak'


class TestSpecificModelPricing:
    """Tests for specific model pricing"""
    
    def test_kunert_plat_12_pricing(self):
        """Plat 12 (Kunert): €74.950 / €90.690 incl BTW / €1.349 lease"""
        response = requests.get(f"{BASE_URL}/api/chalet/models/kunert-plat-12")
        assert response.status_code == 200
        data = response.json()
        
        assert data['name'] == 'Plat 12'
        assert data['supplier_name'] == 'Kunert Group'
        assert data['basisprijs'] == 74950
        
        pricing = data['pricing']
        assert pricing['totaal_incl_btw'] == 90690
        assert pricing['lease_monthly'] == 1349
    
    def test_wood_lodge_junior_pricing(self):
        """Wood Lodge Junior (Campsolutions): €3.236 / €3.916 incl BTW / €58 lease"""
        response = requests.get(f"{BASE_URL}/api/chalet/models/camp-wood-lodge-jr")
        assert response.status_code == 200
        data = response.json()
        
        assert data['name'] == 'Wood Lodge Junior'
        assert data['supplier_name'] == 'Campsolutions'
        assert data['categorie'] == 'glamping'
        assert data['basisprijs'] == 3236
        
        pricing = data['pricing']
        assert pricing['totaal_incl_btw'] == 3916
        assert pricing['lease_monthly'] == 58


class TestModelStructure:
    """Tests for model data structure"""
    
    def test_models_have_required_fields(self):
        """Each model should have all required fields including categorie"""
        response = requests.get(f"{BASE_URL}/api/chalet/models")
        assert response.status_code == 200
        data = response.json()
        
        required_fields = ['id', 'name', 'supplier_id', 'supplier_name', 'categorie',
                          'oppervlakte_m2', 'model_vorm', 'dak_vorm', 'bestemmingen',
                          'slaapkamers', 'badkamers', 'max_personen', 'basisprijs',
                          'stijlen', 'pricing', 'images']
        
        for model in data:
            for field in required_fields:
                assert field in model, f"Model {model.get('name', 'unknown')} missing field: {field}"
    
    def test_glamping_models_have_tent_category(self):
        """All Campsolutions models should have categorie=glamping"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?supplier_id=campsolutions")
        assert response.status_code == 200
        data = response.json()
        
        for model in data:
            assert model['categorie'] == 'glamping'
    
    def test_chalet_models_have_chalet_category(self):
        """Kunert, Arcabo, BBS models should have categorie=chalet"""
        for supplier in ['kunert', 'arcabo', 'bbs']:
            response = requests.get(f"{BASE_URL}/api/chalet/models?supplier_id={supplier}")
            assert response.status_code == 200
            data = response.json()
            
            for model in data:
                assert model['categorie'] == 'chalet', f"{model['name']} should be chalet"


class TestBTWCalculation:
    """Tests for BTW (VAT) calculation"""
    
    def test_btw_21_percent(self):
        """BTW should be calculated as 21% of basisprijs"""
        response = requests.get(f"{BASE_URL}/api/chalet/models")
        assert response.status_code == 200
        data = response.json()
        
        for model in data[:5]:  # Test first 5 models
            pricing = model['pricing']
            expected_btw = round(pricing['basisprijs'] * 0.21)
            assert pricing['btw_bedrag'] == expected_btw, f"{model['name']} BTW mismatch"
            assert pricing['btw_percentage'] == 21


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
