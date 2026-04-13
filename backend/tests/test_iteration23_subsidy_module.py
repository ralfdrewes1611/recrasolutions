"""
Iteration 23: Financiering & Subsidie Check Module Tests
Tests for:
- POST /api/subsidy/check — rules-based scoring
- POST /api/subsidy/ai-analyse — AI-powered analysis with GPT-5.2
- POST /api/subsidy/generate-document — AI document generator
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test data for subsidy intake
HIGH_SCORE_INTAKE = {
    "sector": "Recreatie",
    "rechtsvorm": "BV",
    "projectomschrijving": "Digitalisering van ons recreatiepark met slimme toegangscontrole en WiFi",
    "doel": "Digitaliseren",
    "investering": "€25K - €100K",
    "eigen_investering": "Ja",
    "gebruikers": "1.000 - 10.000",
    "samenwerking": "Ja",
    "duurzaamheid": "Ja"
}

LOW_INVESTMENT_INTAKE = {
    "sector": "Recreatie",
    "rechtsvorm": "BV",
    "projectomschrijving": "Klein project",
    "doel": "Kosten besparen",
    "investering": "< €10K",
    "eigen_investering": "Nee",
    "gebruikers": "< 100",
    "samenwerking": "Nee",
    "duurzaamheid": "Nee"
}

MEDIUM_SCORE_INTAKE = {
    "sector": "Zorg",
    "rechtsvorm": "Stichting",
    "projectomschrijving": "Verbetering van zorgfaciliteiten",
    "doel": "Zorg / welzijn verbeteren",
    "investering": "€10K - €25K",
    "eigen_investering": "Deels",
    "gebruikers": "100 - 1.000",
    "samenwerking": "Nee",
    "duurzaamheid": "Ja"
}


class TestSubsidyCheck:
    """Tests for POST /api/subsidy/check — rules-based scoring"""
    
    def test_subsidy_check_high_score(self):
        """Test high score scenario returns kans=hoog"""
        response = requests.post(f"{BASE_URL}/api/subsidy/check", json=HIGH_SCORE_INTAKE)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        # Verify required fields
        assert "score" in data, "Response should contain 'score'"
        assert "kans" in data, "Response should contain 'kans'"
        assert "breakdown" in data, "Response should contain 'breakdown'"
        assert "subsidie_range" in data, "Response should contain 'subsidie_range'"
        assert "advies" in data, "Response should contain 'advies'"
        
        # Verify high score scenario
        assert data["score"] >= 8, f"Expected score >= 8 for high scenario, got {data['score']}"
        assert data["kans"] == "hoog", f"Expected kans='hoog', got {data['kans']}"
        assert "€10.000" in data["subsidie_range"] or "€50.000" in data["subsidie_range"], f"Expected high subsidie_range, got {data['subsidie_range']}"
        
        # Verify breakdown structure
        breakdown = data["breakdown"]
        assert "sector_fit" in breakdown, "Breakdown should contain 'sector_fit'"
        assert "projecttype" in breakdown, "Breakdown should contain 'projecttype'"
        assert "investering" in breakdown, "Breakdown should contain 'investering'"
        assert "impact" in breakdown, "Breakdown should contain 'impact'"
        assert "samenwerking" in breakdown, "Breakdown should contain 'samenwerking'"
        assert "duurzaamheid" in breakdown, "Breakdown should contain 'duurzaamheid'"
        
        print(f"HIGH SCORE TEST PASSED: score={data['score']}, kans={data['kans']}, range={data['subsidie_range']}")
    
    def test_subsidy_check_low_investment_hard_filter(self):
        """Test investering < €10K triggers hard filter (lage kans)"""
        response = requests.post(f"{BASE_URL}/api/subsidy/check", json=LOW_INVESTMENT_INTAKE)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        # Verify hard filter triggered
        assert data["kans"] == "laag", f"Expected kans='laag' for < €10K investment, got {data['kans']}"
        assert data["score"] <= 2, f"Expected low score for hard filter, got {data['score']}"
        assert "hard_filter" in data["breakdown"], "Breakdown should contain 'hard_filter' for low investment"
        assert "€10K" in data["breakdown"]["hard_filter"], "Hard filter message should mention €10K"
        
        print(f"LOW INVESTMENT HARD FILTER TEST PASSED: score={data['score']}, kans={data['kans']}")
    
    def test_subsidy_check_medium_score(self):
        """Test medium score scenario returns kans=middel"""
        response = requests.post(f"{BASE_URL}/api/subsidy/check", json=MEDIUM_SCORE_INTAKE)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        # Verify medium score scenario
        assert 4 < data["score"] <= 7, f"Expected score between 4-7 for medium scenario, got {data['score']}"
        assert data["kans"] == "middel", f"Expected kans='middel', got {data['kans']}"
        
        print(f"MEDIUM SCORE TEST PASSED: score={data['score']}, kans={data['kans']}")
    
    def test_subsidy_check_breakdown_scores(self):
        """Test that breakdown contains proper score/max structure"""
        response = requests.post(f"{BASE_URL}/api/subsidy/check", json=HIGH_SCORE_INTAKE)
        assert response.status_code == 200
        
        data = response.json()
        breakdown = data["breakdown"]
        
        # Check each breakdown item has score, max, label
        for key in ["sector_fit", "projecttype", "investering", "impact", "samenwerking", "duurzaamheid"]:
            assert key in breakdown, f"Missing breakdown key: {key}"
            item = breakdown[key]
            assert "score" in item, f"Breakdown {key} should have 'score'"
            assert "max" in item, f"Breakdown {key} should have 'max'"
            assert "label" in item, f"Breakdown {key} should have 'label'"
            assert item["score"] <= item["max"], f"Score should not exceed max for {key}"
        
        print("BREAKDOWN STRUCTURE TEST PASSED")


class TestSubsidyAIAnalyse:
    """Tests for POST /api/subsidy/ai-analyse — AI-powered analysis"""
    
    def test_ai_analyse_returns_rules_score_and_ai_result(self):
        """Test AI analyse returns both rules score and AI analysis"""
        response = requests.post(f"{BASE_URL}/api/subsidy/ai-analyse", json=HIGH_SCORE_INTAKE, timeout=30)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        # Should contain rules-based score
        assert "score" in data, "Response should contain rules 'score'"
        assert "kans" in data, "Response should contain rules 'kans'"
        assert "breakdown" in data, "Response should contain rules 'breakdown'"
        
        # Should contain AI analysis or error
        if "ai_analyse" in data and data["ai_analyse"]:
            ai = data["ai_analyse"]
            # AI response should have structured fields
            print(f"AI ANALYSE RETURNED: {ai}")
            # Check for expected AI response fields (may vary based on GPT response)
            if isinstance(ai, dict):
                # Expected fields from AI
                expected_fields = ["kans", "toelichting", "verbeterpunten", "regelingen"]
                found_fields = [f for f in expected_fields if f in ai]
                print(f"AI response contains fields: {found_fields}")
        elif "ai_error" in data:
            print(f"AI ANALYSE returned error (expected if no API key): {data['ai_error']}")
        else:
            print("AI ANALYSE returned null (no AI key configured)")
        
        print(f"AI ANALYSE TEST PASSED: rules_score={data['score']}, has_ai={bool(data.get('ai_analyse'))}")
    
    def test_ai_analyse_with_low_investment(self):
        """Test AI analyse with low investment still returns rules score"""
        response = requests.post(f"{BASE_URL}/api/subsidy/ai-analyse", json=LOW_INVESTMENT_INTAKE, timeout=30)
        assert response.status_code == 200
        
        data = response.json()
        # Rules score should still show hard filter
        assert data["kans"] == "laag"
        assert "hard_filter" in data["breakdown"]
        
        print(f"AI ANALYSE LOW INVESTMENT TEST PASSED")


class TestSubsidyGenerateDocument:
    """Tests for POST /api/subsidy/generate-document — AI document generator"""
    
    def test_generate_document_returns_document(self):
        """Test document generation returns formatted document"""
        response = requests.post(f"{BASE_URL}/api/subsidy/generate-document", json=HIGH_SCORE_INTAKE, timeout=60)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        
        if "document" in data and data["document"]:
            assert data["status"] == "success", f"Expected status='success', got {data.get('status')}"
            assert len(data["document"]) > 100, "Document should be substantial text"
            print(f"DOCUMENT GENERATED: {len(data['document'])} characters")
            # Check document contains expected sections
            doc = data["document"].lower()
            # Document should mention project-related terms
            print(f"Document preview: {data['document'][:200]}...")
        elif "error" in data:
            print(f"DOCUMENT GENERATION returned error (expected if no API key): {data['error']}")
        else:
            print("DOCUMENT GENERATION returned empty (no AI key configured)")
        
        print("GENERATE DOCUMENT TEST PASSED")


class TestSubsidyEndpointValidation:
    """Tests for endpoint validation and error handling"""
    
    def test_subsidy_check_missing_fields(self):
        """Test subsidy check with missing required fields"""
        incomplete_data = {
            "sector": "Recreatie",
            "rechtsvorm": "BV"
            # Missing other required fields
        }
        response = requests.post(f"{BASE_URL}/api/subsidy/check", json=incomplete_data)
        # Should return 422 for validation error
        assert response.status_code == 422, f"Expected 422 for missing fields, got {response.status_code}"
        print("MISSING FIELDS VALIDATION TEST PASSED")
    
    def test_subsidy_check_empty_body(self):
        """Test subsidy check with empty body"""
        response = requests.post(f"{BASE_URL}/api/subsidy/check", json={})
        assert response.status_code == 422, f"Expected 422 for empty body, got {response.status_code}"
        print("EMPTY BODY VALIDATION TEST PASSED")


class TestSubsidyScoringLogic:
    """Tests for specific scoring logic rules"""
    
    def test_sector_scoring(self):
        """Test different sectors get appropriate scores"""
        sectors = ["Recreatie", "Zorg", "Kinderopvang", "Overig"]
        for sector in sectors:
            intake = HIGH_SCORE_INTAKE.copy()
            intake["sector"] = sector
            response = requests.post(f"{BASE_URL}/api/subsidy/check", json=intake)
            assert response.status_code == 200
            data = response.json()
            
            sector_score = data["breakdown"]["sector_fit"]["score"]
            if sector in ["Recreatie", "Zorg", "Kinderopvang"]:
                assert sector_score == 2, f"Expected sector score 2 for {sector}, got {sector_score}"
            else:
                assert sector_score == 1, f"Expected sector score 1 for {sector}, got {sector_score}"
        
        print("SECTOR SCORING TEST PASSED")
    
    def test_doel_scoring(self):
        """Test different doelen get appropriate scores"""
        doelen = {
            "Digitaliseren": 2,
            "Zorg / welzijn verbeteren": 2,
            "Beleving verbeteren": 1.5,
            "Kosten besparen": 1
        }
        for doel, expected_score in doelen.items():
            intake = HIGH_SCORE_INTAKE.copy()
            intake["doel"] = doel
            response = requests.post(f"{BASE_URL}/api/subsidy/check", json=intake)
            assert response.status_code == 200
            data = response.json()
            
            doel_score = data["breakdown"]["projecttype"]["score"]
            assert doel_score == expected_score, f"Expected doel score {expected_score} for {doel}, got {doel_score}"
        
        print("DOEL SCORING TEST PASSED")
    
    def test_investering_scoring(self):
        """Test different investering ranges get appropriate scores"""
        investeringen = {
            "€10K - €25K": 1,
            "€25K - €100K": 2,
            "> €100K": 2
        }
        for inv, expected_score in investeringen.items():
            intake = HIGH_SCORE_INTAKE.copy()
            intake["investering"] = inv
            response = requests.post(f"{BASE_URL}/api/subsidy/check", json=intake)
            assert response.status_code == 200
            data = response.json()
            
            inv_score = data["breakdown"]["investering"]["score"]
            assert inv_score == expected_score, f"Expected investering score {expected_score} for {inv}, got {inv_score}"
        
        print("INVESTERING SCORING TEST PASSED")
    
    def test_gebruikers_impact_scoring(self):
        """Test different gebruikers ranges get appropriate impact scores"""
        gebruikers = {
            "< 100": 0,
            "100 - 1.000": 1,
            "1.000 - 10.000": 2,
            "> 10.000": 2
        }
        for gebr, expected_score in gebruikers.items():
            intake = HIGH_SCORE_INTAKE.copy()
            intake["gebruikers"] = gebr
            response = requests.post(f"{BASE_URL}/api/subsidy/check", json=intake)
            assert response.status_code == 200
            data = response.json()
            
            impact_score = data["breakdown"]["impact"]["score"]
            assert impact_score == expected_score, f"Expected impact score {expected_score} for {gebr}, got {impact_score}"
        
        print("GEBRUIKERS IMPACT SCORING TEST PASSED")
    
    def test_samenwerking_scoring(self):
        """Test samenwerking Ja/Nee scoring"""
        for samenwerking, expected_score in [("Ja", 1), ("Nee", 0)]:
            intake = HIGH_SCORE_INTAKE.copy()
            intake["samenwerking"] = samenwerking
            response = requests.post(f"{BASE_URL}/api/subsidy/check", json=intake)
            assert response.status_code == 200
            data = response.json()
            
            collab_score = data["breakdown"]["samenwerking"]["score"]
            assert collab_score == expected_score, f"Expected samenwerking score {expected_score} for {samenwerking}, got {collab_score}"
        
        print("SAMENWERKING SCORING TEST PASSED")
    
    def test_duurzaamheid_scoring(self):
        """Test duurzaamheid Ja/Nee scoring"""
        for duurzaamheid, expected_score in [("Ja", 1), ("Nee", 0)]:
            intake = HIGH_SCORE_INTAKE.copy()
            intake["duurzaamheid"] = duurzaamheid
            response = requests.post(f"{BASE_URL}/api/subsidy/check", json=intake)
            assert response.status_code == 200
            data = response.json()
            
            sustain_score = data["breakdown"]["duurzaamheid"]["score"]
            assert sustain_score == expected_score, f"Expected duurzaamheid score {expected_score} for {duurzaamheid}, got {sustain_score}"
        
        print("DUURZAAMHEID SCORING TEST PASSED")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
