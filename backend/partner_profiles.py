"""
Partner/Leverancier Profielen — Verrijkt met podcasts, trendwatcher quotes, top 3 producten, evenementen.
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
        "tagline": "Toonaangevende fabrikant van chalets in Europa sinds 1997",
        "description": "Kunert Mobile Homes is een toonaangevende fabrikant van stacaravans en chalets in Polen en Europa. Met meer dan 25 jaar ervaring produceren zij jaarrondhuizen in vele varianten. Het bedrijf begon in 1997 als importeur van Nederlandse huizen en breidde in 2013 uit naar zelfstandige productie. Kunert levert chalets in 8 landen met eigen transport door heel Europa.",
        "website": "https://www.chaletskunert.nl",
        "logo": "https://chaletskunert.nl/wp-content/uploads/2023/11/cropped-white-2-1-768x52-1.webp",
        "hero_image": "https://chaletskunert.nl/wp-content/uploads/slider/cache/596c295a46e6a41280859315325ba1bc/Image1.png",
        "categorieen": ["chalets", "stacaravans", "sanitair units"],
        "pleisureworld_partner": True,
        "pleisureworld_badge": "Preferred Partner",
        "pleisureworld_sinds": "2023",
        "blog_url": "https://www.pleisureworld.nl/blog/kunert-chalets-modulair-bouwen",
        "blog_titel": "Modulair bouwen: hoe Kunert Group de chaletmarkt verandert",
        "podcast": {
            "titel": "Leisure Talk #8 — De Europese chaletmarkt in beweging",
            "beschrijving": "Een gesprek over hoe Kunert Group vanuit Polen de Nederlandse en Europese markt bedient met innovatieve, betaalbare chalets. Over schaalvoordelen, maatwerk en de toekomst van modulaire vakantiewoningen.",
            "url": "https://www.pleisureworld.nl/podcast/leisure-talk-8",
            "duur": "42 min",
            "gast": "Kunert Group Management — Europees Chaletfabrikant",
        },
        "trendwatcher_quote": {
            "tekst": "De chaletmarkt verschuift van standaard naar premium. Parkeigenaren die investeren in kwalitatieve, jaarronde chalets zien hun bezettingsgraad met 20-30% stijgen. Kunert speelt hier slim op in met hun Premium-lijn — betaalbare luxe, direct leverbaar.",
            "auteur": "Richard Otten",
            "functie": "Trendwatcher Recreatie & Hospitality",
        },
        "stats": {
            "parken_actief": "200+",
            "jaren_ervaring": "27+",
            "producten_geinstalleerd": "10.000+",
            "klanttevredenheid": "4.6/5",
        },
        "deelname": [
            {"event": "Vakantiebeurs Utrecht 2026", "type": "Exposant"},
            {"event": "Recron Jaarcongres 2025", "type": "Partner"},
            {"event": "Holiday & Leisure Expo 2025", "type": "Exposant"},
            {"event": "Pleisureworld Summit 2026", "type": "Preferred Partner"},
        ],
        "top_producten": [
            {
                "id": "kunert-haven",
                "name": "Haven",
                "prijs": 74950,
                "image": "https://chaletskunert.nl/wp-content/uploads/slider/cache/596c295a46e6a41280859315325ba1bc/Image1.png",
                "reden": "Meest gekozen — Modern design, open keuken, ideaal voor verhuur",
                "configuraties": 312,
            },
            {
                "id": "kunert-plat-18",
                "name": "Plat 18",
                "prijs": 89500,
                "image": "https://chaletskunert.nl/wp-content/uploads/slider/cache/a7d32cf654945640a6ba12c117e735de/13-scaled-1.webp",
                "reden": "Premium bestseller — Ruim, 3 slaapkamers, plat dak",
                "configuraties": 245,
            },
            {
                "id": "kunert-plat-12",
                "name": "Plat 12",
                "prijs": 59950,
                "image": "https://chaletskunert.nl/wp-content/uploads/slider/cache/9bb15a9fd5ca8225826fd1bd0d3c2b44/w2.webp",
                "reden": "Budget favoriet — Compact, modern, snel leverbaar",
                "configuraties": 189,
            },
        ],
        "usps": [
            "Fabrieksgarantie 2 jaar (verlengbaar tot 5 jaar)",
            "10 jaar garantie op gegalvaniseerd chassis",
            "Eigen transport door heel Europa",
            "Volledig maatwerk mogelijk",
            "3D Matterport tours beschikbaar",
            "Levertijd slechts 5 weken",
        ],
    },
    "arcabo": {
        "id": "arcabo",
        "name": "Arcabo",
        "tagline": "Al bijna 30 jaar Europa's grootste specialist in chaletbouw",
        "description": "ARCABO is een van de grootste producenten van wintervaste chalets in Europa. Met bijna 30 jaar ervaring brengen zij dagelijks een groot team experts samen om tot in de kleinste details de mooiste chalets te bouwen. ARCABO begeleidt zowel particulieren als recreatieondernemers van planning tot uitvoering, met een eigen showroom en geavanceerde 3D-ontwerpmogelijkheden.",
        "website": "https://www.arcabo.nl",
        "logo": "https://www.arcabo.nl/wp-content/themes/arcabo/library/images/arcabo-logo.svg",
        "hero_image": "https://arcabo.nl/wp-content/uploads/1-New-Bay-A-buitenzijde-2024.png",
        "categorieen": ["chalets", "wintervaste chalets", "recreatie"],
        "pleisureworld_partner": True,
        "pleisureworld_badge": "Preferred Partner",
        "pleisureworld_sinds": "2024",
        "blog_url": "https://www.pleisureworld.nl/blog/arcabo-wintervaste-chalets",
        "blog_titel": "Wintervaste chalets: jaarrond rendement voor parkeigenaren",
        "podcast": {
            "titel": "Leisure Talk #11 — Design als onderscheidend vermogen",
            "beschrijving": "Arcabo over hoe design en kwaliteit het verschil maken in de recreatiemarkt. Over hun showroom, het 3D-ontwerpproces en waarom steeds meer parken kiezen voor wintervaste chalets met een uniek karakter.",
            "url": "https://www.pleisureworld.nl/podcast/leisure-talk-11",
            "duur": "35 min",
            "gast": "Arcabo Design Team — Europa's chaletspecialist",
        },
        "trendwatcher_quote": {
            "tekst": "Gasten willen geen standaard chalet meer. Ze zoeken karakter, een 'wow-factor'. Arcabo snapt dat — hun New Bay en Charleston modellen hebben die Instagrammable uitstraling die parken nodig hebben om de nieuwe generatie gasten aan te trekken.",
            "auteur": "Richard Otten",
            "functie": "Trendwatcher Recreatie & Hospitality",
        },
        "stats": {
            "parken_actief": "150+",
            "jaren_ervaring": "29+",
            "producten_geinstalleerd": "5.000+",
            "klanttevredenheid": "4.7/5",
        },
        "deelname": [
            {"event": "Vakantiebeurs Utrecht 2026", "type": "Exposant"},
            {"event": "Recron Jaarcongres 2025", "type": "Spreker"},
            {"event": "Holiday & Leisure Expo 2025", "type": "Exposant"},
            {"event": "Pleisureworld Summit 2026", "type": "Preferred Partner"},
        ],
        "top_producten": [
            {
                "id": "arcabo-new-bay",
                "name": "New Bay",
                "prijs": 94500,
                "image": "https://arcabo.nl/wp-content/uploads/1-New-Bay-A-buitenzijde-2024.png",
                "reden": "Meest gekozen — Een lust voor het oog, premium afwerking",
                "configuraties": 278,
            },
            {
                "id": "arcabo-charleston",
                "name": "Charleston",
                "prijs": 112000,
                "image": "https://arcabo.nl/wp-content/uploads/1-Charleston-buitenzijde-met-opmaak-1-uitgelicht-klein-2024.png",
                "reden": "Luxe favoriet — Voor de levensgenieters, royale indeling",
                "configuraties": 156,
            },
            {
                "id": "arcabo-ocala",
                "name": "Ocala",
                "prijs": 79950,
                "image": "https://arcabo.nl/wp-content/uploads/Ocala-website-groot-1.png",
                "reden": "Beste prijs/kwaliteit — Eenvoud in levende schoonheid",
                "configuraties": 203,
            },
        ],
        "usps": [
            "Eigen showroom — bezoek onze modellen live",
            "Gratis 3D-ontwerp op maat",
            "Innovatieve productie in Europa",
            "Advies voor recreatieparken door branche-experts",
            "Wintervast en jaarrond bewoonbaar",
            "Seriematig maatwerk mogelijk",
        ],
    },
    "campsolutions": {
        "id": "campsolutions",
        "name": "Campsolutions",
        "tagline": "#1 in Pop-up Campings & Glamping sinds 2008",
        "description": "CampSolutions is expert in het realiseren van belevenisrijke campings en het ontwikkelen van comfortabele glampingtenten. Opgericht in 2008, met het hart van de operatie in Twello. Daar bewaren zij hun voorraad, vervaardigen interieur in eigen werkplaats en voeren reparaties uit in hun eigen naaiatelier. CampSolutions werkt samen met partners als Ten Cate, Vieww en Solvos4Leisure.",
        "website": "https://www.campsolutions.com",
        "logo": "",
        "hero_image": "https://campsolutions.com/wp-content/uploads/2020/12/Scherm%C2%ADafbeelding-2025-12-08-om-15.52.21-min-e1765205821482.png",
        "categorieen": ["glamping", "safaritenten", "lodges", "domes"],
        "pleisureworld_partner": True,
        "pleisureworld_badge": "Glamping Partner",
        "pleisureworld_sinds": "2025",
        "blog_url": "https://www.pleisureworld.nl/blog/campsolutions-glamping-revolutie",
        "blog_titel": "De glamping revolutie: van tent naar beleving",
        "podcast": {
            "titel": "Leisure Talk #16 — Glamping als businessmodel",
            "beschrijving": "Patrick Damen en Dennis Aalders van CampSolutions over de explosieve groei van glamping in Nederland. Hoe zij met maatwerk tenten, eigen naaiatelier en turnkey concepten de markt veroveren. Tips voor ondernemers die willen starten met glamping.",
            "url": "https://www.pleisureworld.nl/podcast/leisure-talk-16",
            "duur": "44 min",
            "gast": "Patrick Damen & Dennis Aalders — Eigenaren CampSolutions",
        },
        "trendwatcher_quote": {
            "tekst": "Glamping is de snelst groeiende sector in de recreatie. Het combineert de charme van kamperen met het comfort dat de moderne gast verwacht. CampSolutions is pionier — hun Wood Lodges en Safari Lodges zetten de standaard voor wat glamping kan zijn.",
            "auteur": "Richard Otten",
            "functie": "Trendwatcher Recreatie & Hospitality",
        },
        "stats": {
            "parken_actief": "80+",
            "jaren_ervaring": "17+",
            "producten_geinstalleerd": "3.000+",
            "klanttevredenheid": "4.5/5",
        },
        "deelname": [
            {"event": "Glamping Show 2025", "type": "Hoofdsponsor"},
            {"event": "Vakantiebeurs Utrecht 2026", "type": "Exposant"},
            {"event": "Recron Jaarcongres 2025", "type": "Partner"},
            {"event": "Pleisureworld Summit 2026", "type": "Glamping Partner"},
        ],
        "top_producten": [
            {
                "id": "camp-wood-lodge",
                "name": "Wood Lodge",
                "prijs": 34950,
                "image": "https://campsolutions.com/wp-content/uploads/2020/12/Scherm%C2%ADafbeelding-2025-12-08-om-15.52.21-min-e1765205821482.png",
                "reden": "Meest gekozen — Unieke beleving, duurzaam hout, snel opbouwbaar",
                "configuraties": 412,
            },
            {
                "id": "camp-safari-lodge",
                "name": "Safari Lodge",
                "prijs": 28500,
                "image": "https://campsolutions.com/wp-content/uploads/2020/12/Scherm%C2%ADafbeelding-2025-12-08-om-15.35.00-min-400x284.png",
                "reden": "Avontuur favoriet — Authentieke safari-ervaring in Nederland",
                "configuraties": 334,
            },
            {
                "id": "camp-panorama-dome",
                "name": "Panorama Dome",
                "prijs": 19950,
                "image": "https://campsolutions.com/wp-content/uploads/2021/12/dof-panorama-uitgelicht-400x284.jpeg",
                "reden": "Instagrammable — Slapen onder de sterren, uniek concept",
                "configuraties": 289,
            },
        ],
        "usps": [
            "Turnkey glamping concepten",
            "Eigen werkplaats en naaiatelier in Twello",
            "Pop-up en permanente oplossingen",
            "Maatwerk tenten naar uw wensen",
            "Samenwerking met Ten Cate (premium tentdoek)",
            "Eigen montageteam voor snelle opbouw",
        ],
    },
    "eijsink": {
        "id": "eijsink",
        "name": "Eijsink",
        "tagline": "POS-systemen, kassa's & bestelzuilen voor horeca die meer wil verkopen",
        "description": "Eijsink is dé Nederlandse specialist in POS-systemen voor de horeca. Met meer dan 35 jaar ervaring leveren zij turn-key kassa-oplossingen, mobiele bestel-tablets, self-order zuilen en een volledig cloud-gebaseerd analytics-platform. Van strandtent tot recreatiepark, van sportbar tot camping-restaurant: Eijsink helpt ondernemers hun omzet te verhogen door snellere afhandeling, slimmere upselling via bestelzuilen en realtime inzicht in wat de bar en de keuken doen. Eén partner, één systeem, één punt van contact.",
        "website": "https://www.eijsink.nl",
        "logo": "",
        "hero_image": "https://images.unsplash.com/photo-1556742044-3c52d6e88c62?w=1200&h=600&fit=crop",
        "categorieen": ["kassa", "bestelzuil", "horeca POS", "betaaloplossingen"],
        "pleisureworld_partner": True,
        "pleisureworld_badge": "Preferred Partner",
        "pleisureworld_sinds": "2025",
        "blog_url": "https://www.pleisureworld.nl/blog/eijsink-bestelzuilen-recreatie",
        "blog_titel": "Bestelzuilen op het recreatiepark: zo verhoog je de gemiddelde besteding met 28%",
        "podcast": {
            "titel": "Leisure Talk #21 — Self-order is geen luxe, het is een must",
            "beschrijving": "Jesse van Eijsink in gesprek met Richard Otten over de stille revolutie in horeca-POS: hoe self-order zuilen de wachttijd halveren, fooien verhogen en de keuken efficiënter maken. Met praktijkcases van Nederlandse recreatieparken en campings.",
            "url": "https://www.pleisureworld.nl/podcast/leisure-talk-21",
            "duur": "39 min",
            "gast": "Jesse — Eijsink",
        },
        "trendwatcher_quote": {
            "tekst": "Wachten is dood geld. Elke minuut die een gast in de rij staat, is een gemiste verkoop. Eijsink begrijpt dat — hun bestelzuilen verkopen ook door, óók als jouw personeel even niet kan. Op recreatieparken zie ik bestedingen 25-30% omhoog gaan zodra de zuil draait.",
            "auteur": "Richard Otten",
            "functie": "Trendwatcher Recreatie & Hospitality",
        },
        "stats": {
            "parken_actief": "350+",
            "jaren_ervaring": "35+",
            "producten_geinstalleerd": "8.000+",
            "klanttevredenheid": "4.7/5",
        },
        "deelname": [
            {"event": "Horecava 2026", "type": "Hoofd-exposant"},
            {"event": "Vakantiebeurs Utrecht 2026", "type": "Exposant"},
            {"event": "Recron Jaarcongres 2025", "type": "Partner"},
            {"event": "Pleisureworld Summit 2026", "type": "Preferred Partner"},
        ],
        "top_producten": [
            {
                "id": "eijsink-bestelzuil-22",
                "name": "Eijsink Bestelzuil 22\" (zelfbestel)",
                "prijs": 4750,
                "image": "https://images.unsplash.com/photo-1581235720704-06d3acfcb36f?w=800&h=600&fit=crop",
                "reden": "Meest gekozen — verhoogt gemiddelde besteding met 25-30%",
                "configuraties": 412,
            },
            {
                "id": "eijsink-pos-touch",
                "name": "Eijsink POS Touchkassa",
                "prijs": 2950,
                "image": "https://images.unsplash.com/photo-1556742393-d75f468bfcb0?w=800&h=600&fit=crop",
                "reden": "Backbone — onmisbaar voor afrekenen, voorraad & rapportage",
                "configuraties": 687,
            },
            {
                "id": "eijsink-outdoor-zuil",
                "name": "Eijsink Outdoor Bestelzuil (IP65)",
                "prijs": 6450,
                "image": "https://images.unsplash.com/photo-1551218372-a8789b81b253?w=800&h=600&fit=crop",
                "reden": "Park-favoriet — werkt 24/7 buiten, verlaagt personeelsdruk",
                "configuraties": 289,
            },
        ],
        "usps": [
            "35+ jaar specialist in horeca-POS",
            "Cloud-platform met realtime analytics",
            "Eigen 24/7 service-team in Nederland",
            "Integreert met alle pin-aanbieders",
            "Bestelzuilen meertalig — perfect voor toeristen",
            "Lease-constructies via RECRA mogelijk",
        ],
    },
    "bbs-systeembouw": {
        "id": "bbs-systeembouw",
        "name": "BBS Systeembouw",
        "tagline": "Maatwerk systeembouw — van idee tot sleutelklare oplevering",
        "description": "BBS Systeembouw uit Heinenoord ontwikkelt, produceert en plaatst hoogwaardige maatwerk woon- en werkoplossingen. Van vakantiewoningen en chalets tot bedrijfsruimtes. Met een 5.0 Google review score en meer dan 100 gerealiseerde projecten is BBS een betrouwbare partner voor recreatieparken die op zoek zijn naar kwaliteit en maatwerk.",
        "website": "https://www.bbssysteembouw.nl",
        "logo": "",
        "hero_image": "https://ucarecdn.com/76932055-baf1-402d-bedb-68e5b903160e/-/format/auto/-/resize/800x500/",
        "categorieen": ["chalets", "vakantiewoningen", "maatwerk"],
        "pleisureworld_partner": False,
        "pleisureworld_badge": "",
        "pleisureworld_sinds": "",
        "blog_url": "https://www.pleisureworld.nl/blog/bbs-systeembouw-maatwerk",
        "blog_titel": "Maatwerk systeembouw: de toekomst van vakantiewoningen",
        "podcast": {
            "titel": "Leisure Talk #19 — Systeembouw als gamechanger",
            "beschrijving": "BBS Systeembouw over hun aanpak van maatwerk modulaire woningen voor recreatie. Hoe zij met een gestructureerde werkwijze van eerste gesprek tot sleutelklare oplevering ontzorgen, en waarom steeds meer parken kiezen voor kwaliteit boven kwantiteit.",
            "url": "https://www.pleisureworld.nl/podcast/leisure-talk-19",
            "duur": "31 min",
            "gast": "BBS Systeembouw Team — Heinenoord",
        },
        "trendwatcher_quote": {
            "tekst": "De recreatiemarkt vraagt om meer dan een standaard chalet. BBS Systeembouw laat zien dat maatwerk niet duur hoeft te zijn als je slim bouwt. Hun 3-stappen aanpak — bespreken, uitwerken, leveren — is een voorbeeld voor de hele branche.",
            "auteur": "Richard Otten",
            "functie": "Trendwatcher Recreatie & Hospitality",
        },
        "stats": {
            "parken_actief": "40+",
            "jaren_ervaring": "20+",
            "producten_geinstalleerd": "100+",
            "klanttevredenheid": "5.0/5",
        },
        "deelname": [
            {"event": "Bouw & Wonen Beurs 2025", "type": "Exposant"},
            {"event": "Recreatie Vakbeurs 2025", "type": "Spreker"},
            {"event": "Pleisureworld Meetup 2026", "type": "Genodigde"},
        ],
        "top_producten": [
            {
                "id": "bbs-comfort",
                "name": "BBS Comfort Vakantiewoning",
                "prijs": 89950,
                "image": "https://ucarecdn.com/16fbc617-c09f-4a02-a022-03d455ad438a/-/format/auto/-/resize/800x500/",
                "reden": "Meest gekozen — Compleet maatwerk, premium afwerking",
                "configuraties": 67,
            },
            {
                "id": "bbs-compact",
                "name": "BBS Compact Chalet",
                "prijs": 64950,
                "image": "https://ucarecdn.com/76932055-baf1-402d-bedb-68e5b903160e/-/format/auto/-/resize/800x500/",
                "reden": "Starter keuze — Betaalbaar maatwerk, snel leverbaar",
                "configuraties": 54,
            },
            {
                "id": "bbs-premium",
                "name": "BBS Premium Woning",
                "prijs": 124500,
                "image": "https://ucarecdn.com/17ae1b5b-9eb9-4c0a-9507-b46fe3a05c33/-/format/auto/-/resize/800x500/",
                "reden": "Luxe segment — Volledig uitgerust, duurzaam",
                "configuraties": 38,
            },
        ],
        "usps": [
            "5.0 Google review score (12 reviews)",
            "Volledig maatwerk — geen standaard prefab",
            "Van ontwerp tot sleutelklare oplevering",
            "3D presentatie van uw ontwerp",
            "Eigen werkplaats in Heinenoord",
            "Ondersteuning bij vergunningsaanvraag",
        ],
    },
    "madino": {
        "id": "madino",
        "name": "Madino",
        "tagline": "Premium terras- en buitenmeubilair voor recreatie en hospitality",
        "description": "Madino is dé specialist in premium terras- en buitenmeubilair voor de recreatie- en hospitality-sector. Van lounge-sets en dining-sets tot daybeds en firepit-loungers — elk product wordt ontworpen voor het Nederlandse buitenklimaat, met weerbestendige materialen (teak, RVS, gepoedercoat aluminium) en duurzame kussens. Voor parkeigenaren leveren we maatwerk per chalet of glamping-unit: van bistro-set bij een budget-chalet tot een complete firepit-lounge bij premium accommodatie. Inclusief installatie, opslag in winter en SLA-onderhoud.",
        "website": "https://www.madino.nl",
        "logo": "",
        "hero_image": "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=1200&h=600&fit=crop",
        "categorieen": ["terras-meubilair", "lounge", "dining", "firepit", "daybeds"],
        "pleisureworld_partner": True,
        "pleisureworld_badge": "Preferred Partner",
        "pleisureworld_sinds": "2026",
        "blog_url": "https://www.pleisureworld.nl/blog/madino-terras-meubilair-recreatie",
        "blog_titel": "Het terras maakt het verschil: zo verhoog je je reviewscore met premium buitenmeubilair",
        "podcast": {
            "titel": "Leisure Talk #23 — Het terras als verdienmodel",
            "beschrijving": "Madino in gesprek met Richard Otten over hoe parkeigenaren hun chalets en glamping-units onderscheiden met premium terras-meubilair. Over weerbestendigheid, kussenkwaliteit, winteropslag en de impact op gastreviews.",
            "url": "https://www.pleisureworld.nl/podcast/leisure-talk-23",
            "duur": "33 min",
            "gast": "Madino Team",
        },
        "trendwatcher_quote": {
            "tekst": "Een chalet zonder een mooi terras is een gemiste kans. Gasten brengen 60% van hun verblijftijd buiten door — dat is waar de Instagram-foto's worden gemaakt en waar de review wordt geschreven. Madino snapt dat: hun firepit lounges zijn dé reden waarom parken in hun pakkettenniveau een stap omhoog kunnen.",
            "auteur": "Richard Otten",
            "functie": "Trendwatcher Recreatie & Hospitality",
        },
        "stats": {
            "parken_actief": "75+",
            "jaren_ervaring": "12+",
            "producten_geinstalleerd": "1.800+",
            "klanttevredenheid": "4.7/5",
        },
        "deelname": [
            {"event": "Vakantiebeurs Utrecht 2026", "type": "Exposant"},
            {"event": "Recron Jaarcongres 2025", "type": "Partner"},
            {"event": "Glamping Show 2025", "type": "Exposant"},
            {"event": "Pleisureworld Summit 2026", "type": "Preferred Partner"},
        ],
        "top_producten": [
            {
                "id": "terras-madino-lounge",
                "name": "Madino Premium Lounge Set",
                "prijs": 3950,
                "image": "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=800&h=600&fit=crop",
                "reden": "Meest gekozen — perfecte balans voor mid-range chalets",
                "configuraties": 287,
            },
            {
                "id": "terras-madino-firepit",
                "name": "Madino Firepit Lounge Set",
                "prijs": 5450,
                "image": "https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=800&h=600&fit=crop",
                "reden": "Premium favoriet — verlengt het terras-seizoen tot november",
                "configuraties": 134,
            },
            {
                "id": "terras-madino-dining",
                "name": "Madino Dining Set (8p)",
                "prijs": 4750,
                "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop",
                "reden": "Top voor familie-chalets — 8 personen, robuust teak",
                "configuraties": 198,
            },
        ],
        "usps": [
            "Weerbestendig — ontworpen voor Nederlands klimaat",
            "Maatwerk per chalet of glamping-unit mogelijk",
            "Inclusief professionele installatie",
            "Winter-opslag service (optioneel)",
            "5 jaar garantie op frames",
            "Duurzame kussens met afneembare hoezen",
        ],
    },
}


# ==================== MONGODB INTEGRATION ====================

import os
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

_db = None
_seeded = False


def _get_db():
    global _db
    if _db is None:
        _db = AsyncIOMotorClient(os.environ['MONGO_URL'])[os.environ['DB_NAME']]
    return _db


async def _ensure_seeded():
    """Seed PARTNER_PROFILES dict into MongoDB if collection is empty (idempotent)."""
    global _seeded
    if _seeded:
        return
    db = _get_db()
    count = await db.partner_profiles.count_documents({})
    if count == 0:
        for pid, profile in PARTNER_PROFILES.items():
            doc = {**profile, "id": pid}
            await db.partner_profiles.insert_one(doc)
    else:
        # Make sure seeded-but-new profiles (e.g., Madino added later) are inserted
        existing_ids = set()
        async for d in db.partner_profiles.find({}, {"id": 1}):
            existing_ids.add(d.get("id"))
        for pid, profile in PARTNER_PROFILES.items():
            if pid not in existing_ids:
                doc = {**profile, "id": pid}
                await db.partner_profiles.insert_one(doc)
    _seeded = True


def _clean(doc: dict) -> dict:
    """Strip MongoDB _id from response."""
    if not doc:
        return doc
    d = dict(doc)
    d.pop("_id", None)
    return d


class PartnerProfileUpsert(BaseModel):
    id: Optional[str] = None
    name: str
    tagline: str = ""
    description: str = ""
    website: str = ""
    logo: str = ""
    hero_image: str = ""
    categorieen: List[str] = []
    pleisureworld_partner: bool = False
    pleisureworld_badge: str = ""
    pleisureworld_sinds: str = ""
    blog_url: str = ""
    blog_titel: str = ""
    podcast: Dict[str, Any] = {}
    trendwatcher_quote: Dict[str, Any] = {}
    stats: Dict[str, Any] = {}
    deelname: List[Dict[str, Any]] = []
    top_producten: List[Dict[str, Any]] = []
    usps: List[str] = []


# ==================== PUBLIC PARTNER ROUTES ====================

@partner_router.get("/profiles")
async def get_all_profiles():
    """Alle leveranciersprofielen (summary). Reads from MongoDB."""
    await _ensure_seeded()
    db = _get_db()
    out = []
    async for p in db.partner_profiles.find({}, {"_id": 0, "id": 1, "name": 1, "tagline": 1, "hero_image": 1, "categorieen": 1, "pleisureworld_partner": 1, "pleisureworld_badge": 1}):
        out.append(p)
    return out


@partner_router.get("/profiles/{partner_id}")
async def get_partner_profile(partner_id: str):
    """Gedetailleerd leveranciersprofiel — leest uit MongoDB met fallback naar seed-dict."""
    await _ensure_seeded()
    db = _get_db()
    profile = await db.partner_profiles.find_one({"id": partner_id}, {"_id": 0})
    if not profile:
        # Fallback to in-memory seed (in case DB ever cleared)
        profile = PARTNER_PROFILES.get(partner_id)
    if not profile:
        return {"error": "Partner niet gevonden"}
    return _clean(profile)


@partner_router.get("/profiles/{partner_id}/dynamic-top3")
async def get_dynamic_top3(partner_id: str):
    """Dynamische top 3 op basis van benchmark-data; fallback naar statische top 3."""
    from supabase_module import get_benchmark_data
    await _ensure_seeded()
    db = _get_db()
    profile = await db.partner_profiles.find_one({"id": partner_id}, {"_id": 0})
    if not profile:
        profile = PARTNER_PROFILES.get(partner_id)
    if not profile:
        return {"error": "Partner niet gevonden"}

    static_top3 = profile.get("top_producten", [])

    try:
        benchmark = await get_benchmark_data()
        if not benchmark:
            return {"source": "statisch", "top_producten": static_top3}

        supplier_name = profile["name"]
        product_counts = {}
        for entry in benchmark:
            for prod in entry.get("products_selected", []):
                if prod.get("supplier_name") == supplier_name or prod.get("supplier") == supplier_name:
                    name = prod.get("name", prod.get("product_name", ""))
                    if name:
                        product_counts[name] = product_counts.get(name, 0) + 1

        if len(product_counts) < 3:
            return {"source": "statisch", "top_producten": static_top3}

        sorted_products = sorted(product_counts.items(), key=lambda x: -x[1])
        dynamic_top3 = []
        for name, count in sorted_products[:3]:
            existing = next((p for p in static_top3 if p.get("name") == name or p.get("naam") == name), None)
            if existing:
                dynamic_top3.append({**existing, "configuraties": count, "bron": "dynamisch"})
            else:
                dynamic_top3.append({"name": name, "configuraties": count, "bron": "dynamisch"})
        return {"source": "dynamisch", "top_producten": dynamic_top3}
    except Exception:
        return {"source": "statisch", "top_producten": static_top3}


# ==================== ADMIN CRUD ====================

@partner_router.get("/admin/profiles")
async def admin_list_profiles():
    """Volledige profielen (alle velden) voor admin scherm."""
    await _ensure_seeded()
    db = _get_db()
    out = []
    async for p in db.partner_profiles.find({}, {"_id": 0}):
        out.append(p)
    return out


@partner_router.post("/admin/profiles")
async def admin_create_profile(payload: PartnerProfileUpsert):
    """Nieuwe partner aanmaken."""
    await _ensure_seeded()
    db = _get_db()
    data = payload.model_dump()
    if not data.get("id"):
        # Slug-ify name as id
        import re
        slug = re.sub(r"[^a-z0-9]+", "-", data["name"].lower()).strip("-")
        data["id"] = slug or f"partner-{int(__import__('time').time())}"
    # Ensure unique
    existing = await db.partner_profiles.find_one({"id": data["id"]}, {"_id": 0})
    if existing:
        return {"error": "Partner met deze id bestaat al", "id": data["id"]}
    await db.partner_profiles.insert_one(data)
    return {"success": True, "id": data["id"], "profile": _clean(data)}


@partner_router.put("/admin/profiles/{partner_id}")
async def admin_update_profile(partner_id: str, payload: PartnerProfileUpsert):
    """Partner bijwerken."""
    await _ensure_seeded()
    db = _get_db()
    data = payload.model_dump()
    data["id"] = partner_id
    res = await db.partner_profiles.update_one({"id": partner_id}, {"$set": data}, upsert=False)
    if res.matched_count == 0:
        return {"error": "Partner niet gevonden"}
    return {"success": True, "id": partner_id, "profile": data}


@partner_router.delete("/admin/profiles/{partner_id}")
async def admin_delete_profile(partner_id: str):
    """Partner verwijderen."""
    await _ensure_seeded()
    db = _get_db()
    res = await db.partner_profiles.delete_one({"id": partner_id})
    if res.deleted_count == 0:
        return {"error": "Partner niet gevonden"}
    return {"success": True, "id": partner_id}

