"""
Test suite for Iteration 20: Location Intelligence + Ticra Wellness Products
Tests:
1. Location Intelligence API (12 Dutch provinces with land prices, regulations)
2. Ticra Wellness products in Recreatie flow (14 products)
3. Ticra Wellness upgrades in Chalet Samenstellen tab
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestLocationIntelligence:
    """Tests for Location Intelligence API - 12 Dutch provinces"""
    
    def test_get_all_provinces(self):
        """GET /api/location/provinces returns 12 Dutch provinces"""
        response = requests.get(f"{BASE_URL}/api/location/provinces")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 12, f"Expected 12 provinces, got {len(data)}"
        
        # Verify sorted by toerisme_score descending
        scores = [p['toerisme_score'] for p in data]
        assert scores == sorted(scores, reverse=True), "Provinces should be sorted by toerisme_score descending"
        
        # Verify each province has required fields
        for province in data:
            assert 'id' in province
            assert 'name' in province
            assert 'grondprijs_m2' in province
            assert 'indicatief' in province['grondprijs_m2']
            assert 'min' in province['grondprijs_m2']
            assert 'max' in province['grondprijs_m2']
            assert 'recreatie_potentie' in province
            assert 'toerisme_score' in province
            assert 'kenmerken' in province
        print(f"✓ All 12 provinces returned with correct structure")
    
    def test_province_names(self):
        """Verify all 12 Dutch provinces are present"""
        response = requests.get(f"{BASE_URL}/api/location/provinces")
        assert response.status_code == 200
        data = response.json()
        
        expected_provinces = [
            'Groningen', 'Friesland', 'Drenthe', 'Overijssel', 'Flevoland',
            'Gelderland', 'Utrecht', 'Noord-Holland', 'Zuid-Holland', 
            'Zeeland', 'Noord-Brabant', 'Limburg'
        ]
        actual_names = [p['name'] for p in data]
        
        for expected in expected_provinces:
            assert expected in actual_names, f"Province {expected} not found"
        print(f"✓ All 12 Dutch provinces present: {', '.join(actual_names)}")
    
    def test_province_detail_gelderland(self):
        """GET /api/location/provinces/gelderland returns detailed info"""
        response = requests.get(f"{BASE_URL}/api/location/provinces/gelderland")
        assert response.status_code == 200
        data = response.json()
        
        assert data['id'] == 'gelderland'
        assert data['name'] == 'Gelderland'
        assert 'grondprijs_m2' in data
        assert data['grondprijs_m2']['indicatief'] == 50
        assert data['recreatie_potentie'] == 'zeer hoog'
        assert data['toerisme_score'] == 8.5
        
        # Verify regelgeving structure
        assert 'regelgeving' in data
        assert 'bestemmingsplan' in data['regelgeving']
        assert 'max_bouwhoogte' in data['regelgeving']
        assert 'seizoen' in data['regelgeving']
        assert 'bijzonderheden' in data['regelgeving']
        
        # Verify kenmerken
        assert 'kenmerken' in data
        assert 'Veluwe' in data['kenmerken']
        print(f"✓ Gelderland detail: €{data['grondprijs_m2']['indicatief']}/m², score {data['toerisme_score']}")
    
    def test_province_detail_zeeland(self):
        """GET /api/location/provinces/zeeland returns highest recreation density"""
        response = requests.get(f"{BASE_URL}/api/location/provinces/zeeland")
        assert response.status_code == 200
        data = response.json()
        
        assert data['name'] == 'Zeeland'
        assert data['recreatie_potentie'] == 'zeer hoog'
        assert data['toerisme_score'] == 8.8  # Highest score
        assert 'Hoogste recreatiedichtheid' in data['kenmerken']
        print(f"✓ Zeeland: highest toerisme_score {data['toerisme_score']}")
    
    def test_province_not_found(self):
        """GET /api/location/provinces/invalid returns error"""
        response = requests.get(f"{BASE_URL}/api/location/provinces/invalid")
        assert response.status_code == 200  # API returns 200 with error object
        data = response.json()
        assert 'error' in data
        print(f"✓ Invalid province returns error: {data['error']}")
    
    def test_investering_calculator(self):
        """GET /api/location/investering-calculator calculates land costs"""
        params = {
            'province_id': 'gelderland',
            'oppervlakte_m2': 5000,
            'units': 10
        }
        response = requests.get(f"{BASE_URL}/api/location/investering-calculator", params=params)
        assert response.status_code == 200
        data = response.json()
        
        assert data['provincie'] == 'Gelderland'
        assert data['oppervlakte_m2'] == 5000
        assert data['units'] == 10
        
        # Verify grondkosten calculation (€50/m² indicatief for Gelderland)
        assert 'grondkosten' in data
        assert data['grondkosten']['indicatief'] == 50 * 5000  # €250,000
        
        # Verify kosten_per_unit
        assert 'kosten_per_unit' in data
        assert data['kosten_per_unit']['indicatief'] == 25000  # €250,000 / 10 units
        
        # Verify m2_per_unit
        assert data['m2_per_unit'] == 500  # 5000 / 10
        
        # Verify regelgeving included
        assert 'regelgeving' in data
        assert 'kenmerken' in data
        print(f"✓ Investment calculator: €{data['grondkosten']['indicatief']:,} for {data['oppervlakte_m2']}m² in {data['provincie']}")
    
    def test_grondprijs_vergelijking(self):
        """GET /api/location/grondprijs-vergelijking returns sorted comparison"""
        response = requests.get(f"{BASE_URL}/api/location/grondprijs-vergelijking")
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) == 12
        
        # Verify sorted by indicatief price ascending
        prices = [p['indicatief_m2'] for p in data]
        assert prices == sorted(prices), "Should be sorted by price ascending"
        
        # Groningen should be cheapest
        assert data[0]['name'] == 'Groningen'
        assert data[0]['indicatief_m2'] == 28
        
        # Noord-Holland should be most expensive
        assert data[-1]['name'] == 'Noord-Holland'
        assert data[-1]['indicatief_m2'] == 70
        print(f"✓ Price comparison: cheapest {data[0]['name']} (€{data[0]['indicatief_m2']}/m²), most expensive {data[-1]['name']} (€{data[-1]['indicatief_m2']}/m²)")


class TestTicraWellnessProducts:
    """Tests for Ticra Wellness products in Recreatie flow"""
    
    def test_wellness_category_in_recreatie_products(self):
        """GET /api/products?flow=recreatie includes wellness category"""
        response = requests.get(f"{BASE_URL}/api/products", params={'flow': 'recreatie'})
        assert response.status_code == 200
        data = response.json()
        
        categories = set(p['category'] for p in data)
        assert 'wellness' in categories, "Wellness category should be in recreatie flow"
        print(f"✓ Wellness category present in recreatie flow. Categories: {categories}")
    
    def test_wellness_products_count(self):
        """Verify 14 Ticra wellness products exist"""
        response = requests.get(f"{BASE_URL}/api/products", params={'flow': 'recreatie'})
        assert response.status_code == 200
        data = response.json()
        
        wellness_products = [p for p in data if p['category'] == 'wellness']
        assert len(wellness_products) == 14, f"Expected 14 wellness products, got {len(wellness_products)}"
        print(f"✓ Found {len(wellness_products)} wellness products")
    
    def test_wellness_products_have_ticra_supplier(self):
        """All wellness products should have supplier='Ticra Outdoor'"""
        response = requests.get(f"{BASE_URL}/api/products", params={'flow': 'recreatie'})
        assert response.status_code == 200
        data = response.json()
        
        wellness_products = [p for p in data if p['category'] == 'wellness']
        for product in wellness_products:
            assert product.get('supplier') == 'Ticra Outdoor', f"Product {product['name']} should have Ticra Outdoor supplier"
        print(f"✓ All {len(wellness_products)} wellness products have 'Ticra Outdoor' supplier")
    
    def test_wellness_products_have_images(self):
        """All wellness products should have images from ticraoutdoor.com"""
        response = requests.get(f"{BASE_URL}/api/products", params={'flow': 'recreatie'})
        assert response.status_code == 200
        data = response.json()
        
        wellness_products = [p for p in data if p['category'] == 'wellness']
        for product in wellness_products:
            assert 'image' in product and product['image'], f"Product {product['name']} should have image"
            assert 'ticraoutdoor.com' in product['image'], f"Product {product['name']} image should be from ticraoutdoor.com"
        print(f"✓ All wellness products have images from ticraoutdoor.com")
    
    def test_wellness_subcategories(self):
        """Verify wellness products have correct subcategories"""
        response = requests.get(f"{BASE_URL}/api/products", params={'flow': 'recreatie'})
        assert response.status_code == 200
        data = response.json()
        
        wellness_products = [p for p in data if p['category'] == 'wellness']
        subcategories = set(p.get('subcategory', '') for p in wellness_products)
        
        expected_subcategories = {'hottub', 'sauna', 'buitendouche'}
        assert expected_subcategories.issubset(subcategories), f"Expected subcategories {expected_subcategories}, got {subcategories}"
        
        # Count per subcategory
        hottubs = [p for p in wellness_products if p.get('subcategory') == 'hottub']
        saunas = [p for p in wellness_products if p.get('subcategory') == 'sauna']
        showers = [p for p in wellness_products if p.get('subcategory') == 'buitendouche']
        
        assert len(hottubs) == 5, f"Expected 5 hottubs, got {len(hottubs)}"
        assert len(saunas) == 5, f"Expected 5 saunas, got {len(saunas)}"
        assert len(showers) == 4, f"Expected 4 outdoor showers, got {len(showers)}"
        print(f"✓ Wellness subcategories: {len(hottubs)} hottubs, {len(saunas)} saunas, {len(showers)} outdoor showers")
    
    def test_wellness_price_ranges(self):
        """Verify wellness products have correct price ranges"""
        response = requests.get(f"{BASE_URL}/api/products", params={'flow': 'recreatie'})
        assert response.status_code == 200
        data = response.json()
        
        wellness_products = [p for p in data if p['category'] == 'wellness']
        
        # Hottubs: €2,995 - €8,995
        hottubs = [p for p in wellness_products if p.get('subcategory') == 'hottub']
        hottub_prices = [p['price_purchase'] for p in hottubs]
        assert min(hottub_prices) == 2995, f"Cheapest hottub should be €2,995"
        assert max(hottub_prices) == 8995, f"Most expensive hottub should be €8,995"
        
        # Saunas: €3,295 - €14,395
        saunas = [p for p in wellness_products if p.get('subcategory') == 'sauna']
        sauna_prices = [p['price_purchase'] for p in saunas]
        assert min(sauna_prices) == 3295, f"Cheapest sauna should be €3,295"
        assert max(sauna_prices) == 14395, f"Most expensive sauna should be €14,395"
        
        # Outdoor showers: €695 - €3,354
        showers = [p for p in wellness_products if p.get('subcategory') == 'buitendouche']
        shower_prices = [p['price_purchase'] for p in showers]
        assert min(shower_prices) == 695, f"Cheapest shower should be €695"
        assert max(shower_prices) == 3354, f"Most expensive shower should be €3,354"
        
        print(f"✓ Price ranges: Hottubs €{min(hottub_prices)}-€{max(hottub_prices)}, Saunas €{min(sauna_prices)}-€{max(sauna_prices)}, Showers €{min(shower_prices)}-€{max(shower_prices)}")


class TestTicraWellnessInChaletUpgrades:
    """Tests for Ticra Wellness upgrades in Chalet Samenstellen tab"""
    
    def test_chalet_upgrade_options_include_wellness(self):
        """GET /api/chalet/upgrade-options/chalet includes wellness category"""
        response = requests.get(f"{BASE_URL}/api/chalet/upgrade-options/chalet")
        assert response.status_code == 200
        data = response.json()
        
        assert 'wellness' in data, "Chalet upgrades should include wellness category"
        wellness_options = data['wellness']
        assert len(wellness_options) == 8, f"Expected 8 wellness options for chalet, got {len(wellness_options)}"
        print(f"✓ Chalet upgrades include wellness with {len(wellness_options)} options")
    
    def test_glamping_upgrade_options_include_wellness(self):
        """GET /api/chalet/upgrade-options/glamping includes wellness category"""
        response = requests.get(f"{BASE_URL}/api/chalet/upgrade-options/glamping")
        assert response.status_code == 200
        data = response.json()
        
        assert 'wellness' in data, "Glamping upgrades should include wellness category"
        wellness_options = data['wellness']
        assert len(wellness_options) == 7, f"Expected 7 wellness options for glamping, got {len(wellness_options)}"
        print(f"✓ Glamping upgrades include wellness with {len(wellness_options)} options")
    
    def test_wellness_upgrade_options_have_ticra_supplier(self):
        """Wellness upgrade options should have Ticra Outdoor supplier"""
        response = requests.get(f"{BASE_URL}/api/chalet/upgrade-options/chalet")
        assert response.status_code == 200
        data = response.json()
        
        wellness_options = data['wellness']
        # Skip the first "Geen Wellness" option
        ticra_options = [opt for opt in wellness_options if opt['price'] > 0]
        
        for opt in ticra_options:
            assert opt.get('supplier') == 'Ticra Outdoor', f"Option {opt['name']} should have Ticra Outdoor supplier"
        print(f"✓ All {len(ticra_options)} paid wellness options have 'Ticra Outdoor' supplier")
    
    def test_wellness_upgrade_options_have_images(self):
        """Wellness upgrade options should have images from ticraoutdoor.com"""
        response = requests.get(f"{BASE_URL}/api/chalet/upgrade-options/chalet")
        assert response.status_code == 200
        data = response.json()
        
        wellness_options = data['wellness']
        # Skip the first "Geen Wellness" option
        ticra_options = [opt for opt in wellness_options if opt['price'] > 0]
        
        for opt in ticra_options:
            assert 'image' in opt and opt['image'], f"Option {opt['name']} should have image"
            assert 'ticraoutdoor.com' in opt['image'], f"Option {opt['name']} image should be from ticraoutdoor.com"
        print(f"✓ All paid wellness options have images from ticraoutdoor.com")
    
    def test_wellness_upgrade_pricing_calculation(self):
        """Selecting wellness upgrade should update pricing correctly"""
        # First get a chalet model
        response = requests.get(f"{BASE_URL}/api/chalet/models", params={'categorie': 'chalet'})
        assert response.status_code == 200
        models = response.json()
        assert len(models) > 0
        model = models[0]
        
        # Calculate with wellness upgrade
        calc_response = requests.post(f"{BASE_URL}/api/chalet/calculate-with-upgrades", json={
            'model_id': model['id'],
            'upgrades': {
                'wellness': 'well-hottub-basis'  # €2,995 hottub
            }
        })
        assert calc_response.status_code == 200
        calc_data = calc_response.json()
        
        assert calc_data['pricing']['upgrades_total'] == 2995
        assert calc_data['pricing']['totaal_excl_btw'] == model['basisprijs'] + 2995
        print(f"✓ Wellness upgrade pricing: base €{model['basisprijs']:,} + wellness €2,995 = €{calc_data['pricing']['totaal_excl_btw']:,}")


class TestAllFlowsStillWork:
    """Verify all 4 flows still work after changes"""
    
    def test_recreatie_flow_products(self):
        """Recreatie flow returns products including wellness"""
        response = requests.get(f"{BASE_URL}/api/products", params={'flow': 'recreatie'})
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        categories = set(p['category'] for p in data)
        assert 'wellness' in categories
        print(f"✓ Recreatie flow: {len(data)} products, categories: {categories}")
    
    def test_chalet_flow_models(self):
        """Chalet flow returns models"""
        response = requests.get(f"{BASE_URL}/api/chalet/models")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        print(f"✓ Chalet flow: {len(data)} models")
    
    def test_fec_flow_products(self):
        """FEC flow returns products"""
        response = requests.get(f"{BASE_URL}/api/fec/products")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        print(f"✓ FEC flow: {len(data)} products")
    
    def test_dashboard_projects(self):
        """Dashboard can list projects"""
        response = requests.get(f"{BASE_URL}/api/projects")
        assert response.status_code == 200
        # May be empty list, that's OK
        print(f"✓ Dashboard: projects endpoint working")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
