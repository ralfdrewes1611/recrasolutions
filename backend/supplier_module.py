"""
RECRA Supplier & Logistics Module
- Supplier CRUD
- Distance calculation (Haversine)
- Travel cost engine
- Partner matching
"""
import os
import math
import uuid
import logging
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger("suppliers")
supplier_router = APIRouter(prefix="/api/suppliers")

# DB connection (lazy init)
_db = None

def get_db():
    global _db
    if _db is None:
        client = AsyncIOMotorClient(os.environ['MONGO_URL'])
        _db = client[os.environ['DB_NAME']]
    return _db


# ─── MODELS ─────────────────────────────────────────────────────

class SupplierBase(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str
    address: str = ""
    lat: float = 52.0
    lng: float = 5.0
    categories: List[str] = []  # slagboom, camera, sanitair, wifi, etc.
    flows: List[str] = []  # recreatie, chalet, fec — welke configurators
    price_per_km: float = 0.45
    start_fee: float = 75.0
    hourly_rate_travel: float = 65.0
    avg_speed_kmh: float = 80.0
    verified_status: str = "basic"  # verified | compatible | basic
    contact_email: str = ""
    contact_phone: str = ""
    website: str = ""
    notes: str = ""


class Supplier(SupplierBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    categories: Optional[List[str]] = None
    flows: Optional[List[str]] = None
    price_per_km: Optional[float] = None
    start_fee: Optional[float] = None
    hourly_rate_travel: Optional[float] = None
    avg_speed_kmh: Optional[float] = None
    verified_status: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    website: Optional[str] = None
    notes: Optional[str] = None


# ─── DISTANCE & LOGISTICS ───────────────────────────────────────

def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Calculate distance between two points using Haversine formula."""
    R = 6371.0  # Earth radius in km
    lat1_r, lat2_r = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlng / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


class TravelCostResult(BaseModel):
    supplier_id: str
    supplier_name: str
    distance_km: float
    travel_time_hours: float
    cost_km: float
    cost_start: float
    cost_travel_time: float
    total_travel_cost: float  # heen + terug


def calculate_travel_cost(supplier: dict, project_lat: float, project_lng: float) -> TravelCostResult:
    """Calculate travel cost for a supplier to a project location (heen + terug)."""
    distance = haversine_km(supplier['lat'], supplier['lng'], project_lat, project_lng)
    # Road distance is typically 1.3x straight-line
    road_distance = distance * 1.3
    travel_time = road_distance / max(supplier.get('avg_speed_kmh', 80), 1)

    cost_km = road_distance * supplier.get('price_per_km', 0.45) * 2  # heen + terug
    cost_start = supplier.get('start_fee', 75)
    cost_travel_time = travel_time * supplier.get('hourly_rate_travel', 65) * 2  # heen + terug

    total = round(cost_km + cost_start + cost_travel_time, 2)

    return TravelCostResult(
        supplier_id=supplier.get('id', ''),
        supplier_name=supplier.get('name', ''),
        distance_km=round(road_distance, 1),
        travel_time_hours=round(travel_time, 2),
        cost_km=round(cost_km, 2),
        cost_start=cost_start,
        cost_travel_time=round(cost_travel_time, 2),
        total_travel_cost=total,
    )


# ─── SUPPLIER CRUD ──────────────────────────────────────────────

@supplier_router.get("")
async def list_suppliers(category: Optional[str] = None, flow: Optional[str] = None):
    db = get_db()
    query = {}
    if category:
        query["categories"] = category
    if flow:
        query["flows"] = flow
    suppliers = []
    async for doc in db.suppliers.find(query, {"_id": 0}):
        suppliers.append(doc)
    return suppliers


@supplier_router.get("/stats")
async def supplier_stats():
    """Overzicht statistieken van leveranciers."""
    db = get_db()
    suppliers = []
    async for doc in db.suppliers.find({}, {"_id": 0}):
        suppliers.append(doc)

    flow_counts = {"recreatie": 0, "chalet": 0, "fec": 0}
    status_counts = {"verified": 0, "compatible": 0, "basic": 0}
    all_categories = set()

    for s in suppliers:
        for f in s.get("flows", []):
            if f in flow_counts:
                flow_counts[f] += 1
        status = s.get("verified_status", "basic")
        status_counts[status] = status_counts.get(status, 0) + 1
        for c in s.get("categories", []):
            all_categories.add(c)

    return {
        "total": len(suppliers),
        "per_flow": flow_counts,
        "per_status": status_counts,
        "categories": sorted(all_categories),
    }


@supplier_router.post("")
async def create_supplier(supplier_data: SupplierCreate):
    db = get_db()
    supplier = Supplier(**supplier_data.model_dump())
    doc = supplier.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.suppliers.insert_one(doc)
    return {k: v for k, v in doc.items() if k != '_id'}


@supplier_router.get("/{supplier_id}")
async def get_supplier(supplier_id: str):
    db = get_db()
    doc = await db.suppliers.find_one({"id": supplier_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Leverancier niet gevonden")
    return doc


@supplier_router.put("/{supplier_id}")
async def update_supplier(supplier_id: str, updates: SupplierUpdate):
    db = get_db()
    update_data = {k: v for k, v in updates.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="Geen velden om bij te werken")
    await db.suppliers.update_one({"id": supplier_id}, {"$set": update_data})
    doc = await db.suppliers.find_one({"id": supplier_id}, {"_id": 0})
    return doc


@supplier_router.delete("/{supplier_id}")
async def delete_supplier(supplier_id: str):
    db = get_db()
    result = await db.suppliers.delete_one({"id": supplier_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Leverancier niet gevonden")
    return {"deleted": True}


# ─── PARTNER MATCHING ────────────────────────────────────────────

class MatchRequest(BaseModel):
    project_lat: float
    project_lng: float
    category: Optional[str] = None


class MatchedSupplier(BaseModel):
    supplier: dict
    travel: TravelCostResult


@supplier_router.post("/match")
async def match_suppliers(request: MatchRequest):
    """Match suppliers to a project, sorted by distance + verified status."""
    db = get_db()
    query = {}
    if request.category:
        query["categories"] = request.category

    suppliers = []
    async for doc in db.suppliers.find(query, {"_id": 0}):
        suppliers.append(doc)

    if not suppliers:
        return []

    # Calculate travel cost for each supplier
    results = []
    verified_order = {"verified": 0, "compatible": 1, "basic": 2}
    for sup in suppliers:
        travel = calculate_travel_cost(sup, request.project_lat, request.project_lng)
        results.append({
            "supplier": sup,
            "travel": travel.model_dump(),
            "_sort_verified": verified_order.get(sup.get('verified_status', 'basic'), 2),
            "_sort_distance": travel.distance_km,
        })

    # Sort: verified first, then by distance
    results.sort(key=lambda x: (x['_sort_verified'], x['_sort_distance']))

    return [{"supplier": r["supplier"], "travel": r["travel"]} for r in results]


# ─── TRAVEL COST CALCULATION ────────────────────────────────────

class TravelCalcRequest(BaseModel):
    project_lat: float
    project_lng: float
    supplier_ids: List[str] = []


@supplier_router.post("/calculate-travel")
async def calculate_travel_costs(request: TravelCalcRequest):
    """Calculate travel costs for specific suppliers to a project."""
    db = get_db()
    query = {}
    if request.supplier_ids:
        query["id"] = {"$in": request.supplier_ids}

    results = []
    async for doc in db.suppliers.find(query, {"_id": 0}):
        travel = calculate_travel_cost(doc, request.project_lat, request.project_lng)
        results.append(travel.model_dump())

    return results


# ─── SEED DEFAULT SUPPLIERS ─────────────────────────────────────

SEED_SUPPLIERS = [
    {
        "name": "Nice Benelux",
        "address": "Helmond, Nederland",
        "lat": 51.4775,
        "lng": 5.6611,
        "categories": ["slagboom"],
        "flows": ["recreatie"],
        "price_per_km": 0.42,
        "start_fee": 85,
        "hourly_rate_travel": 65,
        "avg_speed_kmh": 80,
        "verified_status": "verified",
        "contact_email": "info@nice-benelux.nl",
        "website": "https://www.nice-benelux.nl",
    },
    {
        "name": "Ubiquiti / UI.com Distributeur NL",
        "address": "Amsterdam, Nederland",
        "lat": 52.3676,
        "lng": 4.9041,
        "categories": ["camera", "wifi", "toegangscontrole"],
        "flows": ["recreatie", "fec"],
        "price_per_km": 0.45,
        "start_fee": 75,
        "hourly_rate_travel": 70,
        "avg_speed_kmh": 80,
        "verified_status": "verified",
        "contact_email": "info@ui-distributeur.nl",
        "website": "https://www.ui.com",
    },
    {
        "name": "Sanitec Recreatie",
        "address": "Apeldoorn, Nederland",
        "lat": 52.2112,
        "lng": 5.9699,
        "categories": ["sanitair"],
        "flows": ["recreatie"],
        "price_per_km": 0.50,
        "start_fee": 100,
        "hourly_rate_travel": 72,
        "avg_speed_kmh": 70,
        "verified_status": "compatible",
        "contact_email": "info@sanitec-recreatie.nl",
        "website": "https://www.sanitec-recreatie.nl",
    },
    {
        "name": "Adyen Payments",
        "address": "Amsterdam, Nederland",
        "lat": 52.3546,
        "lng": 4.8622,
        "categories": ["betaalsysteem", "douchelezer"],
        "flows": ["recreatie", "fec"],
        "price_per_km": 0.40,
        "start_fee": 50,
        "hourly_rate_travel": 80,
        "avg_speed_kmh": 80,
        "verified_status": "verified",
        "contact_email": "support@adyen.com",
        "website": "https://www.adyen.com",
    },
    {
        "name": "Van Loon Verlichting",
        "address": "Eindhoven, Nederland",
        "lat": 51.4416,
        "lng": 5.4697,
        "categories": ["verlichting"],
        "flows": ["recreatie", "chalet", "fec"],
        "price_per_km": 0.48,
        "start_fee": 65,
        "hourly_rate_travel": 60,
        "avg_speed_kmh": 80,
        "verified_status": "basic",
        "contact_email": "info@vanloonverlichting.nl",
        "website": "https://www.vanloonverlichting.nl",
    },
]


async def seed_suppliers(db_override=None):
    """Seed default suppliers if none exist."""
    db_ref = db_override if db_override is not None else get_db()
    count = await db_ref.suppliers.count_documents({})
    if count == 0:
        for sup_data in SEED_SUPPLIERS:
            supplier = Supplier(**sup_data)
            doc = supplier.model_dump()
            doc['created_at'] = doc['created_at'].isoformat()
            await db_ref.suppliers.insert_one(doc)
        logger.info(f"Seeded {len(SEED_SUPPLIERS)} suppliers")
    else:
        # Migrate: add flows + website to existing suppliers missing them
        flow_map = {s["name"]: s for s in SEED_SUPPLIERS}
        async for doc in db_ref.suppliers.find({}):
            if not doc.get("flows"):
                seed = flow_map.get(doc["name"], {})
                updates = {}
                if seed.get("flows"):
                    updates["flows"] = seed["flows"]
                if seed.get("website"):
                    updates["website"] = seed["website"]
                if not updates:
                    updates = {"flows": ["recreatie"], "website": ""}
                await db_ref.suppliers.update_one({"id": doc["id"]}, {"$set": updates})
        logger.info(f"Database has {count} suppliers (migrated flows)")
