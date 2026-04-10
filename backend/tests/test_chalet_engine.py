"""
Test suite for Chalet & Stay Engine API endpoints.
Tests: models, suppliers, inspiratie pakketten, upgrade options, dynamic pricing.
Iteration 19 - Real product images from supplier websites.
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://pleasure-engine.preview.emergentagent.com')

class TestChaletModels:
    """Tests for GET /api/chalet/models endpoint"""
    
    def test_get_all_models_returns_26(self):
        """Verify 26 models are returned"""
        response = requests.get(f"{BASE_URL}/api/chalet/models")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 26, f"Expected 26 models, got {len(data)}"
        print(f"✓ GET /api/chalet/models returns {len(data)} models")
    
    def test_models_have_real_product_images(self):
        """Verify models have real product images from supplier websites"""
        response = requests.get(f"{BASE_URL}/api/chalet/models")
        assert response.status_code == 200
        data = response.json()
        
        # Check first model has images from supplier website
        model = data[0]
        assert "images" in model, "Model should have images"
        assert "modern" in model["images"], "Model should have modern style images"
        
        # Verify images are from real supplier websites (not Unsplash)
        images = model["images"]["modern"]
        assert len(images) > 0, "Should have at least one image"
        
        # Check images are from supplier domains
        supplier_domains = ["chaletskunert.nl", "arcabo.nl", "ucarecdn.com", "campsolutions.com"]
        first_image = images[0]
        is_real_supplier_image = any(domain in first_image for domain in supplier_domains)
        assert is_real_supplier_image, f"Image should be from supplier website, got: {first_image}"
        print(f"✓ Models have real product images from supplier websites")
    
    def test_filter_by_category_chalet(self):
        """Filter models by categorie=chalet"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?categorie=chalet")
        assert response.status_code == 200
        data = response.json()
        
        # All returned models should be chalets
        for model in data:
            assert model["categorie"] == "chalet", f"Expected chalet, got {model['categorie']}"
        
        chalet_count = len(data)
        assert chalet_count > 0, "Should have chalet models"
        print(f"✓ Category filter 'chalet' returns {chalet_count} models")
    
    def test_filter_by_category_glamping(self):
        """Filter models by categorie=glamping"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?categorie=glamping")
        assert response.status_code == 200
        data = response.json()
        
        # All returned models should be glamping
        for model in data:
            assert model["categorie"] == "glamping", f"Expected glamping, got {model['categorie']}"
        
        glamping_count = len(data)
        assert glamping_count > 0, "Should have glamping models"
        print(f"✓ Category filter 'glamping' returns {glamping_count} models")
    
    def test_filter_by_supplier_kunert(self):
        """Filter models by supplier_id=kunert"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?supplier_id=kunert")
        assert response.status_code == 200
        data = response.json()
        
        for model in data:
            assert model["supplier_id"] == "kunert", f"Expected kunert, got {model['supplier_id']}"
        
        print(f"✓ Supplier filter 'kunert' returns {len(data)} models")
    
    def test_filter_by_supplier_arcabo(self):
        """Filter models by supplier_id=arcabo"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?supplier_id=arcabo")
        assert response.status_code == 200
        data = response.json()
        
        for model in data:
            assert model["supplier_id"] == "arcabo"
        
        print(f"✓ Supplier filter 'arcabo' returns {len(data)} models")
    
    def test_filter_by_supplier_campsolutions(self):
        """Filter models by supplier_id=campsolutions (glamping)"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?supplier_id=campsolutions")
        assert response.status_code == 200
        data = response.json()
        
        for model in data:
            assert model["supplier_id"] == "campsolutions"
            assert model["categorie"] == "glamping", "Campsolutions should only have glamping"
        
        print(f"✓ Supplier filter 'campsolutions' returns {len(data)} glamping models")
    
    def test_model_has_pricing_structure(self):
        """Verify model has complete pricing structure"""
        response = requests.get(f"{BASE_URL}/api/chalet/models")
        assert response.status_code == 200
        data = response.json()
        
        model = data[0]
        pricing = model.get("pricing", {})
        
        required_fields = ["basisprijs", "totaal_excl_btw", "btw_bedrag", "totaal_incl_btw", "lease_monthly", "lease_months"]
        for field in required_fields:
            assert field in pricing, f"Pricing should have {field}"
        
        assert pricing["btw_percentage"] == 21, "BTW should be 21%"
        assert pricing["lease_months"] == 60, "Lease should be 60 months"
        print(f"✓ Model has complete pricing structure with BTW 21% and 60 month lease")


class TestChaletSuppliers:
    """Tests for GET /api/chalet/suppliers endpoint"""
    
    def test_get_suppliers_returns_4(self):
        """Verify 4 suppliers are returned"""
        response = requests.get(f"{BASE_URL}/api/chalet/suppliers")
        assert response.status_code == 200
        data = response.json()
        
        # Should have 4 suppliers: Kunert, Arcabo, BBS, Campsolutions
        assert len(data) == 4, f"Expected 4 suppliers, got {len(data)}"
        print(f"✓ GET /api/chalet/suppliers returns {len(data)} suppliers")
    
    def test_all_suppliers_are_pleisureworld_partners(self):
        """Verify all suppliers have pleisureworld_partner badge"""
        response = requests.get(f"{BASE_URL}/api/chalet/suppliers")
        assert response.status_code == 200
        data = response.json()
        
        for supplier in data:
            assert supplier.get("pleisureworld_partner") == True, f"{supplier['name']} should be Pleisureworld Partner"
        
        print(f"✓ All 4 suppliers have Pleisureworld Partner badge")
    
    def test_supplier_structure(self):
        """Verify supplier has required fields"""
        response = requests.get(f"{BASE_URL}/api/chalet/suppliers")
        assert response.status_code == 200
        data = response.json()
        
        required_fields = ["id", "name", "color", "website", "types", "pleisureworld_partner"]
        for supplier in data:
            for field in required_fields:
                assert field in supplier, f"Supplier should have {field}"
        
        print(f"✓ All suppliers have required fields")
    
    def test_supplier_names(self):
        """Verify correct supplier names"""
        response = requests.get(f"{BASE_URL}/api/chalet/suppliers")
        assert response.status_code == 200
        data = response.json()
        
        supplier_names = [s["name"] for s in data]
        expected_names = ["Kunert Group", "Arcabo", "BBS Systeembouw", "Campsolutions"]
        
        for name in expected_names:
            assert name in supplier_names, f"Missing supplier: {name}"
        
        print(f"✓ All expected suppliers present: {', '.join(expected_names)}")


class TestInspiratiePakketten:
    """Tests for GET /api/chalet/inspiratie endpoints"""
    
    def test_get_inspiratie_returns_3_packages(self):
        """Verify 3 inspiration packages are returned"""
        response = requests.get(f"{BASE_URL}/api/chalet/inspiratie")
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) == 3, f"Expected 3 packages, got {len(data)}"
        print(f"✓ GET /api/chalet/inspiratie returns {len(data)} packages")
    
    def test_inspiratie_package_names(self):
        """Verify correct package names"""
        response = requests.get(f"{BASE_URL}/api/chalet/inspiratie")
        assert response.status_code == 200
        data = response.json()
        
        package_names = [p["name"] for p in data]
        expected_names = ["Populair Glamping Pakket", "Luxe Chaletpark Setup", "Starter Park — Budget"]
        
        for name in expected_names:
            assert name in package_names, f"Missing package: {name}"
        
        print(f"✓ All 3 expected packages present")
    
    def test_inspiratie_package_structure(self):
        """Verify package has required fields"""
        response = requests.get(f"{BASE_URL}/api/chalet/inspiratie")
        assert response.status_code == 200
        data = response.json()
        
        required_fields = ["id", "name", "subtitle", "description", "badge", "badge_color", "models", "total_units", "estimated_investment", "highlights"]
        for package in data:
            for field in required_fields:
                assert field in package, f"Package should have {field}"
        
        print(f"✓ All packages have required fields")
    
    def test_inspiratie_detail_endpoint(self):
        """Test GET /api/chalet/inspiratie/{pakket_id} returns enriched data"""
        response = requests.get(f"{BASE_URL}/api/chalet/inspiratie/glamping-tour-populair")
        assert response.status_code == 200
        data = response.json()
        
        # Should have enriched_models with full model details
        assert "enriched_models" in data, "Should have enriched_models"
        assert len(data["enriched_models"]) > 0, "Should have at least one enriched model"
        
        # Should have totals
        assert "totals" in data, "Should have totals"
        totals = data["totals"]
        assert "total_investment_incl_btw" in totals
        assert "total_lease_monthly" in totals
        assert "total_units" in totals
        
        print(f"✓ Inspiratie detail returns enriched models and totals")


class TestUpgradeOptions:
    """Tests for GET /api/chalet/upgrade-options/{categorie} endpoint"""
    
    def test_chalet_upgrade_options(self):
        """Verify chalet upgrade categories"""
        response = requests.get(f"{BASE_URL}/api/chalet/upgrade-options/chalet")
        assert response.status_code == 200
        data = response.json()
        
        expected_categories = ["keuken", "badkamer", "terras", "interieur", "klimaat", "duurzaamheid"]
        for cat in expected_categories:
            assert cat in data, f"Missing upgrade category: {cat}"
        
        print(f"✓ Chalet has {len(expected_categories)} upgrade categories")
    
    def test_glamping_upgrade_options(self):
        """Verify glamping upgrade categories"""
        response = requests.get(f"{BASE_URL}/api/chalet/upgrade-options/glamping")
        assert response.status_code == 200
        data = response.json()
        
        expected_categories = ["sanitair", "inrichting", "vlonder", "verlichting"]
        for cat in expected_categories:
            assert cat in data, f"Missing upgrade category: {cat}"
        
        print(f"✓ Glamping has {len(expected_categories)} upgrade categories")
    
    def test_upgrade_option_structure(self):
        """Verify upgrade option has required fields"""
        response = requests.get(f"{BASE_URL}/api/chalet/upgrade-options/chalet")
        assert response.status_code == 200
        data = response.json()
        
        # Check keuken options
        keuken_options = data.get("keuken", [])
        assert len(keuken_options) >= 3, "Should have at least 3 keuken options"
        
        for option in keuken_options:
            assert "id" in option
            assert "name" in option
            assert "description" in option
            assert "price" in option
        
        print(f"✓ Upgrade options have required fields (id, name, description, price)")


class TestDynamicPricing:
    """Tests for POST /api/chalet/calculate-with-upgrades endpoint"""
    
    def test_calculate_with_no_upgrades(self):
        """Calculate pricing with no upgrades"""
        response = requests.post(
            f"{BASE_URL}/api/chalet/calculate-with-upgrades",
            json={"model_id": "kunert-plat-12", "upgrades": {}}
        )
        assert response.status_code == 200
        data = response.json()
        
        pricing = data.get("pricing", {})
        assert pricing["upgrades_total"] == 0, "No upgrades should mean 0 upgrade cost"
        assert pricing["basisprijs"] == 74950, "Base price should be 74950"
        
        print(f"✓ Calculate with no upgrades returns base price only")
    
    def test_calculate_with_upgrades(self):
        """Calculate pricing with selected upgrades"""
        response = requests.post(
            f"{BASE_URL}/api/chalet/calculate-with-upgrades",
            json={
                "model_id": "kunert-plat-12",
                "upgrades": {
                    "keuken": "keuken-luxe",
                    "badkamer": "bad-wellness"
                }
            }
        )
        assert response.status_code == 200
        data = response.json()
        
        pricing = data.get("pricing", {})
        # keuken-luxe = 8500, bad-wellness = 7500 = 16000 total
        assert pricing["upgrades_total"] == 16000, f"Expected 16000 upgrades, got {pricing['upgrades_total']}"
        assert pricing["totaal_excl_btw"] == 74950 + 16000, "Total should be base + upgrades"
        
        # Check upgrade details
        upgrade_details = data.get("upgrade_details", [])
        assert len(upgrade_details) == 2, "Should have 2 upgrade details"
        
        print(f"✓ Calculate with upgrades correctly adds upgrade costs")
    
    def test_calculate_updates_lease_monthly(self):
        """Verify lease monthly is recalculated with upgrades"""
        # Without upgrades
        response1 = requests.post(
            f"{BASE_URL}/api/chalet/calculate-with-upgrades",
            json={"model_id": "kunert-plat-12", "upgrades": {}}
        )
        base_lease = response1.json()["pricing"]["lease_monthly"]
        
        # With upgrades
        response2 = requests.post(
            f"{BASE_URL}/api/chalet/calculate-with-upgrades",
            json={
                "model_id": "kunert-plat-12",
                "upgrades": {"keuken": "keuken-luxe"}
            }
        )
        upgraded_lease = response2.json()["pricing"]["lease_monthly"]
        
        assert upgraded_lease > base_lease, "Lease should increase with upgrades"
        print(f"✓ Lease monthly increases with upgrades ({base_lease} → {upgraded_lease})")


class TestImageSources:
    """Tests to verify real product images from supplier websites"""
    
    def test_kunert_images_from_chaletskunert(self):
        """Verify Kunert models have images from chaletskunert.nl"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?supplier_id=kunert")
        assert response.status_code == 200
        data = response.json()
        
        for model in data:
            images = model.get("images", {}).get("modern", [])
            if images:
                assert any("chaletskunert.nl" in img for img in images), f"Kunert model {model['name']} should have chaletskunert.nl images"
        
        print(f"✓ Kunert models have images from chaletskunert.nl")
    
    def test_arcabo_images_from_arcabo(self):
        """Verify Arcabo models have images from arcabo.nl"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?supplier_id=arcabo")
        assert response.status_code == 200
        data = response.json()
        
        for model in data:
            images = model.get("images", {}).get("modern", [])
            if images:
                assert any("arcabo.nl" in img for img in images), f"Arcabo model {model['name']} should have arcabo.nl images"
        
        print(f"✓ Arcabo models have images from arcabo.nl")
    
    def test_campsolutions_images_from_campsolutions(self):
        """Verify Campsolutions models have images from campsolutions.com"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?supplier_id=campsolutions")
        assert response.status_code == 200
        data = response.json()
        
        for model in data:
            images = model.get("images", {}).get("modern", [])
            if images:
                assert any("campsolutions.com" in img for img in images), f"Campsolutions model {model['name']} should have campsolutions.com images"
        
        print(f"✓ Campsolutions models have images from campsolutions.com")
    
    def test_bbs_images_from_ucarecdn(self):
        """Verify BBS models have images from ucarecdn.com (BBS hosting)"""
        response = requests.get(f"{BASE_URL}/api/chalet/models?supplier_id=bbs")
        assert response.status_code == 200
        data = response.json()
        
        for model in data:
            images = model.get("images", {}).get("modern", [])
            if images:
                assert any("ucarecdn.com" in img for img in images), f"BBS model {model['name']} should have ucarecdn.com images"
        
        print(f"✓ BBS models have images from ucarecdn.com")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
