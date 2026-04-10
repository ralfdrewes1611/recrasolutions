"""
White-label Engine — Configureerbare branding voor Pleisureworld en partners.
Stelt partners in staat om het platform te gebruiken onder eigen merk.
"""
from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel

whitelabel_router = APIRouter(prefix="/whitelabel", tags=["White-label"])

# Default RECRA branding
DEFAULT_CONFIG = {
    "id": "recra-default",
    "brand_name": "RECRA Solutions",
    "tagline": "Recreation Project Configurator & Partner Matching Platform",
    "primary_color": "#244628",
    "secondary_color": "#70C26C",
    "accent_color": "#FDF9ED",
    "logo_url": "/recra-logo-white.png",
    "logo_dark_url": "/recra-logo-white.png",
    "favicon_url": "/favicon.ico",
    "contact_email": "info@recrasolutions.com",
    "contact_phone": "+31 634200253",
    "website_url": "https://www.recrasolutions.com",
    "powered_by": "RECRA Solutions",
    "show_powered_by": True,
    "custom_css": "",
    "features_enabled": {
        "recreatie": True,
        "chalet": True,
        "fec": True,
        "dashboard": True,
        "roadmap": True,
        "pdf_export": True,
        "ai_recommendations": True,
        "supplier_profiles": True,
    },
}

# Pleisureworld branded configuration
PLEISUREWORLD_CONFIG = {
    "id": "pleisureworld",
    "brand_name": "Pleisureworld",
    "tagline": "Van Inspiratie naar Realisatie",
    "primary_color": "#244628",
    "secondary_color": "#70C26C",
    "accent_color": "#FDF9ED",
    "logo_url": "/recra-logo-white.png",
    "logo_dark_url": "/recra-logo-white.png",
    "favicon_url": "/favicon.ico",
    "contact_email": "info@pleisureworld.nl",
    "contact_phone": "+31 634200253",
    "website_url": "https://www.pleisureworld.nl",
    "powered_by": "Pleisureworld x RECRA Solutions",
    "show_powered_by": True,
    "custom_css": "",
    "features_enabled": {
        "recreatie": True,
        "chalet": True,
        "fec": True,
        "dashboard": True,
        "roadmap": True,
        "pdf_export": True,
        "ai_recommendations": True,
        "supplier_profiles": True,
    },
}

CONFIGS = {
    "recra-default": DEFAULT_CONFIG,
    "pleisureworld": PLEISUREWORLD_CONFIG,
}


class WhiteLabelUpdate(BaseModel):
    brand_name: Optional[str] = None
    tagline: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    accent_color: Optional[str] = None
    logo_url: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    website_url: Optional[str] = None
    powered_by: Optional[str] = None
    show_powered_by: Optional[bool] = None
    custom_css: Optional[str] = None


@whitelabel_router.get("/config")
async def get_active_config():
    """Haal de actieve white-label configuratie op."""
    return DEFAULT_CONFIG


@whitelabel_router.get("/config/{config_id}")
async def get_config(config_id: str):
    """Haal een specifieke white-label configuratie op."""
    config = CONFIGS.get(config_id)
    if not config:
        return {"error": "Configuratie niet gevonden", "available": list(CONFIGS.keys())}
    return config


@whitelabel_router.get("/configs")
async def list_configs():
    """Lijst van alle beschikbare white-label configuraties."""
    return [
        {"id": c["id"], "brand_name": c["brand_name"], "tagline": c["tagline"]}
        for c in CONFIGS.values()
    ]


@whitelabel_router.post("/config/{config_id}")
async def update_config(config_id: str, updates: WhiteLabelUpdate):
    """Update een white-label configuratie."""
    config = CONFIGS.get(config_id)
    if not config:
        return {"error": "Configuratie niet gevonden"}
    update_dict = {k: v for k, v in updates.model_dump().items() if v is not None}
    config.update(update_dict)
    return config
