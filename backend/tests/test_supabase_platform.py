"""
Test Supabase Platform Integration - Iteration 18
Tests: Health, Sessions, Benchmark, Scenarios, Leads, Partners
"""
import pytest
import requests
import os
import uuid
from datetime import datetime

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://recra-config.preview.emergentagent.com').rstrip('/')

class TestPlatformHealth:
    """Platform health endpoint tests"""
    
    def test_platform_health_connected(self):
        """GET /api/platform/health should return status:connected, tables_ready:true"""
        response = requests.get(f"{BASE_URL}/api/platform/health")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "connected", f"Expected status 'connected', got {data.get('status')}"
        assert data.get("tables_ready") == True, f"Expected tables_ready True, got {data.get('tables_ready')}"
        assert data.get("supabase") == True, f"Expected supabase True, got {data.get('supabase')}"
        print(f"✓ Platform health: {data}")


class TestPlatformSessions:
    """Session tracking tests"""
    
    def test_start_session(self):
        """POST /api/platform/sessions/start should create a new session in Supabase"""
        session_id = f"test-session-{uuid.uuid4().hex[:8]}"
        payload = {
            "session_id": session_id,
            "flow_type": "recreatie"
        }
        response = requests.post(f"{BASE_URL}/api/platform/sessions/start", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data.get("ok") == True, f"Expected ok=True, got {data}"
        assert "session" in data, "Response should contain session data"
        session = data["session"]
        assert session.get("session_id") == session_id
        assert session.get("flow_type") == "recreatie"
        assert session.get("status") == "active"
        assert session.get("phase") == "orientatie"
        print(f"✓ Session created: {session_id}")
        return session_id
    
    def test_start_session_chalet_flow(self):
        """POST /api/platform/sessions/start with chalet flow"""
        session_id = f"test-chalet-{uuid.uuid4().hex[:8]}"
        payload = {
            "session_id": session_id,
            "flow_type": "chalet"
        }
        response = requests.post(f"{BASE_URL}/api/platform/sessions/start", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data.get("ok") == True
        assert data["session"]["flow_type"] == "chalet"
        print(f"✓ Chalet session created: {session_id}")
    
    def test_update_session(self):
        """POST /api/platform/sessions/update should update session data"""
        # First create a session
        session_id = f"test-update-{uuid.uuid4().hex[:8]}"
        requests.post(f"{BASE_URL}/api/platform/sessions/start", json={
            "session_id": session_id,
            "flow_type": "recreatie"
        })
        
        # Update the session
        update_payload = {
            "session_id": session_id,
            "lead_score": 75,
            "phase": "vergelijking",
            "budget_range": "€50.000 - €100.000",
            "contact_email": "test@example.com",
            "contact_name": "Test User"
        }
        response = requests.post(f"{BASE_URL}/api/platform/sessions/update", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data.get("ok") == True
        print(f"✓ Session updated: {session_id}")


class TestPlatformBenchmark:
    """Benchmark data tests"""
    
    def test_record_benchmark_model_selected(self):
        """POST /api/platform/benchmark/record should store benchmark data"""
        payload = {
            "flow_type": "chalet",
            "metric_type": "model_selected",
            "metric_key": "Plat 12",
            "metric_value": 1,
            "meta": {"session_id": f"test-{uuid.uuid4().hex[:8]}"}
        }
        response = requests.post(f"{BASE_URL}/api/platform/benchmark/record", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data.get("ok") == True, f"Expected ok=True, got {data}"
        print(f"✓ Benchmark recorded: model_selected - Plat 12")
    
    def test_record_benchmark_supplier_selected(self):
        """POST /api/platform/benchmark/record for supplier selection"""
        payload = {
            "flow_type": "chalet",
            "metric_type": "supplier_selected",
            "metric_key": "Kunert Group",
            "metric_value": 1,
            "meta": {}
        }
        response = requests.post(f"{BASE_URL}/api/platform/benchmark/record", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data.get("ok") == True
        print(f"✓ Benchmark recorded: supplier_selected - Kunert Group")
    
    def test_record_benchmark_investment(self):
        """POST /api/platform/benchmark/record for total investment"""
        payload = {
            "flow_type": "recreatie",
            "metric_type": "total_investment",
            "metric_key": "project_total",
            "metric_value": 85000,
            "meta": {}
        }
        response = requests.post(f"{BASE_URL}/api/platform/benchmark/record", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data.get("ok") == True
        print(f"✓ Benchmark recorded: total_investment - €85.000")
    
    def test_get_benchmark_trends(self):
        """GET /api/platform/benchmark/trends should return trends with top_models and top_suppliers"""
        response = requests.get(f"{BASE_URL}/api/platform/benchmark/trends")
        assert response.status_code == 200
        data = response.json()
        
        # Verify structure
        assert "top_models" in data, "Response should contain top_models"
        assert "top_suppliers" in data, "Response should contain top_suppliers"
        assert "avg_investment" in data, "Response should contain avg_investment"
        assert "total_sessions" in data, "Response should contain total_sessions"
        assert "total_data_points" in data, "Response should contain total_data_points"
        
        # Verify types
        assert isinstance(data["top_models"], list)
        assert isinstance(data["top_suppliers"], list)
        assert isinstance(data["avg_investment"], (int, float))
        
        print(f"✓ Benchmark trends: {len(data['top_models'])} models, {len(data['top_suppliers'])} suppliers, avg €{data['avg_investment']}")
    
    def test_get_benchmark_trends_filtered(self):
        """GET /api/platform/benchmark/trends?flow_type=chalet should filter by flow"""
        response = requests.get(f"{BASE_URL}/api/platform/benchmark/trends?flow_type=chalet")
        assert response.status_code == 200
        data = response.json()
        assert "top_models" in data
        print(f"✓ Benchmark trends (chalet): {len(data['top_models'])} models")


class TestPlatformScenarios:
    """Scenario comparison tests"""
    
    def test_save_scenario_basis(self):
        """POST /api/platform/scenarios/save should create scenario"""
        payload = {
            "session_id": f"test-scenario-{uuid.uuid4().hex[:8]}",
            "name": "Test Basis Scenario",
            "flow_type": "chalet",
            "scenario_type": "basis",
            "config_data": {"models": ["Plat 12"], "count": 10},
            "total_investment": 749500,
            "total_lease_monthly": 13490,
            "annual_revenue": 180000,
            "roi_years": 4.2,
            "cashflow_monthly": 1500,
            "notes": "Test scenario for iteration 18"
        }
        response = requests.post(f"{BASE_URL}/api/platform/scenarios/save", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data.get("ok") == True, f"Expected ok=True, got {data}"
        assert "scenario" in data, "Response should contain scenario"
        scenario = data["scenario"]
        assert scenario.get("name") == "Test Basis Scenario"
        assert scenario.get("scenario_type") == "basis"
        assert scenario.get("total_investment") == 749500
        print(f"✓ Scenario saved: {scenario.get('name')} - €{scenario.get('total_investment')}")
        return scenario.get("id")
    
    def test_save_scenario_luxe(self):
        """POST /api/platform/scenarios/save with luxe type"""
        payload = {
            "name": "Test Luxe Scenario",
            "flow_type": "chalet",
            "scenario_type": "luxe",
            "total_investment": 1250000,
            "total_lease_monthly": 22500,
            "annual_revenue": 320000,
            "roi_years": 3.9,
            "cashflow_monthly": 4200
        }
        response = requests.post(f"{BASE_URL}/api/platform/scenarios/save", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data.get("ok") == True
        assert data["scenario"]["scenario_type"] == "luxe"
        print(f"✓ Luxe scenario saved")
    
    def test_save_scenario_max_bezetting(self):
        """POST /api/platform/scenarios/save with max_bezetting type"""
        payload = {
            "name": "Test Max Bezetting",
            "flow_type": "chalet",
            "scenario_type": "max_bezetting",
            "total_investment": 1875000,
            "total_lease_monthly": 33750,
            "annual_revenue": 480000,
            "roi_years": 3.5,
            "cashflow_monthly": 6250
        }
        response = requests.post(f"{BASE_URL}/api/platform/scenarios/save", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data.get("ok") == True
        assert data["scenario"]["scenario_type"] == "max_bezetting"
        print(f"✓ Max bezetting scenario saved")
    
    def test_get_all_scenarios(self):
        """GET /api/platform/scenarios should return all scenarios"""
        response = requests.get(f"{BASE_URL}/api/platform/scenarios")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        print(f"✓ All scenarios: {len(data)} scenarios found")
        
        # Verify scenario structure if any exist
        if len(data) > 0:
            scenario = data[0]
            assert "name" in scenario
            assert "scenario_type" in scenario
            assert "total_investment" in scenario
            print(f"  First scenario: {scenario.get('name')} ({scenario.get('scenario_type')})")


class TestPlatformLeads:
    """Lead scoring tests"""
    
    def test_get_leads(self):
        """GET /api/platform/leads should return lead data"""
        response = requests.get(f"{BASE_URL}/api/platform/leads")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        print(f"✓ Leads: {len(data)} leads found")
        
        # Verify lead structure if any exist
        if len(data) > 0:
            lead = data[0]
            assert "session_id" in lead
            assert "flow_type" in lead
            assert "phase" in lead
            assert "status" in lead
            print(f"  First lead: {lead.get('session_id')} - {lead.get('phase')} - {lead.get('status')}")
    
    def test_get_leads_filtered_by_status(self):
        """GET /api/platform/leads?status=active should filter by status"""
        response = requests.get(f"{BASE_URL}/api/platform/leads?status=active")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # All returned leads should have status=active
        for lead in data:
            assert lead.get("status") == "active", f"Expected status 'active', got {lead.get('status')}"
        print(f"✓ Active leads: {len(data)} found")
    
    def test_get_leads_filtered_by_min_score(self):
        """GET /api/platform/leads?min_score=50 should filter by minimum score"""
        response = requests.get(f"{BASE_URL}/api/platform/leads?min_score=50")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # All returned leads should have lead_score >= 50
        for lead in data:
            assert lead.get("lead_score", 0) >= 50, f"Expected lead_score >= 50, got {lead.get('lead_score')}"
        print(f"✓ High-score leads (>=50): {len(data)} found")


class TestPlatformPartners:
    """Partner interaction tracking tests"""
    
    def test_track_partner_view(self):
        """POST /api/platform/partners/track should track supplier interaction"""
        payload = {
            "supplier_id": "kunert",
            "supplier_name": "Kunert Group",
            "flow_type": "chalet",
            "interaction_type": "view",
            "session_id": f"test-partner-{uuid.uuid4().hex[:8]}"
        }
        response = requests.post(f"{BASE_URL}/api/platform/partners/track", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data.get("ok") == True, f"Expected ok=True, got {data}"
        print(f"✓ Partner interaction tracked: view - Kunert Group")
    
    def test_track_partner_select(self):
        """POST /api/platform/partners/track with select interaction"""
        payload = {
            "supplier_id": "campsolutions",
            "supplier_name": "Campsolutions",
            "flow_type": "chalet",
            "interaction_type": "select"
        }
        response = requests.post(f"{BASE_URL}/api/platform/partners/track", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data.get("ok") == True
        print(f"✓ Partner interaction tracked: select - Campsolutions")


class TestMigrationSQL:
    """Migration SQL endpoint test"""
    
    def test_get_migration_sql(self):
        """GET /api/platform/migration-sql should return SQL script"""
        response = requests.get(f"{BASE_URL}/api/platform/migration-sql")
        assert response.status_code == 200
        data = response.json()
        assert "sql" in data, "Response should contain sql"
        assert "instructions" in data, "Response should contain instructions"
        assert "CREATE TABLE" in data["sql"], "SQL should contain CREATE TABLE statements"
        assert "configurator_sessions" in data["sql"], "SQL should create configurator_sessions table"
        assert "scenarios" in data["sql"], "SQL should create scenarios table"
        print(f"✓ Migration SQL available ({len(data['sql'])} chars)")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
