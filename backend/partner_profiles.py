"""
Partner/Leverancier Profielen — Ticra Outdoor als voorbeeld.
Bevat bedrijfsinfo, Pleisureworld badges, podcast/blog links, testimonials, en top producten.
"""
from fastapi import APIRouter

partner_router = APIRouter(prefix="/partners", tags=["Partner Profielen"])

PARTNER_PROFILES = {
    "ticra-outdoor": {
        "id": "ticra-outdoor",
        "name": "Ticra Outdoor",
        "tagline": "Outdoor & Wellness products voor recreatie en hospitality",
        "description": "Ticra Outdoor is de toonaangevende leverancier van outdoor wellness producten in de Benelux. Met een uitgebreid assortiment van hottubs, buitensauna's en buitendouches voorzien zij recreatieparken, glamping resorts en vakantieparken van premium wellness faciliteiten. Alle producten worden geleverd met professionele installatie en onderhoud.",
        "website": "https://www.ticraoutdoor.com",
        "logo": "https://www.ticraoutdoor.com/nl/assets/images/ticra-outdoor-logo.svg",
        "hero_image": "https://www.ticraoutdoor.com/nl/assets/galleries/126/_thumbs/medium_327_1_ticra_outdoor_hot_tub_flevoland_skargards_rojal_190_dualburn_1.webp",
        "categorieen": ["hottubs", "buitensaunas", "buitendouches"],
        "pleisureworld_partner": True,
        "pleisureworld_badge": "Preferred Partner",
        "pleisureworld_sinds": "2024",
        "blog_url": "https://www.pleisureworld.nl/blog/ticra-outdoor-wellness-trends",
        "blog_titel": "Wellness op het recreatiepark: de trends van 2026",
        "podcast": {
            "titel": "Leisure Talk #14 — Wellness als verdienmodel",
            "beschrijving": "Richard Otten (Trendwatcher Recreatie) in gesprek met Ticra Outdoor over de groeiende vraag naar wellness op recreatieparken en hoe parkeigenaren hun omzet kunnen verhogen met hottubs en sauna's.",
            "url": "https://www.pleisureworld.nl/podcast/leisure-talk-14",
            "duur": "38 min",
            "gast": "Richard Otten — Trendwatcher Recreatie & Hospitality",
        },
        "trendwatcher_quote": {
            "tekst": "Wellness is geen luxe meer, het is een verwachting. Gasten kiezen een park op basis van de ervaring — en een hottub of sauna bij het chalet maakt het verschil tussen een 7 en een 9 op de review. Ticra begrijpt dat als geen ander.",
            "auteur": "Richard Otten",
            "functie": "Trendwatcher Recreatie & Hospitality",
        },
        "stats": {
            "parken_actief": "120+",
            "jaren_ervaring": "15+",
            "producten_geinstalleerd": "2.500+",
            "klanttevredenheid": "4.8/5",
        },
        "deelname": [
            {"event": "Vakantiebeurs Utrecht 2026", "type": "Exposant"},
            {"event": "Glamping Show 2025", "type": "Keynote Speaker"},
            {"event": "HISWA te Water 2025", "type": "Exposant"},
            {"event": "Pleisureworld Summit 2026", "type": "Preferred Partner"},
        ],
        "top_producten": [
            {
                "id": "well-hottub-basis",
                "name": "TICRA Hottub Houtgestookt",
                "prijs": 2995,
                "image": "https://www.ticraoutdoor.com/nl/assets/galleries/133/_thumbs/medium_409_1_ticra_outdoor_hottub_hout_interne_kachel_welltub_160.webp",
                "reden": "Meest gekozen — Perfecte prijs/kwaliteit voor verhuur",
                "configuraties": 847,
            },
            {
                "id": "well-sauna-barrel",
                "name": "Barrel Sauna Thermowood",
                "prijs": 5495,
                "image": "https://www.ticraoutdoor.com/nl/assets/galleries/97/_thumbs/medium_25-4-buitensauna-barrel-thermowood-ticra-outdoor.webp",
                "reden": "Populairste sauna — Authentieke uitstraling, laag onderhoud",
                "configuraties": 623,
            },
            {
                "id": "well-douche-sunlight",
                "name": "Sunlight Buitendouche",
                "prijs": 695,
                "image": "https://www.ticraoutdoor.com/nl/assets/galleries/141/_thumbs/medium_478_2_buitendouche_red_cedar_sunlightshower_ticra_outdoor_dundalk.webp",
                "reden": "Best seller — Compacte toevoeging bij elke hottub",
                "configuraties": 1204,
            },
        ],
        "usps": [
            "Gratis bezorging bij recreatieparken",
            "2 jaar volledige garantie",
            "Professionele installatie inbegrepen",
            "24/7 service voor recreatiepartners",
            "Leaseconstructies beschikbaar",
        ],
    },
    "kunert-group": {
        "id": "kunert-group",
        "name": "Kunert Group",
        "tagline": "Premium chalets & mobiele woningen sinds 1994",
        "description": "Kunert Group is een van Europa's grootste producenten van vakantiechalets en mobiele woningen. Met fabrieken in Polen en een uitgebreid dealernetwerk in de Benelux levert Kunert kwalitatieve chalets voor recreatieparken.",
        "website": "https://www.chaletskunert.nl",
        "logo": "",
        "hero_image": "https://chaletskunert.nl/wp-content/uploads/slider/cache/596c295a46e6a41280859315325ba1bc/Image1.png",
        "categorieen": ["chalets"],
        "pleisureworld_partner": True,
        "pleisureworld_badge": "Preferred Partner",
        "pleisureworld_sinds": "2023",
        "blog_url": "https://www.pleisureworld.nl/blog/kunert-chalets-trends",
        "blog_titel": "De toekomst van het vakantiechalet: modulair en duurzaam",
        "podcast": None,
        "trendwatcher_quote": None,
        "stats": {
            "parken_actief": "200+",
            "jaren_ervaring": "30+",
            "producten_geinstalleerd": "10.000+",
            "klanttevredenheid": "4.6/5",
        },
        "deelname": [],
        "top_producten": [],
        "usps": [
            "Fabrieksgarantie 10 jaar",
            "Maatwerk mogelijk",
            "Snelle levertijden (8-12 weken)",
        ],
    },
    "arcabo": {
        "id": "arcabo",
        "name": "Arcabo",
        "tagline": "Al 27 jaar Europa's meest veelzijdige chaletbouwer",
        "description": "Arcabo ontwerpt en bouwt chalets die opvallen. Met meer dan 27 jaar ervaring en een breed portfolio van moderne tot klassieke chalets, bedient Arcabo de top van de recreatiemarkt.",
        "website": "https://www.arcabo.nl",
        "logo": "",
        "hero_image": "https://arcabo.nl/wp-content/uploads/1-New-Bay-A-buitenzijde-2024.png",
        "categorieen": ["chalets"],
        "pleisureworld_partner": True,
        "pleisureworld_badge": "Preferred Partner",
        "pleisureworld_sinds": "2024",
        "blog_url": "",
        "blog_titel": "",
        "podcast": None,
        "trendwatcher_quote": None,
        "stats": {
            "parken_actief": "150+",
            "jaren_ervaring": "27+",
            "producten_geinstalleerd": "5.000+",
            "klanttevredenheid": "4.7/5",
        },
        "deelname": [],
        "top_producten": [],
        "usps": [
            "Volledig op maat",
            "Eigen ontwerpafdeling",
            "Transport door heel Europa",
        ],
    },
    "campsolutions": {
        "id": "campsolutions",
        "name": "Campsolutions",
        "tagline": "#1 in Pop-up Campings & Glamping",
        "description": "Campsolutions is marktleider in glamping accommodaties en pop-up camping concepten. Van safaritenten tot panorama domes — Campsolutions levert complete glamping oplossingen.",
        "website": "https://www.campsolutions.com",
        "logo": "",
        "hero_image": "https://campsolutions.com/wp-content/uploads/2020/12/Scherm%C2%ADafbeelding-2025-12-08-om-15.52.21-min-e1765205821482.png",
        "categorieen": ["glamping"],
        "pleisureworld_partner": False,
        "pleisureworld_badge": "",
        "pleisureworld_sinds": "",
        "blog_url": "",
        "blog_titel": "",
        "podcast": None,
        "trendwatcher_quote": None,
        "stats": {
            "parken_actief": "80+",
            "jaren_ervaring": "10+",
            "producten_geinstalleerd": "3.000+",
            "klanttevredenheid": "4.5/5",
        },
        "deelname": [],
        "top_producten": [],
        "usps": [
            "Turnkey glamping concepten",
            "Pop-up & permanente oplossingen",
            "Eigen montageteam",
        ],
    },
    "bbs-systeembouw": {
        "id": "bbs-systeembouw",
        "name": "BBS Systeembouw",
        "tagline": "Maatwerk woon- & werkoplossingen",
        "description": "BBS Systeembouw levert modulaire vakantiewoningen en chalets op maat. Met een focus op systeembouw en snelle levertijden is BBS een betrouwbare partner voor recreatieparken.",
        "website": "https://www.bbssysteembouw.nl",
        "logo": "",
        "hero_image": "https://ucarecdn.com/76932055-baf1-402d-bedb-68e5b903160e/-/format/auto/-/resize/800x500/",
        "categorieen": ["chalets", "vakantiewoningen"],
        "pleisureworld_partner": False,
        "pleisureworld_badge": "",
        "pleisureworld_sinds": "",
        "blog_url": "",
        "blog_titel": "",
        "podcast": None,
        "trendwatcher_quote": None,
        "stats": {
            "parken_actief": "40+",
            "jaren_ervaring": "20+",
            "producten_geinstalleerd": "1.500+",
            "klanttevredenheid": "4.4/5",
        },
        "deelname": [],
        "top_producten": [],
        "usps": [
            "Modulaire systeembouw",
            "Korte bouwtijd",
            "Maatwerk op locatie",
        ],
    },
}


@partner_router.get("/profiles")
async def get_all_profiles():
    """Alle leveranciersprofielen (summary)."""
    return [
        {
            "id": p["id"],
            "name": p["name"],
            "tagline": p["tagline"],
            "hero_image": p["hero_image"],
            "categorieen": p["categorieen"],
            "pleisureworld_partner": p["pleisureworld_partner"],
            "pleisureworld_badge": p["pleisureworld_badge"],
        }
        for p in PARTNER_PROFILES.values()
    ]


@partner_router.get("/profiles/{partner_id}")
async def get_partner_profile(partner_id: str):
    """Gedetailleerd leveranciersprofiel."""
    profile = PARTNER_PROFILES.get(partner_id)
    if not profile:
        return {"error": "Partner niet gevonden"}
    return profile
