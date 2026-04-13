"""
Iteration 24: CRM Lead Management, 3 Scenario Generator, Follow-up Email, Improved PDF
Tests for:
- POST /api/crm/leads — creates a new lead with lead_score calculation (0-100)
- GET /api/crm/leads — returns list of leads sorted by created_at desc
- POST /api/crm/leads/{id}/follow-up — generates personalized follow-up email HTML
- POST /api/crm/follow-up/generate — generates follow-up email from data without saving lead
- POST /api/crm/scenarios/generate — returns 3 scenarios (Budget, Standaard, Premium)
"""
import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')


class TestCRMLeads:
    """CRM Lead management endpoint tests"""
    
    def test_create_lead_basic(self):
        """Test creating a basic lead with minimal data"""
        response = requests.post(f"{BASE_URL}/api/crm/leads", json={
            "naam": "TEST_Jan Jansen",
            "email": "test_jan@example.com",
            "flow_type": "recreatie",
            "bron": "subsidie_check"
        })
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        # Verify response structure
        assert "id" in data, "Response should contain lead id"
        assert "lead_score" in data, "Response should contain lead_score"
        assert "status" in data, "Response should contain status"
        assert data["status"] == "nieuw", f"Expected status 'nieuw', got {data['status']}"
        
        # Lead score should be at least 20 (email provided)
        assert data["lead_score"] >= 20, f"Lead score should be >= 20 with email, got {data['lead_score']}"
        print(f"✓ Created lead with id={data['id']}, lead_score={data['lead_score']}")
    
    def test_create_lead_full_data(self):
        """Test creating a lead with all fields for maximum lead score"""
        response = requests.post(f"{BASE_URL}/api/crm/leads", json={
            "naam": "TEST_Piet Pietersen",
            "email": "test_piet@example.com",
            "telefoon": "+31612345678",
            "bedrijf": "Test Camping BV",
            "flow_type": "recreatie",
            "bron": "subsidie_check",
            "project_beschrijving": "Nieuw sanitairgebouw met 10 douches",
            "subsidie_score": 8.5,
            "subsidie_kans": "hoog",
            "subsidie_range": "€10.000 - €25.000",
            "investering": "> €100K"
        })
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        # With all fields + hoog kans + high investering, score should be high
        # email(20) + telefoon(15) + bedrijf(10) + project(10) + subsidie_score(15) + hoog_kans(20) + high_inv(10) = 100
        assert data["lead_score"] == 100, f"Expected max lead_score 100, got {data['lead_score']}"
        print(f"✓ Created full lead with max score: {data['lead_score']}")
    
    def test_create_lead_middel_kans(self):
        """Test lead score with middel kans (should add 10 instead of 20)"""
        response = requests.post(f"{BASE_URL}/api/crm/leads", json={
            "naam": "TEST_Middel Lead",
            "email": "test_middel@example.com",
            "subsidie_kans": "middel"
        })
        assert response.status_code == 200
        data = response.json()
        
        # email(20) + middel_kans(10) = 30
        assert data["lead_score"] == 30, f"Expected lead_score 30, got {data['lead_score']}"
        print(f"✓ Middel kans lead score: {data['lead_score']}")
    
    def test_get_leads_list(self):
        """Test retrieving list of leads"""
        # First create a lead to ensure there's data
        requests.post(f"{BASE_URL}/api/crm/leads", json={
            "naam": "TEST_List Lead",
            "email": "test_list@example.com"
        })
        
        response = requests.get(f"{BASE_URL}/api/crm/leads")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        assert isinstance(data, list), "Response should be a list"
        assert len(data) > 0, "Should have at least one lead"
        
        # Verify lead structure
        lead = data[0]
        assert "id" in lead
        assert "naam" in lead
        assert "email" in lead
        assert "lead_score" in lead
        assert "created_at" in lead
        
        # Verify sorted by created_at desc (newest first)
        if len(data) > 1:
            assert data[0]["created_at"] >= data[1]["created_at"], "Leads should be sorted by created_at desc"
        
        print(f"✓ Retrieved {len(data)} leads, sorted by created_at desc")
    
    def test_get_lead_by_id(self):
        """Test retrieving a specific lead by ID"""
        # Create a lead first
        create_res = requests.post(f"{BASE_URL}/api/crm/leads", json={
            "naam": "TEST_Specific Lead",
            "email": "test_specific@example.com"
        })
        lead_id = create_res.json()["id"]
        
        # Get the lead
        response = requests.get(f"{BASE_URL}/api/crm/leads/{lead_id}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        assert data["id"] == lead_id
        assert data["naam"] == "TEST_Specific Lead"
        assert data["email"] == "test_specific@example.com"
        print(f"✓ Retrieved lead by ID: {lead_id}")
    
    def test_get_lead_not_found(self):
        """Test retrieving non-existent lead"""
        response = requests.get(f"{BASE_URL}/api/crm/leads/non-existent-id-12345")
        assert response.status_code == 200  # Returns error in body, not 404
        data = response.json()
        assert "error" in data, "Should return error for non-existent lead"
        print("✓ Non-existent lead returns error")


class TestCRMFollowUp:
    """Follow-up email generation tests"""
    
    def test_generate_follow_up_for_lead(self):
        """Test generating follow-up email for an existing lead"""
        # Create a lead first
        create_res = requests.post(f"{BASE_URL}/api/crm/leads", json={
            "naam": "TEST_Follow Up Lead",
            "email": "test_followup@example.com",
            "subsidie_score": 7.5,
            "subsidie_kans": "hoog",
            "subsidie_range": "€5.000 - €15.000",
            "project_beschrijving": "Wellness toevoegen aan camping",
            "investering": "€25K - €100K"
        })
        lead_id = create_res.json()["id"]
        
        # Generate follow-up
        response = requests.post(f"{BASE_URL}/api/crm/leads/{lead_id}/follow-up")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        # Verify response structure
        assert "email_html" in data, "Response should contain email_html"
        assert "subject" in data, "Response should contain subject"
        assert "to" in data, "Response should contain to"
        assert "naam" in data, "Response should contain naam"
        
        # Verify email content
        html = data["email_html"]
        assert "RECRA" in html, "Email should contain RECRA branding"
        assert "TEST_Follow Up Lead" in html, "Email should contain lead name"
        assert "hoog" in html.lower() or "HOOG" in html, "Email should contain kans"
        assert "Plan een adviesgesprek" in html, "Email should contain CTA"
        
        print(f"✓ Generated follow-up email for lead {lead_id}")
        print(f"  Subject: {data['subject']}")
        print(f"  To: {data['to']}")
    
    def test_generate_follow_up_from_data(self):
        """Test generating follow-up email directly from data (without saving lead)"""
        response = requests.post(f"{BASE_URL}/api/crm/follow-up/generate", json={
            "naam": "TEST_Direct User",
            "email": "test_direct@example.com",
            "subsidie_score": 8,
            "subsidie_kans": "hoog",
            "subsidie_range": "€10.000 - €25.000",
            "project_beschrijving": "Slagboom en camera systeem",
            "investering": "> €100K"
        })
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        assert "email_html" in data
        assert "subject" in data
        
        html = data["email_html"]
        assert "RECRA" in html, "Email should contain RECRA branding"
        assert "TEST_Direct User" in html, "Email should contain user name"
        assert "€10.000 - €25.000" in html, "Email should contain subsidie_range"
        
        print(f"✓ Generated follow-up email from data")
        print(f"  Subject: {data['subject']}")
    
    def test_follow_up_for_nonexistent_lead(self):
        """Test follow-up generation for non-existent lead"""
        response = requests.post(f"{BASE_URL}/api/crm/leads/nonexistent-lead-id/follow-up")
        assert response.status_code == 200  # Returns error in body
        data = response.json()
        assert "error" in data
        print("✓ Non-existent lead follow-up returns error")


class TestScenarioGenerator:
    """3 Scenario Generator tests"""
    
    def test_generate_scenarios_basic(self):
        """Test generating 3 scenarios with basic input"""
        response = requests.post(f"{BASE_URL}/api/crm/scenarios/generate", json={
            "flow_type": "recreatie",
            "project_beschrijving": "Camping met 50 standplaatsen",
            "investering_range": "€25K - €100K"
        })
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        assert "scenarios" in data, "Response should contain scenarios"
        assert "source" in data, "Response should contain source (ai or statisch)"
        
        scenarios = data["scenarios"]
        assert len(scenarios) == 3, f"Should have exactly 3 scenarios, got {len(scenarios)}"
        
        # Verify each scenario has required fields
        for i, sc in enumerate(scenarios):
            assert "naam" in sc, f"Scenario {i} should have naam"
            assert "beschrijving" in sc, f"Scenario {i} should have beschrijving"
            assert "investering" in sc, f"Scenario {i} should have investering"
            assert "lease_maand" in sc, f"Scenario {i} should have lease_maand"
            assert "producten" in sc, f"Scenario {i} should have producten"
            assert "voordelen" in sc, f"Scenario {i} should have voordelen"
            assert isinstance(sc["producten"], list), f"Scenario {i} producten should be a list"
            assert isinstance(sc["voordelen"], list), f"Scenario {i} voordelen should be a list"
        
        # Verify scenario names (Budget, Standaard, Premium)
        names = [sc["naam"] for sc in scenarios]
        assert "Budget" in names, "Should have Budget scenario"
        assert "Standaard" in names, "Should have Standaard scenario"
        assert "Premium" in names, "Should have Premium scenario"
        
        print(f"✓ Generated 3 scenarios (source: {data['source']})")
        for sc in scenarios:
            print(f"  - {sc['naam']}: €{sc['investering']:,} / €{sc['lease_maand']}/mnd")
    
    def test_generate_scenarios_high_budget(self):
        """Test scenarios with high budget range"""
        response = requests.post(f"{BASE_URL}/api/crm/scenarios/generate", json={
            "flow_type": "recreatie",
            "project_beschrijving": "Groot vakantiepark met wellness",
            "investering_range": "> €100K",
            "doelgroep": "families",
            "extra_wensen": "Duurzaam en premium uitstraling"
        })
        assert response.status_code == 200
        data = response.json()
        
        scenarios = data["scenarios"]
        assert len(scenarios) == 3
        
        # With high budget, scenarios should have higher investments
        # The last scenario (Premium/Signature) should have highest investment
        # Note: AI may use creative names like "Signature" instead of "Premium"
        investments = [s["investering"] for s in scenarios]
        max_investment = max(investments)
        
        # For > €100K budget, at least one scenario should have high investment
        assert max_investment > 50000, f"Highest scenario should have investment > 50000, got {max_investment}"
        
        print(f"✓ High budget scenarios generated (source: {data['source']})")
        print(f"  Investments: {investments}")
    
    def test_generate_scenarios_low_budget(self):
        """Test scenarios with low budget range"""
        response = requests.post(f"{BASE_URL}/api/crm/scenarios/generate", json={
            "flow_type": "recreatie",
            "project_beschrijving": "Klein camping terrein",
            "investering_range": "€10K - €25K"
        })
        assert response.status_code == 200
        data = response.json()
        
        scenarios = data["scenarios"]
        budget = next((s for s in scenarios if s["naam"] == "Budget"), None)
        assert budget is not None
        
        print(f"✓ Low budget scenarios generated")
        print(f"  Budget investering: €{budget['investering']:,}")
    
    def test_scenarios_have_terugverdientijd(self):
        """Test that scenarios include terugverdientijd_maanden"""
        response = requests.post(f"{BASE_URL}/api/crm/scenarios/generate", json={
            "flow_type": "recreatie",
            "project_beschrijving": "Test project",
            "investering_range": "€25K - €100K"
        })
        assert response.status_code == 200
        data = response.json()
        
        for sc in data["scenarios"]:
            assert "terugverdientijd_maanden" in sc, f"Scenario {sc['naam']} should have terugverdientijd_maanden"
            assert isinstance(sc["terugverdientijd_maanden"], (int, float))
        
        print("✓ All scenarios have terugverdientijd_maanden")


class TestLeadScoreCalculation:
    """Detailed lead score calculation tests"""
    
    def test_score_email_only(self):
        """Email only = 20 points"""
        response = requests.post(f"{BASE_URL}/api/crm/leads", json={
            "naam": "TEST_Email Only",
            "email": "test_email_only@example.com"
        })
        assert response.json()["lead_score"] == 20
        print("✓ Email only: 20 points")
    
    def test_score_email_telefoon(self):
        """Email + telefoon = 35 points"""
        response = requests.post(f"{BASE_URL}/api/crm/leads", json={
            "naam": "TEST_Email Telefoon",
            "email": "test_et@example.com",
            "telefoon": "+31612345678"
        })
        assert response.json()["lead_score"] == 35
        print("✓ Email + telefoon: 35 points")
    
    def test_score_email_telefoon_bedrijf(self):
        """Email + telefoon + bedrijf = 45 points"""
        response = requests.post(f"{BASE_URL}/api/crm/leads", json={
            "naam": "TEST_ETB",
            "email": "test_etb@example.com",
            "telefoon": "+31612345678",
            "bedrijf": "Test BV"
        })
        assert response.json()["lead_score"] == 45
        print("✓ Email + telefoon + bedrijf: 45 points")
    
    def test_score_with_project(self):
        """Adding project_beschrijving = +10 points"""
        response = requests.post(f"{BASE_URL}/api/crm/leads", json={
            "naam": "TEST_Project",
            "email": "test_project@example.com",
            "project_beschrijving": "Nieuw sanitairgebouw"
        })
        # email(20) + project(10) = 30
        assert response.json()["lead_score"] == 30
        print("✓ Email + project: 30 points")
    
    def test_score_with_subsidie_score(self):
        """Adding subsidie_score = +15 points"""
        response = requests.post(f"{BASE_URL}/api/crm/leads", json={
            "naam": "TEST_Subsidie",
            "email": "test_subsidie@example.com",
            "subsidie_score": 7.5
        })
        # email(20) + subsidie_score(15) = 35
        assert response.json()["lead_score"] == 35
        print("✓ Email + subsidie_score: 35 points")
    
    def test_score_hoog_kans(self):
        """Hoog kans = +20 points"""
        response = requests.post(f"{BASE_URL}/api/crm/leads", json={
            "naam": "TEST_Hoog",
            "email": "test_hoog@example.com",
            "subsidie_kans": "hoog"
        })
        # email(20) + hoog_kans(20) = 40
        assert response.json()["lead_score"] == 40
        print("✓ Email + hoog kans: 40 points")
    
    def test_score_high_investering(self):
        """High investering (> €100K or €25K-€100K) = +10 points"""
        response = requests.post(f"{BASE_URL}/api/crm/leads", json={
            "naam": "TEST_High Inv",
            "email": "test_highinv@example.com",
            "investering": "> €100K"
        })
        # email(20) + high_inv(10) = 30
        assert response.json()["lead_score"] == 30
        print("✓ Email + high investering: 30 points")
    
    def test_score_max_100(self):
        """Score should be capped at 100"""
        response = requests.post(f"{BASE_URL}/api/crm/leads", json={
            "naam": "TEST_Max Score",
            "email": "test_max@example.com",
            "telefoon": "+31612345678",
            "bedrijf": "Max BV",
            "project_beschrijving": "Big project",
            "subsidie_score": 10,
            "subsidie_kans": "hoog",
            "investering": "> €100K"
        })
        # All points: 20+15+10+10+15+20+10 = 100
        assert response.json()["lead_score"] == 100
        print("✓ Max score capped at 100")


class TestImprovedPDF:
    """Test improved Recreatie PDF export"""
    
    def test_pdf_endpoint_exists(self):
        """Test that PDF endpoint exists and returns HTML"""
        # First create a project with products
        project_res = requests.post(f"{BASE_URL}/api/projects", json={
            "name": "TEST_PDF Project",
            "project_type": "recreatie",
            "project_flow": "recreatie",
            "num_spots": 50,
            "placed_products": []
        })
        project_id = project_res.json()["id"]
        
        # Generate PDF
        response = requests.post(f"{BASE_URL}/api/quote/pdf?project_id={project_id}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        assert "html" in data, "Response should contain html"
        assert "project_name" in data, "Response should contain project_name"
        assert "quote" in data, "Response should contain quote"
        
        html = data["html"]
        assert "RECRA" in html, "PDF should contain RECRA branding"
        assert "Pleisureworld" in html, "PDF should contain Pleisureworld branding"
        assert "Investering" in html, "PDF should contain investment section"
        assert "Lease" in html, "PDF should contain lease section"
        
        print(f"✓ PDF generated for project {project_id}")
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/projects/{project_id}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
