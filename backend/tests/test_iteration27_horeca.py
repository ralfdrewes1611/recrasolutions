"""Iteration 27: Horeca flow backend tests."""
import os
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://lease-simulator.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"


@pytest.fixture(scope="module")
def session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


# === LEASE FORMULA ===
def calc_lease(investment):
    if investment <= 0:
        return 0.0
    base = investment + max(investment * 0.10, 500)
    return round(base * 0.0219, 2)


# === HORECA PRODUCTS ===
class TestHorecaProducts:
    def test_get_products_count_32(self, session):
        r = session.get(f"{API}/horeca/products")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        assert len(data) == 32, f"Expected 32 products, got {len(data)}"

    def test_lease_formula_eijsink_pos(self, session):
        r = session.get(f"{API}/horeca/products")
        data = r.json()
        pos = next((p for p in data if p["name"] == "Eijsink POS Touchkassa"), None)
        assert pos is not None
        assert pos["price_purchase"] == 2950
        assert pos["installation_cost"] == 350
        # investment=3300, max(330,500)=500, lease=(3300+500)*0.0219=83.22
        assert pos["price_lease_monthly"] == 83.22

    def test_lease_formula_all_products(self, session):
        r = session.get(f"{API}/horeca/products")
        data = r.json()
        for p in data:
            inv = p["price_purchase"] + p["installation_cost"]
            expected = calc_lease(inv)
            assert p["price_lease_monthly"] == expected, f"Mismatch on {p['name']}: got {p['price_lease_monthly']}, expected {expected}"

    def test_no_raw_margin_in_response(self, session):
        """API should not expose raw 0.0219 multiplier or 0.10 margin."""
        r = session.get(f"{API}/horeca/products")
        # The response should only contain price_lease_monthly, not raw multiplier fields
        text = r.text
        # 'margin' or 'multiplier' shouldn't appear as keys
        data = r.json()
        for p in data:
            assert "lease_multiplier" not in p
            assert "margin" not in p
            assert "lease_margin" not in p


# === SUPPLIERS ===
class TestHorecaSuppliers:
    def test_suppliers_count_7(self, session):
        r = session.get(f"{API}/horeca/suppliers")
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 7

    def test_suppliers_names(self, session):
        r = session.get(f"{API}/horeca/suppliers")
        data = r.json()
        names = {s["name"] for s in data}
        expected = {"Eijsink", "Selecta Vending", "Heineken Tap-installatie",
                    "Shuffly", "Horeca Meubel Centrum", "Rational Keuken Solutions",
                    "Terraz Outdoor"}
        assert expected == names


# === ZONE TYPES ===
class TestHorecaZoneTypes:
    def test_zone_types_count_7(self, session):
        r = session.get(f"{API}/horeca/zone-types")
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 7
        ids = {z["id"] for z in data}
        assert {"bar", "zit", "games", "terras", "keuken", "entree", "routing"} == ids


# === TOP 5 ===
class TestHorecaTop5:
    def test_top5_returns_5(self, session):
        r = session.get(f"{API}/horeca/top5")
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 5

    def test_top5_sorted_by_revenue_per_m2(self, session):
        r = session.get(f"{API}/horeca/top5")
        data = r.json()
        rpms = [p["revenue_per_m2"] for p in data]
        assert rpms == sorted(rpms, reverse=True)

    def test_top5_lease_monthly_field(self, session):
        r = session.get(f"{API}/horeca/top5")
        data = r.json()
        for p in data:
            assert "lease_monthly" in p
            expected = calc_lease(p["investment"])
            assert p["lease_monthly"] == expected


# === CALCULATE REVENUE ===
class TestHorecaCalculateRevenue:
    def test_calculate_with_products(self, session):
        payload = {
            "products": [
                {"product_id": "horeca-0", "quantity": 1},  # Eijsink POS Touchkassa
                {"product_id": "horeca-3", "quantity": 1},  # Eijsink Bestelzuil 22"
            ],
            "operating_hours": 8,
            "operating_days": 30,
            "project": {"setting": "park", "seats_target": 60, "style": "casual"},
        }
        r = session.post(f"{API}/horeca/calculate-revenue", json=payload)
        assert r.status_code == 200
        data = r.json()
        for k in ["total_investment", "total_lease_monthly", "total_monthly_revenue",
                  "break_even_months", "top_performers", "all_products", "suggestions"]:
            assert k in data, f"Missing field {k}"

        # Lease must equal sum of per-product lease
        sum_lease = sum(p["lease_monthly"] for p in data["all_products"])
        assert round(sum_lease, 2) == round(data["total_lease_monthly"], 2)

        # Verify Eijsink POS lease
        pos = next((p for p in data["all_products"] if "POS Touchkassa" in p["product_name"]), None)
        assert pos is not None
        assert pos["lease_monthly"] == 83.22

    def test_calculate_empty_products(self, session):
        payload = {"products": [], "project": {}}
        r = session.post(f"{API}/horeca/calculate-revenue", json=payload)
        assert r.status_code == 200
        data = r.json()
        assert data["total_investment"] == 0
        assert data["total_lease_monthly"] == 0
        assert data["total_monthly_revenue"] == 0
        assert isinstance(data["all_products"], list)
        assert len(data["all_products"]) == 0


# === EIJSINK PARTNER PROFILE ===
class TestEijsinkProfile:
    def test_get_eijsink_profile(self, session):
        r = session.get(f"{API}/partners/profiles/eijsink")
        assert r.status_code == 200
        data = r.json()
        assert data.get("name") == "Eijsink"
        assert "tagline" in data and len(data["tagline"]) > 0
        assert len(data.get("top_producten", [])) == 3
        assert len(data.get("usps", [])) == 6
        # Podcast - Leisure Talk #21 with Jesse
        podcast = data.get("podcast", {})
        assert "Leisure Talk #21" in podcast.get("titel", "")
        assert "Jesse" in podcast.get("gast", "")
        # Trendwatcher quote
        tq = data.get("trendwatcher_quote", {})
        assert "tekst" in tq and len(tq["tekst"]) > 0
        # Stats and deelname
        assert "stats" in data
        assert "deelname" in data and len(data["deelname"]) > 0


# === AUTH ===
class TestAuth:
    def test_login_admin(self, session):
        r = session.post(f"{API}/auth/login", json={
            "username": "AdminRECRA",
            "password": "Welkom123$",
        })
        assert r.status_code == 200, f"Login failed: {r.text}"
        data = r.json()
        # Just verify some indication of success
        assert "user" in data or "token" in data or "access_token" in data or "session" in data or data.get("success") is True
