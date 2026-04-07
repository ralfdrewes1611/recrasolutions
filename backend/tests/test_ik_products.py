"""
Test IK Display Solutions Products - Iteration 15
Tests for newly added IK products in Recra database (informatiezuil category)
and IK indoor kiosks in FEC database (entree category).
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestIKProductsRecra:
    """Tests for IK products in Recreatie/Chalet/FEC flows (informatiezuil category)"""
    
    def test_recreatie_flow_product_count(self):
        """GET /api/products?flow=recreatie should return 35 products"""
        response = requests.get(f"{BASE_URL}/api/products?flow=recreatie")
        assert response.status_code == 200
        products = response.json()
        print(f"Recreatie flow product count: {len(products)}")
        # Should have 35 products total
        assert len(products) >= 35, f"Expected at least 35 products, got {len(products)}"
    
    def test_recreatie_flow_has_informatiezuil_category(self):
        """GET /api/products?flow=recreatie should include informatiezuil products"""
        response = requests.get(f"{BASE_URL}/api/products?flow=recreatie")
        assert response.status_code == 200
        products = response.json()
        
        informatiezuil_products = [p for p in products if p.get('category') == 'informatiezuil']
        print(f"Informatiezuil products in recreatie: {len(informatiezuil_products)}")
        for p in informatiezuil_products:
            print(f"  - {p['name']}: €{p['price_purchase']}")
        
        # Should have 8 IK products with category informatiezuil
        assert len(informatiezuil_products) == 8, f"Expected 8 informatiezuil products, got {len(informatiezuil_products)}"
    
    def test_chalet_flow_has_informatiezuil_products(self):
        """GET /api/products?flow=chalet should include IK informatiezuil products"""
        response = requests.get(f"{BASE_URL}/api/products?flow=chalet")
        assert response.status_code == 200
        products = response.json()
        
        informatiezuil_products = [p for p in products if p.get('category') == 'informatiezuil']
        print(f"Informatiezuil products in chalet: {len(informatiezuil_products)}")
        
        # Chalet flow should also include informatiezuil
        assert len(informatiezuil_products) == 8, f"Expected 8 informatiezuil products in chalet, got {len(informatiezuil_products)}"
    
    def test_fec_flow_has_informatiezuil_products(self):
        """GET /api/products?flow=fec should include IK informatiezuil products"""
        response = requests.get(f"{BASE_URL}/api/products?flow=fec")
        assert response.status_code == 200
        products = response.json()
        
        informatiezuil_products = [p for p in products if p.get('category') == 'informatiezuil']
        print(f"Informatiezuil products in fec: {len(informatiezuil_products)}")
        
        # FEC flow should also include informatiezuil
        assert len(informatiezuil_products) == 8, f"Expected 8 informatiezuil products in fec, got {len(informatiezuil_products)}"
    
    def test_ik_outdoor_portrait_kiosk_price(self):
        """IK 21.5 Outdoor Portrait Kiosk should cost €4800"""
        response = requests.get(f"{BASE_URL}/api/products?flow=recreatie")
        assert response.status_code == 200
        products = response.json()
        
        kiosk = next((p for p in products if 'IK 21.5" Outdoor Portrait Kiosk' in p.get('name', '')), None)
        assert kiosk is not None, "IK 21.5\" Outdoor Portrait Kiosk not found"
        assert kiosk['price_purchase'] == 4800, f"Expected €4800, got €{kiosk['price_purchase']}"
        print(f"IK 21.5\" Outdoor Portrait Kiosk price: €{kiosk['price_purchase']} ✓")
    
    def test_ik_55_outdoor_landscape_kiosk_price(self):
        """IK 55 Outdoor Landscape Kiosk should cost €5250"""
        response = requests.get(f"{BASE_URL}/api/products?flow=recreatie")
        assert response.status_code == 200
        products = response.json()
        
        kiosk = next((p for p in products if 'IK 55" Outdoor Landscape Kiosk' in p.get('name', '')), None)
        assert kiosk is not None, "IK 55\" Outdoor Landscape Kiosk not found"
        assert kiosk['price_purchase'] == 5250, f"Expected €5250, got €{kiosk['price_purchase']}"
        print(f"IK 55\" Outdoor Landscape Kiosk price: €{kiosk['price_purchase']} ✓")
    
    def test_all_ik_products_have_correct_category(self):
        """All IK products should have category 'informatiezuil'"""
        response = requests.get(f"{BASE_URL}/api/products?flow=recreatie")
        assert response.status_code == 200
        products = response.json()
        
        ik_products = [p for p in products if p.get('name', '').startswith('IK ')]
        print(f"Found {len(ik_products)} IK products")
        
        for p in ik_products:
            assert p['category'] == 'informatiezuil', f"IK product '{p['name']}' has category '{p['category']}' instead of 'informatiezuil'"
            print(f"  - {p['name']}: category={p['category']} ✓")


class TestIKProductsFEC:
    """Tests for IK indoor kiosks in FEC database (entree category)"""
    
    def test_fec_products_count(self):
        """GET /api/fec/products should return 17 products"""
        response = requests.get(f"{BASE_URL}/api/fec/products")
        assert response.status_code == 200
        products = response.json()
        print(f"FEC products count: {len(products)}")
        # Should have 17 products total
        assert len(products) == 17, f"Expected 17 FEC products, got {len(products)}"
    
    def test_fec_products_has_ik_indoor_kiosks(self):
        """GET /api/fec/products should include 3 IK indoor kiosks with category 'entree'"""
        response = requests.get(f"{BASE_URL}/api/fec/products")
        assert response.status_code == 200
        products = response.json()
        
        ik_entree_products = [p for p in products if p.get('category') == 'entree' and 'IK' in p.get('name', '')]
        print(f"IK entree products in FEC: {len(ik_entree_products)}")
        for p in ik_entree_products:
            print(f"  - {p['name']}: €{p['price_purchase']}/purchase, €{p['price_lease_monthly']}/mnd lease")
        
        # Should have 3 IK indoor kiosks
        assert len(ik_entree_products) == 3, f"Expected 3 IK indoor kiosks in FEC, got {len(ik_entree_products)}"
    
    def test_fec_suppliers_count(self):
        """GET /api/fec/suppliers should return 6 suppliers"""
        response = requests.get(f"{BASE_URL}/api/fec/suppliers")
        assert response.status_code == 200
        suppliers = response.json()
        print(f"FEC suppliers count: {len(suppliers)}")
        # Should have 6 suppliers
        assert len(suppliers) == 6, f"Expected 6 FEC suppliers, got {len(suppliers)}"
    
    def test_fec_suppliers_includes_ik_display(self):
        """GET /api/fec/suppliers should include 'IK Display Solutions'"""
        response = requests.get(f"{BASE_URL}/api/fec/suppliers")
        assert response.status_code == 200
        suppliers = response.json()
        
        ik_supplier = next((s for s in suppliers if 'IK Display Solutions' in s.get('name', '')), None)
        assert ik_supplier is not None, "IK Display Solutions not found in FEC suppliers"
        print(f"IK Display Solutions found: {ik_supplier['name']}")
        print(f"  - Address: {ik_supplier.get('address')}")
        print(f"  - Categories: {ik_supplier.get('categories')}")
        print(f"  - Specialization: {ik_supplier.get('specialization')}")
    
    def test_ik_21_indoor_lease_price(self):
        """IK 21.5 Indoor Portrait Kiosk should have lease price €105/mnd"""
        response = requests.get(f"{BASE_URL}/api/fec/products")
        assert response.status_code == 200
        products = response.json()
        
        kiosk = next((p for p in products if 'IK 21.5" Indoor Portrait Kiosk' in p.get('name', '')), None)
        assert kiosk is not None, "IK 21.5\" Indoor Portrait Kiosk not found in FEC"
        assert kiosk['price_lease_monthly'] == 105, f"Expected €105/mnd lease, got €{kiosk['price_lease_monthly']}"
        print(f"IK 21.5\" Indoor Portrait Kiosk lease: €{kiosk['price_lease_monthly']}/mnd ✓")
    
    def test_ik_43_indoor_lease_price(self):
        """IK 43 Indoor Landscape Kiosk should have lease price €75/mnd"""
        response = requests.get(f"{BASE_URL}/api/fec/products")
        assert response.status_code == 200
        products = response.json()
        
        kiosk = next((p for p in products if 'IK 43" Indoor Landscape Kiosk' in p.get('name', '')), None)
        assert kiosk is not None, "IK 43\" Indoor Landscape Kiosk not found in FEC"
        assert kiosk['price_lease_monthly'] == 75, f"Expected €75/mnd lease, got €{kiosk['price_lease_monthly']}"
        print(f"IK 43\" Indoor Landscape Kiosk lease: €{kiosk['price_lease_monthly']}/mnd ✓")
    
    def test_ik_fec_products_have_revenue_data(self):
        """IK FEC products should have revenue_per_hour and capacity_per_hour"""
        response = requests.get(f"{BASE_URL}/api/fec/products")
        assert response.status_code == 200
        products = response.json()
        
        ik_products = [p for p in products if 'IK' in p.get('name', '')]
        for p in ik_products:
            assert 'revenue_per_hour' in p, f"Missing revenue_per_hour for {p['name']}"
            assert 'capacity_per_hour' in p, f"Missing capacity_per_hour for {p['name']}"
            print(f"  - {p['name']}: €{p['revenue_per_hour']}/hr revenue, {p['capacity_per_hour']}/hr capacity")


class TestIKProductsIntegration:
    """Integration tests for IK products across flows"""
    
    def test_ik_products_list_all_names(self):
        """List all IK products in Recra database"""
        response = requests.get(f"{BASE_URL}/api/products?flow=recreatie")
        assert response.status_code == 200
        products = response.json()
        
        ik_products = [p for p in products if p.get('name', '').startswith('IK ')]
        print(f"\n=== All IK Products in Recra Database ({len(ik_products)}) ===")
        for p in ik_products:
            print(f"  - {p['name']}")
            print(f"    Category: {p['category']}")
            print(f"    Purchase: €{p['price_purchase']}")
            print(f"    Lease: €{p['price_lease_monthly']}/mnd")
            print(f"    Tier: {p.get('tier', 'N/A')}")
    
    def test_fec_ik_products_list_all_names(self):
        """List all IK products in FEC database"""
        response = requests.get(f"{BASE_URL}/api/fec/products")
        assert response.status_code == 200
        products = response.json()
        
        ik_products = [p for p in products if 'IK' in p.get('name', '')]
        print(f"\n=== All IK Products in FEC Database ({len(ik_products)}) ===")
        for p in ik_products:
            print(f"  - {p['name']}")
            print(f"    Category: {p['category']}")
            print(f"    Purchase: €{p['price_purchase']}")
            print(f"    Lease: €{p['price_lease_monthly']}/mnd")
            print(f"    Revenue/hr: €{p.get('revenue_per_hour', 'N/A')}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
