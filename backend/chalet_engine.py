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
    {"id": "kunert", "name": "Kunert Group", "color": "#244628", "website": "chaletskunert.nl", "types": ["chalet"], "pleisureworld_partner": True},
    {"id": "arcabo", "name": "Arcabo", "color": "#8B6914", "website": "arcabo.nl", "types": ["chalet"], "pleisureworld_partner": True},
    {"id": "bbs", "name": "BBS Systeembouw", "color": "#4A6741", "website": "bbssysteembouw.nl", "types": ["chalet"], "pleisureworld_partner": True},
    {"id": "campsolutions", "name": "Campsolutions", "color": "#2D6A4F", "website": "campsolutions.com", "types": ["glamping"], "pleisureworld_partner": True},
]

# ==================== IMAGES PER SUPPLIER + STIJL ====================

# ==================== REAL PRODUCT IMAGES PER MODEL ====================
# Images sourced from actual supplier websites

MODEL_IMAGES = {
    # Kunert Group
    "kunert-plat-12": [
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/9bb15a9fd5ca8225826fd1bd0d3c2b44/w2.webp",
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/21360c1d25e0b79e2241df7736a66610/11-scaled-2.webp",
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/a6f3180fbc02492d899cbc5b02b63e8e/12-scaled-1.webp",
    ],
    "kunert-plat-18": [
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/a7d32cf654945640a6ba12c117e735de/13-scaled-1.webp",
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/68da8ee0d54984a681705d89a909e163/14-scaled-1.webp",
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/9bb15a9fd5ca8225826fd1bd0d3c2b44/w2.webp",
    ],
    "kunert-lazy-juliana": [
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/fde7c3b8d28232241bc5367a7d3e6e2b/mobilehome-2.webp",
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/b4efa0dfce7392c71bf98c30e4107108/invierno_s1-scaled-1.webp",
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/3abd295cfedd4e21a7876c278eb86862/invierno_s3-scaled-1.webp",
    ],
    "kunert-haven": [
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/596c295a46e6a41280859315325ba1bc/Image1.png",
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/fa91b9a5ebe6455d93e1d3737316adc9/2-_2_.webp",
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/fb9cde0d5c961a3f5af88637408b062c/4-_2_.webp",
    ],
    "kunert-ohara-premium": [
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/cce715b7f00f81ed3d7f51722398606e/invierno_m1-scaled-2.webp",
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/a52277a64cc3fbcf8cd5bd985f5f3ef3/invierno_l1-scaled-1.webp",
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/fde7c3b8d28232241bc5367a7d3e6e2b/mobilehome-2.webp",
    ],
    "kunert-irm-habitat": [
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/b4efa0dfce7392c71bf98c30e4107108/invierno_s1-scaled-1.webp",
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/cce715b7f00f81ed3d7f51722398606e/invierno_m1-scaled-2.webp",
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/3abd295cfedd4e21a7876c278eb86862/invierno_s3-scaled-1.webp",
    ],
    "kunert-mansarde-20": [
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/68da8ee0d54984a681705d89a909e163/14-scaled-1.webp",
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/a7d32cf654945640a6ba12c117e735de/13-scaled-1.webp",
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/21360c1d25e0b79e2241df7736a66610/11-scaled-2.webp",
    ],
    "kunert-t-vorm-22": [
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/9bb15a9fd5ca8225826fd1bd0d3c2b44/w2.webp",
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/a6f3180fbc02492d899cbc5b02b63e8e/12-scaled-1.webp",
        "https://chaletskunert.nl/wp-content/uploads/slider/cache/68da8ee0d54984a681705d89a909e163/14-scaled-1.webp",
    ],
    # Arcabo
    "arcabo-zadel-12": [
        "https://arcabo.nl/wp-content/uploads/Lodge-3D-9-2023-buitenzijde-klein-2023-uitgelicht.png",
        "https://arcabo.nl/wp-content/uploads/1-Buitenzijde-Long-Beach-A-klein-2023-uitgelicht.png",
        "https://arcabo.nl/wp-content/uploads/Ocala-website-groot-1.png",
    ],
    "arcabo-zadel-18": [
        "https://arcabo.nl/wp-content/uploads/1-New-Bay-A-buitenzijde-2024-uitgelicht.png",
        "https://arcabo.nl/wp-content/uploads/2-New-Bay-A-woonkamer-1-2-klein-2023.png",
        "https://arcabo.nl/wp-content/uploads/4-New-Bay-A-keuken-3-klein-2023.png",
    ],
    "arcabo-charleston": [
        "https://arcabo.nl/wp-content/uploads/1-Charleston-buitenzijde-met-opmaak-1-uitgelicht-klein-2024.png",
        "https://arcabo.nl/wp-content/uploads/3-Charleston-C-woonkamer-2-klein-2024.png",
        "https://arcabo.nl/wp-content/uploads/4-Charleston-C-keuken-klein-2024.png",
    ],
    "arcabo-new-bay": [
        "https://arcabo.nl/wp-content/uploads/1-New-Bay-A-buitenzijde-2024.png",
        "https://arcabo.nl/wp-content/uploads/2-New-Bay-A-woonkamer-1-2-klein-2023.png",
        "https://arcabo.nl/wp-content/uploads/5-New-Bay-A-slaapkamer-2-klein-2023.png",
    ],
    "arcabo-ocala": [
        "https://arcabo.nl/wp-content/uploads/Ocala-website-groot-1.png",
        "https://arcabo.nl/wp-content/uploads/Ocala-woonkamer-website-1.png",
        "https://arcabo.nl/wp-content/uploads/Ocala-keuken-website-1.png",
    ],
    "arcabo-dubbel-24": [
        "https://arcabo.nl/wp-content/uploads/1-carlington-70m2-buitenzijde2-uitgelicht.png",
        "https://arcabo.nl/wp-content/uploads/1-Miami-L-buitenzijde3-klein-2023-uitgelicht.png",
        "https://arcabo.nl/wp-content/uploads/1-New-Port-B-buitenzijde1-uitgelicht-klein-2024.png",
    ],
    # BBS Systeembouw
    "bbs-compact": [
        "https://ucarecdn.com/76932055-baf1-402d-bedb-68e5b903160e/-/format/auto/-/resize/800x500/",
        "https://ucarecdn.com/3b93939b-90ac-4bf0-8bd7-f492cf4fd253/-/format/auto/-/resize/800x500/",
        "https://ucarecdn.com/51e8be1e-9c5c-4e0c-b9af-eab7b2f66652/-/format/auto/-/resize/800x500/",
    ],
    "bbs-comfort": [
        "https://ucarecdn.com/16fbc617-c09f-4a02-a022-03d455ad438a/-/format/auto/-/resize/800x500/",
        "https://ucarecdn.com/2502c7b1-a3be-46ee-b8ac-0c8e367a1473/-/format/auto/-/resize/800x500/",
        "https://ucarecdn.com/76932055-baf1-402d-bedb-68e5b903160e/-/format/auto/-/resize/800x500/",
    ],
    "bbs-premium": [
        "https://ucarecdn.com/17ae1b5b-9eb9-4c0a-9507-b46fe3a05c33/-/format/auto/-/resize/800x500/",
        "https://ucarecdn.com/16fbc617-c09f-4a02-a022-03d455ad438a/-/format/auto/-/resize/800x500/",
        "https://ucarecdn.com/2502c7b1-a3be-46ee-b8ac-0c8e367a1473/-/format/auto/-/resize/800x500/",
    ],
    # Campsolutions Glamping
    "camp-wood-lodge-jr": [
        "https://campsolutions.com/wp-content/uploads/2020/12/Scherm%C2%ADafbeelding-2025-12-08-om-16.16.00-min-400x284.png",
        "https://campsolutions.com/wp-content/uploads/2020/12/Scherm%C2%ADafbeelding-2025-12-08-om-15.52.21-min-e1765205821482.png",
        "https://campsolutions.com/wp-content/uploads/2020/12/Naamloos-1.png",
    ],
    "camp-wood-lodge-cozy": [
        "https://campsolutions.com/wp-content/uploads/2025/04/20250512-DickRuumpolFotografie-Campsolutions-LR-014-e1749747535515-400x284.jpg",
        "https://campsolutions.com/wp-content/uploads/2020/12/Scherm%C2%ADafbeelding-2025-12-08-om-15.52.21-min-e1765205821482.png",
        "https://campsolutions.com/wp-content/uploads/2020/12/Naamloos-1.png",
    ],
    "camp-wood-lodge-midi": [
        "https://campsolutions.com/wp-content/uploads/2022/01/Scherm%C2%ADafbeelding-2025-12-08-om-12.23.56-min-e1765379989312-400x284.png",
        "https://campsolutions.com/wp-content/uploads/2020/12/Scherm%C2%ADafbeelding-2025-12-08-om-15.52.21-min-e1765205821482.png",
        "https://campsolutions.com/wp-content/uploads/2020/12/Scherm%C2%ADafbeelding-2025-12-08-om-15.51.57-min-e1765205971348.png",
    ],
    "camp-wood-lodge": [
        "https://campsolutions.com/wp-content/uploads/2020/12/Scherm%C2%ADafbeelding-2025-12-08-om-15.52.21-min-e1765205821482.png",
        "https://campsolutions.com/wp-content/uploads/2020/12/Scherm%C2%ADafbeelding-2025-12-08-om-15.51.57-min-e1765205971348.png",
        "https://campsolutions.com/wp-content/uploads/2020/12/Naamloos-1.png",
    ],
    "camp-panorama-dome": [
        "https://campsolutions.com/wp-content/uploads/2021/12/dof-panorama-uitgelicht-400x284.jpeg",
        "https://campsolutions.com/wp-content/uploads/2021/12/dof-panorama-uitgelicht.jpeg",
        "https://campsolutions.com/wp-content/uploads/2020/12/Naamloos-1.png",
    ],
    "camp-glamping-lodge": [
        "https://campsolutions.com/wp-content/uploads/2022/01/CS-GL-Featured-img-400x284.jpg",
        "https://campsolutions.com/wp-content/uploads/2022/01/CS-GL-Featured-img.jpg",
        "https://campsolutions.com/wp-content/uploads/2020/12/Naamloos-1.png",
    ],
    "camp-safari-lodge": [
        "https://campsolutions.com/wp-content/uploads/2020/12/Scherm%C2%ADafbeelding-2025-12-08-om-15.35.00-min-400x284.png",
        "https://campsolutions.com/wp-content/uploads/2020/12/Scherm%C2%ADafbeelding-2025-12-08-om-15.35.00-min.png",
        "https://campsolutions.com/wp-content/uploads/2020/12/Naamloos-1.png",
    ],
    "camp-giant-hat": [
        "https://campsolutions.com/wp-content/uploads/2020/12/Giant-Hat_Triple_CampSolutions-400x284.jpg",
        "https://campsolutions.com/wp-content/uploads/2020/12/Giant-Hat_Triple_CampSolutions.jpg",
        "https://campsolutions.com/wp-content/uploads/2020/12/Naamloos-1.png",
    ],
    "camp-arcade": [
        "https://campsolutions.com/wp-content/uploads/2020/12/BDP57623-GOC-Hoenderloo-Bas-Driessen-Photography-1024x683-1-400x284.jpg",
        "https://campsolutions.com/wp-content/uploads/2020/12/BDP57623-GOC-Hoenderloo-Bas-Driessen-Photography-1024x683-1.jpg",
        "https://campsolutions.com/wp-content/uploads/2020/12/Naamloos-1.png",
    ],
}

# Fallback supplier-level images (used when model-specific images not available)
SUPPLIER_IMAGES = {
    "kunert": {
        "modern": [
            "https://chaletskunert.nl/wp-content/uploads/slider/cache/9bb15a9fd5ca8225826fd1bd0d3c2b44/w2.webp",
            "https://chaletskunert.nl/wp-content/uploads/slider/cache/21360c1d25e0b79e2241df7736a66610/11-scaled-2.webp",
            "https://chaletskunert.nl/wp-content/uploads/slider/cache/a6f3180fbc02492d899cbc5b02b63e8e/12-scaled-1.webp",
        ],
        "luxe": [
            "https://chaletskunert.nl/wp-content/uploads/slider/cache/a7d32cf654945640a6ba12c117e735de/13-scaled-1.webp",
            "https://chaletskunert.nl/wp-content/uploads/slider/cache/68da8ee0d54984a681705d89a909e163/14-scaled-1.webp",
            "https://chaletskunert.nl/wp-content/uploads/slider/cache/9bb15a9fd5ca8225826fd1bd0d3c2b44/w2.webp",
        ],
        "landelijk": [
            "https://chaletskunert.nl/wp-content/uploads/slider/cache/fde7c3b8d28232241bc5367a7d3e6e2b/mobilehome-2.webp",
            "https://chaletskunert.nl/wp-content/uploads/slider/cache/b4efa0dfce7392c71bf98c30e4107108/invierno_s1-scaled-1.webp",
            "https://chaletskunert.nl/wp-content/uploads/slider/cache/3abd295cfedd4e21a7876c278eb86862/invierno_s3-scaled-1.webp",
        ],
    },
    "arcabo": {
        "modern": [
            "https://arcabo.nl/wp-content/uploads/1-New-Bay-A-buitenzijde-2024-uitgelicht.png",
            "https://arcabo.nl/wp-content/uploads/1-Charleston-buitenzijde-met-opmaak-1-uitgelicht-klein-2024.png",
            "https://arcabo.nl/wp-content/uploads/Ocala-website-groot-1.png",
        ],
        "luxe": [
            "https://arcabo.nl/wp-content/uploads/1-New-Bay-A-buitenzijde-2024.png",
            "https://arcabo.nl/wp-content/uploads/3-Charleston-C-woonkamer-2-klein-2024.png",
            "https://arcabo.nl/wp-content/uploads/2-New-Bay-A-woonkamer-1-2-klein-2023.png",
        ],
        "landelijk": [
            "https://arcabo.nl/wp-content/uploads/Lodge-3D-9-2023-buitenzijde-klein-2023-uitgelicht.png",
            "https://arcabo.nl/wp-content/uploads/1-Buitenzijde-Long-Beach-A-klein-2023-uitgelicht.png",
            "https://arcabo.nl/wp-content/uploads/1-carlington-70m2-buitenzijde2-uitgelicht.png",
        ],
    },
    "bbs": {
        "modern": [
            "https://ucarecdn.com/76932055-baf1-402d-bedb-68e5b903160e/-/format/auto/-/resize/800x500/",
            "https://ucarecdn.com/3b93939b-90ac-4bf0-8bd7-f492cf4fd253/-/format/auto/-/resize/800x500/",
            "https://ucarecdn.com/16fbc617-c09f-4a02-a022-03d455ad438a/-/format/auto/-/resize/800x500/",
        ],
        "luxe": [
            "https://ucarecdn.com/17ae1b5b-9eb9-4c0a-9507-b46fe3a05c33/-/format/auto/-/resize/800x500/",
            "https://ucarecdn.com/2502c7b1-a3be-46ee-b8ac-0c8e367a1473/-/format/auto/-/resize/800x500/",
            "https://ucarecdn.com/51e8be1e-9c5c-4e0c-b9af-eab7b2f66652/-/format/auto/-/resize/800x500/",
        ],
        "landelijk": [
            "https://ucarecdn.com/16fbc617-c09f-4a02-a022-03d455ad438a/-/format/auto/-/resize/800x500/",
            "https://ucarecdn.com/76932055-baf1-402d-bedb-68e5b903160e/-/format/auto/-/resize/800x500/",
            "https://ucarecdn.com/3b93939b-90ac-4bf0-8bd7-f492cf4fd253/-/format/auto/-/resize/800x500/",
        ],
    },
    "campsolutions": {
        "modern": [
            "https://campsolutions.com/wp-content/uploads/2020/12/Scherm%C2%ADafbeelding-2025-12-08-om-15.52.21-min-e1765205821482.png",
            "https://campsolutions.com/wp-content/uploads/2022/01/CS-GL-Featured-img.jpg",
            "https://campsolutions.com/wp-content/uploads/2020/12/BDP57623-GOC-Hoenderloo-Bas-Driessen-Photography-1024x683-1.jpg",
        ],
        "luxe": [
            "https://campsolutions.com/wp-content/uploads/2020/12/Scherm%C2%ADafbeelding-2025-12-08-om-15.35.00-min.png",
            "https://campsolutions.com/wp-content/uploads/2021/12/dof-panorama-uitgelicht.jpeg",
            "https://campsolutions.com/wp-content/uploads/2020/12/Giant-Hat_Triple_CampSolutions.jpg",
        ],
        "landelijk": [
            "https://campsolutions.com/wp-content/uploads/2020/12/Naamloos-1.png",
            "https://campsolutions.com/wp-content/uploads/2020/12/Scherm%C2%ADafbeelding-2025-12-08-om-15.51.57-min-e1765205971348.png",
            "https://campsolutions.com/wp-content/uploads/2025/04/20250512-DickRuumpolFotografie-Campsolutions-LR-014-e1749747535515-400x284.jpg",
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

# ==================== UPGRADE OPTIONS ====================

UPGRADE_OPTIONS = {
    "chalet": {
        "keuken": [
            {"id": "keuken-basis", "name": "Basis Keuken", "description": "2-pits kookplaat, mini koelkast, gootsteen", "price": 0},
            {"id": "keuken-compleet", "name": "Complete Keuken", "description": "4-pits, vaatwasser, combi oven, grote koelkast", "price": 3500},
            {"id": "keuken-luxe", "name": "Luxe Keuken", "description": "Inductie, Miele apparatuur, granieten blad, wijnkoeler", "price": 8500},
        ],
        "badkamer": [
            {"id": "bad-basis", "name": "Basis Badkamer", "description": "Douche, toilet, wastafel", "price": 0},
            {"id": "bad-compleet", "name": "Complete Badkamer", "description": "Regendouche, dubbele wastafel, vloerverwarming", "price": 2800},
            {"id": "bad-wellness", "name": "Wellness Badkamer", "description": "Vrijstaand bad, regendouche, sauna", "price": 7500},
        ],
        "terras": [
            {"id": "terras-geen", "name": "Geen Terras", "description": "Alleen deur naar buiten", "price": 0},
            {"id": "terras-klein", "name": "Klein Terras 6m²", "description": "Overdekt terras, tuinmeubilair", "price": 3200},
            {"id": "terras-groot", "name": "Groot Terras 15m²", "description": "Wraparound terras, loungeset, buitenkeuken", "price": 8000},
        ],
        "interieur": [
            {"id": "int-basis", "name": "Basis Interieur", "description": "Functioneel meubilair, eenvoudige afwerking", "price": 0},
            {"id": "int-comfort", "name": "Comfort Interieur", "description": "Houten meubelen, sfeerverlichting, textiel", "price": 4500},
            {"id": "int-luxe", "name": "Luxe Interieur", "description": "Design meubelen, smart home, custom styling", "price": 12000},
        ],
        "klimaat": [
            {"id": "klim-geen", "name": "Geen", "description": "Geen verwarming of airco", "price": 0},
            {"id": "klim-cv", "name": "CV Verwarming", "description": "Gasverwarming, radiatoren", "price": 2200},
            {"id": "klim-wp", "name": "Warmtepomp + Airco", "description": "Lucht-lucht warmtepomp, koelt en verwarmt", "price": 4800},
        ],
        "duurzaamheid": [
            {"id": "duur-geen", "name": "Standaard", "description": "Aansluiting op netwerk", "price": 0},
            {"id": "duur-solar", "name": "Zonnepanelen", "description": "4 panelen, 1.6 kWp, deels zelfvoorzienend", "price": 3200},
            {"id": "duur-offgrid", "name": "Off-Grid Pakket", "description": "8 panelen, thuisbatterij, waterrecycling", "price": 14000},
        ],
    },
    "glamping": {
        "sanitair": [
            {"id": "san-geen", "name": "Geen Sanitair", "description": "Gebruik centraal sanitairblok", "price": 0},
            {"id": "san-basis", "name": "Basis Sanitair", "description": "Chemisch toilet, wasbak", "price": 1800},
            {"id": "san-compleet", "name": "Compleet Sanitair", "description": "Douche, toilet, wastafel, warm water", "price": 4500},
        ],
        "inrichting": [
            {"id": "inr-kaal", "name": "Kale Tent", "description": "Leeg, eigen inrichting", "price": 0},
            {"id": "inr-basis", "name": "Basis Inrichting", "description": "Bedden, tafel, stoelen, verlichting", "price": 2500},
            {"id": "inr-luxe", "name": "Luxe Inrichting", "description": "Boxsprings, design meubelen, sfeerverlichting", "price": 6000},
        ],
        "vlonder": [
            {"id": "vl-geen", "name": "Geen", "description": "Direct op de grond", "price": 0},
            {"id": "vl-hout", "name": "Houten Vlonder", "description": "Duurzaam hardhout, verhoogd", "price": 1500},
            {"id": "vl-beton", "name": "Betonnen Fundament", "description": "Permanente fundering", "price": 3200},
        ],
        "verlichting": [
            {"id": "verl-basis", "name": "Basis", "description": "Enkele lamp, stopcontact", "price": 0},
            {"id": "verl-sfeer", "name": "Sfeerverlichting", "description": "LED strips, lantaarns, dimbaar", "price": 800},
            {"id": "verl-smart", "name": "Smart Lighting", "description": "App-gestuurd, kleurwisseling, timer", "price": 2500},
        ],
    },
}

# ==================== INSPIRATIE PAKKETTEN ====================

INSPIRATIE_PAKKETTEN = [
    {
        "id": "glamping-tour-populair",
        "name": "Populair Glamping Pakket",
        "subtitle": "Na de inspiratie reis van de Glamping Tour 30-31 maart",
        "description": "Dit pakket is samengesteld na de Glamping Tour inspiratiereis van 30-31 maart. De meest populaire configuratie onder parkondernemers: een mix van Wood Lodges en een Safari Lodge als blikvanger.",
        "badge": "Glamping Tour 2025",
        "badge_color": "#2D6A4F",
        "flow_type": "chalet",
        "categorie": "glamping",
        "models": [
            {"model_id": "camp-wood-lodge-midi", "quantity": 4, "upgrades": {"sanitair": "san-compleet", "inrichting": "inr-luxe", "vlonder": "vl-hout", "verlichting": "verl-sfeer"}},
            {"model_id": "camp-wood-lodge", "quantity": 2, "upgrades": {"sanitair": "san-compleet", "inrichting": "inr-luxe", "vlonder": "vl-hout", "verlichting": "verl-sfeer"}},
            {"model_id": "camp-safari-lodge", "quantity": 1, "upgrades": {"sanitair": "san-compleet", "inrichting": "inr-luxe", "vlonder": "vl-hout", "verlichting": "verl-sfeer"}},
        ],
        "total_units": 7,
        "estimated_investment": 112000,
        "highlights": ["7 glamping units", "Mix van formaten", "Compleet sanitair + luxe inrichting", "Sfeerverlichting + houten vlonders"],
    },
    {
        "id": "luxe-chalet-park",
        "name": "Luxe Chaletpark Setup",
        "subtitle": "Premium vakantiepark met hoge nachtprijs",
        "description": "Bewezen concept voor vakantieparken die mikken op het premium segment. Arcabo zadeldak chalets met luxe keuken, wellness badkamer en groot terras. Gemiddelde nachtprijs €180+.",
        "badge": "Premium Concept",
        "badge_color": "#8B6914",
        "flow_type": "chalet",
        "categorie": "chalet",
        "models": [
            {"model_id": "arcabo-zadel-18", "quantity": 5, "upgrades": {"keuken": "keuken-luxe", "badkamer": "bad-wellness", "terras": "terras-groot", "interieur": "int-luxe", "klimaat": "klim-wp", "duurzaamheid": "duur-solar"}},
            {"model_id": "arcabo-charleston", "quantity": 2, "upgrades": {"keuken": "keuken-luxe", "badkamer": "bad-wellness", "terras": "terras-groot", "interieur": "int-luxe", "klimaat": "klim-wp", "duurzaamheid": "duur-solar"}},
        ],
        "total_units": 7,
        "estimated_investment": 1120000,
        "highlights": ["7 premium chalets", "Wellness badkamers + jacuzzi", "Zonnepanelen + warmtepomp", "Groot terras met buitenkeuken"],
    },
    {
        "id": "budget-starter-park",
        "name": "Starter Park — Budget",
        "subtitle": "Snel rendabel, laag instapniveau",
        "description": "Ideaal voor ondernemers die willen starten met recreatieverhuur. Mix van BBS vakantiewoningen en Kunert chalets met basis upgrades. Laagste investering per bed.",
        "badge": "Starter Concept",
        "badge_color": "#244628",
        "flow_type": "chalet",
        "categorie": "chalet",
        "models": [
            {"model_id": "bbs-compact", "quantity": 3, "upgrades": {"keuken": "keuken-compleet", "badkamer": "bad-basis", "terras": "terras-klein", "interieur": "int-comfort", "klimaat": "klim-cv", "duurzaamheid": "duur-geen"}},
            {"model_id": "kunert-haven", "quantity": 4, "upgrades": {"keuken": "keuken-compleet", "badkamer": "bad-basis", "terras": "terras-klein", "interieur": "int-comfort", "klimaat": "klim-cv", "duurzaamheid": "duur-geen"}},
        ],
        "total_units": 7,
        "estimated_investment": 480000,
        "highlights": ["7 betaalbare units", "Complete keuken + CV", "Klein terras + comfort interieur", "Snelle terugverdientijd"],
    },
]

# ==================== PRICING ====================

BTW_PERCENTAGE = 21
LEASE_MONTHS = 60
LEASE_FACTOR = 0.018  # ~1.8% of price per month for 60 months

def calculate_pricing(basisprijs: float, upgrades_total: float = 0) -> dict:
    total_excl = basisprijs + upgrades_total
    btw = round(total_excl * BTW_PERCENTAGE / 100)
    totaal_incl = total_excl + btw
    lease_monthly = round(total_excl * LEASE_FACTOR)
    return {
        "basisprijs": basisprijs,
        "upgrades_total": upgrades_total,
        "totaal_excl_btw": total_excl,
        "btw_percentage": BTW_PERCENTAGE,
        "btw_bedrag": btw,
        "totaal_incl_btw": totaal_incl,
        "lease_monthly": lease_monthly,
        "lease_months": LEASE_MONTHS,
    }


def calculate_upgrades_total(categorie: str, selections: dict) -> tuple:
    """Calculate total upgrade cost and details."""
    options = UPGRADE_OPTIONS.get(categorie, {})
    total = 0
    details = []
    for cat_key, option_id in selections.items():
        cat_options = options.get(cat_key, [])
        option = next((o for o in cat_options if o["id"] == option_id), None)
        if option and option["price"] > 0:
            total += option["price"]
            details.append({"category": cat_key, "name": option["name"], "price": option["price"]})
    return total, details

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

    # Add pricing + images (model-specific product photos take priority)
    result = []
    for m in filtered:
        pricing = calculate_pricing(m["basisprijs"])
        model_imgs = MODEL_IMAGES.get(m["id"])
        if model_imgs:
            images = {"modern": model_imgs, "luxe": model_imgs, "landelijk": model_imgs}
        else:
            images = SUPPLIER_IMAGES.get(m["supplier_id"], {})
        result.append({**m, "pricing": pricing, "images": images})

    return result


@chalet_router.get("/models/{model_id}")
async def get_model_detail(model_id: str):
    model = next((m for m in CHALET_MODELS if m["id"] == model_id), None)
    if not model:
        return {"error": "Model niet gevonden"}
    pricing = calculate_pricing(model["basisprijs"])
    model_imgs = MODEL_IMAGES.get(model["id"])
    if model_imgs:
        images = {"modern": model_imgs, "luxe": model_imgs, "landelijk": model_imgs}
    else:
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


@chalet_router.get("/upgrade-options/{categorie}")
async def get_upgrade_options(categorie: str):
    """Return upgrade options for chalet or glamping."""
    return UPGRADE_OPTIONS.get(categorie, UPGRADE_OPTIONS.get("chalet", {}))


@chalet_router.post("/calculate-with-upgrades")
async def calculate_with_upgrades(data: dict):
    """Calculate pricing including selected upgrades."""
    model_id = data.get("model_id")
    selections = data.get("upgrades", {})

    model = next((m for m in CHALET_MODELS if m["id"] == model_id), None)
    if not model:
        return {"error": "Model niet gevonden"}

    upgrades_total, upgrade_details = calculate_upgrades_total(model["categorie"], selections)
    pricing = calculate_pricing(model["basisprijs"], upgrades_total)

    return {
        "model_id": model_id,
        "model_name": model["name"],
        "pricing": pricing,
        "upgrade_details": upgrade_details,
    }


@chalet_router.get("/inspiratie")
async def get_inspiratie_pakketten():
    """Return all inspiration packages."""
    return INSPIRATIE_PAKKETTEN


@chalet_router.get("/inspiratie/{pakket_id}")
async def get_inspiratie_detail(pakket_id: str):
    """Return a single inspiration package with full model details."""
    pakket = next((p for p in INSPIRATIE_PAKKETTEN if p["id"] == pakket_id), None)
    if not pakket:
        return {"error": "Pakket niet gevonden"}

    # Enrich with model details
    enriched_models = []
    for item in pakket["models"]:
        model = next((m for m in CHALET_MODELS if m["id"] == item["model_id"]), None)
        if model:
            upgrades_total, upgrade_details = calculate_upgrades_total(model["categorie"], item.get("upgrades", {}))
            unit_pricing = calculate_pricing(model["basisprijs"], upgrades_total)
            enriched_models.append({
                "model": model,
                "quantity": item["quantity"],
                "upgrades": item.get("upgrades", {}),
                "upgrade_details": upgrade_details,
                "unit_pricing": unit_pricing,
                "line_total": unit_pricing["totaal_incl_btw"] * item["quantity"],
                "line_lease": unit_pricing["lease_monthly"] * item["quantity"],
            })

    # Calculate totals
    total_investment = sum(m["line_total"] for m in enriched_models)
    total_lease = sum(m["line_lease"] for m in enriched_models)
    total_units = sum(m["quantity"] for m in enriched_models)

    return {
        **pakket,
        "enriched_models": enriched_models,
        "totals": {
            "total_investment_incl_btw": total_investment,
            "total_lease_monthly": total_lease,
            "total_units": total_units,
        },
    }

