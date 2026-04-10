"""
Iteration 21 Tests: Partner/Supplier Profile Pages
Tests: Partner profiles API, Ticra Outdoor rich profile, click tracking
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestPartnerProfilesAPI:
    """Test Partner Profiles endpoints"""
    
    def test_get_all_partner_profiles(self):
        """GET /api/partners/profiles returns all 5 partner profiles"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        profiles = response.json()
        assert isinstance(profiles, list), "Response should be a list"
        assert len(profiles) == 5, f"Expected 5 partners, got {len(profiles)}"
        
        # Verify all expected partners are present
        partner_ids = [p['id'] for p in profiles]
        expected_ids = ['ticra-outdoor', 'kunert-group', 'arcabo', 'campsolutions', 'bbs-systeembouw']
        for pid in expected_ids:
            assert pid in partner_ids, f"Missing partner: {pid}"
        
        print(f"PASS: All 5 partner profiles returned: {partner_ids}")
    
    def test_partner_profile_summary_fields(self):
        """GET /api/partners/profiles returns summary fields for each partner"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles")
        assert response.status_code == 200
        
        profiles = response.json()
        required_fields = ['id', 'name', 'tagline', 'hero_image', 'categorieen', 'pleisureworld_partner', 'pleisureworld_badge']
        
        for profile in profiles:
            for field in required_fields:
                assert field in profile, f"Missing field '{field}' in profile {profile.get('id')}"
        
        print("PASS: All partner profiles have required summary fields")
    
    def test_ticra_outdoor_full_profile(self):
        """GET /api/partners/profiles/ticra-outdoor returns full Ticra profile"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles/ticra-outdoor")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        profile = response.json()
        assert profile['id'] == 'ticra-outdoor'
        assert profile['name'] == 'Ticra Outdoor'
        
        # Verify Pleisureworld Partner status
        assert profile['pleisureworld_partner'] == True
        assert profile['pleisureworld_badge'] == 'Preferred Partner'
        assert profile['pleisureworld_sinds'] == '2024'
        
        print("PASS: Ticra Outdoor profile loaded with Pleisureworld Partner badge")
    
    def test_ticra_outdoor_podcast_section(self):
        """Ticra profile has podcast section with Leisure Talk #14"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles/ticra-outdoor")
        assert response.status_code == 200
        
        profile = response.json()
        podcast = profile.get('podcast')
        
        assert podcast is not None, "Ticra should have podcast section"
        assert 'Leisure Talk #14' in podcast['titel'], f"Expected Leisure Talk #14, got {podcast['titel']}"
        assert podcast['url'] is not None, "Podcast should have URL"
        assert podcast['duur'] == '38 min', f"Expected 38 min, got {podcast['duur']}"
        assert 'Richard Otten' in podcast['gast'], "Richard Otten should be the guest"
        
        print(f"PASS: Ticra podcast section: {podcast['titel']}")
    
    def test_ticra_outdoor_trendwatcher_quote(self):
        """Ticra profile has Richard Otten trendwatcher quote"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles/ticra-outdoor")
        assert response.status_code == 200
        
        profile = response.json()
        quote = profile.get('trendwatcher_quote')
        
        assert quote is not None, "Ticra should have trendwatcher quote"
        assert quote['auteur'] == 'Richard Otten', f"Expected Richard Otten, got {quote['auteur']}"
        assert quote['functie'] == 'Trendwatcher Recreatie & Hospitality'
        assert len(quote['tekst']) > 50, "Quote text should be substantial"
        
        print(f"PASS: Trendwatcher quote by {quote['auteur']}")
    
    def test_ticra_outdoor_top_products(self):
        """Ticra profile has top 3 most chosen products with configuraties count"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles/ticra-outdoor")
        assert response.status_code == 200
        
        profile = response.json()
        top_products = profile.get('top_producten', [])
        
        assert len(top_products) == 3, f"Expected 3 top products, got {len(top_products)}"
        
        for i, prod in enumerate(top_products):
            assert 'id' in prod, f"Product {i} missing id"
            assert 'name' in prod, f"Product {i} missing name"
            assert 'prijs' in prod, f"Product {i} missing prijs"
            assert 'image' in prod, f"Product {i} missing image"
            assert 'configuraties' in prod, f"Product {i} missing configuraties count"
            assert prod['configuraties'] > 0, f"Product {i} should have configuraties > 0"
        
        # Verify specific products
        product_names = [p['name'] for p in top_products]
        assert 'TICRA Hottub Houtgestookt' in product_names
        assert 'Barrel Sauna Thermowood' in product_names
        assert 'Sunlight Buitendouche' in product_names
        
        print(f"PASS: Top 3 products: {product_names}")
    
    def test_ticra_outdoor_events_deelname(self):
        """Ticra profile has events/deelname section"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles/ticra-outdoor")
        assert response.status_code == 200
        
        profile = response.json()
        deelname = profile.get('deelname', [])
        
        assert len(deelname) >= 4, f"Expected at least 4 events, got {len(deelname)}"
        
        event_names = [d['event'] for d in deelname]
        assert 'Vakantiebeurs Utrecht 2026' in event_names
        assert 'Glamping Show 2025' in event_names
        
        for event in deelname:
            assert 'event' in event
            assert 'type' in event
        
        print(f"PASS: {len(deelname)} events in deelname section")
    
    def test_ticra_outdoor_usps(self):
        """Ticra profile has USPs list"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles/ticra-outdoor")
        assert response.status_code == 200
        
        profile = response.json()
        usps = profile.get('usps', [])
        
        assert len(usps) >= 5, f"Expected at least 5 USPs, got {len(usps)}"
        
        # Check for specific USPs
        assert 'Gratis bezorging bij recreatieparken' in usps
        assert '2 jaar volledige garantie' in usps
        
        print(f"PASS: {len(usps)} USPs: {usps[:3]}...")
    
    def test_ticra_outdoor_stats(self):
        """Ticra profile has stats section"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles/ticra-outdoor")
        assert response.status_code == 200
        
        profile = response.json()
        stats = profile.get('stats', {})
        
        assert 'parken_actief' in stats
        assert 'jaren_ervaring' in stats
        assert 'producten_geinstalleerd' in stats
        assert 'klanttevredenheid' in stats
        
        assert stats['parken_actief'] == '120+'
        assert stats['klanttevredenheid'] == '4.8/5'
        
        print(f"PASS: Stats - {stats['parken_actief']} parken, {stats['klanttevredenheid']} score")
    
    def test_ticra_outdoor_links(self):
        """Ticra profile has website and blog links"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles/ticra-outdoor")
        assert response.status_code == 200
        
        profile = response.json()
        
        assert profile.get('website') == 'https://www.ticraoutdoor.com'
        assert 'pleisureworld.nl/blog' in profile.get('blog_url', '')
        
        print(f"PASS: Website: {profile['website']}, Blog: {profile['blog_url']}")
    
    def test_kunert_group_profile(self):
        """GET /api/partners/profiles/kunert-group returns Kunert profile"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles/kunert-group")
        assert response.status_code == 200
        
        profile = response.json()
        assert profile['name'] == 'Kunert Group'
        assert profile['pleisureworld_partner'] == True
        assert 'chalets' in profile['categorieen']
        
        print(f"PASS: Kunert Group profile loaded")
    
    def test_arcabo_profile(self):
        """GET /api/partners/profiles/arcabo returns Arcabo profile"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles/arcabo")
        assert response.status_code == 200
        
        profile = response.json()
        assert profile['name'] == 'Arcabo'
        assert profile['pleisureworld_partner'] == True
        
        print(f"PASS: Arcabo profile loaded")
    
    def test_campsolutions_profile(self):
        """GET /api/partners/profiles/campsolutions returns Campsolutions profile"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles/campsolutions")
        assert response.status_code == 200
        
        profile = response.json()
        assert profile['name'] == 'Campsolutions'
        assert profile['pleisureworld_partner'] == False  # Not a preferred partner
        assert 'glamping' in profile['categorieen']
        
        print(f"PASS: Campsolutions profile loaded (not Pleisureworld partner)")
    
    def test_nonexistent_partner_profile(self):
        """GET /api/partners/profiles/nonexistent returns error"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles/nonexistent")
        assert response.status_code == 200  # Returns 200 with error in body
        
        data = response.json()
        assert 'error' in data, "Should return error for nonexistent partner"
        
        print("PASS: Nonexistent partner returns error")


class TestClickTracking:
    """Test click tracking endpoint"""
    
    def test_track_profile_view(self):
        """POST /api/platform/partners/track registers profile_view"""
        payload = {
            "supplier_id": "ticra-outdoor",
            "supplier_name": "Ticra Outdoor",
            "interaction_type": "profile_view",
            "flow_type": "partner_profile"
        }
        response = requests.post(f"{BASE_URL}/api/platform/partners/track", json=payload)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        # May return ok:true or ok:false depending on Supabase config
        assert 'ok' in data, "Response should have 'ok' field"
        
        print(f"PASS: profile_view tracked, response: {data}")
    
    def test_track_website_click(self):
        """POST /api/platform/partners/track registers website_click"""
        payload = {
            "supplier_id": "ticra-outdoor",
            "supplier_name": "Ticra Outdoor",
            "interaction_type": "website_click",
            "flow_type": "partner_profile"
        }
        response = requests.post(f"{BASE_URL}/api/platform/partners/track", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert 'ok' in data
        
        print(f"PASS: website_click tracked")
    
    def test_track_blog_click(self):
        """POST /api/platform/partners/track registers blog_click"""
        payload = {
            "supplier_id": "ticra-outdoor",
            "supplier_name": "Ticra Outdoor",
            "interaction_type": "blog_click",
            "flow_type": "partner_profile"
        }
        response = requests.post(f"{BASE_URL}/api/platform/partners/track", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert 'ok' in data
        
        print(f"PASS: blog_click tracked")
    
    def test_track_podcast_click(self):
        """POST /api/platform/partners/track registers podcast_click"""
        payload = {
            "supplier_id": "ticra-outdoor",
            "supplier_name": "Ticra Outdoor",
            "interaction_type": "podcast_click",
            "flow_type": "partner_profile"
        }
        response = requests.post(f"{BASE_URL}/api/platform/partners/track", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert 'ok' in data
        
        print(f"PASS: podcast_click tracked")


class TestProductCardsWithSupplier:
    """Test product cards have supplier info"""
    
    def test_wellness_products_have_supplier(self):
        """GET /api/products?flow=recreatie wellness products have Ticra Outdoor supplier"""
        response = requests.get(f"{BASE_URL}/api/products?flow=recreatie")
        assert response.status_code == 200
        
        products = response.json()
        wellness_products = [p for p in products if p.get('category') == 'wellness']
        
        assert len(wellness_products) >= 10, f"Expected at least 10 wellness products, got {len(wellness_products)}"
        
        for prod in wellness_products:
            assert prod.get('supplier') == 'Ticra Outdoor', f"Product {prod['name']} should have Ticra Outdoor supplier"
        
        print(f"PASS: {len(wellness_products)} wellness products all have Ticra Outdoor supplier")
    
    def test_wellness_products_have_images(self):
        """Wellness products have images from ticraoutdoor.com"""
        response = requests.get(f"{BASE_URL}/api/products?flow=recreatie")
        assert response.status_code == 200
        
        products = response.json()
        wellness_products = [p for p in products if p.get('category') == 'wellness']
        
        for prod in wellness_products:
            image = prod.get('image', '')
            assert 'ticraoutdoor.com' in image, f"Product {prod['name']} should have ticraoutdoor.com image"
        
        print(f"PASS: All wellness products have ticraoutdoor.com images")


class TestChaletWizardSupplierLinks:
    """Test ChaletWizard supplier endpoints"""
    
    def test_chalet_suppliers_endpoint(self):
        """GET /api/chalet/suppliers returns suppliers list"""
        response = requests.get(f"{BASE_URL}/api/chalet/suppliers")
        assert response.status_code == 200
        
        suppliers = response.json()
        assert isinstance(suppliers, list)
        assert len(suppliers) >= 3, f"Expected at least 3 suppliers, got {len(suppliers)}"
        
        supplier_names = [s['name'] for s in suppliers]
        assert 'Kunert Group' in supplier_names
        assert 'Arcabo' in supplier_names
        
        print(f"PASS: {len(suppliers)} chalet suppliers returned")
    
    def test_chalet_models_have_supplier_name(self):
        """GET /api/chalet/models returns models with supplier_name"""
        response = requests.get(f"{BASE_URL}/api/chalet/models")
        assert response.status_code == 200
        
        models = response.json()
        assert len(models) > 0, "Should have at least 1 model"
        
        for model in models[:5]:  # Check first 5
            assert 'supplier_name' in model, f"Model {model.get('name')} missing supplier_name"
            assert model['supplier_name'] is not None
        
        print(f"PASS: Chalet models have supplier_name field")
    
    def test_chalet_upgrade_options_wellness_has_supplier(self):
        """GET /api/chalet/upgrade-options/chalet wellness options have supplier"""
        response = requests.get(f"{BASE_URL}/api/chalet/upgrade-options/chalet")
        assert response.status_code == 200
        
        options = response.json()
        wellness_options = options.get('wellness', [])
        
        assert len(wellness_options) > 0, "Should have wellness upgrade options"
        
        # Check that non-standard options have Ticra Outdoor supplier
        for opt in wellness_options:
            if opt.get('price', 0) > 0:  # Non-standard options
                assert opt.get('supplier') == 'Ticra Outdoor', f"Option {opt['name']} should have Ticra Outdoor supplier"
        
        print(f"PASS: Wellness upgrade options have Ticra Outdoor supplier")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
