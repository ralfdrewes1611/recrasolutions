"""
Test iteration 9: Verify new UniFi and Nice M5BAR products
- Nice M5BAR slagboom products
- UniFi Protect cameras (G5 Bullet, G5 Dome Ultra, G5 Pro, G5 Turret Ultra, AI LPR)
- UniFi Access products (Hub, Lite, Pro, Starter Kit)
- Verify old products removed (Muntautomaat, IP Camera Basis, PTZ Camera Pro, ANPR Camera, RFID Lezer, Mobile Key Systeem)
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestProductCount:
    """Test total product count"""
    
    def test_total_products_count(self):
        """GET /api/products should return 25 products total"""
        response = requests.get(f"{BASE_URL}/api/products")
        assert response.status_code == 200
        products = response.json()
        assert len(products) == 25, f"Expected 25 products, got {len(products)}"


class TestNiceM5BARProducts:
    """Test Nice M5BAR slagboom products"""
    
    def test_nice_m5bar_exists(self):
        """Nice M5BAR should exist in slagboom category with price 3079"""
        response = requests.get(f"{BASE_URL}/api/products/category/slagboom")
        assert response.status_code == 200
        products = response.json()
        
        m5bar = next((p for p in products if p['name'] == 'Nice M5BAR'), None)
        assert m5bar is not None, "Nice M5BAR not found"
        assert m5bar['category'] == 'slagboom'
        assert m5bar['price_purchase'] == 3079, f"Expected price 3079, got {m5bar['price_purchase']}"
    
    def test_nice_m5bar_kentekenherkenning_exists(self):
        """Nice M5BAR + Kentekenherkenning should exist with price 3628"""
        response = requests.get(f"{BASE_URL}/api/products/category/slagboom")
        assert response.status_code == 200
        products = response.json()
        
        m5bar_lpr = next((p for p in products if 'Kentekenherkenning' in p['name']), None)
        assert m5bar_lpr is not None, "Nice M5BAR + Kentekenherkenning not found"
        assert m5bar_lpr['price_purchase'] == 3628, f"Expected price 3628, got {m5bar_lpr['price_purchase']}"


class TestUniFiCameras:
    """Test UniFi Protect camera products"""
    
    def test_unifi_g5_bullet_exists(self):
        """UniFi G5 Bullet should exist in camera category with price 139"""
        response = requests.get(f"{BASE_URL}/api/products/category/camera")
        assert response.status_code == 200
        products = response.json()
        
        g5_bullet = next((p for p in products if p['name'] == 'UniFi G5 Bullet'), None)
        assert g5_bullet is not None, "UniFi G5 Bullet not found"
        assert g5_bullet['category'] == 'camera'
        assert g5_bullet['price_purchase'] == 139, f"Expected price 139, got {g5_bullet['price_purchase']}"
    
    def test_unifi_g5_dome_ultra_exists(self):
        """UniFi G5 Dome Ultra should exist in camera category"""
        response = requests.get(f"{BASE_URL}/api/products/category/camera")
        assert response.status_code == 200
        products = response.json()
        
        g5_dome = next((p for p in products if p['name'] == 'UniFi G5 Dome Ultra'), None)
        assert g5_dome is not None, "UniFi G5 Dome Ultra not found"
        assert g5_dome['category'] == 'camera'
        assert g5_dome['price_purchase'] == 139
    
    def test_unifi_g5_pro_exists(self):
        """UniFi G5 Pro should exist in camera category with price 399"""
        response = requests.get(f"{BASE_URL}/api/products/category/camera")
        assert response.status_code == 200
        products = response.json()
        
        g5_pro = next((p for p in products if p['name'] == 'UniFi G5 Pro'), None)
        assert g5_pro is not None, "UniFi G5 Pro not found"
        assert g5_pro['category'] == 'camera'
        assert g5_pro['price_purchase'] == 399, f"Expected price 399, got {g5_pro['price_purchase']}"
    
    def test_unifi_g5_turret_ultra_exists(self):
        """UniFi G5 Turret Ultra should exist in camera category"""
        response = requests.get(f"{BASE_URL}/api/products/category/camera")
        assert response.status_code == 200
        products = response.json()
        
        g5_turret = next((p for p in products if p['name'] == 'UniFi G5 Turret Ultra'), None)
        assert g5_turret is not None, "UniFi G5 Turret Ultra not found"
        assert g5_turret['category'] == 'camera'
    
    def test_unifi_ai_lpr_camera_exists(self):
        """UniFi AI LPR Camera should exist in camera category with price 549"""
        response = requests.get(f"{BASE_URL}/api/products/category/camera")
        assert response.status_code == 200
        products = response.json()
        
        ai_lpr = next((p for p in products if p['name'] == 'UniFi AI LPR Camera'), None)
        assert ai_lpr is not None, "UniFi AI LPR Camera not found"
        assert ai_lpr['category'] == 'camera'
        assert ai_lpr['price_purchase'] == 549, f"Expected price 549, got {ai_lpr['price_purchase']}"
    
    def test_camera_category_has_5_products(self):
        """Camera category should have exactly 5 UniFi cameras"""
        response = requests.get(f"{BASE_URL}/api/products/category/camera")
        assert response.status_code == 200
        products = response.json()
        assert len(products) == 5, f"Expected 5 cameras, got {len(products)}"


class TestUniFiAccessProducts:
    """Test UniFi Access toegangscontrole products"""
    
    def test_unifi_access_hub_exists(self):
        """UniFi Access Hub should exist in toegangscontrole category with price 219"""
        response = requests.get(f"{BASE_URL}/api/products/category/toegangscontrole")
        assert response.status_code == 200
        products = response.json()
        
        hub = next((p for p in products if p['name'] == 'UniFi Access Hub'), None)
        assert hub is not None, "UniFi Access Hub not found"
        assert hub['category'] == 'toegangscontrole'
        assert hub['price_purchase'] == 219, f"Expected price 219, got {hub['price_purchase']}"
    
    def test_unifi_access_reader_lite_exists(self):
        """UniFi Access Reader Lite (UA-Lite) should exist"""
        response = requests.get(f"{BASE_URL}/api/products/category/toegangscontrole")
        assert response.status_code == 200
        products = response.json()
        
        ua_lite = next((p for p in products if 'UA-Lite' in p['name']), None)
        assert ua_lite is not None, "UniFi Access Reader Lite (UA-Lite) not found"
        assert ua_lite['category'] == 'toegangscontrole'
    
    def test_unifi_access_reader_pro_exists(self):
        """UniFi Access Reader Pro (UA-Pro) should exist with price 329"""
        response = requests.get(f"{BASE_URL}/api/products/category/toegangscontrole")
        assert response.status_code == 200
        products = response.json()
        
        ua_pro = next((p for p in products if 'UA-Pro' in p['name']), None)
        assert ua_pro is not None, "UniFi Access Reader Pro (UA-Pro) not found"
        assert ua_pro['price_purchase'] == 329, f"Expected price 329, got {ua_pro['price_purchase']}"
    
    def test_unifi_access_starter_kit_exists(self):
        """UniFi Access Starter Kit should exist with price 599"""
        response = requests.get(f"{BASE_URL}/api/products/category/toegangscontrole")
        assert response.status_code == 200
        products = response.json()
        
        starter_kit = next((p for p in products if p['name'] == 'UniFi Access Starter Kit'), None)
        assert starter_kit is not None, "UniFi Access Starter Kit not found"
        assert starter_kit['price_purchase'] == 599, f"Expected price 599, got {starter_kit['price_purchase']}"
    
    def test_toegangscontrole_category_has_4_products(self):
        """Toegangscontrole category should have exactly 4 UniFi Access products"""
        response = requests.get(f"{BASE_URL}/api/products/category/toegangscontrole")
        assert response.status_code == 200
        products = response.json()
        assert len(products) == 4, f"Expected 4 toegangscontrole products, got {len(products)}"


class TestRemovedProducts:
    """Test that old/banned products have been removed"""
    
    def test_no_muntautomaat(self):
        """No product named 'Muntautomaat' should exist"""
        response = requests.get(f"{BASE_URL}/api/products")
        assert response.status_code == 200
        products = response.json()
        
        muntautomaat = [p for p in products if 'Muntautomaat' in p['name']]
        assert len(muntautomaat) == 0, f"Found Muntautomaat products: {[p['name'] for p in muntautomaat]}"
    
    def test_no_old_cameras(self):
        """No old camera products (IP Camera Basis, PTZ Camera Pro, ANPR Camera) should exist"""
        response = requests.get(f"{BASE_URL}/api/products")
        assert response.status_code == 200
        products = response.json()
        
        old_cameras = ['IP Camera Basis', 'PTZ Camera Pro', 'ANPR Camera']
        found = [p['name'] for p in products if p['name'] in old_cameras]
        assert len(found) == 0, f"Found old camera products: {found}"
    
    def test_no_old_access_control(self):
        """No old access control products (RFID Lezer, Mobile Key Systeem) should exist"""
        response = requests.get(f"{BASE_URL}/api/products")
        assert response.status_code == 200
        products = response.json()
        
        old_access = ['RFID Lezer', 'Mobile Key Systeem']
        found = [p['name'] for p in products if p['name'] in old_access]
        assert len(found) == 0, f"Found old access control products: {found}"


class TestCategoryFilter:
    """Test category filtering endpoint"""
    
    def test_filter_by_camera_category(self):
        """Filtering by 'camera' should return only UniFi cameras"""
        response = requests.get(f"{BASE_URL}/api/products/category/camera")
        assert response.status_code == 200
        products = response.json()
        
        # All should be camera category
        for p in products:
            assert p['category'] == 'camera', f"Product {p['name']} has wrong category: {p['category']}"
        
        # All should be UniFi cameras
        for p in products:
            assert 'UniFi' in p['name'], f"Non-UniFi camera found: {p['name']}"
    
    def test_filter_by_slagboom_category(self):
        """Filtering by 'slagboom' should return Nice M5BAR products"""
        response = requests.get(f"{BASE_URL}/api/products/category/slagboom")
        assert response.status_code == 200
        products = response.json()
        
        # Should have 3 slagboom products
        assert len(products) == 3, f"Expected 3 slagboom products, got {len(products)}"
        
        # All should be slagboom category
        for p in products:
            assert p['category'] == 'slagboom'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
