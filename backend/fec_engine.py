"""
FEC Revenue Engine — Business Simulator for Fun & Entertainment Centers
Handles FEC-specific products, zones, revenue calculations, and AI rules.
"""
import uuid
import math
import logging
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from fastapi import APIRouter

logger = logging.getLogger(__name__)

fec_router = APIRouter(prefix="/fec", tags=["FEC Engine"])

# ==================== FEC MODELS ====================

class FecZone(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str  # entree, arcade, horeca, karting, interactive, indoor_play, routing
    name: str
    area_m2: float
    expected_capacity: int = 0
    color: str = "#70C26C"

class FecProject(BaseModel):
    total_area_m2: float = 500
    ceiling_height_m: float = 5.0
    target_audience: str = "families"  # families | teens | all_ages | corporate
    budget_range: str = "midrange"  # budget | midrange | premium
    zones: List[FecZone] = Field(default_factory=list)
    operating_hours: float = 10  # hours/day
    operating_days: int = 30  # days/month
    ticket_price_avg: float = 15.0

class FecProductRevenue(BaseModel):
    product_id: str
    product_name: str
    category: str
    supplier: str
    footprint_m2: float
    investment: float
    revenue_per_hour: float
    capacity_per_hour: int
    daily_revenue: float
    monthly_revenue: float
    roi_months: float
    revenue_per_m2: float

class FecRevenueReport(BaseModel):
    total_investment: float
    total_monthly_revenue: float
    total_daily_revenue: float
    break_even_months: float
    revenue_per_m2_month: float
    top_performers: List[FecProductRevenue]
    all_products: List[FecProductRevenue]
    zone_summary: List[Dict[str, Any]]
    suggestions: List[Dict[str, str]]

# ==================== FEC ZONE TYPES ====================

FEC_ZONE_TYPES = [
    {"id": "entree", "name": "Entree & Ticketing", "color": "#6366f1", "min_m2": 20, "revenue_factor": 0},
    {"id": "arcade", "name": "Arcade & Games", "color": "#8b5cf6", "min_m2": 40, "revenue_factor": 1.2},
    {"id": "karting", "name": "Karting", "color": "#ef4444", "min_m2": 200, "revenue_factor": 1.8},
    {"id": "interactive", "name": "Interactive Experiences", "color": "#f59e0b", "min_m2": 60, "revenue_factor": 1.5},
    {"id": "indoor_play", "name": "Indoor Speelparadijs", "color": "#10b981", "min_m2": 100, "revenue_factor": 1.0},
    {"id": "horeca", "name": "Food & Beverage", "color": "#f97316", "min_m2": 30, "revenue_factor": 0.8},
    {"id": "routing", "name": "Routing & Looppad", "color": "#94a3b8", "min_m2": 0, "revenue_factor": 0},
]

# ==================== FEC SUPPLIERS ====================

FEC_SUPPLIERS = [
    {
        "id": "sup-xwall",
        "name": "X-Wall",
        "address": "Utrecht, Nederland",
        "lat": 52.0907,
        "lng": 5.1214,
        "categories": ["interactive"],
        "specialization": "Interactieve klim- en spelwanden",
        "price_per_km": 1.80,
        "start_fee": 250,
        "hourly_rate_travel": 75,
    },
    {
        "id": "sup-shuffly",
        "name": "Shuffly",
        "address": "Amsterdam, Nederland",
        "lat": 52.3676,
        "lng": 4.9041,
        "categories": ["arcade", "interactive"],
        "specialization": "Shuffle boards & interactieve games",
        "price_per_km": 1.50,
        "start_fee": 200,
        "hourly_rate_travel": 65,
    },
    {
        "id": "sup-heemskerk",
        "name": "Heemskerk Play",
        "address": "Heemskerk, Nederland",
        "lat": 52.5069,
        "lng": 4.6609,
        "categories": ["indoor_play"],
        "specialization": "Indoor speeltoestellen & speelparadijzen",
        "price_per_km": 2.00,
        "start_fee": 300,
        "hourly_rate_travel": 80,
    },
    {
        "id": "sup-prokarting",
        "name": "Pro Karting",
        "address": "Eindhoven, Nederland",
        "lat": 51.4416,
        "lng": 5.4697,
        "categories": ["karting"],
        "specialization": "Professionele kartbanen & elektrische karts",
        "price_per_km": 2.50,
        "start_fee": 500,
        "hourly_rate_travel": 90,
    },
    {
        "id": "sup-timemission",
        "name": "Time Mission",
        "address": "Den Haag, Nederland",
        "lat": 52.0705,
        "lng": 4.3007,
        "categories": ["interactive", "arcade"],
        "specialization": "Escape rooms & immersive experiences",
        "price_per_km": 1.60,
        "start_fee": 350,
        "hourly_rate_travel": 70,
    },
]

# ==================== FEC PRODUCTS ====================

FEC_PRODUCTS = [
    # === ARCADE & GAMES ===
    {
        "name": "Shuffleboard Pro Table",
        "category": "arcade",
        "supplier": "Shuffly",
        "description": "Professionele shuffleboard tafel 6m, LED scoring, multiplayer",
        "footprint_m2": 8,
        "min_height_m": 2.5,
        "price_purchase": 4500,
        "revenue_per_hour": 25,
        "capacity_per_hour": 8,
        "installation_cost": 500,
        "tier": "midrange",
    },
    {
        "name": "Arcade Game Wall (6 units)",
        "category": "arcade",
        "supplier": "Shuffly",
        "description": "6 retro + moderne arcade games, muntloos/QR betaling",
        "footprint_m2": 12,
        "min_height_m": 2.5,
        "price_purchase": 18000,
        "revenue_per_hour": 60,
        "capacity_per_hour": 18,
        "installation_cost": 1500,
        "tier": "premium",
    },
    {
        "name": "Air Hockey Premium",
        "category": "arcade",
        "supplier": "Shuffly",
        "description": "LED air hockey tafel, digitale score, muntloos",
        "footprint_m2": 4,
        "min_height_m": 2.5,
        "price_purchase": 3200,
        "revenue_per_hour": 20,
        "capacity_per_hour": 4,
        "installation_cost": 300,
        "tier": "budget",
    },
    # === KARTING ===
    {
        "name": "Elektrische Kartbaan (8 karts)",
        "category": "karting",
        "supplier": "Pro Karting",
        "description": "Compleet pakket: 8 e-karts, timing systeem, vangrails, 200m² circuit",
        "footprint_m2": 200,
        "min_height_m": 3.5,
        "price_purchase": 95000,
        "revenue_per_hour": 240,
        "capacity_per_hour": 16,
        "installation_cost": 15000,
        "tier": "premium",
    },
    {
        "name": "Mini Kart Track (kids)",
        "category": "karting",
        "supplier": "Pro Karting",
        "description": "Kinderkartbaan: 6 mini e-karts, 120m² circuit, leeftijd 4-10",
        "footprint_m2": 120,
        "min_height_m": 3.0,
        "price_purchase": 45000,
        "revenue_per_hour": 120,
        "capacity_per_hour": 12,
        "installation_cost": 8000,
        "tier": "midrange",
    },
    # === INTERACTIVE EXPERIENCES ===
    {
        "name": "X-Wall Interactieve Klimwand",
        "category": "interactive",
        "supplier": "X-Wall",
        "description": "AR-geprojecteerde klimmuur met 6 games, 3m hoog, auto-belay",
        "footprint_m2": 15,
        "min_height_m": 4.0,
        "price_purchase": 35000,
        "revenue_per_hour": 80,
        "capacity_per_hour": 12,
        "installation_cost": 5000,
        "tier": "premium",
    },
    {
        "name": "Escape Room Module",
        "category": "interactive",
        "supplier": "Time Mission",
        "description": "Turnkey escape room: thema, puzzels, electronica, timer, 20m²",
        "footprint_m2": 20,
        "min_height_m": 2.8,
        "price_purchase": 28000,
        "revenue_per_hour": 65,
        "capacity_per_hour": 6,
        "installation_cost": 4000,
        "tier": "premium",
    },
    {
        "name": "VR Experience Pod (4 stations)",
        "category": "interactive",
        "supplier": "Time Mission",
        "description": "4 VR-stations met bril, controllers, 12+ games, multiplayer",
        "footprint_m2": 16,
        "min_height_m": 3.0,
        "price_purchase": 22000,
        "revenue_per_hour": 55,
        "capacity_per_hour": 8,
        "installation_cost": 2000,
        "tier": "midrange",
    },
    # === INDOOR PLAY ===
    {
        "name": "Mega Speeltoestel Indoor",
        "category": "indoor_play",
        "supplier": "Heemskerk Play",
        "description": "3 verdiepingen, glijbanen, ballenbak, netten, 100m²",
        "footprint_m2": 100,
        "min_height_m": 5.0,
        "price_purchase": 65000,
        "revenue_per_hour": 100,
        "capacity_per_hour": 40,
        "installation_cost": 12000,
        "tier": "premium",
    },
    {
        "name": "Toddler Play Zone",
        "category": "indoor_play",
        "supplier": "Heemskerk Play",
        "description": "Veilige speelzone 0-4 jaar, zachte elementen, minibalenbak",
        "footprint_m2": 30,
        "min_height_m": 2.5,
        "price_purchase": 15000,
        "revenue_per_hour": 25,
        "capacity_per_hour": 15,
        "installation_cost": 3000,
        "tier": "budget",
    },
    {
        "name": "Trampoline Park Zone",
        "category": "indoor_play",
        "supplier": "Heemskerk Play",
        "description": "8 trampolines + dodgeball court, foam pit, 80m²",
        "footprint_m2": 80,
        "min_height_m": 5.0,
        "price_purchase": 48000,
        "revenue_per_hour": 90,
        "capacity_per_hour": 24,
        "installation_cost": 8000,
        "tier": "midrange",
    },
    # === FOOD & BEVERAGE ===
    {
        "name": "Snackbar Module Compleet",
        "category": "horeca",
        "supplier": "Shuffly",
        "description": "Frietketel, tosti, softijs, kassa, toonbank — plug & play",
        "footprint_m2": 15,
        "min_height_m": 2.5,
        "price_purchase": 22000,
        "revenue_per_hour": 80,
        "capacity_per_hour": 30,
        "installation_cost": 5000,
        "tier": "midrange",
    },
    {
        "name": "Self-Service Drinks Station",
        "category": "horeca",
        "supplier": "Shuffly",
        "description": "4 taps + koffie + frisdrank, contactloos betalen, 3m²",
        "footprint_m2": 3,
        "min_height_m": 2.5,
        "price_purchase": 8500,
        "revenue_per_hour": 35,
        "capacity_per_hour": 40,
        "installation_cost": 1500,
        "tier": "budget",
    },
    {
        "name": "Premium Restaurant Setup",
        "category": "horeca",
        "supplier": "Shuffly",
        "description": "Volledige keuken + 40 zitplaatsen + bar, 60m²",
        "footprint_m2": 60,
        "min_height_m": 3.0,
        "price_purchase": 85000,
        "revenue_per_hour": 200,
        "capacity_per_hour": 60,
        "installation_cost": 15000,
        "tier": "premium",
    },
]


# ==================== REVENUE ENGINE ====================

def calculate_fec_revenue(
    products_selected: list,
    operating_hours: float = 10,
    operating_days: int = 30,
) -> FecRevenueReport:
    """Core revenue engine: calculates ROI per product and overall."""
    all_products = []
    total_investment = 0
    total_monthly_revenue = 0
    total_daily_revenue = 0

    for sel in products_selected:
        product = sel["product"]
        quantity = sel.get("quantity", 1)

        investment = (product["price_purchase"] + product["installation_cost"]) * quantity
        daily_rev = product["revenue_per_hour"] * operating_hours * quantity
        monthly_rev = daily_rev * operating_days
        roi_months = round(investment / monthly_rev, 1) if monthly_rev > 0 else 999
        footprint = product["footprint_m2"] * quantity
        rev_per_m2 = round(monthly_rev / footprint, 2) if footprint > 0 else 0

        entry = FecProductRevenue(
            product_id=sel.get("id", ""),
            product_name=product["name"],
            category=product["category"],
            supplier=product.get("supplier", ""),
            footprint_m2=footprint,
            investment=investment,
            revenue_per_hour=product["revenue_per_hour"] * quantity,
            capacity_per_hour=product["capacity_per_hour"] * quantity,
            daily_revenue=daily_rev,
            monthly_revenue=monthly_rev,
            roi_months=roi_months,
            revenue_per_m2=rev_per_m2,
        )
        all_products.append(entry)
        total_investment += investment
        total_monthly_revenue += monthly_rev
        total_daily_revenue += daily_rev

    # Sort by monthly revenue descending
    top_performers = sorted(all_products, key=lambda x: -x.monthly_revenue)[:5]
    break_even = round(total_investment / total_monthly_revenue, 1) if total_monthly_revenue > 0 else 0
    total_footprint = sum(p.footprint_m2 for p in all_products)
    rev_per_m2 = round(total_monthly_revenue / total_footprint, 2) if total_footprint > 0 else 0

    return FecRevenueReport(
        total_investment=total_investment,
        total_monthly_revenue=total_monthly_revenue,
        total_daily_revenue=total_daily_revenue,
        break_even_months=break_even,
        revenue_per_m2_month=rev_per_m2,
        top_performers=top_performers,
        all_products=all_products,
        zone_summary=[],
        suggestions=[],
    )


# ==================== FEC AI RULES ====================

def generate_fec_recommendations(project_data: dict, products_selected: list) -> list:
    """Rule-based advisor for FEC projects."""
    recs = []
    categories_used = set()
    total_footprint = 0
    total_capacity = 0
    total_revenue_hr = 0

    for sel in products_selected:
        p = sel["product"]
        q = sel.get("quantity", 1)
        categories_used.add(p["category"])
        total_footprint += p["footprint_m2"] * q
        total_capacity += p["capacity_per_hour"] * q
        total_revenue_hr += p["revenue_per_hour"] * q

    total_area = project_data.get("total_area_m2", 500)
    ceiling = project_data.get("ceiling_height_m", 5)
    remaining_m2 = total_area - total_footprint

    # Rule 1: No horeca = missing 30% revenue
    if "horeca" not in categories_used and len(categories_used) > 0:
        recs.append({
            "type": "warning",
            "title": "Geen horeca zone!",
            "description": "FEC's zonder horeca missen gemiddeld 30% van de totale omzet. Food & Beverage is de #2 geldverdiener.",
            "action": "Voeg minimaal een snackbar of drinks station toe",
        })

    # Rule 2: Karting = high revenue flag
    if "karting" in categories_used:
        recs.append({
            "type": "optimization",
            "title": "Karting = top revenue driver",
            "description": "Karting heeft de hoogste omzet per uur. Overweeg premium karts voor nog hogere marges.",
            "action": None,
        })

    # Rule 3: Low capacity warning
    if total_capacity < 20 and len(products_selected) > 0:
        recs.append({
            "type": "warning",
            "title": "Lage bezoekercapaciteit",
            "description": f"Huidige capaciteit: {total_capacity} bezoekers/uur. Overweeg een high-turnover attractie zoals trampoline of arcade.",
            "action": "Voeg high-turnover attractie toe",
        })

    # Rule 4: No interactive experience
    if "interactive" not in categories_used and len(categories_used) > 0:
        recs.append({
            "type": "suggestion",
            "title": "Interactive experiences toevoegen",
            "description": "VR, escape rooms en klimwanden verhogen de verblijftijd en besteding per bezoeker met 40%.",
            "action": "Voeg interactive experience toe",
        })

    # Rule 5: Ceiling height check for karting/play
    if ceiling < 4.0 and ("karting" in categories_used or "indoor_play" in categories_used):
        recs.append({
            "type": "warning",
            "title": "Plafondhoogte te laag",
            "description": f"Karting en speeltoestellen vereisen minimaal 4m plafondhoogte. Uw locatie: {ceiling}m.",
            "action": "Controleer plafondhoogte",
        })

    # Rule 6: Remaining space
    if remaining_m2 > 50:
        recs.append({
            "type": "suggestion",
            "title": f"{remaining_m2:.0f}m² onbenut",
            "description": "Er is ruimte over. Overweeg een extra attractie of vergroot de horeca zone.",
            "action": f"Vul resterende {remaining_m2:.0f}m² in",
        })

    # Rule 7: No entree
    zones = project_data.get("zones", [])
    has_entree = any(z.get("type") == "entree" for z in zones)
    if not has_entree and len(products_selected) > 0:
        recs.append({
            "type": "suggestion",
            "title": "Entree zone ontbreekt",
            "description": "Een professionele entree met ticketing verhoogt de conversie en maakt upselling mogelijk.",
            "action": "Voeg entree zone toe",
        })

    # Rule 8: Cross-sell recreatie
    if total_area > 800:
        recs.append({
            "type": "optimization",
            "title": "Overweeg buitenruimte",
            "description": "Bij grote FEC's loont een buitenuitbreiding (recreatie). Dit verlengt het seizoen en de omzet.",
            "action": "Bekijk Recreatie Infra flow",
        })

    if not recs:
        recs.append({
            "type": "optimization",
            "title": "Goed bezig!",
            "description": "Uw FEC configuratie ziet er compleet uit.",
            "action": None,
        })

    return recs[:6]


# ==================== FEC API ROUTES ====================

@fec_router.get("/products")
async def get_fec_products():
    """Return all FEC products with revenue data."""
    products = []
    for i, p in enumerate(FEC_PRODUCTS):
        products.append({
            "id": f"fec-{i}",
            **p,
            "daily_revenue_10h": p["revenue_per_hour"] * 10,
            "monthly_revenue": p["revenue_per_hour"] * 10 * 30,
            "roi_months": round((p["price_purchase"] + p["installation_cost"]) / (p["revenue_per_hour"] * 10 * 30), 1) if p["revenue_per_hour"] > 0 else 999,
        })
    return products


@fec_router.get("/zone-types")
async def get_fec_zone_types():
    """Return available zone types for FEC layout."""
    return FEC_ZONE_TYPES


@fec_router.get("/suppliers")
async def get_fec_suppliers():
    """Return FEC-specific suppliers."""
    return FEC_SUPPLIERS


@fec_router.post("/calculate-revenue")
async def calculate_revenue(data: dict):
    """Calculate revenue for selected FEC products."""
    products_selected = data.get("products", [])
    operating_hours = data.get("operating_hours", 10)
    operating_days = data.get("operating_days", 30)

    # Map product IDs to actual products
    mapped = []
    for sel in products_selected:
        pid = sel.get("product_id", "")
        idx = pid.replace("fec-", "") if pid.startswith("fec-") else None
        if idx is not None and idx.isdigit() and int(idx) < len(FEC_PRODUCTS):
            mapped.append({
                "id": pid,
                "product": FEC_PRODUCTS[int(idx)],
                "quantity": sel.get("quantity", 1),
            })

    report = calculate_fec_revenue(mapped, operating_hours, operating_days)

    # Add AI recommendations
    project_data = data.get("project", {})
    suggestions = generate_fec_recommendations(project_data, mapped)
    report.suggestions = suggestions

    return report


@fec_router.get("/top5")
async def get_top5_revenue_drivers():
    """Return the top 5 revenue drivers sorted by ROI."""
    products = []
    for i, p in enumerate(FEC_PRODUCTS):
        investment = p["price_purchase"] + p["installation_cost"]
        monthly = p["revenue_per_hour"] * 10 * 30
        products.append({
            "id": f"fec-{i}",
            "name": p["name"],
            "category": p["category"],
            "supplier": p["supplier"],
            "investment": investment,
            "monthly_revenue": monthly,
            "roi_months": round(investment / monthly, 1) if monthly > 0 else 999,
            "revenue_per_m2": round(monthly / p["footprint_m2"], 2) if p["footprint_m2"] > 0 else 0,
            "revenue_per_hour": p["revenue_per_hour"],
        })
    # Sort by revenue per m² (most efficient use of space)
    products.sort(key=lambda x: -x["revenue_per_m2"])
    return products[:5]
