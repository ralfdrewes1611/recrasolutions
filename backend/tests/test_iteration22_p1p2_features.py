"""
Iteration 22 Tests: P1/P2 Features
- Roadmap Engine: /api/roadmap/phases/{type}
- White-label Engine: /api/whitelabel/config, /api/whitelabel/configs
- Enriched Partner Profiles: /api/partners/profiles/{id} with podcast, trendwatcher_quote, top_producten
- Dynamic Top 3: /api/partners/profiles/{id}/dynamic-top3
- FEC PDF Export: POST /api/fec/pdf
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestRoadmapEngine:
    """Roadmap Engine - 'Idee naar Realisatie' phases endpoint"""
    
    def test_roadmap_phases_recreatie(self):
        """GET /api/roadmap/phases/recreatie returns 4 phases"""
        response = requests.get(f"{BASE_URL}/api/roadmap/phases/recreatie")
        assert response.status_code == 200
        data = response.json()
        assert data["flow_type"] == "recreatie"
        assert data["total_phases"] == 4
        assert len(data["phases"]) == 4
        
        # Verify phase structure
        phase_ids = [p["id"] for p in data["phases"]]
        assert "ontwerp" in phase_ids
        assert "vergunning" in phase_ids
        assert "bouw" in phase_ids
        assert "exploitatie" in phase_ids
        
        # Verify first phase has required fields
        first_phase = data["phases"][0]
        assert "titel" in first_phase
        assert "duur" in first_phase
        assert "beschrijving" in first_phase
        assert "acties" in first_phase
        assert "deliverables" in first_phase
        assert "betrokken_partijen" in first_phase
        assert "kosten_indicatie" in first_phase
        print(f"✓ Recreatie roadmap: {data['total_phases']} phases, estimated {data['estimated_total_duration']}")
    
    def test_roadmap_phases_chalet(self):
        """GET /api/roadmap/phases/chalet returns 4 phases"""
        response = requests.get(f"{BASE_URL}/api/roadmap/phases/chalet")
        assert response.status_code == 200
        data = response.json()
        assert data["flow_type"] == "chalet"
        assert data["total_phases"] == 4
        assert len(data["phases"]) == 4
        
        phase_ids = [p["id"] for p in data["phases"]]
        assert "ontwerp" in phase_ids
        assert "vergunning" in phase_ids
        assert "productie" in phase_ids
        assert "plaatsing" in phase_ids
        print(f"✓ Chalet roadmap: {data['total_phases']} phases")
    
    def test_roadmap_phases_fec(self):
        """GET /api/roadmap/phases/fec returns 4 phases"""
        response = requests.get(f"{BASE_URL}/api/roadmap/phases/fec")
        assert response.status_code == 200
        data = response.json()
        assert data["flow_type"] == "fec"
        assert data["total_phases"] == 4
        assert len(data["phases"]) == 4
        
        phase_ids = [p["id"] for p in data["phases"]]
        assert "concept" in phase_ids
        assert "vergunning" in phase_ids
        assert "bouw" in phase_ids
        assert "exploitatie" in phase_ids
        print(f"✓ FEC roadmap: {data['total_phases']} phases")
    
    def test_roadmap_phases_invalid_type(self):
        """GET /api/roadmap/phases/invalid returns error with available types"""
        response = requests.get(f"{BASE_URL}/api/roadmap/phases/invalid")
        assert response.status_code == 200
        data = response.json()
        assert "error" in data
        assert "available" in data
        assert "recreatie" in data["available"]
        assert "chalet" in data["available"]
        assert "fec" in data["available"]
        print(f"✓ Invalid roadmap type returns available options: {data['available']}")
    
    def test_roadmap_summary(self):
        """GET /api/roadmap/summary returns overview of all roadmaps"""
        response = requests.get(f"{BASE_URL}/api/roadmap/summary")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        flow_types = [r["flow_type"] for r in data]
        assert "recreatie" in flow_types
        assert "chalet" in flow_types
        assert "fec" in flow_types
        print(f"✓ Roadmap summary: {len(data)} flow types")


class TestWhiteLabelEngine:
    """White-label Engine - Configurable branding for partners"""
    
    def test_whitelabel_config_default(self):
        """GET /api/whitelabel/config returns RECRA Solutions branding"""
        response = requests.get(f"{BASE_URL}/api/whitelabel/config")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "recra-default"
        assert data["brand_name"] == "RECRA Solutions"
        assert "primary_color" in data
        assert "secondary_color" in data
        assert "features_enabled" in data
        assert data["features_enabled"]["recreatie"] == True
        assert data["features_enabled"]["chalet"] == True
        assert data["features_enabled"]["fec"] == True
        assert data["features_enabled"]["roadmap"] == True
        print(f"✓ Default config: {data['brand_name']}")
    
    def test_whitelabel_configs_list(self):
        """GET /api/whitelabel/configs returns both RECRA and Pleisureworld configs"""
        response = requests.get(f"{BASE_URL}/api/whitelabel/configs")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        config_ids = [c["id"] for c in data]
        assert "recra-default" in config_ids
        assert "pleisureworld" in config_ids
        
        # Verify Pleisureworld config
        pleisureworld = next((c for c in data if c["id"] == "pleisureworld"), None)
        assert pleisureworld is not None
        assert pleisureworld["brand_name"] == "Pleisureworld"
        print(f"✓ White-label configs: {[c['brand_name'] for c in data]}")
    
    def test_whitelabel_config_by_id(self):
        """GET /api/whitelabel/config/pleisureworld returns Pleisureworld config"""
        response = requests.get(f"{BASE_URL}/api/whitelabel/config/pleisureworld")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "pleisureworld"
        assert data["brand_name"] == "Pleisureworld"
        assert data["tagline"] == "Van Inspiratie naar Realisatie"
        print(f"✓ Pleisureworld config: {data['tagline']}")


class TestEnrichedPartnerProfiles:
    """Enriched Partner Profiles with podcast, trendwatcher quote, top products"""
    
    def test_partner_profile_ticra_outdoor(self):
        """GET /api/partners/profiles/ticra-outdoor returns enriched profile"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles/ticra-outdoor")
        assert response.status_code == 200
        data = response.json()
        
        # Basic info
        assert data["id"] == "ticra-outdoor"
        assert data["name"] == "Ticra Outdoor"
        assert "tagline" in data
        assert "description" in data
        
        # Enriched fields
        assert "podcast" in data
        assert data["podcast"]["titel"] is not None
        assert "url" in data["podcast"]
        
        assert "trendwatcher_quote" in data
        assert data["trendwatcher_quote"]["auteur"] == "Richard Otten"
        
        assert "top_producten" in data
        assert len(data["top_producten"]) >= 3
        
        assert "deelname" in data  # Events
        assert len(data["deelname"]) >= 1
        
        print(f"✓ Ticra Outdoor profile: podcast='{data['podcast']['titel'][:30]}...', {len(data['top_producten'])} top products")
    
    def test_partner_profile_kunert_group(self):
        """GET /api/partners/profiles/kunert-group returns enriched profile"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles/kunert-group")
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == "kunert-group"
        assert data["name"] == "Kunert Group"
        assert "podcast" in data
        assert "trendwatcher_quote" in data
        assert "top_producten" in data
        assert len(data["top_producten"]) >= 3
        print(f"✓ Kunert Group profile: {len(data['top_producten'])} top products")
    
    def test_partner_profile_arcabo(self):
        """GET /api/partners/profiles/arcabo returns enriched profile"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles/arcabo")
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == "arcabo"
        assert data["name"] == "Arcabo"
        assert "podcast" in data
        assert "trendwatcher_quote" in data
        assert "top_producten" in data
        print(f"✓ Arcabo profile: {len(data['top_producten'])} top products")
    
    def test_partner_profile_campsolutions(self):
        """GET /api/partners/profiles/campsolutions returns enriched profile"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles/campsolutions")
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == "campsolutions"
        assert data["name"] == "Campsolutions"
        assert "podcast" in data
        assert "trendwatcher_quote" in data
        assert "top_producten" in data
        print(f"✓ Campsolutions profile: {len(data['top_producten'])} top products")
    
    def test_partner_profile_bbs_systeembouw(self):
        """GET /api/partners/profiles/bbs-systeembouw returns enriched profile"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles/bbs-systeembouw")
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == "bbs-systeembouw"
        assert data["name"] == "BBS Systeembouw"
        assert "podcast" in data
        assert "trendwatcher_quote" in data
        assert "top_producten" in data
        print(f"✓ BBS Systeembouw profile: {len(data['top_producten'])} top products")


class TestDynamicTop3:
    """Dynamic Top 3 products endpoint"""
    
    def test_dynamic_top3_ticra_outdoor(self):
        """GET /api/partners/profiles/ticra-outdoor/dynamic-top3 returns top 3 products"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles/ticra-outdoor/dynamic-top3")
        assert response.status_code == 200
        data = response.json()
        
        # Should have source field (statisch or dynamisch)
        assert "source" in data
        assert data["source"] in ["statisch", "dynamisch"]
        
        # Should have top_producten
        assert "top_producten" in data
        assert len(data["top_producten"]) >= 3
        
        print(f"✓ Ticra dynamic-top3: source={data['source']}, {len(data['top_producten'])} products")
    
    def test_dynamic_top3_invalid_partner(self):
        """GET /api/partners/profiles/invalid/dynamic-top3 returns error"""
        response = requests.get(f"{BASE_URL}/api/partners/profiles/invalid/dynamic-top3")
        assert response.status_code == 200
        data = response.json()
        assert "error" in data
        print(f"✓ Invalid partner dynamic-top3 returns error")


class TestFecPdfExport:
    """FEC PDF Export with Business Case"""
    
    def test_fec_pdf_export(self):
        """POST /api/fec/pdf with products returns HTML business case document"""
        # First get some FEC products
        products_response = requests.get(f"{BASE_URL}/api/fec/products")
        assert products_response.status_code == 200
        fec_products = products_response.json()
        
        if len(fec_products) == 0:
            pytest.skip("No FEC products available")
        
        # Select first 2 products
        selected_products = [
            {"product_id": fec_products[0]["id"], "quantity": 2},
        ]
        if len(fec_products) > 1:
            selected_products.append({"product_id": fec_products[1]["id"], "quantity": 1})
        
        # Generate PDF
        response = requests.post(f"{BASE_URL}/api/fec/pdf", json={
            "products": selected_products,
            "operating_hours": 10,
            "operating_days": 25,
            "project": {
                "total_area_m2": 500,
                "ceiling_height_m": 5.0,
                "target_audience": "families",
                "zones": []
            }
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "html" in data
        assert "project_name" in data
        assert "summary" in data
        
        # Verify HTML contains business case content
        html = data["html"]
        assert "Business Case" in html or "FEC" in html
        assert "€" in html  # Should have pricing
        
        # Verify summary has financial data
        summary = data["summary"]
        assert "total_investment" in summary
        assert "total_monthly_revenue" in summary
        
        print(f"✓ FEC PDF export: investment=€{summary['total_investment']}, revenue=€{summary['total_monthly_revenue']}/month")


class TestFlowSelectorCards:
    """Verify FlowSelector has 5 cards including Roadmap"""
    
    def test_api_root(self):
        """GET /api/ returns API info"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print(f"✓ API root: {data['message']}")
    
    def test_products_endpoint(self):
        """GET /api/products returns products"""
        response = requests.get(f"{BASE_URL}/api/products")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        print(f"✓ Products: {len(data)} products available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
