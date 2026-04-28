from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import base64
import io
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
from emergentintegrations.llm.chat import LlmChat, UserMessage, ImageContent

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

from ai_services import ai_router
from supplier_module import supplier_router, seed_suppliers, calculate_travel_cost
from fec_engine import fec_router
from horeca_engine import horeca_router
from chalet_engine import chalet_router
from supabase_module import supabase_router
from location_engine import location_router
from partner_profiles import partner_router
from roadmap_engine import roadmap_router
from whitelabel_engine import whitelabel_router
from subsidy_engine import subsidy_router
from crm_engine import crm_router
from auth_engine import auth_router

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== MODELS ====================

class ProductBase(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str
    category: str
    subcategory: str = ""
    description: str
    price_purchase: float
    price_lease_monthly: float
    installation_cost: float
    maintenance_yearly: float
    dimensions: Dict[str, float] = Field(default_factory=lambda: {"width": 1, "height": 1})
    coverage_radius: Optional[float] = None
    icon: str = "box"
    color: str = "#0ea5e9"
    tier: str = "midrange"  # budget | midrange | premium
    supplier_id: Optional[str] = None
    supplier: Optional[str] = None
    image: Optional[str] = None

class Product(ProductBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ProductCreate(ProductBase):
    pass

class PlacedProduct(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    product_id: str
    x: float
    y: float
    rotation: float = 0
    quantity: int = 1

class Zone(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    type: str  # standplaats, sanitair, toegangsweg, technisch
    points: List[Dict[str, float]]  # Polygon points
    color: str = "#0ea5e9"

class ProjectBase(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str
    project_type: str  # recreatie | chalet | fec
    project_flow: str = "recreatie"  # recreatie | chalet | fec
    address: str = ""
    lat: float = 52.0
    lng: float = 5.0
    floor_plan_base64: Optional[str] = None
    scale_meters_per_pixel: float = 0.1
    canvas_width: int = 800
    canvas_height: int = 600
    placed_products: List[PlacedProduct] = Field(default_factory=list)
    zones: List[Zone] = Field(default_factory=list)
    num_spots: int = 0

class Project(ProjectBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    project_type: Optional[str] = None
    project_flow: Optional[str] = None
    address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    floor_plan_base64: Optional[str] = None
    scale_meters_per_pixel: Optional[float] = None
    placed_products: Optional[List[PlacedProduct]] = None
    zones: Optional[List[Zone]] = None
    num_spots: Optional[int] = None

class QuoteResponse(BaseModel):
    capex_total: float
    opex_monthly: float
    opex_yearly: float
    installation_total: float
    maintenance_yearly: float
    travel_costs: List[Dict[str, Any]] = []
    travel_total: float = 0
    project_total: float = 0  # capex + install + travel
    items: List[Dict[str, Any]]

class AIRecommendation(BaseModel):
    type: str  # warning, suggestion, optimization
    title: str
    description: str
    action: Optional[str] = None
    product_id: Optional[str] = None

class AIAnalysisResponse(BaseModel):
    recommendations: List[AIRecommendation]
    detected_zones: Optional[List[Dict[str, Any]]] = None

# ==================== SEED DATA ====================

SEED_PRODUCTS = [
    # Sanitair units - realistische maten
    {
        "name": "Compact Sanitair Unit",
        "category": "sanitair",
        "description": "2 toiletten, 2 douches, geschikt voor 15-20 standplaatsen. Afmeting 3x6m",
        "price_purchase": 18500,
        "price_lease_monthly": 450,
        "installation_cost": 2500,
        "maintenance_yearly": 1200,
        "dimensions": {"width": 3, "height": 6},
        "icon": "bath",
        "color": "#0ea5e9"
    },
    {
        "name": "Medium Sanitair Unit",
        "category": "sanitair",
        "description": "4 toiletten, 4 douches, geschikt voor 30-40 standplaatsen. Afmeting 6x8m",
        "price_purchase": 32000,
        "price_lease_monthly": 750,
        "installation_cost": 4000,
        "maintenance_yearly": 2000,
        "dimensions": {"width": 6, "height": 8},
        "icon": "bath",
        "color": "#0ea5e9"
    },
    {
        "name": "Premium Sanitair Blok",
        "category": "sanitair",
        "description": "6 toiletten, 6 douches, familiecabines, geschikt voor 50+ standplaatsen. Afmeting 8x12m",
        "price_purchase": 55000,
        "price_lease_monthly": 1200,
        "installation_cost": 6500,
        "maintenance_yearly": 3500,
        "dimensions": {"width": 8, "height": 12},
        "icon": "bath",
        "color": "#0ea5e9"
    },
    # Slagbomen
    {
        "name": "Nice M5BAR",
        "category": "slagboom",
        "description": "24VDC slagboom tot 5m, IP54, 450 cycli/uur, BlueBus, incl. fundatieplaat. Behuizing 0.4x0.3m",
        "price_purchase": 3079,
        "price_lease_monthly": 75,
        "installation_cost": 800,
        "maintenance_yearly": 250,
        "dimensions": {"width": 0.4, "height": 5},
        "icon": "boom",
        "color": "#f59e0b"
    },
    {
        "name": "Nice M5BAR + Kentekenherkenning",
        "category": "slagboom",
        "description": "Nice M5BAR slagboom met UniFi AI LPR kentekenherkenning, automatische doorgang",
        "price_purchase": 3628,
        "price_lease_monthly": 95,
        "installation_cost": 1200,
        "maintenance_yearly": 350,
        "dimensions": {"width": 0.4, "height": 5},
        "icon": "boom",
        "color": "#f59e0b"
    },
    {
        "name": "Premium Toegangspoort",
        "category": "slagboom",
        "description": "Dubbele Nice M5BAR met UniFi camera's, intercom en betaalterminal",
        "price_purchase": 12000,
        "price_lease_monthly": 280,
        "installation_cost": 3500,
        "maintenance_yearly": 800,
        "dimensions": {"width": 1, "height": 6},
        "icon": "boom",
        "color": "#f59e0b"
    },
    # UniFi Camera systemen
    {
        "name": "UniFi G5 Bullet",
        "category": "camera",
        "description": "2K 4MP, IR nachtzicht 9m, IP67, PoE, AI-detectie (personen/voertuigen). 75x74mm",
        "price_purchase": 139,
        "price_lease_monthly": 5,
        "installation_cost": 100,
        "maintenance_yearly": 25,
        "dimensions": {"width": 0.08, "height": 0.08},
        "coverage_radius": 30,
        "icon": "camera",
        "color": "#ef4444"
    },
    {
        "name": "UniFi G5 Dome Ultra",
        "category": "camera",
        "description": "2K 4MP, IR 20m, IP65, IK06, PoE, 120° beeldhoek, vandaalbestendig. 64x68mm",
        "price_purchase": 139,
        "price_lease_monthly": 5,
        "installation_cost": 100,
        "maintenance_yearly": 25,
        "dimensions": {"width": 0.07, "height": 0.07},
        "coverage_radius": 20,
        "icon": "camera",
        "color": "#ef4444"
    },
    {
        "name": "UniFi G5 Pro",
        "category": "camera",
        "description": "4K 8MP, 3x optische zoom, IR 25-40m, IP65, IK04, PoE. Premium buitencamera. 86x154mm",
        "price_purchase": 399,
        "price_lease_monthly": 12,
        "installation_cost": 200,
        "maintenance_yearly": 50,
        "dimensions": {"width": 0.09, "height": 0.15},
        "coverage_radius": 40,
        "icon": "camera",
        "color": "#ef4444"
    },
    {
        "name": "UniFi G5 Turret Ultra",
        "category": "camera",
        "description": "2K 4MP, 102° beeldhoek, IR nachtzicht, IP66, PoE, AI-detectie",
        "price_purchase": 159,
        "price_lease_monthly": 6,
        "installation_cost": 100,
        "maintenance_yearly": 30,
        "dimensions": {"width": 0.08, "height": 0.08},
        "coverage_radius": 25,
        "icon": "camera",
        "color": "#ef4444"
    },
    {
        "name": "UniFi AI LPR Camera",
        "category": "camera",
        "description": "4K 8MP kentekenherkenning, 3x zoom, IR 15m, IP66, tot 90 km/h, 2 rijbanen. 130x151x303mm",
        "price_purchase": 549,
        "price_lease_monthly": 16,
        "installation_cost": 300,
        "maintenance_yearly": 75,
        "dimensions": {"width": 0.13, "height": 0.3},
        "coverage_radius": 12,
        "icon": "camera",
        "color": "#ef4444"
    },
    # WiFi systemen
    {
        "name": "UniFi Access Point Indoor",
        "category": "wifi",
        "description": "WiFi 6, 100+ gebruikers, 50m indoor bereik",
        "price_purchase": 280,
        "price_lease_monthly": 8,
        "installation_cost": 100,
        "maintenance_yearly": 30,
        "dimensions": {"width": 0.3, "height": 0.3},
        "coverage_radius": 50,
        "icon": "wifi",
        "color": "#10b981"
    },
    {
        "name": "UniFi Access Point Outdoor",
        "category": "wifi",
        "description": "WiFi 6, weerbestendig, 100m outdoor bereik",
        "price_purchase": 450,
        "price_lease_monthly": 15,
        "installation_cost": 200,
        "maintenance_yearly": 50,
        "dimensions": {"width": 0.3, "height": 0.3},
        "coverage_radius": 100,
        "icon": "wifi",
        "color": "#10b981"
    },
    {
        "name": "Mesh WiFi Systeem",
        "category": "wifi",
        "description": "Complete oplossing voor 50 standplaatsen",
        "price_purchase": 3500,
        "price_lease_monthly": 95,
        "installation_cost": 800,
        "maintenance_yearly": 300,
        "dimensions": {"width": 0.5, "height": 0.5},
        "coverage_radius": 200,
        "icon": "wifi",
        "color": "#10b981"
    },
    # Verlichting
    {
        "name": "LED Terreinverlichting",
        "category": "verlichting",
        "description": "Solar-powered, bewegingssensor, IP65",
        "price_purchase": 180,
        "price_lease_monthly": 5,
        "installation_cost": 80,
        "maintenance_yearly": 20,
        "dimensions": {"width": 0.3, "height": 0.3},
        "coverage_radius": 15,
        "icon": "lightbulb",
        "color": "#fbbf24"
    },
    {
        "name": "Lichtmast 6m",
        "category": "verlichting",
        "description": "LED, dimbaar, 360° verlichting",
        "price_purchase": 1200,
        "price_lease_monthly": 30,
        "installation_cost": 500,
        "maintenance_yearly": 100,
        "dimensions": {"width": 0.5, "height": 0.5},
        "coverage_radius": 25,
        "icon": "lightbulb",
        "color": "#fbbf24"
    },
    # Betaalsystemen
    {
        "name": "Betaalzuil Basis",
        "category": "betaalsysteem",
        "description": "PIN, contactloos, bonprinter",
        "price_purchase": 2200,
        "price_lease_monthly": 55,
        "installation_cost": 400,
        "maintenance_yearly": 200,
        "dimensions": {"width": 0.5, "height": 0.5},
        "icon": "credit-card",
        "color": "#8b5cf6"
    },
    {
        "name": "Self-Service Kiosk",
        "category": "betaalsysteem",
        "description": "Check-in/out, betaling, sleuteluitgifte",
        "price_purchase": 8500,
        "price_lease_monthly": 220,
        "installation_cost": 1500,
        "maintenance_yearly": 600,
        "dimensions": {"width": 1, "height": 1},
        "icon": "credit-card",
        "color": "#8b5cf6"
    },
    # UniFi Access - Toegangscontrole
    {
        "name": "UniFi Access Hub",
        "category": "toegangscontrole",
        "description": "Single-door PoE hub, 6000 gebruikers, DIN-rail, 5x GbE poorten, UL 294. 175x126x33mm",
        "price_purchase": 219,
        "price_lease_monthly": 8,
        "installation_cost": 200,
        "maintenance_yearly": 50,
        "dimensions": {"width": 0.18, "height": 0.13},
        "icon": "key",
        "color": "#ec4899"
    },
    {
        "name": "UniFi Access Reader Lite (UA-Lite)",
        "category": "toegangscontrole",
        "description": "NFC kaartlezer, PoE, koppelt met UA-Hub, smartphone toegang via UniFi Identity app",
        "price_purchase": 109,
        "price_lease_monthly": 4,
        "installation_cost": 100,
        "maintenance_yearly": 25,
        "dimensions": {"width": 0.1, "height": 0.1},
        "icon": "key",
        "color": "#ec4899"
    },
    {
        "name": "UniFi Access Reader Pro (UA-Pro)",
        "category": "toegangscontrole",
        "description": "NFC + PIN + intercom, PoE, premium toegangslezer met display en camera",
        "price_purchase": 329,
        "price_lease_monthly": 10,
        "installation_cost": 200,
        "maintenance_yearly": 50,
        "dimensions": {"width": 0.12, "height": 0.12},
        "icon": "key",
        "color": "#ec4899"
    },
    {
        "name": "UniFi Access Starter Kit",
        "category": "toegangscontrole",
        "description": "Compleet pakket: UA-Hub + UA-Pro + UA-Lite + bekabeling. Eenvoudige installatie voor 1 deur",
        "price_purchase": 599,
        "price_lease_monthly": 18,
        "installation_cost": 350,
        "maintenance_yearly": 100,
        "dimensions": {"width": 0.2, "height": 0.2},
        "icon": "key",
        "color": "#ec4899"
    },
    # Douchelezers - RECRA Specialty
    {
        "name": "Contactloze Douchelezer Basis",
        "category": "douchelezer",
        "description": "PIN/contactloos betalen per douchebeurt, online tariefbeheer",
        "price_purchase": 850,
        "price_lease_monthly": 25,
        "installation_cost": 150,
        "maintenance_yearly": 75,
        "dimensions": {"width": 0.2, "height": 0.3},
        "icon": "droplets",
        "color": "#06b6d4"
    },
    {
        "name": "Douchelezer Pro",
        "category": "douchelezer",
        "description": "Geavanceerde betaalterminal, Apple Pay/Google Pay, realtime dashboard",
        "price_purchase": 1250,
        "price_lease_monthly": 35,
        "installation_cost": 200,
        "maintenance_yearly": 100,
        "dimensions": {"width": 0.2, "height": 0.3},
        "icon": "droplets",
        "color": "#06b6d4"
    },
    {
        "name": "Douchelezer Enterprise",
        "category": "douchelezer",
        "description": "Premium systeem met touchscreen, meerdere betaalopties, integratie reserveringssysteem",
        "price_purchase": 1850,
        "price_lease_monthly": 50,
        "installation_cost": 300,
        "maintenance_yearly": 150,
        "dimensions": {"width": 0.25, "height": 0.35},
        "icon": "droplets",
        "color": "#06b6d4"
    },
    # UniFi Network - Switches & NVR
    {
        "name": "UniFi USW-Lite-8-PoE",
        "category": "wifi",
        "description": "8-poorts PoE switch, 4x PoE+ (52W budget), 1x GbE uplink, managed via UniFi Network",
        "price_purchase": 119,
        "price_lease_monthly": 4,
        "installation_cost": 50,
        "maintenance_yearly": 15,
        "dimensions": {"width": 0.2, "height": 0.1},
        "icon": "wifi",
        "color": "#10b981",
        "tier": "budget"
    },
    {
        "name": "UniFi UNVR Pro",
        "category": "camera",
        "description": "Network Video Recorder, 7x 3.5\" HDD bays (tot 84TB), tot 20 camera's, RAID, rackmount 1U",
        "price_purchase": 499,
        "price_lease_monthly": 15,
        "installation_cost": 200,
        "maintenance_yearly": 60,
        "dimensions": {"width": 0.44, "height": 0.04},
        "icon": "camera",
        "color": "#ef4444",
        "tier": "premium"
    },
    # IK Display Solutions - Outdoor Kiosken & Displays
    {
        "name": "IK 21.5\" Outdoor Portrait Kiosk",
        "category": "informatiezuil",
        "description": "21.5\" outdoor kiosk, 1500 nits, IP55, capacitive touch, QR scanner, camera, NFC kaartlezer. Ref: KIO-005",
        "price_purchase": 4800,
        "price_lease_monthly": 144,
        "installation_cost": 800,
        "maintenance_yearly": 300,
        "dimensions": {"width": 0.5, "height": 0.5},
        "icon": "monitor",
        "color": "#0891b2",
        "tier": "midrange"
    },
    {
        "name": "IK 21.5\" Outdoor Display Unit (wall)",
        "category": "informatiezuil",
        "description": "21.5\" outdoor wandmontage display, 1500 nits, IP55, touch, QR scanner, camera. Ref: AIO-009",
        "price_purchase": 3750,
        "price_lease_monthly": 113,
        "installation_cost": 600,
        "maintenance_yearly": 250,
        "dimensions": {"width": 0.4, "height": 0.4},
        "icon": "monitor",
        "color": "#0891b2",
        "tier": "budget"
    },
    {
        "name": "IK 55\" Outdoor Landscape Kiosk",
        "category": "informatiezuil",
        "description": "55\" outdoor landscape kiosk, 2500 nits, IP55, capacitive touch, QR scanner, speakers. Ref: KIO-015",
        "price_purchase": 5250,
        "price_lease_monthly": 158,
        "installation_cost": 1200,
        "maintenance_yearly": 400,
        "dimensions": {"width": 1.4, "height": 0.8},
        "icon": "monitor",
        "color": "#0891b2",
        "tier": "premium"
    },
    {
        "name": "IK 55\" Outdoor Portrait Kiosk",
        "category": "informatiezuil",
        "description": "55\" outdoor portrait kiosk, 2500 nits, IP55, capacitive touch, camera, speakers. Ref: KIO-017",
        "price_purchase": 4950,
        "price_lease_monthly": 149,
        "installation_cost": 1100,
        "maintenance_yearly": 380,
        "dimensions": {"width": 0.8, "height": 1.4},
        "icon": "monitor",
        "color": "#0891b2",
        "tier": "premium"
    },
    {
        "name": "IK 55\" Outdoor Display Unit",
        "category": "informatiezuil",
        "description": "55\" outdoor display, 2500 nits, IP65, no-touch, Android. Ref: AIO-008/NT",
        "price_purchase": 4750,
        "price_lease_monthly": 143,
        "installation_cost": 900,
        "maintenance_yearly": 350,
        "dimensions": {"width": 1.3, "height": 0.8},
        "icon": "monitor",
        "color": "#0891b2",
        "tier": "midrange"
    },
    # IK Display Solutions - Indoor Kiosken
    {
        "name": "IK 21.5\" Indoor Portrait Kiosk (tilted)",
        "category": "informatiezuil",
        "description": "21.5\" indoor kiosk schuin, 350 nits, IP21, capacitive touch, camera, speakers. Ref: KIO-002",
        "price_purchase": 3500,
        "price_lease_monthly": 105,
        "installation_cost": 500,
        "maintenance_yearly": 200,
        "dimensions": {"width": 0.4, "height": 0.5},
        "icon": "monitor",
        "color": "#0891b2",
        "tier": "budget"
    },
    {
        "name": "IK 43\" Indoor Landscape Kiosk (tilted)",
        "category": "informatiezuil",
        "description": "43\" indoor landscape kiosk schuin, 350 nits, IP21, capacitive touch, speakers. Ref: KIO-013",
        "price_purchase": 2500,
        "price_lease_monthly": 75,
        "installation_cost": 400,
        "maintenance_yearly": 150,
        "dimensions": {"width": 1.0, "height": 0.6},
        "icon": "monitor",
        "color": "#0891b2",
        "tier": "budget"
    },
    {
        "name": "IK 55\" Indoor Portrait Kiosk",
        "category": "informatiezuil",
        "description": "55\" indoor portrait kiosk, 350 nits, IP21, capacitive touch, speakers. Ref: KIO-014",
        "price_purchase": 2650,
        "price_lease_monthly": 80,
        "installation_cost": 500,
        "maintenance_yearly": 180,
        "dimensions": {"width": 0.8, "height": 1.4},
        "icon": "monitor",
        "color": "#0891b2",
        "tier": "midrange"
    },
    # ==================== TICRA OUTDOOR - Wellness Producten ====================
    # Hottubs
    {
        "name": "TICRA Hottub Houtgestookt",
        "category": "wellness",
        "subcategory": "hottub",
        "description": "Thermowood hottub met interne houtkachel, tot 6 personen. Gezellig buitenbad voor gasten.",
        "price_purchase": 2995,
        "price_lease_monthly": 54,
        "installation_cost": 350,
        "maintenance_yearly": 120,
        "dimensions": {"width": 1.8, "height": 1.8},
        "icon": "droplets",
        "color": "#8B5E3C",
        "tier": "budget",
        "supplier": "Ticra Outdoor",
        "image": "https://www.ticraoutdoor.com/nl/assets/galleries/133/_thumbs/medium_409_1_ticra_outdoor_hottub_hout_interne_kachel_welltub_160.webp"
    },
    {
        "name": "Skargards Rojal Hottub",
        "category": "wellness",
        "subcategory": "hottub",
        "description": "Zweedse premium hottub met geintegreerde kachel, tot 10 personen. Dualburn technologie.",
        "price_purchase": 4880,
        "price_lease_monthly": 88,
        "installation_cost": 450,
        "maintenance_yearly": 150,
        "dimensions": {"width": 2.2, "height": 2.2},
        "icon": "droplets",
        "color": "#8B5E3C",
        "tier": "midrange",
        "supplier": "Ticra Outdoor",
        "image": "https://www.ticraoutdoor.com/nl/assets/galleries/126/_thumbs/medium_327_1_ticra_outdoor_hot_tub_flevoland_skargards_rojal_190_dualburn_1.webp"
    },
    {
        "name": "Nordic Hottub Classic Serie",
        "category": "wellness",
        "subcategory": "hottub",
        "description": "Elektrische hottub, Red Cedar, massagejets, bubbels, tot 6 personen. Premium wellness.",
        "price_purchase": 7795,
        "price_lease_monthly": 140,
        "installation_cost": 600,
        "maintenance_yearly": 200,
        "dimensions": {"width": 2.0, "height": 2.0},
        "icon": "droplets",
        "color": "#8B5E3C",
        "tier": "premium",
        "supplier": "Ticra Outdoor",
        "image": "https://www.ticraoutdoor.com/nl/assets/galleries/95/_thumbs/medium_204_1_ticra_nordic_hot_tub_classic_series.webp"
    },
    {
        "name": "Nordic Hottub Spa",
        "category": "wellness",
        "subcategory": "hottub",
        "description": "Elektrische spa met 30+ massagejets, Red Cedar, tot 6 personen. Ultieme wellness ervaring.",
        "price_purchase": 8995,
        "price_lease_monthly": 162,
        "installation_cost": 800,
        "maintenance_yearly": 250,
        "dimensions": {"width": 2.1, "height": 2.1},
        "icon": "droplets",
        "color": "#8B5E3C",
        "tier": "premium",
        "supplier": "Ticra Outdoor",
        "image": "https://www.ticraoutdoor.com/nl/assets/galleries/124/_thumbs/medium_308_1_ticra_hot_tub_nordic_spa_encore_ls.webp"
    },
    {
        "name": "TICRA Hottub Warmtepomp 5kW",
        "category": "wellness",
        "subcategory": "hottub",
        "description": "Wifi-gestuurde warmtepomp hottub, Thermowood, tot 6 personen. Energiezuinig.",
        "price_purchase": 3595,
        "price_lease_monthly": 65,
        "installation_cost": 400,
        "maintenance_yearly": 100,
        "dimensions": {"width": 1.9, "height": 1.9},
        "icon": "droplets",
        "color": "#8B5E3C",
        "tier": "midrange",
        "supplier": "Ticra Outdoor",
        "image": "https://www.ticraoutdoor.com/nl/assets/galleries/1710/_thumbs/medium_3643-ticra-hottub-met-wifi-warmtepomp-thermowood-hottub-rand-2.webp"
    },
    # Sauna's
    {
        "name": "Barrel Sauna Nordic Grenen",
        "category": "wellness",
        "subcategory": "sauna",
        "description": "Barrel sauna, Nordic Grenen hout, houtkachel, max. 6 personen. Traditionele sauna.",
        "price_purchase": 3295,
        "price_lease_monthly": 59,
        "installation_cost": 300,
        "maintenance_yearly": 100,
        "dimensions": {"width": 2.0, "height": 2.0},
        "icon": "flame",
        "color": "#C7522A",
        "tier": "budget",
        "supplier": "Ticra Outdoor",
        "image": "https://www.ticraoutdoor.com/nl/assets/galleries/172/_thumbs/medium_606-barrel-sauna-thermo-hout-ticra-buitensauna-24.webp"
    },
    {
        "name": "Barrel Sauna Thermowood",
        "category": "wellness",
        "subcategory": "sauna",
        "description": "Barrel sauna, Thermowood, max. 6 personen, zonder veranda. Premium houtsoort.",
        "price_purchase": 5495,
        "price_lease_monthly": 99,
        "installation_cost": 350,
        "maintenance_yearly": 120,
        "dimensions": {"width": 2.0, "height": 2.0},
        "icon": "flame",
        "color": "#C7522A",
        "tier": "midrange",
        "supplier": "Ticra Outdoor",
        "image": "https://www.ticraoutdoor.com/nl/assets/galleries/97/_thumbs/medium_25-4-buitensauna-barrel-thermowood-ticra-outdoor.webp"
    },
    {
        "name": "Barrel Sauna met Veranda Red Cedar",
        "category": "wellness",
        "subcategory": "sauna",
        "description": "Luxe barrel sauna met veranda, Red Cedar, max. 6 personen. Overdekt rustgebied.",
        "price_purchase": 9795,
        "price_lease_monthly": 176,
        "installation_cost": 500,
        "maintenance_yearly": 180,
        "dimensions": {"width": 2.0, "height": 3.5},
        "icon": "flame",
        "color": "#C7522A",
        "tier": "premium",
        "supplier": "Ticra Outdoor",
        "image": "https://www.ticraoutdoor.com/nl/assets/galleries/98/_thumbs/medium_3577-knotty-barrel-sauna-4.webp"
    },
    {
        "name": "Pure Cube Buitensauna Red Cedar",
        "category": "wellness",
        "subcategory": "sauna",
        "description": "Moderne buitensauna, Red Cedar, panoramisch uitzicht, max. 6 personen.",
        "price_purchase": 8995,
        "price_lease_monthly": 162,
        "installation_cost": 600,
        "maintenance_yearly": 200,
        "dimensions": {"width": 2.3, "height": 2.3},
        "icon": "flame",
        "color": "#C7522A",
        "tier": "premium",
        "supplier": "Ticra Outdoor",
        "image": "https://www.ticraoutdoor.com/nl/assets/galleries/112/_thumbs/medium_124-2-pure-cube-red-cedar-knotty-buitensauna-panoramisch-uitzicht-tuinsauna-1.webp"
    },
    {
        "name": "Panorama Barrel Sauna Red Cedar",
        "category": "wellness",
        "subcategory": "sauna",
        "description": "Panoramische barrel sauna met veranda, Red Cedar, max. 6 personen. Spectaculair uitzicht.",
        "price_purchase": 14395,
        "price_lease_monthly": 259,
        "installation_cost": 800,
        "maintenance_yearly": 250,
        "dimensions": {"width": 2.0, "height": 4.0},
        "icon": "flame",
        "color": "#C7522A",
        "tier": "premium",
        "supplier": "Ticra Outdoor",
        "image": "https://www.ticraoutdoor.com/nl/assets/galleries/94/_thumbs/medium_1682-leisurecraft-europe-panoramic-sauna-knotty-red-cedar-outdoor-sauna.webp"
    },
    # Buitendouches
    {
        "name": "Sunlight Buitendouche Red Cedar",
        "category": "wellness",
        "subcategory": "buitendouche",
        "description": "Compacte buitendouche, Knotty Red Cedar. Ideaal bij hottub of sauna.",
        "price_purchase": 695,
        "price_lease_monthly": 13,
        "installation_cost": 150,
        "maintenance_yearly": 30,
        "dimensions": {"width": 0.8, "height": 0.8},
        "icon": "shower-head",
        "color": "#4A90D9",
        "tier": "budget",
        "supplier": "Ticra Outdoor",
        "image": "https://www.ticraoutdoor.com/nl/assets/galleries/141/_thumbs/medium_478_2_buitendouche_red_cedar_sunlightshower_ticra_outdoor_dundalk.webp"
    },
    {
        "name": "Savannah Buitendouche White Cedar",
        "category": "wellness",
        "subcategory": "buitendouche",
        "description": "Buitendouche, White Cedar, natuurlijk design. Duurzaam cederhout.",
        "price_purchase": 825,
        "price_lease_monthly": 15,
        "installation_cost": 150,
        "maintenance_yearly": 30,
        "dimensions": {"width": 0.8, "height": 0.8},
        "icon": "shower-head",
        "color": "#4A90D9",
        "tier": "budget",
        "supplier": "Ticra Outdoor",
        "image": "https://www.ticraoutdoor.com/nl/assets/galleries/147/_thumbs/medium_533_1_savannah_canadees_buitendouche_white_cedar_ticra_outdoor.webp"
    },
    {
        "name": "Cloudburst Buitendouche Red Cedar",
        "category": "wellness",
        "subcategory": "buitendouche",
        "description": "Luxe buitendouche met privacy-scherm, Knotty Red Cedar. Ruime doucheruimte.",
        "price_purchase": 3316,
        "price_lease_monthly": 60,
        "installation_cost": 250,
        "maintenance_yearly": 50,
        "dimensions": {"width": 1.2, "height": 1.2},
        "icon": "shower-head",
        "color": "#4A90D9",
        "tier": "midrange",
        "supplier": "Ticra Outdoor",
        "image": "https://www.ticraoutdoor.com/nl/assets/galleries/155/_thumbs/medium_542_1_buitendouche_shower_cloudburst_canadese_red_cedar_hout.webp"
    },
    {
        "name": "Barrel Buitendouche Red Cedar",
        "category": "wellness",
        "subcategory": "buitendouche",
        "description": "Unieke barrel-vormige buitendouche, Knotty Red Cedar. Eyecatcher op elk terrein.",
        "price_purchase": 3354,
        "price_lease_monthly": 60,
        "installation_cost": 250,
        "maintenance_yearly": 50,
        "dimensions": {"width": 1.2, "height": 1.2},
        "icon": "shower-head",
        "color": "#4A90D9",
        "tier": "midrange",
        "supplier": "Ticra Outdoor",
        "image": "https://www.ticraoutdoor.com/nl/assets/galleries/156/_thumbs/medium_555_1_barrel_buitendouche_ticra_red_cedar.webp"
    },
]

# ==================== ROUTES ====================

@api_router.get("/")
async def root():
    return {"message": "RECRA Solutions Configurator API"}

# Products endpoints
FLOW_CATEGORIES = {
    "recreatie": ["sanitair", "slagboom", "camera", "wifi", "verlichting", "betaalsysteem", "toegangscontrole", "douchelezer", "informatiezuil", "wellness"],
    "chalet": ["sanitair", "camera", "wifi", "verlichting", "betaalsysteem", "toegangscontrole", "douchelezer", "informatiezuil", "wellness"],
    "fec": ["camera", "wifi", "verlichting", "betaalsysteem", "toegangscontrole", "slagboom", "informatiezuil"],
}

@api_router.get("/products", response_model=List[Product])
async def get_products(flow: Optional[str] = None):
    query = {}
    if flow and flow in FLOW_CATEGORIES:
        query["category"] = {"$in": FLOW_CATEGORIES[flow]}
    products = await db.products.find(query, {"_id": 0}).to_list(1000)
    return products

@api_router.get("/products/category/{category}", response_model=List[Product])
async def get_products_by_category(category: str):
    products = await db.products.find({"category": category}, {"_id": 0}).to_list(1000)
    return products

@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = await db.products.find_one({"id": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product niet gevonden")
    return product

@api_router.post("/products", response_model=Product)
async def create_product(product_data: ProductCreate):
    product = Product(**product_data.model_dump())
    doc = product.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.products.insert_one(doc)
    return product

@api_router.get("/products/compare/{category}")
async def compare_products(category: str):
    """Vergelijk producten per tier (budget/midrange/premium) binnen een categorie."""
    products = await db.products.find({"category": category}, {"_id": 0}).to_list(100)
    result = {"budget": [], "midrange": [], "premium": []}
    for p in products:
        tier = p.get("tier", "midrange")
        if tier in result:
            result[tier].append(p)
    return result


# Projects endpoints
@api_router.get("/projects", response_model=List[Project])
async def get_projects():
    projects = await db.projects.find({}, {"_id": 0}).to_list(1000)
    for p in projects:
        if isinstance(p.get('created_at'), str):
            p['created_at'] = datetime.fromisoformat(p['created_at'])
        if isinstance(p.get('updated_at'), str):
            p['updated_at'] = datetime.fromisoformat(p['updated_at'])
    return projects

@api_router.get("/projects/{project_id}", response_model=Project)
async def get_project(project_id: str):
    project = await db.projects.find_one({"id": project_id}, {"_id": 0})
    if not project:
        raise HTTPException(status_code=404, detail="Project niet gevonden")
    if isinstance(project.get('created_at'), str):
        project['created_at'] = datetime.fromisoformat(project['created_at'])
    if isinstance(project.get('updated_at'), str):
        project['updated_at'] = datetime.fromisoformat(project['updated_at'])
    return project

@api_router.post("/projects", response_model=Project)
async def create_project(project_data: ProjectCreate):
    project = Project(**project_data.model_dump())
    doc = project.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    await db.projects.insert_one(doc)
    return project

@api_router.put("/projects/{project_id}", response_model=Project)
async def update_project(project_id: str, update_data: ProjectUpdate):
    existing = await db.projects.find_one({"id": project_id}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Project niet gevonden")
    
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
    update_dict['updated_at'] = datetime.now(timezone.utc).isoformat()
    
    await db.projects.update_one({"id": project_id}, {"$set": update_dict})
    
    updated = await db.projects.find_one({"id": project_id}, {"_id": 0})
    if isinstance(updated.get('created_at'), str):
        updated['created_at'] = datetime.fromisoformat(updated['created_at'])
    if isinstance(updated.get('updated_at'), str):
        updated['updated_at'] = datetime.fromisoformat(updated['updated_at'])
    return updated

@api_router.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    result = await db.projects.delete_one({"id": project_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project niet gevonden")
    return {"message": "Project verwijderd"}

# Quote calculation
@api_router.post("/quote/calculate", response_model=QuoteResponse)
async def calculate_quote(project_id: str):
    project = await db.projects.find_one({"id": project_id}, {"_id": 0})
    if not project:
        raise HTTPException(status_code=404, detail="Project niet gevonden")
    
    items = []
    capex_total = 0
    opex_monthly = 0
    installation_total = 0
    maintenance_yearly = 0
    
    placed_products = project.get('placed_products', [])
    product_counts = {}
    
    for pp in placed_products:
        pid = pp['product_id']
        qty = pp.get('quantity', 1)
        product_counts[pid] = product_counts.get(pid, 0) + qty
    
    # Collect categories used for travel cost calculation
    categories_used = set()
    
    for pid, qty in product_counts.items():
        product = await db.products.find_one({"id": pid}, {"_id": 0})
        if product:
            item_capex = product['price_purchase'] * qty
            item_opex = product['price_lease_monthly'] * qty
            item_install = product['installation_cost'] * qty
            item_maint = product['maintenance_yearly'] * qty
            
            items.append({
                "product_name": product['name'],
                "category": product['category'],
                "quantity": qty,
                "unit_price": product['price_purchase'],
                "total_price": item_capex,
                "lease_monthly": item_opex,
                "installation": item_install,
                "maintenance": item_maint
            })
            
            capex_total += item_capex
            opex_monthly += item_opex
            installation_total += item_install
            maintenance_yearly += item_maint
            categories_used.add(product['category'])
    
    # Calculate travel costs per category (nearest supplier)
    travel_costs = []
    travel_total = 0.0
    project_lat = project.get('lat', 52.0)
    project_lng = project.get('lng', 5.0)
    
    for category in categories_used:
        suppliers = await db.suppliers.find({"categories": category}, {"_id": 0}).to_list(100)
        if suppliers:
            best = None
            for sup in suppliers:
                tc = calculate_travel_cost(sup, project_lat, project_lng)
                if best is None or tc.total_travel_cost < best.total_travel_cost:
                    best = tc
            if best:
                travel_costs.append({
                    "category": category,
                    "supplier_name": best.supplier_name,
                    "distance_km": best.distance_km,
                    "travel_time_hours": best.travel_time_hours,
                    "total_travel_cost": best.total_travel_cost,
                })
                travel_total += best.total_travel_cost
    
    return QuoteResponse(
        capex_total=capex_total,
        opex_monthly=opex_monthly,
        opex_yearly=opex_monthly * 12,
        installation_total=installation_total,
        maintenance_yearly=maintenance_yearly,
        travel_costs=travel_costs,
        travel_total=round(travel_total, 2),
        project_total=round(capex_total + installation_total + travel_total, 2),
        items=items
    )

# AI Recommendations - Rule-based (lightweight, saves AI credits)
@api_router.post("/ai/recommendations", response_model=AIAnalysisResponse)
async def get_ai_recommendations(project_id: str, use_ai: bool = False):
    project = await db.projects.find_one({"id": project_id}, {"_id": 0})
    if not project:
        raise HTTPException(status_code=404, detail="Project niet gevonden")
    
    products = await db.products.find({}, {"_id": 0}).to_list(1000)
    products_by_id = {p['id']: p for p in products}
    
    placed_products = project.get('placed_products', [])
    num_spots = project.get('num_spots', 0)
    
    category_counts = {}
    for pp in placed_products:
        product = products_by_id.get(pp['product_id'])
        if product:
            cat = product['category']
            category_counts[cat] = category_counts.get(cat, 0) + pp.get('quantity', 1)
    
    # Always use rule-based by default (saves credits)
    return generate_rule_based_recommendations(project, category_counts, num_spots, products)

def generate_rule_based_recommendations(project, category_counts, num_spots, products):
    recommendations = []
    
    # Rule 1: Sanitair check (1 unit per 20 spots)
    sanitair_count = category_counts.get('sanitair', 0)
    required_sanitair = max(1, num_spots // 20) if num_spots > 0 else 0
    if sanitair_count < required_sanitair:
        recommendations.append(AIRecommendation(
            type="warning",
            title="Onvoldoende sanitair",
            description=f"Met {num_spots} standplaatsen adviseren wij minimaal {required_sanitair} sanitair unit(s). U heeft er {sanitair_count}.",
            action="Voeg sanitair units toe"
        ))
    elif sanitair_count > 0 and num_spots > 30 and sanitair_count < 2:
        recommendations.append(AIRecommendation(
            type="suggestion",
            title="Overweeg extra sanitair",
            description=f"Bij {num_spots} standplaatsen adviseren wij minimaal 2 sanitair units voor comfort en spreiding.",
            action="Voeg een tweede sanitair unit toe"
        ))
    
    # Rule 2: WiFi check (1 AP per 30 spots)
    wifi_count = category_counts.get('wifi', 0)
    required_wifi = max(1, num_spots // 30) if num_spots > 0 else 0
    if wifi_count < required_wifi:
        recommendations.append(AIRecommendation(
            type="suggestion",
            title="WiFi dekking uitbreiden",
            description=f"Voor optimale dekking van {num_spots} standplaatsen adviseren wij minimaal {required_wifi} access point(s). U heeft er {wifi_count}.",
            action="Voeg WiFi access points toe"
        ))
    
    # Rule 3: Camera bewaking
    camera_count = category_counts.get('camera', 0)
    if camera_count == 0 and num_spots > 0:
        recommendations.append(AIRecommendation(
            type="suggestion",
            title="Camerabewaking ontbreekt",
            description="Overweeg camera's te plaatsen bij toegangswegen en centrale zones voor veiligheid.",
            action="Voeg camera's toe"
        ))
    elif camera_count > 0 and camera_count < 3 and num_spots > 30:
        recommendations.append(AIRecommendation(
            type="optimization",
            title="Camera dekking verbeteren",
            description=f"Bij {num_spots} plekken adviseren wij minimaal 3 camera's voor volledige dekking.",
            action="Voeg extra camera's toe"
        ))
    
    # Rule 4: Toegangscontrole
    slagboom_count = category_counts.get('slagboom', 0)
    if slagboom_count == 0 and num_spots > 10:
        recommendations.append(AIRecommendation(
            type="optimization",
            title="Toegangscontrole optimaliseren",
            description="Een slagboom met toegangscontrole verbetert de veiligheid en registratie van gasten.",
            action="Voeg een slagboom toe"
        ))
    
    # Rule 5: Verlichting
    verlichting_count = category_counts.get('verlichting', 0)
    if verlichting_count == 0 and num_spots > 0:
        recommendations.append(AIRecommendation(
            type="suggestion",
            title="Terreinverlichting toevoegen",
            description="LED-verlichting verhoogt de veiligheid en het comfort op uw terrein.",
            action="Voeg verlichting toe"
        ))
    
    # Rule 6: Betaalsysteem check
    betaal_count = category_counts.get('betaalsysteem', 0)
    douchelezer_count = category_counts.get('douchelezer', 0)
    if betaal_count == 0 and sanitair_count > 0 and douchelezer_count == 0:
        recommendations.append(AIRecommendation(
            type="suggestion",
            title="Betaalsysteem overwegen",
            description="Met sanitair units geplaatst adviseren wij een Adyen betaalterminal of douchelezer voor automatische afrekening.",
            action="Voeg betaalsysteem of douchelezer toe"
        ))
    
    # Rule 7: Kentekenherkenning bij slagboom
    if slagboom_count > 0 and camera_count > 0:
        # Check if they have LPR camera
        has_lpr = any(
            'LPR' in p.get('name', '') 
            for p in products 
            if p.get('id') in [pp['product_id'] for pp in project.get('placed_products', [])]
        )
        if not has_lpr:
            recommendations.append(AIRecommendation(
                type="optimization",
                title="Kentekenherkenning toevoegen",
                description="Combineer uw slagboom met een AI LPR camera voor automatische kentekendoorgang.",
                action="Voeg UniFi AI LPR Camera toe"
            ))
    
    # Rule 8: Large parks need mesh WiFi
    if num_spots > 50 and wifi_count > 0 and wifi_count < 3:
        recommendations.append(AIRecommendation(
            type="warning",
            title="WiFi capaciteit onvoldoende",
            description=f"Een park met {num_spots} plekken heeft een mesh WiFi systeem nodig voor stabiele dekking.",
            action="Upgrade naar Mesh WiFi Systeem"
        ))
    
    if not recommendations:
        recommendations.append(AIRecommendation(
            type="optimization",
            title="Configuratie ziet er goed uit!",
            description="Uw huidige configuratie lijkt compleet. Bekijk de offerte voor prijsdetails.",
            action=None
        ))
    
    return AIAnalysisResponse(recommendations=recommendations[:5])

# Floor plan analysis
@api_router.post("/ai/analyze-floorplan")
async def analyze_floorplan(image_base64: str, project_type: str = "camping"):
    try:
        llm_key = os.environ.get('EMERGENT_LLM_KEY')
        if not llm_key:
            return {"error": "AI niet geconfigureerd", "detected_zones": []}
        
        chat = LlmChat(
            api_key=llm_key,
            session_id=f"floorplan-{uuid.uuid4()}",
            system_message="""Je bent een expert in het analyseren van plattegronden voor recreatieparken.
            Analyseer de afbeelding en identificeer zones.
            Geef je antwoord in JSON format:
            {
                "zones": [
                    {"name": "Zone naam", "type": "standplaats|sanitair|toegangsweg|technisch", "description": "beschrijving"}
                ],
                "estimated_spots": nummer,
                "suggestions": ["suggestie 1", "suggestie 2"]
            }
            """
        ).with_model("openai", "gpt-5.2")
        
        # Clean base64 if it has data URL prefix
        if ',' in image_base64:
            image_base64 = image_base64.split(',')[1]
        
        image_content = ImageContent(image_base64=image_base64)
        
        response = await chat.send_message(UserMessage(
            text=f"Analyseer deze plattegrond voor een {project_type}. Identificeer mogelijke zones en schat het aantal standplaatsen.",
            file_contents=[image_content]
        ))
        
        import json
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                result = json.loads(response[json_start:json_end])
                return result
        except:
            pass
        
        return {
            "zones": [],
            "estimated_spots": 0,
            "suggestions": ["Kon de plattegrond niet automatisch analyseren. Definieer zones handmatig."],
            "raw_response": response
        }
        
    except Exception as e:
        logger.error(f"Floor plan analysis error: {e}")
        return {"error": str(e), "zones": [], "estimated_spots": 0}

# PDF Generation endpoint — Verbeterde Recreatie Business Case
@api_router.post("/quote/pdf")
async def generate_quote_pdf(project_id: str):
    project = await db.projects.find_one({"id": project_id}, {"_id": 0})
    if not project:
        raise HTTPException(status_code=404, detail="Project niet gevonden")

    quote_response = await calculate_quote(project_id)
    all_products = await db.products.find({}, {"_id": 0}).to_list(100)

    # Categorize products
    cat_totals = {}
    for item in quote_response.items:
        cat = item.get("category", "overig").title()
        if cat not in cat_totals:
            cat_totals[cat] = {"count": 0, "total": 0, "lease": 0}
        cat_totals[cat]["count"] += item.get("quantity", 1)
        cat_totals[cat]["total"] += item.get("total_price", 0)
        cat_totals[cat]["lease"] += item.get("lease_monthly", 0) * item.get("quantity", 1)

    products_html = ""
    for item in quote_response.items:
        products_html += f"""
        <tr>
            <td>{item['product_name']}</td>
            <td>{item['category'].title()}</td>
            <td class="center">{item['quantity']}</td>
            <td class="price">€ {item['unit_price']:,.0f}</td>
            <td class="price">€ {item.get('lease_monthly', 0):,.0f}</td>
            <td class="price bold">€ {item['total_price']:,.0f}</td>
        </tr>"""

    cat_html = ""
    for cat, data in cat_totals.items():
        cat_html += f"""
        <div class="cat-card">
            <div class="cat-label">{cat}</div>
            <div class="cat-value">€ {data['total']:,.0f}</div>
            <div class="cat-sub">{data['count']} producten · € {data['lease']:,.0f}/mnd</div>
        </div>"""

    project_name = project.get('name', 'Project')
    project_type = project.get('project_type', 'camping').replace('_', ' ').title()
    num_spots = project.get('num_spots', 0)
    annual_lease = quote_response.opex_yearly
    total_inv = quote_response.project_total

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; padding: 40px; color: #333; max-width: 900px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 3px solid #70C26C; }}
        .logo {{ font-size: 28px; font-weight: bold; color: #244628; letter-spacing: 3px; }}
        .subtitle {{ color: #70C26C; font-size: 13px; margin-top: 4px; }}
        .badge {{ display: inline-block; background: #70C26C; color: white; padding: 3px 14px; border-radius: 20px; font-size: 11px; font-weight: 600; margin-top: 8px; }}
        h1 {{ color: #244628; font-size: 22px; margin-bottom: 8px; }}
        h2 {{ color: #333; margin-top: 30px; font-size: 15px; border-bottom: 1px solid #e5e2d9; padding-bottom: 8px; }}
        .meta {{ color: #777; font-size: 13px; line-height: 1.6; }}
        .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 20px 0; }}
        .metric {{ background: #fafaf7; border: 1px solid #e5e2d9; border-radius: 12px; padding: 16px; text-align: center; }}
        .metric .label {{ font-size: 10px; color: #999; text-transform: uppercase; letter-spacing: 0.5px; }}
        .metric .value {{ font-size: 22px; font-weight: bold; margin-top: 4px; }}
        .metric .value.green {{ color: #10b981; }}
        .metric .value.amber {{ color: #f59e0b; }}
        .metric .value.dark {{ color: #244628; }}
        .cats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 16px 0; }}
        .cat-card {{ background: white; border: 1px solid #e5e2d9; border-radius: 10px; padding: 12px; }}
        .cat-label {{ font-size: 11px; color: #999; text-transform: uppercase; letter-spacing: 0.5px; }}
        .cat-value {{ font-size: 16px; font-weight: bold; color: #244628; margin-top: 4px; }}
        .cat-sub {{ font-size: 10px; color: #999; margin-top: 2px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 12px; }}
        th {{ background: #244628; color: white; padding: 10px 8px; text-align: left; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; }}
        td {{ padding: 10px 8px; border-bottom: 1px solid #e5e2d9; }}
        .center {{ text-align: center; }}
        .price {{ font-family: 'Courier New', monospace; text-align: right; }}
        .bold {{ font-weight: bold; }}
        .summary {{ background: #f0fdf4; border: 1px solid #86efac; border-radius: 12px; padding: 20px; margin: 24px 0; }}
        .summary h3 {{ color: #10b981; margin: 0 0 12px; font-size: 14px; }}
        .summary-row {{ display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #dcfce7; font-size: 13px; }}
        .summary-row.total {{ font-weight: bold; font-size: 15px; border-bottom: none; padding-top: 10px; }}
        .lease-box {{ background: #244628; color: white; border-radius: 12px; padding: 20px; margin: 24px 0; }}
        .lease-box h3 {{ color: #70C26C; margin: 0 0 12px; font-size: 14px; }}
        .lease-row {{ display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.1); font-size: 13px; }}
        .lease-row .label {{ color: rgba(255,255,255,0.7); }}
        .lease-row .value {{ font-weight: bold; }}
        .supplier-section {{ margin-top: 24px; }}
        .supplier-tag {{ display: inline-block; background: #70C26C15; color: #244628; font-size: 10px; padding: 4px 10px; border-radius: 12px; margin: 3px; border: 1px solid #70C26C30; }}
        .footer {{ margin-top: 40px; text-align: center; color: #999; font-size: 10px; padding-top: 20px; border-top: 1px solid #e5e2d9; }}
        @media print {{ body {{ padding: 20px; }} }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">RECRA</div>
        <div class="subtitle">S O L U T I O N S</div>
        <div class="badge">Recreatie Infra — Offerte & Business Case</div>
    </div>

    <h1>{project_name}</h1>
    <div class="meta">
        <strong>Type:</strong> {project_type} · <strong>Standplaatsen:</strong> {num_spots} ·
        <strong>Datum:</strong> {datetime.now().strftime('%d-%m-%Y')} ·
        <strong>Geldig tot:</strong> {(datetime.now().replace(day=datetime.now().day)).strftime('%d-%m-%Y')} + 30 dagen
    </div>

    <div class="metrics">
        <div class="metric">
            <div class="label">Totale Investering</div>
            <div class="value dark">€ {total_inv:,.0f}</div>
        </div>
        <div class="metric">
            <div class="label">Lease / Maand</div>
            <div class="value green">€ {quote_response.opex_monthly:,.0f}</div>
        </div>
        <div class="metric">
            <div class="label">Lease / Jaar</div>
            <div class="value amber">€ {annual_lease:,.0f}</div>
        </div>
        <div class="metric">
            <div class="label">Producten</div>
            <div class="value dark">{len(quote_response.items)}</div>
        </div>
    </div>

    <h2>Investeringsoverzicht per categorie</h2>
    <div class="cats">{cat_html}</div>

    <h2>Productoverzicht</h2>
    <table>
        <thead>
            <tr>
                <th>Product</th>
                <th>Categorie</th>
                <th>Aantal</th>
                <th>Stukprijs</th>
                <th>Lease/mnd</th>
                <th>Totaal</th>
            </tr>
        </thead>
        <tbody>
            {products_html}
        </tbody>
    </table>

    <div class="summary">
        <h3>Kostenoverzicht</h3>
        <div class="summary-row">
            <span>Aankoopkosten</span>
            <span class="price">€ {quote_response.capex_total:,.0f}</span>
        </div>
        <div class="summary-row">
            <span>Installatiekosten</span>
            <span class="price">€ {quote_response.installation_total:,.0f}</span>
        </div>
        <div class="summary-row">
            <span>Reiskosten leveranciers</span>
            <span class="price">€ {quote_response.travel_total:,.0f}</span>
        </div>
        <div class="summary-row total">
            <span>Totaal investering</span>
            <span class="price" style="color:#244628;">€ {total_inv:,.0f}</span>
        </div>
    </div>

    <div class="lease-box">
        <h3>Operational Lease Optie</h3>
        <div class="lease-row">
            <span class="label">Lease per maand</span>
            <span class="value" style="color:#f59e0b;">€ {quote_response.opex_monthly:,.0f}</span>
        </div>
        <div class="lease-row">
            <span class="label">Lease per jaar</span>
            <span class="value">€ {annual_lease:,.0f}</span>
        </div>
        <div class="lease-row">
            <span class="label">Onderhoud per jaar</span>
            <span class="value">€ {quote_response.maintenance_yearly:,.0f}</span>
        </div>
        <div class="lease-row">
            <span class="label">Looptijd</span>
            <span class="value">60 maanden</span>
        </div>
        <p style="font-size:10px;color:rgba(255,255,255,0.4);margin-top:10px;">Inclusief SLA onderhoudscontract. Prijzen excl. BTW.</p>
    </div>

    <div class="footer">
        <p><strong>RECRA Solutions</strong> — Recreation Project Configurator & Partner Matching Platform</p>
        <p>info@recrasolutions.com · +31 634200253 · www.recrasolutions.com</p>
        <p>Powered by Pleisureworld x RECRA Solutions</p>
    </div>
</body>
</html>"""

    return {
        "html": html_content,
        "project_name": project_name,
        "quote": quote_response.model_dump()
    }

# Seed products on startup
@api_router.post("/seed-products")
async def seed_products():
    existing = await db.products.count_documents({})
    if existing > 0:
        return {"message": f"Database bevat al {existing} producten", "seeded": False}
    
    for product_data in SEED_PRODUCTS:
        product = Product(**product_data)
        doc = product.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        await db.products.insert_one(doc)
    
    return {"message": f"{len(SEED_PRODUCTS)} producten toegevoegd", "seeded": True}

# Include the router in the main app
# Include routers
app.include_router(api_router)
app.include_router(ai_router)
app.include_router(supplier_router)
app.include_router(fec_router, prefix="/api")
app.include_router(horeca_router, prefix="/api")
app.include_router(chalet_router, prefix="/api")
app.include_router(supabase_router, prefix="/api")
app.include_router(location_router, prefix="/api")
app.include_router(partner_router, prefix="/api")
app.include_router(roadmap_router, prefix="/api")
app.include_router(whitelabel_router, prefix="/api")
app.include_router(subsidy_router, prefix="/api")
app.include_router(crm_router, prefix="/api")
app.include_router(auth_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Remove banned and outdated products
    await db.products.delete_many({"name": {"$regex": "Muntautomaat"}})
    await db.products.delete_many({"name": {"$in": [
        "IP Camera Basis", "PTZ Camera Pro", "ANPR Camera",
        "Basis Slagboom", "Automatische Slagboom",
        "RFID Lezer", "Mobile Key Systeem", "Biometrisch Toegangssysteem"
    ]}})
    
    # Update sanitair dimensions + tiers
    tier_mapping = {
        "Compact Sanitair Unit": {"tier": "budget", "dimensions": {"width": 3, "height": 6}},
        "Medium Sanitair Unit": {"tier": "midrange", "dimensions": {"width": 6, "height": 8}},
        "Premium Sanitair Blok": {"tier": "premium", "dimensions": {"width": 8, "height": 12}},
        "Nice M5BAR": {"tier": "budget"},
        "Nice M5BAR + Kentekenherkenning": {"tier": "midrange"},
        "Premium Toegangspoort": {"tier": "premium"},
        "UniFi G5 Bullet": {"tier": "budget"},
        "UniFi G5 Dome Ultra": {"tier": "budget"},
        "UniFi G5 Turret Ultra": {"tier": "midrange"},
        "UniFi G5 Pro": {"tier": "premium"},
        "UniFi AI LPR Camera": {"tier": "premium"},
        "UniFi Access Reader Lite (UA-Lite)": {"tier": "budget"},
        "UniFi Access Hub": {"tier": "budget"},
        "UniFi Access Reader Pro (UA-Pro)": {"tier": "midrange"},
        "UniFi Access Starter Kit": {"tier": "premium"},
        "WiFi Access Point Indoor": {"tier": "budget"},
        "WiFi Access Point Outdoor": {"tier": "midrange"},
        "Solar LED Padverlichting": {"tier": "budget"},
        "Slimme Lichtmast": {"tier": "premium"},
        "Adyen Betaalterminal": {"tier": "budget"},
        "Adyen + Reserveringssysteem": {"tier": "premium"},
        "Douchelezer Basis": {"tier": "budget"},
        "Douchelezer Pro": {"tier": "midrange"},
        "Douchelezer Enterprise": {"tier": "premium"},
        "IK 21.5\" Outdoor Portrait Kiosk": {"tier": "midrange"},
        "IK 21.5\" Outdoor Display Unit (wall)": {"tier": "budget"},
        "IK 55\" Outdoor Landscape Kiosk": {"tier": "premium"},
        "IK 55\" Outdoor Portrait Kiosk": {"tier": "premium"},
        "IK 55\" Outdoor Display Unit": {"tier": "midrange"},
        "IK 21.5\" Indoor Portrait Kiosk (tilted)": {"tier": "budget"},
        "IK 43\" Indoor Landscape Kiosk (tilted)": {"tier": "budget"},
        "IK 55\" Indoor Portrait Kiosk": {"tier": "midrange"},
    }
    
    for name, updates in tier_mapping.items():
        await db.products.update_one({"name": name}, {"$set": updates})
    
    # Ensure all products exist (upsert by name)
    for product_data in SEED_PRODUCTS:
        existing = await db.products.find_one({"name": product_data["name"]})
        if not existing:
            product = Product(**product_data)
            doc = product.model_dump()
            doc['created_at'] = doc['created_at'].isoformat()
            await db.products.insert_one(doc)
            logger.info(f"Added product: {product_data['name']}")
    
    existing = await db.products.count_documents({})
    logger.info(f"Database contains {existing} products")
    
    # Seed suppliers
    await seed_suppliers(db)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
