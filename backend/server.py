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
    category: str  # sanitair, slagboom, camera, wifi, verlichting, betaalsysteem, toegangscontrole
    description: str
    price_purchase: float
    price_lease_monthly: float
    installation_cost: float
    maintenance_yearly: float
    dimensions: Dict[str, float] = Field(default_factory=lambda: {"width": 1, "height": 1})
    coverage_radius: Optional[float] = None  # For WiFi, cameras
    icon: str = "box"
    color: str = "#0ea5e9"

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
    project_type: str  # camperplaats, camping, resort, tijdelijke_housing
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
    # Sanitair units
    {
        "name": "Compact Sanitair Unit",
        "category": "sanitair",
        "description": "2 toiletten, 2 douches, geschikt voor 15-20 standplaatsen",
        "price_purchase": 18500,
        "price_lease_monthly": 450,
        "installation_cost": 2500,
        "maintenance_yearly": 1200,
        "dimensions": {"width": 3, "height": 2.5},
        "icon": "bath",
        "color": "#0ea5e9"
    },
    {
        "name": "Medium Sanitair Unit",
        "category": "sanitair",
        "description": "4 toiletten, 4 douches, geschikt voor 30-40 standplaatsen",
        "price_purchase": 32000,
        "price_lease_monthly": 750,
        "installation_cost": 4000,
        "maintenance_yearly": 2000,
        "dimensions": {"width": 5, "height": 3},
        "icon": "bath",
        "color": "#0ea5e9"
    },
    {
        "name": "Premium Sanitair Blok",
        "category": "sanitair",
        "description": "6 toiletten, 6 douches, familiecabines, geschikt voor 50+ standplaatsen",
        "price_purchase": 55000,
        "price_lease_monthly": 1200,
        "installation_cost": 6500,
        "maintenance_yearly": 3500,
        "dimensions": {"width": 8, "height": 4},
        "icon": "bath",
        "color": "#0ea5e9"
    },
    # Slagbomen
    {
        "name": "Basis Slagboom",
        "category": "slagboom",
        "description": "Handmatige bediening, 4m arm",
        "price_purchase": 1800,
        "price_lease_monthly": 45,
        "installation_cost": 500,
        "maintenance_yearly": 150,
        "dimensions": {"width": 0.5, "height": 4},
        "icon": "boom",
        "color": "#f59e0b"
    },
    {
        "name": "Automatische Slagboom",
        "category": "slagboom",
        "description": "Geautomatiseerd met RFID/nummerplaat, 5m arm",
        "price_purchase": 4500,
        "price_lease_monthly": 120,
        "installation_cost": 1200,
        "maintenance_yearly": 350,
        "dimensions": {"width": 0.5, "height": 5},
        "icon": "boom",
        "color": "#f59e0b"
    },
    {
        "name": "Premium Toegangspoort",
        "category": "slagboom",
        "description": "Dubbele slagboom met camera, intercom en betaalterminal",
        "price_purchase": 12000,
        "price_lease_monthly": 280,
        "installation_cost": 3500,
        "maintenance_yearly": 800,
        "dimensions": {"width": 1, "height": 6},
        "icon": "boom",
        "color": "#f59e0b"
    },
    # Camera systemen
    {
        "name": "IP Camera Basis",
        "category": "camera",
        "description": "2K resolutie, nachtzicht, 30m bereik",
        "price_purchase": 350,
        "price_lease_monthly": 12,
        "installation_cost": 150,
        "maintenance_yearly": 50,
        "dimensions": {"width": 0.3, "height": 0.3},
        "coverage_radius": 30,
        "icon": "camera",
        "color": "#ef4444"
    },
    {
        "name": "PTZ Camera Pro",
        "category": "camera",
        "description": "4K, 360° draaibaar, 50m bereik, AI-detectie",
        "price_purchase": 1200,
        "price_lease_monthly": 35,
        "installation_cost": 350,
        "maintenance_yearly": 120,
        "dimensions": {"width": 0.4, "height": 0.4},
        "coverage_radius": 50,
        "icon": "camera",
        "color": "#ef4444"
    },
    {
        "name": "ANPR Camera",
        "category": "camera",
        "description": "Nummerplaatherkenning, integratie met toegangssysteem",
        "price_purchase": 2500,
        "price_lease_monthly": 65,
        "installation_cost": 600,
        "maintenance_yearly": 200,
        "dimensions": {"width": 0.4, "height": 0.4},
        "coverage_radius": 15,
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
    # Toegangscontrole
    {
        "name": "RFID Lezer",
        "category": "toegangscontrole",
        "description": "Kaart/tag lezer, integratie met slagboom",
        "price_purchase": 450,
        "price_lease_monthly": 12,
        "installation_cost": 150,
        "maintenance_yearly": 50,
        "dimensions": {"width": 0.2, "height": 0.2},
        "icon": "key",
        "color": "#ec4899"
    },
    {
        "name": "Mobile Key Systeem",
        "category": "toegangscontrole",
        "description": "Smartphone toegang via app, QR-code ondersteuning",
        "price_purchase": 1500,
        "price_lease_monthly": 40,
        "installation_cost": 500,
        "maintenance_yearly": 150,
        "dimensions": {"width": 0.3, "height": 0.3},
        "icon": "key",
        "color": "#ec4899"
    },
    {
        "name": "Biometrisch Toegangssysteem",
        "category": "toegangscontrole",
        "description": "Vingerafdruk + gezichtsherkenning",
        "price_purchase": 3500,
        "price_lease_monthly": 90,
        "installation_cost": 800,
        "maintenance_yearly": 300,
        "dimensions": {"width": 0.4, "height": 0.4},
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
    {
        "name": "Elektra Muntautomaat",
        "category": "douchelezer",
        "description": "Contactloze betaling voor elektra op standplaatsen",
        "price_purchase": 950,
        "price_lease_monthly": 28,
        "installation_cost": 175,
        "maintenance_yearly": 80,
        "dimensions": {"width": 0.2, "height": 0.3},
        "icon": "droplets",
        "color": "#06b6d4"
    },
]

# ==================== ROUTES ====================

@api_router.get("/")
async def root():
    return {"message": "RECRA Solutions Configurator API"}

# Products endpoints
@api_router.get("/products", response_model=List[Product])
async def get_products():
    products = await db.products.find({}, {"_id": 0}).to_list(1000)
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
    
    return QuoteResponse(
        capex_total=capex_total,
        opex_monthly=opex_monthly,
        opex_yearly=opex_monthly * 12,
        installation_total=installation_total,
        maintenance_yearly=maintenance_yearly,
        items=items
    )

# AI Recommendations
@api_router.post("/ai/recommendations", response_model=AIAnalysisResponse)
async def get_ai_recommendations(project_id: str):
    project = await db.projects.find_one({"id": project_id}, {"_id": 0})
    if not project:
        raise HTTPException(status_code=404, detail="Project niet gevonden")
    
    products = await db.products.find({}, {"_id": 0}).to_list(1000)
    products_by_id = {p['id']: p for p in products}
    
    placed_products = project.get('placed_products', [])
    num_spots = project.get('num_spots', 0)
    
    # Count products by category
    category_counts = {}
    for pp in placed_products:
        product = products_by_id.get(pp['product_id'])
        if product:
            cat = product['category']
            category_counts[cat] = category_counts.get(cat, 0) + pp.get('quantity', 1)
    
    # Build context for AI
    context = f"""
    Project: {project.get('name', 'Nieuw project')}
    Type: {project.get('project_type', 'camping')}
    Aantal standplaatsen: {num_spots}
    
    Geplaatste producten per categorie:
    {', '.join([f"{cat}: {count}" for cat, count in category_counts.items()]) or 'Geen producten geplaatst'}
    
    Beschikbare productcategorieën: sanitair, slagboom, camera, wifi, verlichting, betaalsysteem, toegangscontrole
    """
    
    try:
        llm_key = os.environ.get('EMERGENT_LLM_KEY')
        if not llm_key:
            # Return rule-based recommendations if no API key
            return generate_rule_based_recommendations(project, category_counts, num_spots, products)
        
        chat = LlmChat(
            api_key=llm_key,
            session_id=f"recra-{project_id}-{uuid.uuid4()}",
            system_message="""Je bent een expert adviseur voor recreatieparken en campings. 
            Analyseer de configuratie en geef concrete, actionable aanbevelingen in het Nederlands.
            Focus op:
            1. Sanitaire voorzieningen (minimaal 1 unit per 20 standplaatsen)
            2. WiFi dekking (minimaal 1 access point per 30 standplaatsen)
            3. Camerabewaking (minimale dekking van toegangswegen)
            4. Verlichting (veiligheid en comfort)
            5. Toegangscontrole (efficiëntie en veiligheid)
            
            Geef maximaal 5 aanbevelingen in JSON format:
            [{"type": "warning|suggestion|optimization", "title": "korte titel", "description": "uitleg", "action": "specifieke actie"}]
            """
        ).with_model("openai", "gpt-5.2")
        
        response = await chat.send_message(UserMessage(
            text=f"Analyseer deze camping configuratie en geef aanbevelingen:\n{context}"
        ))
        
        # Parse AI response
        import json
        try:
            # Try to extract JSON from response
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start >= 0 and json_end > json_start:
                recommendations_json = json.loads(response[json_start:json_end])
                recommendations = [AIRecommendation(**r) for r in recommendations_json]
                return AIAnalysisResponse(recommendations=recommendations)
        except:
            pass
        
        # Fallback to rule-based
        return generate_rule_based_recommendations(project, category_counts, num_spots, products)
        
    except Exception as e:
        logger.error(f"AI recommendation error: {e}")
        return generate_rule_based_recommendations(project, category_counts, num_spots, products)

def generate_rule_based_recommendations(project, category_counts, num_spots, products):
    recommendations = []
    
    # Sanitair check
    sanitair_count = category_counts.get('sanitair', 0)
    required_sanitair = max(1, num_spots // 20) if num_spots > 0 else 0
    if sanitair_count < required_sanitair:
        recommendations.append(AIRecommendation(
            type="warning",
            title="Onvoldoende sanitair",
            description=f"Met {num_spots} standplaatsen adviseren wij minimaal {required_sanitair} sanitair unit(s). U heeft er {sanitair_count}.",
            action="Voeg sanitair units toe"
        ))
    
    # WiFi check
    wifi_count = category_counts.get('wifi', 0)
    required_wifi = max(1, num_spots // 30) if num_spots > 0 else 0
    if wifi_count < required_wifi:
        recommendations.append(AIRecommendation(
            type="suggestion",
            title="WiFi dekking uitbreiden",
            description=f"Voor optimale dekking van {num_spots} standplaatsen adviseren wij minimaal {required_wifi} access point(s).",
            action="Voeg WiFi access points toe"
        ))
    
    # Camera check
    camera_count = category_counts.get('camera', 0)
    if camera_count == 0 and num_spots > 0:
        recommendations.append(AIRecommendation(
            type="suggestion",
            title="Camerabewaking ontbreekt",
            description="Overweeg camera's te plaatsen bij toegangswegen en centrale zones voor veiligheid.",
            action="Voeg camera's toe"
        ))
    
    # Access control check
    slagboom_count = category_counts.get('slagboom', 0)
    toegang_count = category_counts.get('toegangscontrole', 0)
    if slagboom_count == 0 and num_spots > 10:
        recommendations.append(AIRecommendation(
            type="optimization",
            title="Toegangscontrole optimaliseren",
            description="Een slagboom met toegangscontrole verbetert de veiligheid en registratie van gasten.",
            action="Voeg een slagboom toe"
        ))
    
    # Lighting check
    verlichting_count = category_counts.get('verlichting', 0)
    if verlichting_count == 0 and num_spots > 0:
        recommendations.append(AIRecommendation(
            type="suggestion",
            title="Terreinverlichting toevoegen",
            description="LED-verlichting verhoogt de veiligheid en het comfort op uw terrein.",
            action="Voeg verlichting toe"
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

# PDF Generation endpoint
@api_router.post("/quote/pdf")
async def generate_quote_pdf(project_id: str):
    project = await db.projects.find_one({"id": project_id}, {"_id": 0})
    if not project:
        raise HTTPException(status_code=404, detail="Project niet gevonden")
    
    # Calculate quote
    quote_response = await calculate_quote(project_id)
    
    # Generate simple HTML-based PDF content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; padding: 40px; color: #333; }}
            .header {{ text-align: center; margin-bottom: 40px; }}
            .logo {{ font-size: 32px; font-weight: bold; color: #0ea5e9; }}
            .subtitle {{ color: #10b981; margin-top: 5px; }}
            h1 {{ color: #0ea5e9; border-bottom: 2px solid #0ea5e9; padding-bottom: 10px; }}
            h2 {{ color: #333; margin-top: 30px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #0ea5e9; color: white; }}
            .total-row {{ font-weight: bold; background-color: #f0f9ff; }}
            .summary {{ background-color: #f0fdf4; padding: 20px; border-radius: 8px; margin-top: 30px; }}
            .summary h3 {{ color: #10b981; margin-top: 0; }}
            .price {{ font-family: monospace; font-size: 1.1em; }}
            .footer {{ margin-top: 50px; text-align: center; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">RECRA Solutions</div>
            <div class="subtitle">Configurator & Offerte Platform</div>
        </div>
        
        <h1>Offerte: {project.get('name', 'Project')}</h1>
        <p><strong>Type:</strong> {project.get('project_type', 'Camping').replace('_', ' ').title()}</p>
        <p><strong>Aantal standplaatsen:</strong> {project.get('num_spots', 0)}</p>
        <p><strong>Datum:</strong> {datetime.now().strftime('%d-%m-%Y')}</p>
        
        <h2>Productoverzicht</h2>
        <table>
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Categorie</th>
                    <th>Aantal</th>
                    <th>Stukprijs</th>
                    <th>Totaal</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for item in quote_response.items:
        html_content += f"""
                <tr>
                    <td>{item['product_name']}</td>
                    <td>{item['category'].title()}</td>
                    <td>{item['quantity']}</td>
                    <td class="price">€ {item['unit_price']:,.2f}</td>
                    <td class="price">€ {item['total_price']:,.2f}</td>
                </tr>
        """
    
    html_content += f"""
            </tbody>
        </table>
        
        <div class="summary">
            <h3>Kostenoverzicht</h3>
            <table>
                <tr>
                    <td><strong>CAPEX (Aankoopkosten)</strong></td>
                    <td class="price" style="text-align: right;">€ {quote_response.capex_total:,.2f}</td>
                </tr>
                <tr>
                    <td><strong>Installatiekosten</strong></td>
                    <td class="price" style="text-align: right;">€ {quote_response.installation_total:,.2f}</td>
                </tr>
                <tr class="total-row">
                    <td><strong>Totaal investering</strong></td>
                    <td class="price" style="text-align: right;">€ {(quote_response.capex_total + quote_response.installation_total):,.2f}</td>
                </tr>
            </table>
            
            <h3 style="margin-top: 20px;">OPEX (Operationele kosten)</h3>
            <table>
                <tr>
                    <td>Lease per maand</td>
                    <td class="price" style="text-align: right;">€ {quote_response.opex_monthly:,.2f}</td>
                </tr>
                <tr>
                    <td>Lease per jaar</td>
                    <td class="price" style="text-align: right;">€ {quote_response.opex_yearly:,.2f}</td>
                </tr>
                <tr>
                    <td>Onderhoud per jaar</td>
                    <td class="price" style="text-align: right;">€ {quote_response.maintenance_yearly:,.2f}</td>
                </tr>
            </table>
        </div>
        
        <div class="footer">
            <p>RECRA Solutions - Uw partner voor recreatieparken</p>
            <p>Deze offerte is geldig tot 30 dagen na dagtekening</p>
        </div>
    </body>
    </html>
    """
    
    return {
        "html": html_content,
        "project_name": project.get('name', 'Project'),
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
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Auto-seed products if database is empty
    existing = await db.products.count_documents({})
    if existing == 0:
        for product_data in SEED_PRODUCTS:
            product = Product(**product_data)
            doc = product.model_dump()
            doc['created_at'] = doc['created_at'].isoformat()
            await db.products.insert_one(doc)
        logger.info(f"Seeded {len(SEED_PRODUCTS)} products")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
