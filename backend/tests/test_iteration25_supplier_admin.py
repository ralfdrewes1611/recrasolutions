"""
Iteration 25: Supplier Admin Dashboard Tests
- GET /api/suppliers — returns all suppliers with flows field
- GET /api/suppliers?flow=recreatie — filters by flow
- GET /api/suppliers?flow=chalet — filters by chalet flow
- GET /api/suppliers/stats — returns total, per_flow, per_status, categories
- POST /api/suppliers — creates new supplier with flows array
- PUT /api/suppliers/{id} — updates supplier including flows
- DELETE /api/suppliers/{id} — deletes supplier
"""
import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestSupplierCRUD:
    """Supplier CRUD endpoint tests"""
    
    def test_list_suppliers_returns_all(self):
        """GET /api/suppliers returns all suppliers with flows field"""
        response = requests.get(f"{BASE_URL}/api/suppliers")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        assert len(data) >= 5, f"Expected at least 5 seeded suppliers, got {len(data)}"
        
        # Verify each supplier has required fields including flows
        for supplier in data:
            assert "id" in supplier, "Supplier should have id"
            assert "name" in supplier, "Supplier should have name"
            assert "flows" in supplier, "Supplier should have flows field"
            assert isinstance(supplier["flows"], list), "flows should be a list"
        
        print(f"PASS: GET /api/suppliers returned {len(data)} suppliers with flows field")
    
    def test_list_suppliers_filter_by_recreatie_flow(self):
        """GET /api/suppliers?flow=recreatie filters by recreatie flow"""
        response = requests.get(f"{BASE_URL}/api/suppliers?flow=recreatie")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        
        # All returned suppliers should have 'recreatie' in their flows
        for supplier in data:
            assert "recreatie" in supplier.get("flows", []), f"Supplier {supplier['name']} should have recreatie flow"
        
        print(f"PASS: GET /api/suppliers?flow=recreatie returned {len(data)} suppliers with recreatie flow")
    
    def test_list_suppliers_filter_by_chalet_flow(self):
        """GET /api/suppliers?flow=chalet filters by chalet flow"""
        response = requests.get(f"{BASE_URL}/api/suppliers?flow=chalet")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        
        # All returned suppliers should have 'chalet' in their flows
        for supplier in data:
            assert "chalet" in supplier.get("flows", []), f"Supplier {supplier['name']} should have chalet flow"
        
        print(f"PASS: GET /api/suppliers?flow=chalet returned {len(data)} suppliers with chalet flow")
    
    def test_list_suppliers_filter_by_fec_flow(self):
        """GET /api/suppliers?flow=fec filters by fec flow"""
        response = requests.get(f"{BASE_URL}/api/suppliers?flow=fec")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        
        # All returned suppliers should have 'fec' in their flows
        for supplier in data:
            assert "fec" in supplier.get("flows", []), f"Supplier {supplier['name']} should have fec flow"
        
        print(f"PASS: GET /api/suppliers?flow=fec returned {len(data)} suppliers with fec flow")


class TestSupplierStats:
    """Supplier stats endpoint tests"""
    
    def test_supplier_stats_returns_correct_structure(self):
        """GET /api/suppliers/stats returns total, per_flow, per_status, categories"""
        response = requests.get(f"{BASE_URL}/api/suppliers/stats")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        # Verify structure
        assert "total" in data, "Stats should have total"
        assert "per_flow" in data, "Stats should have per_flow"
        assert "per_status" in data, "Stats should have per_status"
        assert "categories" in data, "Stats should have categories"
        
        # Verify per_flow structure
        assert "recreatie" in data["per_flow"], "per_flow should have recreatie"
        assert "chalet" in data["per_flow"], "per_flow should have chalet"
        assert "fec" in data["per_flow"], "per_flow should have fec"
        
        # Verify per_status structure
        assert "verified" in data["per_status"], "per_status should have verified"
        assert "compatible" in data["per_status"], "per_status should have compatible"
        assert "basic" in data["per_status"], "per_status should have basic"
        
        # Verify categories is a list
        assert isinstance(data["categories"], list), "categories should be a list"
        
        # Verify total matches sum of statuses
        total_from_status = sum(data["per_status"].values())
        assert data["total"] == total_from_status, f"Total {data['total']} should match sum of statuses {total_from_status}"
        
        print(f"PASS: GET /api/suppliers/stats returned correct structure - total: {data['total']}, per_flow: {data['per_flow']}, per_status: {data['per_status']}")


class TestSupplierCreate:
    """Supplier creation tests"""
    
    def test_create_supplier_with_flows(self):
        """POST /api/suppliers creates new supplier with flows array"""
        unique_name = f"TEST_Supplier_{uuid.uuid4().hex[:8]}"
        payload = {
            "name": unique_name,
            "address": "Test City, Nederland",
            "lat": 52.0,
            "lng": 5.0,
            "categories": ["slagboom", "camera"],
            "flows": ["recreatie", "chalet"],
            "price_per_km": 0.50,
            "start_fee": 80,
            "hourly_rate_travel": 70,
            "avg_speed_kmh": 75,
            "verified_status": "compatible",
            "contact_email": "test@example.com",
            "contact_phone": "+31612345678",
            "website": "https://test-supplier.nl",
            "notes": "Test supplier for iteration 25"
        }
        
        response = requests.post(f"{BASE_URL}/api/suppliers", json=payload)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        
        # Verify created supplier has all fields
        assert data["name"] == unique_name, "Name should match"
        assert data["flows"] == ["recreatie", "chalet"], "Flows should match"
        assert data["categories"] == ["slagboom", "camera"], "Categories should match"
        assert data["verified_status"] == "compatible", "Status should match"
        assert "id" in data, "Should have generated id"
        assert "created_at" in data, "Should have created_at"
        
        # Verify persistence with GET
        get_response = requests.get(f"{BASE_URL}/api/suppliers/{data['id']}")
        assert get_response.status_code == 200, f"GET should return 200, got {get_response.status_code}"
        
        fetched = get_response.json()
        assert fetched["name"] == unique_name, "Fetched name should match"
        assert fetched["flows"] == ["recreatie", "chalet"], "Fetched flows should match"
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/suppliers/{data['id']}")
        
        print(f"PASS: POST /api/suppliers created supplier with flows: {data['flows']}")
        return data["id"]
    
    def test_create_supplier_with_single_flow(self):
        """POST /api/suppliers with single flow in array"""
        unique_name = f"TEST_SingleFlow_{uuid.uuid4().hex[:8]}"
        payload = {
            "name": unique_name,
            "flows": ["fec"],
            "categories": ["attracties"],
            "verified_status": "basic"
        }
        
        response = requests.post(f"{BASE_URL}/api/suppliers", json=payload)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert data["flows"] == ["fec"], "Single flow should be preserved"
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/suppliers/{data['id']}")
        
        print(f"PASS: Created supplier with single flow: {data['flows']}")
    
    def test_create_supplier_with_all_flows(self):
        """POST /api/suppliers with all three flows"""
        unique_name = f"TEST_AllFlows_{uuid.uuid4().hex[:8]}"
        payload = {
            "name": unique_name,
            "flows": ["recreatie", "chalet", "fec"],
            "categories": ["verlichting"],
            "verified_status": "verified"
        }
        
        response = requests.post(f"{BASE_URL}/api/suppliers", json=payload)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert set(data["flows"]) == {"recreatie", "chalet", "fec"}, "All flows should be preserved"
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/suppliers/{data['id']}")
        
        print(f"PASS: Created supplier with all flows: {data['flows']}")


class TestSupplierUpdate:
    """Supplier update tests"""
    
    def test_update_supplier_flows(self):
        """PUT /api/suppliers/{id} updates supplier including flows"""
        # First create a supplier
        unique_name = f"TEST_Update_{uuid.uuid4().hex[:8]}"
        create_payload = {
            "name": unique_name,
            "flows": ["recreatie"],
            "categories": ["wifi"],
            "verified_status": "basic"
        }
        
        create_response = requests.post(f"{BASE_URL}/api/suppliers", json=create_payload)
        assert create_response.status_code == 200
        supplier_id = create_response.json()["id"]
        
        # Update the supplier
        update_payload = {
            "flows": ["recreatie", "chalet", "fec"],
            "verified_status": "verified",
            "contact_email": "updated@example.com"
        }
        
        update_response = requests.put(f"{BASE_URL}/api/suppliers/{supplier_id}", json=update_payload)
        assert update_response.status_code == 200, f"Expected 200, got {update_response.status_code}"
        
        updated = update_response.json()
        assert set(updated["flows"]) == {"recreatie", "chalet", "fec"}, "Flows should be updated"
        assert updated["verified_status"] == "verified", "Status should be updated"
        assert updated["contact_email"] == "updated@example.com", "Email should be updated"
        assert updated["name"] == unique_name, "Name should remain unchanged"
        
        # Verify persistence
        get_response = requests.get(f"{BASE_URL}/api/suppliers/{supplier_id}")
        fetched = get_response.json()
        assert set(fetched["flows"]) == {"recreatie", "chalet", "fec"}, "Fetched flows should match update"
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/suppliers/{supplier_id}")
        
        print(f"PASS: PUT /api/suppliers/{supplier_id} updated flows successfully")
    
    def test_update_supplier_partial(self):
        """PUT /api/suppliers/{id} with partial update"""
        # Create supplier
        unique_name = f"TEST_Partial_{uuid.uuid4().hex[:8]}"
        create_response = requests.post(f"{BASE_URL}/api/suppliers", json={
            "name": unique_name,
            "flows": ["recreatie"],
            "verified_status": "basic"
        })
        supplier_id = create_response.json()["id"]
        
        # Partial update - only name
        update_response = requests.put(f"{BASE_URL}/api/suppliers/{supplier_id}", json={
            "name": f"{unique_name}_Updated"
        })
        assert update_response.status_code == 200
        
        updated = update_response.json()
        assert updated["name"] == f"{unique_name}_Updated", "Name should be updated"
        assert updated["flows"] == ["recreatie"], "Flows should remain unchanged"
        
        # Cleanup
        requests.delete(f"{BASE_URL}/api/suppliers/{supplier_id}")
        
        print("PASS: Partial update preserves unchanged fields")


class TestSupplierDelete:
    """Supplier deletion tests"""
    
    def test_delete_supplier(self):
        """DELETE /api/suppliers/{id} deletes supplier"""
        # Create supplier
        unique_name = f"TEST_Delete_{uuid.uuid4().hex[:8]}"
        create_response = requests.post(f"{BASE_URL}/api/suppliers", json={
            "name": unique_name,
            "flows": ["recreatie"]
        })
        supplier_id = create_response.json()["id"]
        
        # Delete
        delete_response = requests.delete(f"{BASE_URL}/api/suppliers/{supplier_id}")
        assert delete_response.status_code == 200, f"Expected 200, got {delete_response.status_code}"
        
        data = delete_response.json()
        assert data.get("deleted") == True, "Should return deleted: true"
        
        # Verify deletion
        get_response = requests.get(f"{BASE_URL}/api/suppliers/{supplier_id}")
        assert get_response.status_code == 404, "Deleted supplier should return 404"
        
        print(f"PASS: DELETE /api/suppliers/{supplier_id} removed supplier")
    
    def test_delete_nonexistent_supplier(self):
        """DELETE /api/suppliers/{id} returns 404 for nonexistent"""
        fake_id = f"nonexistent-{uuid.uuid4().hex}"
        response = requests.delete(f"{BASE_URL}/api/suppliers/{fake_id}")
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        
        print("PASS: DELETE nonexistent supplier returns 404")


class TestSupplierGet:
    """Supplier get by ID tests"""
    
    def test_get_supplier_by_id(self):
        """GET /api/suppliers/{id} returns specific supplier"""
        # First get list to find an existing supplier
        list_response = requests.get(f"{BASE_URL}/api/suppliers")
        suppliers = list_response.json()
        
        if len(suppliers) > 0:
            supplier_id = suppliers[0]["id"]
            response = requests.get(f"{BASE_URL}/api/suppliers/{supplier_id}")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            assert data["id"] == supplier_id, "ID should match"
            assert "name" in data, "Should have name"
            assert "flows" in data, "Should have flows"
            
            print(f"PASS: GET /api/suppliers/{supplier_id} returned supplier: {data['name']}")
        else:
            pytest.skip("No suppliers in database to test")
    
    def test_get_nonexistent_supplier(self):
        """GET /api/suppliers/{id} returns 404 for nonexistent"""
        fake_id = f"nonexistent-{uuid.uuid4().hex}"
        response = requests.get(f"{BASE_URL}/api/suppliers/{fake_id}")
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        
        print("PASS: GET nonexistent supplier returns 404")


class TestSeededSuppliers:
    """Tests for seeded supplier data"""
    
    def test_seeded_suppliers_have_flows(self):
        """Verify seeded suppliers have been migrated with flows"""
        response = requests.get(f"{BASE_URL}/api/suppliers")
        suppliers = response.json()
        
        # Check known seeded suppliers
        known_suppliers = {
            "Nice Benelux": ["recreatie"],
            "Ubiquiti / UI.com Distributeur NL": ["recreatie", "fec"],
            "Sanitec Recreatie": ["recreatie"],
            "Adyen Payments": ["recreatie", "fec"],
            "Van Loon Verlichting": ["recreatie", "chalet", "fec"],
        }
        
        for supplier in suppliers:
            if supplier["name"] in known_suppliers:
                expected_flows = known_suppliers[supplier["name"]]
                actual_flows = supplier.get("flows", [])
                assert set(actual_flows) == set(expected_flows), f"{supplier['name']} should have flows {expected_flows}, got {actual_flows}"
        
        print("PASS: Seeded suppliers have correct flows assigned")
    
    def test_seeded_suppliers_have_website(self):
        """Verify seeded suppliers have website field"""
        response = requests.get(f"{BASE_URL}/api/suppliers")
        suppliers = response.json()
        
        for supplier in suppliers:
            assert "website" in supplier, f"Supplier {supplier['name']} should have website field"
        
        print("PASS: All suppliers have website field")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
