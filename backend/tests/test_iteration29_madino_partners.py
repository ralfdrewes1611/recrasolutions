"""Iteration 29 — Madino partner + MongoDB-backed partner CRUD tests."""
import os
import pytest
import requests

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/') or "https://lease-simulator.preview.emergentagent.com"
EXPECTED_IDS = {"ticra-outdoor", "kunert-group", "arcabo", "campsolutions",
                "bbs-systeembouw", "eijsink", "madino"}


# ---------- Public partner profile endpoints ----------
class TestPartnerProfilesPublic:
    def test_list_profiles_contains_seven_including_madino(self):
        r = requests.get(f"{BASE_URL}/api/partners/profiles", timeout=15)
        assert r.status_code == 200
        data = r.json()
        ids = {p["id"] for p in data}
        assert EXPECTED_IDS.issubset(ids), f"Missing IDs: {EXPECTED_IDS - ids}"
        # madino must have the expected summary fields
        madino_summary = next(p for p in data if p["id"] == "madino")
        assert madino_summary["name"] == "Madino"
        assert "terras" in madino_summary["tagline"].lower()

    def test_madino_detail_full_profile(self):
        r = requests.get(f"{BASE_URL}/api/partners/profiles/madino", timeout=15)
        assert r.status_code == 200
        p = r.json()
        assert p["name"] == "Madino"
        assert "terras" in p["tagline"].lower()
        assert len(p["usps"]) >= 6
        assert len(p["top_producten"]) >= 3
        product_ids = {tp["id"] for tp in p["top_producten"]}
        assert {"terras-madino-lounge", "terras-madino-firepit", "terras-madino-dining"}.issubset(product_ids)
        # stats
        s = p["stats"]
        assert s["parken_actief"] == "75+"
        assert s["jaren_ervaring"] == "12+"
        assert s["producten_geinstalleerd"] == "1.800+"
        assert s["klanttevredenheid"] == "4.7/5"
        # podcast
        assert "Leisure Talk #23" in p["podcast"]["titel"]
        # trendwatcher
        assert p["trendwatcher_quote"]["auteur"] == "Richard Otten"
        # events
        assert len(p["deelname"]) >= 4

    def test_no_mongo_id_leak(self):
        r = requests.get(f"{BASE_URL}/api/partners/profiles/madino", timeout=15)
        assert r.status_code == 200
        assert "_id" not in r.json()


# ---------- Chalet engine: terras category ----------
class TestChaletTerrasCategory:
    def test_terras_has_six_options_with_madino(self):
        r = requests.get(f"{BASE_URL}/api/chalet/upgrade-options/chalet", timeout=15)
        assert r.status_code == 200
        data = r.json()
        terras = data.get("terras")
        assert terras is not None, f"No terras key in {list(data.keys())}"
        assert len(terras) == 6, f"Expected 6 terras options, got {len(terras)}"
        ids = {o["id"] for o in terras}
        expected_madino = {"terras-madino-bistro", "terras-madino-lounge", "terras-madino-dining",
                           "terras-madino-loungebed", "terras-madino-firepit"}
        assert expected_madino.issubset(ids), f"Missing: {expected_madino - ids}"
        assert "terras-geen" in ids
        # Each Madino option must reference Madino supplier and have image
        for o in terras:
            if o["id"].startswith("terras-madino"):
                assert o.get("supplier") == "Madino"
                assert o.get("image"), f"Missing image on {o['id']}"
        # Check specific prices
        by_id = {o["id"]: o for o in terras}
        assert by_id["terras-madino-bistro"]["price"] == 1450
        assert by_id["terras-madino-lounge"]["price"] == 3950
        assert by_id["terras-madino-dining"]["price"] == 4750
        assert by_id["terras-madino-loungebed"]["price"] == 2750
        assert by_id["terras-madino-firepit"]["price"] == 5450


# ---------- Admin CRUD ----------
class TestPartnerAdminCRUD:
    def test_admin_list_full_seven(self):
        r = requests.get(f"{BASE_URL}/api/partners/admin/profiles", timeout=15)
        assert r.status_code == 200
        data = r.json()
        assert len(data) >= 7
        # Full fields per partner
        for p in data:
            assert "usps" in p
            assert "top_producten" in p
            assert "stats" in p

    def test_create_update_delete_flow(self):
        # Create
        payload = {"name": "Test Partner X", "tagline": "x test", "categorieen": ["test"]}
        r = requests.post(f"{BASE_URL}/api/partners/admin/profiles", json=payload, timeout=15)
        assert r.status_code == 200
        body = r.json()
        assert body.get("success") is True
        assert body["id"] == "test-partner-x"

        # Update
        upd = {"name": "Test Partner X", "tagline": "x test updated", "categorieen": ["test"],
               "usps": ["USP-A", "USP-B"]}
        r2 = requests.put(f"{BASE_URL}/api/partners/admin/profiles/test-partner-x", json=upd, timeout=15)
        assert r2.status_code == 200
        assert r2.json().get("success") is True

        # GET to verify persistence
        r3 = requests.get(f"{BASE_URL}/api/partners/profiles/test-partner-x", timeout=15)
        assert r3.status_code == 200
        assert r3.json()["tagline"] == "x test updated"
        assert "USP-A" in r3.json()["usps"]

        # Delete
        r4 = requests.delete(f"{BASE_URL}/api/partners/admin/profiles/test-partner-x", timeout=15)
        assert r4.status_code == 200
        assert r4.json().get("success") is True

        # Verify gone
        r5 = requests.get(f"{BASE_URL}/api/partners/profiles/test-partner-x", timeout=15)
        # endpoint returns {"error": ...} when not found
        assert r5.status_code == 200
        assert r5.json().get("error")

    def test_create_duplicate_id_returns_error(self):
        # Try to create with name conflicting with existing 'madino' id
        payload = {"name": "Madino", "tagline": "dup", "categorieen": []}
        r = requests.post(f"{BASE_URL}/api/partners/admin/profiles", json=payload, timeout=15)
        assert r.status_code == 200
        body = r.json()
        assert "error" in body
        assert body["id"] == "madino"


# ---------- Cleanup ----------
def teardown_module(module):
    for slug in ["test-partner-x", "test-demo"]:
        try:
            requests.delete(f"{BASE_URL}/api/partners/admin/profiles/{slug}", timeout=10)
        except Exception:
            pass
