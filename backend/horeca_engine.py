"""
Horeca Revenue Engine — Business Simulator voor Bar / Pub / Café concepten op
recreatieparken, campings en stand-alone horeca. Modelleert kassa's, bestelzuilen,
vending, bar-inrichting, meubilair, pub games, keuken & terras met omzet/ROI per item.

Lease-formule (deterministisch, identiek aan andere flows):
    monthly = (investment + max(investment * 0.10, 500)) * 0.0219
"""
import uuid
import logging
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from fastapi import APIRouter

logger = logging.getLogger(__name__)

horeca_router = APIRouter(prefix="/horeca", tags=["Horeca Engine"])


# ==================== LEASE FORMULA ====================

def calc_lease_monthly(investment: float) -> float:
    """Deterministische lease-prijs per maand. Marge wordt nooit blootgesteld."""
    if investment <= 0:
        return 0.0
    base = investment + max(investment * 0.10, 500)
    return round(base * 0.0219, 2)


# ==================== HORECA MODELS ====================

class HorecaZone(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str  # bar, zit, games, terras, keuken, entree, routing
    name: str
    area_m2: float
    expected_capacity: int = 0
    color: str = "#b45309"


class HorecaProject(BaseModel):
    setting: str = "park"  # park | camping | standalone
    total_area_m2: float = 200
    seats_target: int = 60
    style: str = "casual"  # casual | premium | sports_bar | beach_bar
    operating_hours: float = 8
    operating_days: int = 30
    avg_spend_per_guest: float = 18.0
    zones: List[HorecaZone] = Field(default_factory=list)


class HorecaProductRevenue(BaseModel):
    product_id: str
    product_name: str
    category: str
    supplier: str
    footprint_m2: float
    investment: float
    lease_monthly: float
    revenue_per_hour: float
    capacity_per_hour: int
    daily_revenue: float
    monthly_revenue: float
    roi_months: float
    revenue_per_m2: float


class HorecaRevenueReport(BaseModel):
    total_investment: float
    total_lease_monthly: float
    total_monthly_revenue: float
    total_daily_revenue: float
    break_even_months: float
    revenue_per_m2_month: float
    top_performers: List[HorecaProductRevenue]
    all_products: List[HorecaProductRevenue]
    zone_summary: List[Dict[str, Any]]
    suggestions: List[Dict[str, str]]


# ==================== HORECA ZONE TYPES ====================

HORECA_ZONE_TYPES = [
    {"id": "bar", "name": "Bar", "color": "#b45309", "min_m2": 12, "revenue_factor": 1.6},
    {"id": "zit", "name": "Zit & Eetgelegenheid", "color": "#10b981", "min_m2": 30, "revenue_factor": 1.0},
    {"id": "games", "name": "Pub Games", "color": "#8b5cf6", "min_m2": 25, "revenue_factor": 1.3},
    {"id": "terras", "name": "Terras", "color": "#06b6d4", "min_m2": 40, "revenue_factor": 0.9},
    {"id": "keuken", "name": "Keuken & Food", "color": "#f97316", "min_m2": 20, "revenue_factor": 1.1},
    {"id": "entree", "name": "Entree & Bestelzuil", "color": "#6366f1", "min_m2": 8, "revenue_factor": 0},
    {"id": "routing", "name": "Routing & Looppad", "color": "#94a3b8", "min_m2": 0, "revenue_factor": 0},
]


# ==================== HORECA SUPPLIERS ====================

HORECA_SUPPLIERS = [
    {
        "id": "sup-eijsink",
        "name": "Eijsink",
        "address": "Almelo, Nederland",
        "lat": 52.3508,
        "lng": 6.6683,
        "categories": ["kassa", "bestelzuil"],
        "specialization": "POS-systemen, kassa's, bestelzuilen & betaaloplossingen voor horeca",
        "price_per_km": 1.40,
        "start_fee": 250,
        "hourly_rate_travel": 70,
    },
    {
        "id": "sup-selecta",
        "name": "Selecta Vending",
        "address": "Utrecht, Nederland",
        "lat": 52.0907,
        "lng": 5.1214,
        "categories": ["vending"],
        "specialization": "Vending machines: koffie, snacks, koude dranken, 24/7 service",
        "price_per_km": 1.20,
        "start_fee": 150,
        "hourly_rate_travel": 60,
    },
    {
        "id": "sup-heineken-tap",
        "name": "Heineken Tap-installatie",
        "address": "Zoeterwoude, Nederland",
        "lat": 52.1326,
        "lng": 4.5092,
        "categories": ["bar_inrichting"],
        "specialization": "Professionele tap-installaties, koeling, fust-systemen & onderhoud",
        "price_per_km": 1.50,
        "start_fee": 300,
        "hourly_rate_travel": 75,
    },
    {
        "id": "sup-shuffly",
        "name": "Shuffly",
        "address": "Amsterdam, Nederland",
        "lat": 52.3676,
        "lng": 4.9041,
        "categories": ["pub_games"],
        "specialization": "Shuffleboards, dart-cabinets & interactieve pub games",
        "price_per_km": 1.50,
        "start_fee": 200,
        "hourly_rate_travel": 65,
    },
    {
        "id": "sup-horeca-meubel",
        "name": "Horeca Meubel Centrum",
        "address": "Apeldoorn, Nederland",
        "lat": 52.2112,
        "lng": 5.9699,
        "categories": ["meubilair"],
        "specialization": "Tafels, stoelen, lounge-banken & terrasmeubilair voor horeca",
        "price_per_km": 1.10,
        "start_fee": 150,
        "hourly_rate_travel": 55,
    },
    {
        "id": "sup-rational",
        "name": "Rational Keuken Solutions",
        "address": "Eindhoven, Nederland",
        "lat": 51.4416,
        "lng": 5.4697,
        "categories": ["keuken"],
        "specialization": "Pizza-ovens, combi-steamers, friteuses & professionele keukenapparatuur",
        "price_per_km": 1.80,
        "start_fee": 350,
        "hourly_rate_travel": 80,
    },
    {
        "id": "sup-terraz",
        "name": "Terraz Outdoor",
        "address": "Rotterdam, Nederland",
        "lat": 51.9244,
        "lng": 4.4777,
        "categories": ["terras"],
        "specialization": "Parasols, terrasverwarming, buitenbars & windschermen",
        "price_per_km": 1.30,
        "start_fee": 200,
        "hourly_rate_travel": 60,
    },
]


# ==================== HORECA PRODUCTS ====================
# Prijs/uur kolom = bijdrage per uur in totale horecaomzet (covers/drinks/food).
# Bestelzuilen, kassa's en vending hebben directe of indirecte omzet-impact via uplift.

HORECA_PRODUCTS = [
    # === KASSA / POS (Eijsink-focused) ===
    {
        "name": "Eijsink POS Touchkassa",
        "category": "kassa",
        "supplier": "Eijsink",
        "description": "Compleet POS-systeem met touchscreen, bonnenprinter, kassalade & cloud-rapportage. Geschikt voor bar, restaurant en terras.",
        "footprint_m2": 1,
        "min_height_m": 0.5,
        "price_purchase": 2950,
        "revenue_per_hour": 18,  # uplift via snellere afhandeling
        "capacity_per_hour": 0,
        "installation_cost": 350,
        "tier": "midrange",
    },
    {
        "name": "Eijsink Mobiel Bestel-Tablet (handheld)",
        "category": "kassa",
        "supplier": "Eijsink",
        "description": "Robuuste handheld voor het opnemen van bestellingen aan tafel of op terras. Direct gekoppeld aan keuken & bar.",
        "footprint_m2": 0,
        "min_height_m": 0,
        "price_purchase": 895,
        "revenue_per_hour": 8,
        "capacity_per_hour": 0,
        "installation_cost": 75,
        "tier": "budget",
    },
    {
        "name": "Eijsink All-in-One POS Pro",
        "category": "kassa",
        "supplier": "Eijsink",
        "description": "Premium kassa-bundel: 2 touchkassa's, keukenprinter, barprinter, pinapparaat-integratie & analytics-dashboard.",
        "footprint_m2": 2,
        "min_height_m": 0.5,
        "price_purchase": 6450,
        "revenue_per_hour": 32,
        "capacity_per_hour": 0,
        "installation_cost": 600,
        "tier": "premium",
    },
    # === BESTELZUILEN ===
    {
        "name": "Eijsink Bestelzuil 22\" (zelfbestel)",
        "category": "bestelzuil",
        "supplier": "Eijsink",
        "description": "Self-order kiosk met 22-inch touchscreen, contactloos betalen, meertalige menu's & bon-printer. Verhoogt gemiddelde besteding met 20-30%.",
        "footprint_m2": 1,
        "min_height_m": 1.6,
        "price_purchase": 4750,
        "revenue_per_hour": 38,
        "capacity_per_hour": 30,
        "installation_cost": 450,
        "tier": "midrange",
    },
    {
        "name": "Eijsink Bestelzuil 32\" Pro (dual)",
        "category": "bestelzuil",
        "supplier": "Eijsink",
        "description": "Dubbele 32-inch self-order kiosk in één unit, ideaal voor entree van paviljoen of camping-restaurant. Korte wachttijden in piekuren.",
        "footprint_m2": 2,
        "min_height_m": 1.6,
        "price_purchase": 8950,
        "revenue_per_hour": 75,
        "capacity_per_hour": 60,
        "installation_cost": 750,
        "tier": "premium",
    },
    {
        "name": "Eijsink Outdoor Bestelzuil (IP65)",
        "category": "bestelzuil",
        "supplier": "Eijsink",
        "description": "Weerbestendige (IP65) self-order zuil voor terras, strand-paviljoen of camping-receptie. Anti-glare display, 24/7 buitenbestendig.",
        "footprint_m2": 1,
        "min_height_m": 1.7,
        "price_purchase": 6450,
        "revenue_per_hour": 45,
        "capacity_per_hour": 35,
        "installation_cost": 600,
        "tier": "premium",
    },
    # === VENDING ===
    {
        "name": "Selecta Koffie-vending Plus",
        "category": "vending",
        "supplier": "Selecta Vending",
        "description": "24/7 koffie-vending met verse bonen, melkschuim, hot chocolate. Cashless betaling, telemetrie voor voorraad.",
        "footprint_m2": 1,
        "min_height_m": 1.9,
        "price_purchase": 4250,
        "revenue_per_hour": 12,
        "capacity_per_hour": 30,
        "installation_cost": 200,
        "tier": "midrange",
    },
    {
        "name": "Selecta Snack & Drink Combi",
        "category": "vending",
        "supplier": "Selecta Vending",
        "description": "Combinatie-automaat snacks + koude dranken. Ideaal voor 24/7 service op camping of recreatiepark.",
        "footprint_m2": 2,
        "min_height_m": 1.9,
        "price_purchase": 5950,
        "revenue_per_hour": 22,
        "capacity_per_hour": 40,
        "installation_cost": 250,
        "tier": "midrange",
    },
    {
        "name": "Selecta Verse Maaltijd-automaat",
        "category": "vending",
        "supplier": "Selecta Vending",
        "description": "Gekoelde verse maaltijden 24/7 verkrijgbaar. Magnetron geïntegreerd, geschikt voor late-night op camping.",
        "footprint_m2": 2,
        "min_height_m": 1.9,
        "price_purchase": 8950,
        "revenue_per_hour": 35,
        "capacity_per_hour": 25,
        "installation_cost": 400,
        "tier": "premium",
    },
    # === BAR INRICHTING ===
    {
        "name": "Heineken Tap 4-krans (compleet)",
        "category": "bar_inrichting",
        "supplier": "Heineken Tap-installatie",
        "description": "4-kraans tap-installatie met koeling, fust-aansluiting, CO2-systeem & SLA-onderhoud. Inclusief installatie.",
        "footprint_m2": 3,
        "min_height_m": 1.2,
        "price_purchase": 6500,
        "revenue_per_hour": 95,
        "capacity_per_hour": 80,
        "installation_cost": 1200,
        "tier": "midrange",
    },
    {
        "name": "Heineken Tap 8-krans Premium",
        "category": "bar_inrichting",
        "supplier": "Heineken Tap-installatie",
        "description": "8 kranen + speciaalbier-tap, geïntegreerde koeling, glazen-spoeler & LED-bar-verlichting.",
        "footprint_m2": 5,
        "min_height_m": 1.2,
        "price_purchase": 14500,
        "revenue_per_hour": 185,
        "capacity_per_hour": 150,
        "installation_cost": 2500,
        "tier": "premium",
    },
    {
        "name": "IJsblokjes-machine (50kg/dag)",
        "category": "bar_inrichting",
        "supplier": "Heineken Tap-installatie",
        "description": "Professionele ijsblokjesmachine, 50kg/dag, voorraad 25kg. Onmisbaar voor cocktail-bar.",
        "footprint_m2": 1,
        "min_height_m": 1.2,
        "price_purchase": 2250,
        "revenue_per_hour": 12,
        "capacity_per_hour": 0,
        "installation_cost": 200,
        "tier": "midrange",
    },
    {
        "name": "Bar-koeling Onderbouw 3-deurs",
        "category": "bar_inrichting",
        "supplier": "Heineken Tap-installatie",
        "description": "Onderbouw-koeling met 3 deuren voor flessen & blikjes, RVS, stille compressor.",
        "footprint_m2": 2,
        "min_height_m": 0.9,
        "price_purchase": 1950,
        "revenue_per_hour": 18,
        "capacity_per_hour": 0,
        "installation_cost": 150,
        "tier": "budget",
    },
    # === MEUBILAIR ===
    {
        "name": "Statafel Set (4 stuks)",
        "category": "meubilair",
        "supplier": "Horeca Meubel Centrum",
        "description": "Set van 4 statafels, RVS-poot, eikenhouten blad. Perfect voor sta-bar of terras.",
        "footprint_m2": 8,
        "min_height_m": 1.1,
        "price_purchase": 1450,
        "revenue_per_hour": 28,
        "capacity_per_hour": 16,
        "installation_cost": 100,
        "tier": "budget",
    },
    {
        "name": "Eettafel + 4 Stoelen Pakket",
        "category": "meubilair",
        "supplier": "Horeca Meubel Centrum",
        "description": "Set: eettafel 80x80cm + 4 horecastoelen. Stapelbaar, onderhoudsvriendelijk.",
        "footprint_m2": 4,
        "min_height_m": 0.8,
        "price_purchase": 750,
        "revenue_per_hour": 22,
        "capacity_per_hour": 4,
        "installation_cost": 50,
        "tier": "budget",
    },
    {
        "name": "Lounge-set Modulair (8-persoons)",
        "category": "meubilair",
        "supplier": "Horeca Meubel Centrum",
        "description": "Modulaire lounge-bank, 8 personen, met salontafels. Ideaal voor relax-zone of beach-bar.",
        "footprint_m2": 12,
        "min_height_m": 0.8,
        "price_purchase": 3950,
        "revenue_per_hour": 42,
        "capacity_per_hour": 8,
        "installation_cost": 150,
        "tier": "premium",
    },
    {
        "name": "Picknick-bank Outdoor (set 4)",
        "category": "meubilair",
        "supplier": "Horeca Meubel Centrum",
        "description": "4 robuuste outdoor picknick-banken, weerbestendig hardhout. Standaard op recreatieparken.",
        "footprint_m2": 16,
        "min_height_m": 0.8,
        "price_purchase": 1850,
        "revenue_per_hour": 38,
        "capacity_per_hour": 32,
        "installation_cost": 80,
        "tier": "midrange",
    },
    # === PUB GAMES ===
    {
        "name": "Shuffleboard Pro 6m (LED)",
        "category": "pub_games",
        "supplier": "Shuffly",
        "description": "Professionele shuffleboard 6m met LED-scoring, multiplayer-mode. Hoogtepunt van elke pub.",
        "footprint_m2": 8,
        "min_height_m": 2.5,
        "price_purchase": 4500,
        "revenue_per_hour": 28,
        "capacity_per_hour": 8,
        "installation_cost": 500,
        "tier": "midrange",
    },
    {
        "name": "Dart Cabinet Pro (digitaal)",
        "category": "pub_games",
        "supplier": "Shuffly",
        "description": "Digitale dart-cabinet met scoring-display, 50+ game-modes, LED-verlichting & soundboard.",
        "footprint_m2": 3,
        "min_height_m": 2.4,
        "price_purchase": 1850,
        "revenue_per_hour": 18,
        "capacity_per_hour": 6,
        "installation_cost": 200,
        "tier": "budget",
    },
    {
        "name": "Pool-tafel 8ft Premium",
        "category": "pub_games",
        "supplier": "Shuffly",
        "description": "Massief eiken pool-tafel 8ft met gefilterde ballen-retrieval. Klassieker voor sportbar.",
        "footprint_m2": 9,
        "min_height_m": 2.5,
        "price_purchase": 3950,
        "revenue_per_hour": 22,
        "capacity_per_hour": 4,
        "installation_cost": 400,
        "tier": "midrange",
    },
    {
        "name": "Foosball Tournament Edition",
        "category": "pub_games",
        "supplier": "Shuffly",
        "description": "Premium tafelvoetbal, telegrafische score, perfect voor toernooi-avonden.",
        "footprint_m2": 3,
        "min_height_m": 2.0,
        "price_purchase": 1450,
        "revenue_per_hour": 14,
        "capacity_per_hour": 4,
        "installation_cost": 100,
        "tier": "budget",
    },
    {
        "name": "Beer Pong Tafel (LED, geijkt)",
        "category": "pub_games",
        "supplier": "Shuffly",
        "description": "LED-verlichte beer pong tafel met ingebouwd scorebord & geluidseffecten. Toernooi-favoriet.",
        "footprint_m2": 4,
        "min_height_m": 2.0,
        "price_purchase": 1250,
        "revenue_per_hour": 16,
        "capacity_per_hour": 6,
        "installation_cost": 80,
        "tier": "budget",
    },
    {
        "name": "Air Hockey Bar Edition",
        "category": "pub_games",
        "supplier": "Shuffly",
        "description": "LED air hockey-tafel, digitale score, muntloos. Snel-spelende publiekstrekker.",
        "footprint_m2": 4,
        "min_height_m": 2.5,
        "price_purchase": 3200,
        "revenue_per_hour": 20,
        "capacity_per_hour": 4,
        "installation_cost": 300,
        "tier": "budget",
    },
    {
        "name": "Karaoke Booth (zelfservice)",
        "category": "pub_games",
        "supplier": "Shuffly",
        "description": "Self-service karaoke-cabine met 30k+ liedjes, touchscreen, microfoons. Hit voor groepen.",
        "footprint_m2": 6,
        "min_height_m": 2.4,
        "price_purchase": 5950,
        "revenue_per_hour": 32,
        "capacity_per_hour": 6,
        "installation_cost": 600,
        "tier": "premium",
    },
    # === KEUKEN ===
    {
        "name": "Pizza-oven Profi (2 niveaus)",
        "category": "keuken",
        "supplier": "Rational Keuken Solutions",
        "description": "2-niveau elektrische pizza-oven, 16 pizza's tegelijk, perfect voor camping-restaurant.",
        "footprint_m2": 2,
        "min_height_m": 1.2,
        "price_purchase": 4950,
        "revenue_per_hour": 95,
        "capacity_per_hour": 32,
        "installation_cost": 350,
        "tier": "midrange",
    },
    {
        "name": "Combi-steamer 10x GN1/1",
        "category": "keuken",
        "supplier": "Rational Keuken Solutions",
        "description": "Multifunctionele combi-steamer, alle bereidingen, automatische reiniging.",
        "footprint_m2": 1,
        "min_height_m": 1.4,
        "price_purchase": 8950,
        "revenue_per_hour": 75,
        "capacity_per_hour": 0,
        "installation_cost": 800,
        "tier": "premium",
    },
    {
        "name": "Frituur Dual 2x9L",
        "category": "keuken",
        "supplier": "Rational Keuken Solutions",
        "description": "Dubbele professionele frituur, snelle opwarmtijd, energiezuinig.",
        "footprint_m2": 1,
        "min_height_m": 0.9,
        "price_purchase": 1850,
        "revenue_per_hour": 45,
        "capacity_per_hour": 0,
        "installation_cost": 200,
        "tier": "budget",
    },
    {
        "name": "Bakplaat / Grill 80cm",
        "category": "keuken",
        "supplier": "Rational Keuken Solutions",
        "description": "Professionele bakplaat 80cm, ideaal voor burgers & ontbijt-service op camping.",
        "footprint_m2": 1,
        "min_height_m": 0.9,
        "price_purchase": 1450,
        "revenue_per_hour": 38,
        "capacity_per_hour": 0,
        "installation_cost": 150,
        "tier": "budget",
    },
    # === TERRAS ===
    {
        "name": "Parasol XL 4x4m (set 4)",
        "category": "terras",
        "supplier": "Terraz Outdoor",
        "description": "4 parasols 4x4m met betonvoeten, RVS-frame. Compleet pakket.",
        "footprint_m2": 64,
        "min_height_m": 0,
        "price_purchase": 2950,
        "revenue_per_hour": 22,
        "capacity_per_hour": 32,
        "installation_cost": 200,
        "tier": "midrange",
    },
    {
        "name": "Terras-verwarmer Gas (set 4)",
        "category": "terras",
        "supplier": "Terraz Outdoor",
        "description": "4 gas-terrasverwarmers, RVS, 13kW. Verlengt het terras-seizoen tot november.",
        "footprint_m2": 4,
        "min_height_m": 2.2,
        "price_purchase": 1950,
        "revenue_per_hour": 18,
        "capacity_per_hour": 0,
        "installation_cost": 100,
        "tier": "budget",
    },
    {
        "name": "Buitenbar Modulair 4m",
        "category": "terras",
        "supplier": "Terraz Outdoor",
        "description": "Mobiele buitenbar 4m met onderbouw-koeling, RVS-blad, weerbestendig. Perfect voor evenement-gebruik.",
        "footprint_m2": 4,
        "min_height_m": 1.2,
        "price_purchase": 5450,
        "revenue_per_hour": 65,
        "capacity_per_hour": 50,
        "installation_cost": 400,
        "tier": "premium",
    },
    {
        "name": "Windscherm Glazen 6m (set)",
        "category": "terras",
        "supplier": "Terraz Outdoor",
        "description": "Glazen windschermen, 6m totaal, in RVS-frames. Comfort voor terras aan zee of camping.",
        "footprint_m2": 6,
        "min_height_m": 1.6,
        "price_purchase": 1850,
        "revenue_per_hour": 12,
        "capacity_per_hour": 0,
        "installation_cost": 250,
        "tier": "budget",
    },
]


# ==================== REVENUE ENGINE ====================

def calculate_horeca_revenue(
    products_selected: list,
    operating_hours: float = 8,
    operating_days: int = 30,
) -> HorecaRevenueReport:
    """Core revenue engine voor Horeca; ROI per item + totaal."""
    all_products = []
    total_investment = 0
    total_lease_monthly = 0
    total_monthly_revenue = 0
    total_daily_revenue = 0

    for sel in products_selected:
        product = sel["product"]
        quantity = sel.get("quantity", 1)

        investment = (product["price_purchase"] + product["installation_cost"]) * quantity
        lease = calc_lease_monthly(investment)
        daily_rev = product["revenue_per_hour"] * operating_hours * quantity
        monthly_rev = daily_rev * operating_days
        roi_months = round(investment / monthly_rev, 1) if monthly_rev > 0 else 999
        footprint = product["footprint_m2"] * quantity
        rev_per_m2 = round(monthly_rev / footprint, 2) if footprint > 0 else 0

        entry = HorecaProductRevenue(
            product_id=sel.get("id", ""),
            product_name=product["name"],
            category=product["category"],
            supplier=product.get("supplier", ""),
            footprint_m2=footprint,
            investment=investment,
            lease_monthly=lease,
            revenue_per_hour=product["revenue_per_hour"] * quantity,
            capacity_per_hour=product["capacity_per_hour"] * quantity,
            daily_revenue=daily_rev,
            monthly_revenue=monthly_rev,
            roi_months=roi_months,
            revenue_per_m2=rev_per_m2,
        )
        all_products.append(entry)
        total_investment += investment
        total_lease_monthly += lease
        total_monthly_revenue += monthly_rev
        total_daily_revenue += daily_rev

    top_performers = sorted(all_products, key=lambda x: -x.monthly_revenue)[:5]
    break_even = round(total_investment / total_monthly_revenue, 1) if total_monthly_revenue > 0 else 0
    total_footprint = sum(p.footprint_m2 for p in all_products)
    rev_per_m2 = round(total_monthly_revenue / total_footprint, 2) if total_footprint > 0 else 0

    return HorecaRevenueReport(
        total_investment=total_investment,
        total_lease_monthly=round(total_lease_monthly, 2),
        total_monthly_revenue=total_monthly_revenue,
        total_daily_revenue=total_daily_revenue,
        break_even_months=break_even,
        revenue_per_m2_month=rev_per_m2,
        top_performers=top_performers,
        all_products=all_products,
        zone_summary=[],
        suggestions=[],
    )


# ==================== AI / RULE-BASED RECOMMENDATIONS ====================

def generate_horeca_recommendations(project_data: dict, products_selected: list) -> list:
    recs = []
    categories_used = set()
    for sel in products_selected:
        categories_used.add(sel["product"]["category"])

    setting = project_data.get("setting", "park")
    seats_target = project_data.get("seats_target", 60)

    if "kassa" not in categories_used and len(products_selected) > 0:
        recs.append({
            "type": "warning",
            "title": "Geen kassa-systeem geselecteerd",
            "description": "Een professioneel POS-systeem (zoals Eijsink) is essentieel voor afrekenen, voorraadbeheer & rapportage. Zonder kassa geen omzet-tracking.",
            "action": "Voeg een Eijsink POS toe",
        })

    if "bestelzuil" not in categories_used and seats_target >= 50:
        recs.append({
            "type": "suggestion",
            "title": "Bestelzuil verhoogt omzet met 20-30%",
            "description": "Bij meer dan 50 zitplaatsen verkort een self-order zuil de wachttijd in piekuren en verhoogt aantoonbaar de gemiddelde besteding.",
            "action": "Voeg een Eijsink Bestelzuil toe",
        })

    if "bar_inrichting" not in categories_used and len(products_selected) > 0:
        recs.append({
            "type": "warning",
            "title": "Bar-inrichting ontbreekt",
            "description": "Een tap-installatie is de #1 omzetdrijver in een horeca-concept. Drank levert de hoogste marge per uur.",
            "action": "Voeg een Heineken Tap toe",
        })

    if "pub_games" not in categories_used and project_data.get("style") in ("sports_bar", "casual"):
        recs.append({
            "type": "suggestion",
            "title": "Pub Games verhogen verblijftijd",
            "description": "Shuffleboard, dart en pool verlengen het bezoek met gemiddeld 45 minuten — directe impact op besteding.",
            "action": "Voeg shuffleboard of dart toe",
        })

    if setting == "camping" and "vending" not in categories_used:
        recs.append({
            "type": "suggestion",
            "title": "24/7 vending op camping",
            "description": "Op een camping is buiten openingstijden vending de enige omzetbron. Selecta-machines draaien 24/7.",
            "action": "Voeg een vending-machine toe",
        })

    if setting in ("park", "standalone") and "terras" not in categories_used:
        recs.append({
            "type": "suggestion",
            "title": "Terras = seizoens-uplift",
            "description": "Een terras met windscherm en heater verlengt het seizoen van 4 naar 8 maanden.",
            "action": "Voeg terras-meubilair en parasols toe",
        })

    if not recs:
        recs.append({
            "type": "optimization",
            "title": "Goede mix!",
            "description": "Je horeca-configuratie ziet er compleet uit. Klaar voor offerte.",
            "action": None,
        })

    return recs[:6]


# ==================== HORECA API ROUTES ====================

@horeca_router.get("/products")
async def get_horeca_products():
    """Alle horeca-producten met deterministische lease-prijs."""
    products = []
    for i, p in enumerate(HORECA_PRODUCTS):
        investment = p["price_purchase"] + p["installation_cost"]
        monthly_rev = p["revenue_per_hour"] * 8 * 30
        products.append({
            "id": f"horeca-{i}",
            **p,
            "price_lease_monthly": calc_lease_monthly(investment),
            "daily_revenue_8h": p["revenue_per_hour"] * 8,
            "monthly_revenue": monthly_rev,
            "roi_months": round(investment / monthly_rev, 1) if monthly_rev > 0 else 999,
        })
    return products


@horeca_router.get("/zone-types")
async def get_horeca_zone_types():
    return HORECA_ZONE_TYPES


@horeca_router.get("/suppliers")
async def get_horeca_suppliers():
    return HORECA_SUPPLIERS


@horeca_router.post("/calculate-revenue")
async def calculate_revenue(data: dict):
    """Bereken omzet voor geselecteerde Horeca-producten."""
    products_selected = data.get("products", [])
    operating_hours = data.get("operating_hours", 8)
    operating_days = data.get("operating_days", 30)

    mapped = []
    for sel in products_selected:
        pid = sel.get("product_id", "")
        idx = pid.replace("horeca-", "") if pid.startswith("horeca-") else None
        if idx is not None and idx.isdigit() and int(idx) < len(HORECA_PRODUCTS):
            mapped.append({
                "id": pid,
                "product": HORECA_PRODUCTS[int(idx)],
                "quantity": sel.get("quantity", 1),
            })

    report = calculate_horeca_revenue(mapped, operating_hours, operating_days)
    project_data = data.get("project", {})
    report.suggestions = generate_horeca_recommendations(project_data, mapped)
    return report


@horeca_router.get("/top5")
async def get_top5():
    """Top 5 omzetdrijvers gesorteerd op omzet per m²."""
    products = []
    for i, p in enumerate(HORECA_PRODUCTS):
        investment = p["price_purchase"] + p["installation_cost"]
        monthly = p["revenue_per_hour"] * 8 * 30
        products.append({
            "id": f"horeca-{i}",
            "name": p["name"],
            "category": p["category"],
            "supplier": p["supplier"],
            "investment": investment,
            "monthly_revenue": monthly,
            "lease_monthly": calc_lease_monthly(investment),
            "roi_months": round(investment / monthly, 1) if monthly > 0 else 999,
            "revenue_per_m2": round(monthly / p["footprint_m2"], 2) if p["footprint_m2"] > 0 else 0,
            "revenue_per_hour": p["revenue_per_hour"],
        })
    products.sort(key=lambda x: -x["revenue_per_m2"])
    return products[:5]
