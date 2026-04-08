"""
Chalet & Stay Engine — Accommodation Configurator matching projectadmin.nl reference.
Real suppliers: Kunert Group, Arcabo, BBS Systeembouw, Campsolutions (Glamping).
"""
import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)

chalet_router = APIRouter(prefix="/chalet", tags=["Chalet Engine"])

# ==================== SUPPLIERS ====================

CHALET_SUPPLIERS = [
    {"id": "kunert", "name": "Kunert Group", "color": "#244628", "website": "chaletskunert.nl", "types": ["chalet"]},
    {"id": "arcabo", "name": "Arcabo", "color": "#8B6914", "website": "arcabo.nl", "types": ["chalet"]},
    {"id": "bbs", "name": "BBS Systeembouw", "color": "#4A6741", "website": "bbssysteembouw.nl", "types": ["chalet"]},
    {"id": "campsolutions", "name": "Campsolutions", "color": "#2D6A4F", "website": "campsolutions.com", "types": ["glamping"]},
]

# ==================== IMAGES PER SUPPLIER + STIJL ====================

SUPPLIER_IMAGES = {
    "kunert": {
        "modern": [
            "https://images.unsplash.com/photo-1712899227535-e076a4489322?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1645132971658-3ffd441ac6fa?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1594886887939-2d2188b08706?w=800&h=500&fit=crop",
        ],
        "luxe": [
            "https://images.unsplash.com/photo-1610054102966-fc6f9a0a0616?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1762782778316-80b05d151915?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1758745018916-627ad7196524?w=800&h=500&fit=crop",
        ],
        "landelijk": [
            "https://images.unsplash.com/photo-1742130754462-f83b21dcc54f?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1598416596014-5626a98dcaad?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1522071500372-f0fd8c452178?w=800&h=500&fit=crop",
        ],
    },
    "arcabo": {
        "modern": [
            "https://images.unsplash.com/photo-1594886887939-2d2188b08706?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1712899227535-e076a4489322?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1645132971658-3ffd441ac6fa?w=800&h=500&fit=crop",
        ],
        "luxe": [
            "https://images.unsplash.com/photo-1762782778316-80b05d151915?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1610054102966-fc6f9a0a0616?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1758745018916-627ad7196524?w=800&h=500&fit=crop",
        ],
        "landelijk": [
            "https://images.unsplash.com/photo-1598416596014-5626a98dcaad?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1742130754462-f83b21dcc54f?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1522071500372-f0fd8c452178?w=800&h=500&fit=crop",
        ],
    },
    "bbs": {
        "modern": [
            "https://images.unsplash.com/photo-1645132971658-3ffd441ac6fa?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1594886887939-2d2188b08706?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1712899227535-e076a4489322?w=800&h=500&fit=crop",
        ],
        "luxe": [
            "https://images.unsplash.com/photo-1758745018916-627ad7196524?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1762782778316-80b05d151915?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1610054102966-fc6f9a0a0616?w=800&h=500&fit=crop",
        ],
        "landelijk": [
            "https://images.unsplash.com/photo-1742130754462-f83b21dcc54f?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1598416596014-5626a98dcaad?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1522071500372-f0fd8c452178?w=800&h=500&fit=crop",
        ],
    },
    "campsolutions": {
        "modern": [
            "https://images.unsplash.com/photo-1721093288938-f4b597de3283?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1763883420965-63130e7ed221?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1762255097010-49e99eadd616?w=800&h=500&fit=crop",
        ],
        "luxe": [
            "https://images.unsplash.com/photo-1763883420965-63130e7ed221?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1721093288938-f4b597de3283?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1774013710036-982f187dfe38?w=800&h=500&fit=crop",
        ],
        "landelijk": [
            "https://images.unsplash.com/photo-1762255097010-49e99eadd616?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1774013710036-982f187dfe38?w=800&h=500&fit=crop",
            "https://images.unsplash.com/photo-1762254799629-b8542e611aa7?w=800&h=500&fit=crop",
        ],
    },
}

# ==================== CHALET MODELS ====================

CHALET_MODELS = [
    # ===== KUNERT GROUP — Chalets =====
    {
        "id": "kunert-plat-12",
        "name": "Plat 12",
        "supplier_id": "kunert",
        "supplier_name": "Kunert Group",
        "categorie": "chalet",
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
        "description": "Compact chalet met platdak, open woonkeuken, ruime slaapkamer. Winterharde isolatie, dubbel glas, CV.",
    },
    {
        "id": "kunert-plat-18",
        "name": "Plat 18",
        "supplier_id": "kunert",
        "supplier_name": "Kunert Group",
        "categorie": "chalet",
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
        "description": "Lang modern chalet, strakke lijnen, grote raampartijen. 2 slaapkamers, volledige keuken.",
    },
    {
        "id": "kunert-lazy-juliana",
        "name": "Reina Lazy Juliana",
        "supplier_id": "kunert",
        "supplier_name": "Kunert Group",
        "categorie": "chalet",
        "oppervlakte_m2": 45,
        "model_vorm": "rechthoek",
        "dak_vorm": "platdak",
        "bestemmingen": ["recreatie", "pre-mantelzorg"],
        "slaapkamers": 2,
        "badkamers": 1,
        "max_personen": 4,
        "basisprijs": 60330,
        "stijlen": ["modern", "luxe", "landelijk"],
        "dimensions": {"width": 11.25, "height": 4},
        "description": "Populair Reina model. 2 (of 3) slaapkamers, premium afwerking, winterharde isolatie, apart toilet.",
    },
    {
        "id": "kunert-haven",
        "name": "Haven",
        "supplier_id": "kunert",
        "supplier_name": "Kunert Group",
        "categorie": "chalet",
        "oppervlakte_m2": 38,
        "model_vorm": "rechthoek",
        "dak_vorm": "platdak",
        "bestemmingen": ["recreatie", "pre-mantelzorg"],
        "slaapkamers": 1,
        "badkamers": 1,
        "max_personen": 3,
        "basisprijs": 52000,
        "stijlen": ["modern"],
        "dimensions": {"width": 10, "height": 3.8},
        "description": "Open keuken, moderne structuur. Compact en efficiënt, ideaal voor verhuur of mantelzorg.",
    },
    {
        "id": "kunert-ohara-premium",
        "name": "O'Hara Premium",
        "supplier_id": "kunert",
        "supplier_name": "Kunert Group",
        "categorie": "chalet",
        "oppervlakte_m2": 58,
        "model_vorm": "rechthoek",
        "dak_vorm": "lessenaars",
        "bestemmingen": ["recreatie"],
        "slaapkamers": 2,
        "badkamers": 1,
        "max_personen": 5,
        "basisprijs": 73550,
        "stijlen": ["modern", "luxe", "landelijk"],
        "dimensions": {"width": 14, "height": 4},
        "description": "Sfeervol O'Hara chalet met moderne kleuren, winterisolatie. Premium afwerking en ruime indeling.",
    },
    {
        "id": "kunert-irm-habitat",
        "name": "IRM Habitat",
        "supplier_id": "kunert",
        "supplier_name": "Kunert Group",
        "categorie": "chalet",
        "oppervlakte_m2": 40,
        "model_vorm": "rechthoek",
        "dak_vorm": "zadeldak",
        "bestemmingen": ["recreatie", "pre-mantelzorg"],
        "slaapkamers": 2,
        "badkamers": 1,
        "max_personen": 4,
        "basisprijs": 53720,
        "stijlen": ["modern", "landelijk"],
        "dimensions": {"width": 10, "height": 4},
        "description": "IRM Habitat, wintervast, 1-4 slaapkamers configureerbaar. Geschikt voor verhuur of particulier recreatiegebruik.",
    },
    {
        "id": "kunert-mansarde-20",
        "name": "Mansarde 20",
        "supplier_id": "kunert",
        "supplier_name": "Kunert Group",
        "categorie": "chalet",
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
        "description": "Luxe chalet met mansardedak, 3 slaapkamers, 2e verdieping, ruim terras. Topmodel Kunert serie.",
    },
    {
        "id": "kunert-t-vorm-22",
        "name": "T-Vorm 22",
        "supplier_id": "kunert",
        "supplier_name": "Kunert Group",
        "categorie": "chalet",
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
        "description": "T-vormig design, aparte master suite, grote leefruimte, dubbel terras.",
    },
    # ===== ARCABO — Premium Chalets =====
    {
        "id": "arcabo-zadel-12",
        "name": "Zadel 12",
        "supplier_id": "arcabo",
        "supplier_name": "Arcabo",
        "categorie": "chalet",
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
        "description": "Ruim chalet met zadeldak, 2 slaapkamers, lichte woonkamer. Eigen fabriek, hoge kwaliteit.",
    },
    {
        "id": "arcabo-zadel-18",
        "name": "Zadel 18",
        "supplier_id": "arcabo",
        "supplier_name": "Arcabo",
        "categorie": "chalet",
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
        "description": "Groot familiechalet met zadeldak, ruime leefruimte, panoramaramen. Bestseller Arcabo.",
    },
    {
        "id": "arcabo-charleston",
        "name": "Charleston",
        "supplier_id": "arcabo",
        "supplier_name": "Arcabo",
        "categorie": "chalet",
        "oppervlakte_m2": 80,
        "model_vorm": "l-vorm",
        "dak_vorm": "schilddak",
        "bestemmingen": ["recreatie"],
        "slaapkamers": 3,
        "badkamers": 2,
        "max_personen": 6,
        "basisprijs": 121966,
        "stijlen": ["luxe", "landelijk"],
        "dimensions": {"width": 12, "height": 8},
        "description": "Ruim recreatiechalet voor aan zee. L-vormig met schilddak, 3 slaapkamers, 2 badkamers. Premium Arcabo.",
    },
    {
        "id": "arcabo-new-bay",
        "name": "New Bay",
        "supplier_id": "arcabo",
        "supplier_name": "Arcabo",
        "categorie": "chalet",
        "oppervlakte_m2": 60,
        "model_vorm": "rechthoek",
        "dak_vorm": "schilddak",
        "bestemmingen": ["recreatie", "pre-mantelzorg"],
        "slaapkamers": 2,
        "badkamers": 1,
        "max_personen": 4,
        "basisprijs": 95000,
        "stijlen": ["modern", "luxe", "landelijk"],
        "dimensions": {"width": 12, "height": 5},
        "description": "Degelijk model met aanpasbare indeling en interieur. Wintervast, eigen Arcabo fabriek.",
    },
    {
        "id": "arcabo-ocala",
        "name": "Ocala",
        "supplier_id": "arcabo",
        "supplier_name": "Arcabo",
        "categorie": "chalet",
        "oppervlakte_m2": 42,
        "model_vorm": "rechthoek",
        "dak_vorm": "zadeldak",
        "bestemmingen": ["recreatie", "pre-mantelzorg"],
        "slaapkamers": 2,
        "badkamers": 1,
        "max_personen": 4,
        "basisprijs": 68000,
        "stijlen": ["modern", "landelijk"],
        "dimensions": {"width": 10.5, "height": 4},
        "description": "Compact Arcabo model, 2 slaapkamers, wintervast. Snel leverbaar, populair instapmodel.",
    },
    {
        "id": "arcabo-dubbel-24",
        "name": "Dubbel 24",
        "supplier_id": "arcabo",
        "supplier_name": "Arcabo",
        "categorie": "chalet",
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
        "description": "Dubbele woning, ideaal voor twee gezinnen, gescheiden ingangen, gedeeld terras.",
    },
    # ===== BBS SYSTEEMBOUW — Vakantiewoningen =====
    {
        "id": "bbs-compact",
        "name": "Vakantiewoning Compact",
        "supplier_id": "bbs",
        "supplier_name": "BBS Systeembouw",
        "categorie": "chalet",
        "oppervlakte_m2": 35,
        "model_vorm": "rechthoek",
        "dak_vorm": "platdak",
        "bestemmingen": ["recreatie", "pre-mantelzorg"],
        "slaapkamers": 1,
        "badkamers": 1,
        "max_personen": 2,
        "basisprijs": 46000,
        "stijlen": ["modern"],
        "dimensions": {"width": 10, "height": 3.5},
        "description": "Betaalbare maatwerk vakantiewoning, hoogwaardige systeembouw, inclusief ontwerp, productie en plaatsing.",
    },
    {
        "id": "bbs-comfort",
        "name": "Vakantiewoning Comfort",
        "supplier_id": "bbs",
        "supplier_name": "BBS Systeembouw",
        "categorie": "chalet",
        "oppervlakte_m2": 55,
        "model_vorm": "rechthoek",
        "dak_vorm": "lessenaars",
        "bestemmingen": ["recreatie", "pre-mantelzorg"],
        "slaapkamers": 2,
        "badkamers": 1,
        "max_personen": 4,
        "basisprijs": 72000,
        "stijlen": ["modern", "landelijk"],
        "dimensions": {"width": 12, "height": 4.5},
        "description": "Ruimere vakantiewoning, 2 slaapkamers, lessenaarsdak. BBS maatwerk met hoge isolatiewaarde.",
    },
    {
        "id": "bbs-premium",
        "name": "Vakantiewoning Premium",
        "supplier_id": "bbs",
        "supplier_name": "BBS Systeembouw",
        "categorie": "chalet",
        "oppervlakte_m2": 75,
        "model_vorm": "l-vorm",
        "dak_vorm": "platdak",
        "bestemmingen": ["recreatie"],
        "slaapkamers": 3,
        "badkamers": 2,
        "max_personen": 6,
        "basisprijs": 98000,
        "stijlen": ["modern", "luxe"],
        "dimensions": {"width": 12, "height": 7},
        "description": "Premium L-vormige vakantiewoning, 3 slaapkamers, 2 badkamers. Volledig op maat, rendabel voor verhuur.",
    },
    # ===== CAMPSOLUTIONS — Glamping =====
    {
        "id": "camp-wood-lodge-jr",
        "name": "Wood Lodge Junior",
        "supplier_id": "campsolutions",
        "supplier_name": "Campsolutions",
        "categorie": "glamping",
        "oppervlakte_m2": 8,
        "model_vorm": "rechthoek",
        "dak_vorm": "platdak",
        "bestemmingen": ["recreatie"],
        "slaapkamers": 1,
        "badkamers": 0,
        "max_personen": 2,
        "basisprijs": 3236,
        "stijlen": ["modern", "landelijk"],
        "dimensions": {"width": 4, "height": 2},
        "description": "Kleinste Wood Lodge, compact en betaalbaar. Ideaal voor kleine plekken, vervangbare deuren/ramen.",
    },
    {
        "id": "camp-wood-lodge-cozy",
        "name": "Wood Lodge Cozy",
        "supplier_id": "campsolutions",
        "supplier_name": "Campsolutions",
        "categorie": "glamping",
        "oppervlakte_m2": 15,
        "model_vorm": "rechthoek",
        "dak_vorm": "platdak",
        "bestemmingen": ["recreatie"],
        "slaapkamers": 1,
        "badkamers": 0,
        "max_personen": 4,
        "basisprijs": 4412,
        "stijlen": ["modern", "landelijk"],
        "dimensions": {"width": 5, "height": 3},
        "description": "Gezellige Wood Lodge, 12-21 m² varianten beschikbaar. Optioneel sanitair en inrichting.",
    },
    {
        "id": "camp-wood-lodge-midi",
        "name": "Wood Lodge Midi",
        "supplier_id": "campsolutions",
        "supplier_name": "Campsolutions",
        "categorie": "glamping",
        "oppervlakte_m2": 35,
        "model_vorm": "rechthoek",
        "dak_vorm": "lessenaars",
        "bestemmingen": ["recreatie"],
        "slaapkamers": 2,
        "badkamers": 1,
        "max_personen": 5,
        "basisprijs": 7452,
        "stijlen": ["modern", "landelijk"],
        "dimensions": {"width": 8, "height": 4.5},
        "description": "Middelgrote Wood Lodge, 32-39 m². Ruimte voor 2-5 personen, met sanitair optie.",
    },
    {
        "id": "camp-wood-lodge",
        "name": "Wood Lodge",
        "supplier_id": "campsolutions",
        "supplier_name": "Campsolutions",
        "categorie": "glamping",
        "oppervlakte_m2": 55,
        "model_vorm": "rechthoek",
        "dak_vorm": "lessenaars",
        "bestemmingen": ["recreatie"],
        "slaapkamers": 2,
        "badkamers": 1,
        "max_personen": 8,
        "basisprijs": 7986,
        "stijlen": ["modern", "luxe", "landelijk"],
        "dimensions": {"width": 10, "height": 5.5},
        "description": "Grootste Wood Lodge, 43-65 m². Ruim voor families, volledige inrichting mogelijk.",
    },
    {
        "id": "camp-panorama-dome",
        "name": "Panorama Dome",
        "supplier_id": "campsolutions",
        "supplier_name": "Campsolutions",
        "categorie": "glamping",
        "oppervlakte_m2": 18,
        "model_vorm": "rechthoek",
        "dak_vorm": "zadeldak",
        "bestemmingen": ["recreatie"],
        "slaapkamers": 1,
        "badkamers": 0,
        "max_personen": 2,
        "basisprijs": 7550,
        "stijlen": ["luxe"],
        "dimensions": {"width": 5, "height": 5},
        "description": "Transparante dome, sterren kijken, unieke beleving. King-size bed, sfeerverlichting.",
    },
    {
        "id": "camp-glamping-lodge",
        "name": "Glamping Lodge",
        "supplier_id": "campsolutions",
        "supplier_name": "Campsolutions",
        "categorie": "glamping",
        "oppervlakte_m2": 56,
        "model_vorm": "rechthoek",
        "dak_vorm": "lessenaars",
        "bestemmingen": ["recreatie"],
        "slaapkamers": 3,
        "badkamers": 1,
        "max_personen": 8,
        "basisprijs": 7995,
        "stijlen": ["modern", "luxe", "landelijk"],
        "dimensions": {"width": 10, "height": 6},
        "description": "Lessenaarsdak, groot terras (22-30 m²), raampartijen. Ideaal voor 4-8 personen. Uniek ontwerp.",
    },
    {
        "id": "camp-safari-lodge",
        "name": "Luxury Safari Lodge",
        "supplier_id": "campsolutions",
        "supplier_name": "Campsolutions",
        "categorie": "glamping",
        "oppervlakte_m2": 60,
        "model_vorm": "rechthoek",
        "dak_vorm": "zadeldak",
        "bestemmingen": ["recreatie"],
        "slaapkamers": 2,
        "badkamers": 1,
        "max_personen": 8,
        "basisprijs": 9351,
        "stijlen": ["luxe", "landelijk"],
        "dimensions": {"width": 10, "height": 6},
        "description": "Luxe safari lodge, 55-64 m², canvas dak, houten vlonder. Eigen sanitair, volledige inrichting.",
    },
    {
        "id": "camp-giant-hat",
        "name": "Giant Hat",
        "supplier_id": "campsolutions",
        "supplier_name": "Campsolutions",
        "categorie": "glamping",
        "oppervlakte_m2": 83,
        "model_vorm": "rechthoek",
        "dak_vorm": "mansarde",
        "bestemmingen": ["recreatie"],
        "slaapkamers": 2,
        "badkamers": 1,
        "max_personen": 4,
        "basisprijs": 13400,
        "stijlen": ["luxe"],
        "dimensions": {"width": 10, "height": 8.3},
        "description": "Indrukwekkende 83 m² tent met uniek dak. Ruimte voor groepen, evenementen of luxe glamping.",
    },
    {
        "id": "camp-arcade",
        "name": "Arcade",
        "supplier_id": "campsolutions",
        "supplier_name": "Campsolutions",
        "categorie": "glamping",
        "oppervlakte_m2": 65,
        "model_vorm": "rechthoek",
        "dak_vorm": "zadeldak",
        "bestemmingen": ["recreatie"],
        "slaapkamers": 2,
        "badkamers": 1,
        "max_personen": 6,
        "basisprijs": 14500,
        "stijlen": ["modern", "luxe"],
        "dimensions": {"width": 10, "height": 6.5},
        "description": "Moderne glamping tent, 65 m², 4-6 personen. Stijlvol design, grote raampartijen, luxe afwerking.",
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

CATEGORIEEN = [
    {"id": "alles", "name": "Alles"},
    {"id": "chalet", "name": "Chalets"},
    {"id": "glamping", "name": "Glamping"},
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
    categorie: str = None,
    supplier_id: str = None,
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

    if categorie and categorie != "alles":
        filtered = [m for m in filtered if m["categorie"] == categorie]

    if supplier_id and supplier_id != "alles":
        filtered = [m for m in filtered if m["supplier_id"] == supplier_id]

    # Add pricing + images
    result = []
    for m in filtered:
        pricing = calculate_pricing(m["basisprijs"])
        images = SUPPLIER_IMAGES.get(m["supplier_id"], {})
        result.append({**m, "pricing": pricing, "images": images})

    return result


@chalet_router.get("/models/{model_id}")
async def get_model_detail(model_id: str):
    model = next((m for m in CHALET_MODELS if m["id"] == model_id), None)
    if not model:
        return {"error": "Model niet gevonden"}
    pricing = calculate_pricing(model["basisprijs"])
    images = SUPPLIER_IMAGES.get(model["supplier_id"], {})
    return {**model, "pricing": pricing, "images": images}


@chalet_router.get("/filters")
async def get_filters():
    return {
        "bestemmingen": BESTEMMINGEN,
        "model_vormen": MODEL_VORMEN,
        "dak_vormen": DAK_VORMEN,
        "stijlen": STIJLEN,
        "categorieen": CATEGORIEEN,
        "oppervlakte_range": {"min": 5, "max": 120},
        "suppliers": CHALET_SUPPLIERS,
    }


@chalet_router.get("/suppliers")
async def get_chalet_suppliers():
    return CHALET_SUPPLIERS
