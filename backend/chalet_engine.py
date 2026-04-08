"""
Chalet & Stay Engine — Accommodation Configurator matching projectadmin.nl reference.
Models with dak vorm, model vorm, bestemming, stijlen, suppliers, and lease pricing.
"""
import uuid
import logging
from typing import List, Optional, Dict, Any
from fastapi import APIRouter

logger = logging.getLogger(__name__)

chalet_router = APIRouter(prefix="/chalet", tags=["Chalet Engine"])

# ==================== SUPPLIERS ====================

CHALET_SUPPLIERS = [
    {"id": "kunert", "name": "Kunert Group", "color": "#244628"},
    {"id": "arcabo", "name": "Arcabo", "color": "#8B6914"},
]

# ==================== CHALET MODELS ====================

CHALET_MODELS = [
    {
        "id": "plat-12",
        "name": "Plat 12",
        "supplier_id": "kunert",
        "supplier_name": "Kunert Group",
        "oppervlakte_m2": 36,
        "model_vorm": "rechthoek",
        "dak_vorm": "platdak",
        "bestemmingen": ["recreatie", "pre-mantelzorg"],
        "slaapkamers": 1,
        "badkamers": 1,
        "max_personen": 2,
        "basisprijs": 74950,
        "stijlen": ["modern", "luxe"],
        "dimensions": {"width": 12, "height": 3},
        "description": "Compact chalet met platdak, open woonkeuken, ruime slaapkamer",
    },
    {
        "id": "zadel-12",
        "name": "Zadel 12",
        "supplier_id": "arcabo",
        "supplier_name": "Arcabo",
        "oppervlakte_m2": 58,
        "model_vorm": "rechthoek",
        "dak_vorm": "zadeldak",
        "bestemmingen": ["recreatie", "pre-mantelzorg"],
        "slaapkamers": 2,
        "badkamers": 1,
        "max_personen": 4,
        "basisprijs": 99500,
        "stijlen": ["modern", "luxe", "landelijk"],
        "dimensions": {"width": 12, "height": 5},
        "description": "Ruim chalet met zadeldak, 2 slaapkamers, lichte woonkamer",
    },
    {
        "id": "plat-18",
        "name": "Plat 18",
        "supplier_id": "kunert",
        "supplier_name": "Kunert Group",
        "oppervlakte_m2": 54,
        "model_vorm": "rechthoek",
        "dak_vorm": "platdak",
        "bestemmingen": ["recreatie"],
        "slaapkamers": 2,
        "badkamers": 1,
        "max_personen": 4,
        "basisprijs": 95800,
        "stijlen": ["modern", "luxe"],
        "dimensions": {"width": 18, "height": 3},
        "description": "Lang modern chalet, strakke lijnen, grote raampartijen",
    },
    {
        "id": "zadel-18",
        "name": "Zadel 18",
        "supplier_id": "arcabo",
        "supplier_name": "Arcabo",
        "oppervlakte_m2": 72,
        "model_vorm": "rechthoek",
        "dak_vorm": "zadeldak",
        "bestemmingen": ["recreatie", "pre-mantelzorg"],
        "slaapkamers": 2,
        "badkamers": 1,
        "max_personen": 5,
        "basisprijs": 128700,
        "stijlen": ["modern", "luxe", "landelijk"],
        "dimensions": {"width": 18, "height": 4},
        "description": "Groot familiechalet met zadeldak, ruime leefruimte, panoramaramen",
    },
    {
        "id": "l-plat-16",
        "name": "L-Plat 16",
        "supplier_id": "kunert",
        "supplier_name": "Kunert Group",
        "oppervlakte_m2": 48,
        "model_vorm": "l-vorm",
        "dak_vorm": "platdak",
        "bestemmingen": ["recreatie"],
        "slaapkamers": 2,
        "badkamers": 1,
        "max_personen": 4,
        "basisprijs": 89500,
        "stijlen": ["modern", "luxe"],
        "dimensions": {"width": 12, "height": 6},
        "description": "L-vormig chalet, gescheiden slaapgedeelte, overdekt terras in de hoek",
    },
    {
        "id": "lessenaars-14",
        "name": "Lessenaars 14",
        "supplier_id": "arcabo",
        "supplier_name": "Arcabo",
        "oppervlakte_m2": 42,
        "model_vorm": "rechthoek",
        "dak_vorm": "lessenaars",
        "bestemmingen": ["recreatie", "pre-mantelzorg"],
        "slaapkamers": 1,
        "badkamers": 1,
        "max_personen": 3,
        "basisprijs": 82000,
        "stijlen": ["modern", "landelijk"],
        "dimensions": {"width": 14, "height": 3},
        "description": "Chalet met lessenaarsdak, hoge lichtinval, compact en efficiënt",
    },
    {
        "id": "mansarde-20",
        "name": "Mansarde 20",
        "supplier_id": "kunert",
        "supplier_name": "Kunert Group",
        "oppervlakte_m2": 80,
        "model_vorm": "rechthoek",
        "dak_vorm": "mansarde",
        "bestemmingen": ["recreatie"],
        "slaapkamers": 3,
        "badkamers": 2,
        "max_personen": 6,
        "basisprijs": 145000,
        "stijlen": ["luxe", "landelijk"],
        "dimensions": {"width": 14, "height": 6},
        "description": "Luxe chalet met mansardedak, 3 slaapkamers, 2e verdieping, ruim terras",
    },
    {
        "id": "schilddak-15",
        "name": "Schilddak 15",
        "supplier_id": "arcabo",
        "supplier_name": "Arcabo",
        "oppervlakte_m2": 60,
        "model_vorm": "rechthoek",
        "dak_vorm": "schilddak",
        "bestemmingen": ["recreatie", "pre-mantelzorg"],
        "slaapkamers": 2,
        "badkamers": 1,
        "max_personen": 4,
        "basisprijs": 110000,
        "stijlen": ["modern", "luxe", "landelijk"],
        "dimensions": {"width": 15, "height": 4},
        "description": "Klassiek chalet met schilddak, robuuste uitstraling, ruime indeling",
    },
    {
        "id": "t-vorm-22",
        "name": "T-Vorm 22",
        "supplier_id": "kunert",
        "supplier_name": "Kunert Group",
        "oppervlakte_m2": 88,
        "model_vorm": "t-vorm",
        "dak_vorm": "platdak",
        "bestemmingen": ["recreatie"],
        "slaapkamers": 3,
        "badkamers": 2,
        "max_personen": 6,
        "basisprijs": 155000,
        "stijlen": ["modern", "luxe"],
        "dimensions": {"width": 14, "height": 8},
        "description": "T-vormig design, aparte master suite, grote leefruimte, dubbel terras",
    },
    {
        "id": "dubbel-24",
        "name": "Dubbel 24",
        "supplier_id": "arcabo",
        "supplier_name": "Arcabo",
        "oppervlakte_m2": 96,
        "model_vorm": "dubbel",
        "dak_vorm": "zadeldak",
        "bestemmingen": ["recreatie"],
        "slaapkamers": 4,
        "badkamers": 2,
        "max_personen": 8,
        "basisprijs": 189000,
        "stijlen": ["modern", "luxe", "landelijk"],
        "dimensions": {"width": 12, "height": 8},
        "description": "Dubbele woning, ideaal voor twee gezinnen, gescheiden ingangen, gedeeld terras",
    },
]

# ==================== FILTER OPTIONS ====================

MODEL_VORMEN = [
    {"id": "alles", "name": "Alles", "icon": "layers"},
    {"id": "rechthoek", "name": "Rechthoek", "icon": "square"},
    {"id": "l-vorm", "name": "L-vorm", "icon": "corner-down-right"},
    {"id": "t-vorm", "name": "T-vorm", "icon": "git-merge"},
    {"id": "dubbel", "name": "Dubbel", "icon": "columns"},
]

DAK_VORMEN = [
    {"id": "alles", "name": "Alles", "icon": "layers"},
    {"id": "platdak", "name": "Platdak", "icon": "minus"},
    {"id": "zadeldak", "name": "Zadeldak", "icon": "triangle"},
    {"id": "lessenaars", "name": "Lessenaars", "icon": "trending-up"},
    {"id": "mansarde", "name": "Mansarde", "icon": "home"},
    {"id": "schilddak", "name": "Schilddak", "icon": "hexagon"},
]

BESTEMMINGEN = [
    {"id": "recreatie", "name": "Recreatie"},
    {"id": "pre-mantelzorg", "name": "Pre-Mantelzorg"},
]

STIJLEN = [
    {"id": "modern", "name": "Modern"},
    {"id": "luxe", "name": "Luxe"},
    {"id": "landelijk", "name": "Landelijk"},
]

# ==================== PRICING ====================

BTW_PERCENTAGE = 21
LEASE_MONTHS = 60
LEASE_FACTOR = 0.018  # ~1.8% of price per month for 60 months

def calculate_pricing(basisprijs: float) -> dict:
    btw = round(basisprijs * BTW_PERCENTAGE / 100)
    totaal_incl = basisprijs + btw
    lease_monthly = round(basisprijs * LEASE_FACTOR)
    return {
        "basisprijs": basisprijs,
        "totaal_excl_btw": basisprijs,
        "btw_percentage": BTW_PERCENTAGE,
        "btw_bedrag": btw,
        "totaal_incl_btw": totaal_incl,
        "lease_monthly": lease_monthly,
        "lease_months": LEASE_MONTHS,
    }

# ==================== API ROUTES ====================

@chalet_router.get("/models")
async def get_chalet_models(
    bestemming: str = None,
    model_vorm: str = None,
    dak_vorm: str = None,
    min_m2: int = None,
    max_m2: int = None,
):
    """Return filtered chalet models."""
    filtered = CHALET_MODELS[:]

    if bestemming and bestemming != "alles":
        filtered = [m for m in filtered if bestemming in m["bestemmingen"]]

    if model_vorm and model_vorm != "alles":
        filtered = [m for m in filtered if m["model_vorm"] == model_vorm]

    if dak_vorm and dak_vorm != "alles":
        filtered = [m for m in filtered if m["dak_vorm"] == dak_vorm]

    if min_m2 is not None:
        filtered = [m for m in filtered if m["oppervlakte_m2"] >= min_m2]

    if max_m2 is not None:
        filtered = [m for m in filtered if m["oppervlakte_m2"] <= max_m2]

    # Add pricing to each model
    result = []
    for m in filtered:
        pricing = calculate_pricing(m["basisprijs"])
        result.append({**m, "pricing": pricing})

    return result


@chalet_router.get("/models/{model_id}")
async def get_model_detail(model_id: str):
    """Return a single model with full pricing."""
    model = next((m for m in CHALET_MODELS if m["id"] == model_id), None)
    if not model:
        return {"error": "Model niet gevonden"}
    pricing = calculate_pricing(model["basisprijs"])
    return {**model, "pricing": pricing}


@chalet_router.get("/filters")
async def get_filters():
    """Return all filter options for the configurator."""
    return {
        "bestemmingen": BESTEMMINGEN,
        "model_vormen": MODEL_VORMEN,
        "dak_vormen": DAK_VORMEN,
        "stijlen": STIJLEN,
        "oppervlakte_range": {"min": 30, "max": 120},
        "suppliers": CHALET_SUPPLIERS,
    }


@chalet_router.get("/suppliers")
async def get_chalet_suppliers():
    return CHALET_SUPPLIERS
