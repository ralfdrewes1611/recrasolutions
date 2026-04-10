"""
Locatie-intelligentie module voor RECRA Solutions.
Grondprijzen, regelgeving en toeristische potentie per provincie/regio.
"""
from fastapi import APIRouter

location_router = APIRouter(prefix="/location", tags=["locatie"])

# Indicatieve grondprijzen per provincie (per m2, recreatiegrond)
# Bron: Kadaster kwartaalberichten 2025, agrarische grondmarkt als basis
# Recreatiegrond is doorgaans 2-4x agrarische grondprijs afhankelijk van locatie
PROVINCE_DATA = {
    "groningen": {
        "name": "Groningen",
        "grondprijs_m2": {"min": 15, "max": 45, "indicatief": 28},
        "agrarisch_ha": 65000,
        "recreatie_potentie": "medium",
        "toerisme_score": 6.2,
        "regelgeving": {
            "bestemmingsplan": "Recreatieterreinen vallen onder bestemmingsplan buitengebied. Vergunning nodig voor nieuw recreatieterrein.",
            "max_bouwhoogte": "6 meter (recreatiewoningen), 4 meter (bijgebouwen)",
            "seizoen": "April - Oktober (toeristisch seizoen)",
            "bijzonderheden": "Waddengebied heeft extra beschermde status. UNESCO Werelderfgoed beperkingen."
        },
        "kenmerken": ["Waddengebied", "Rust & ruimte", "Betaalbare grond", "Groeiende toerisme"],
    },
    "friesland": {
        "name": "Friesland",
        "grondprijs_m2": {"min": 18, "max": 55, "indicatief": 35},
        "agrarisch_ha": 64100,
        "recreatie_potentie": "hoog",
        "toerisme_score": 7.8,
        "regelgeving": {
            "bestemmingsplan": "Sterke recreatietraditie. Friese Meren en Waddengebied hebben speciale zones.",
            "max_bouwhoogte": "7 meter (recreatiewoningen), 4.5 meter (bijgebouwen)",
            "seizoen": "Mei - September (hoogseizoen), Elfstedentocht winter",
            "bijzonderheden": "Watersport-infrastructuur vereist. Friese Meren zone: extra vergunningen voor waterrecreatie."
        },
        "kenmerken": ["Watersport", "Friese Meren", "Wadden", "Sterk merk", "Hoge bezettingsgraad"],
    },
    "drenthe": {
        "name": "Drenthe",
        "grondprijs_m2": {"min": 20, "max": 60, "indicatief": 38},
        "agrarisch_ha": 84100,
        "recreatie_potentie": "hoog",
        "toerisme_score": 7.5,
        "regelgeving": {
            "bestemmingsplan": "Veel bestaande vakantieparken. Uitbreiding mogelijk in aangewezen gebieden.",
            "max_bouwhoogte": "6 meter (recreatiewoningen), 4 meter (bijgebouwen)",
            "seizoen": "April - Oktober, groeiend jaarrond toerisme",
            "bijzonderheden": "Hondsrug UNESCO Global Geopark. Attractieparken (Wildlands, Drouwenerzand) trekken gezinnen."
        },
        "kenmerken": ["Natuur & bos", "Gezinsvriendelijk", "Bestaande parken", "Hondsrug Geopark"],
    },
    "overijssel": {
        "name": "Overijssel",
        "grondprijs_m2": {"min": 22, "max": 70, "indicatief": 42},
        "agrarisch_ha": 78000,
        "recreatie_potentie": "hoog",
        "toerisme_score": 7.6,
        "regelgeving": {
            "bestemmingsplan": "Sallandse Heuvelrug en Vechtdal hebben speciale recreatiezones.",
            "max_bouwhoogte": "7 meter (recreatiewoningen), 4.5 meter (bijgebouwen)",
            "seizoen": "April - Oktober, groeiend wintertoerisme",
            "bijzonderheden": "Giethoorn trekt internationaal toerisme. Vechtdal is opkomend recreatiegebied."
        },
        "kenmerken": ["Vechtdal", "Giethoorn", "Sallandse Heuvelrug", "Waterrecreatie"],
    },
    "flevoland": {
        "name": "Flevoland",
        "grondprijs_m2": {"min": 35, "max": 100, "indicatief": 65},
        "agrarisch_ha": 182100,
        "recreatie_potentie": "medium",
        "toerisme_score": 6.0,
        "regelgeving": {
            "bestemmingsplan": "Relatief nieuw land, duidelijke bestemmingsplannen. Kustgebied populair.",
            "max_bouwhoogte": "8 meter (recreatiewoningen), 5 meter (bijgebouwen)",
            "seizoen": "Mei - September",
            "bijzonderheden": "Markermeer en IJsselmeer kust. Bataviastad als trekker. Nieuwe natuur (Oostvaardersplassen)."
        },
        "kenmerken": ["Waterfront", "Moderne infrastructuur", "Duurste grond", "Nabij Randstad"],
    },
    "gelderland": {
        "name": "Gelderland",
        "grondprijs_m2": {"min": 25, "max": 85, "indicatief": 50},
        "agrarisch_ha": 82000,
        "recreatie_potentie": "zeer hoog",
        "toerisme_score": 8.5,
        "regelgeving": {
            "bestemmingsplan": "Veluwe is kerngebied voor verblijfsrecreatie. Strenge regels in Natura 2000.",
            "max_bouwhoogte": "6 meter (recreatiewoningen), 4 meter (bijgebouwen)",
            "seizoen": "Jaarrond (Veluwe), hoogseizoen mei-september",
            "bijzonderheden": "Veluwe is topbestemming NL. Stikstof-restricties bij Natura 2000. Betuwe: fruitteelt & rivierengebied."
        },
        "kenmerken": ["Veluwe", "Topbestemming NL", "Jaarrond bezetting", "Natura 2000", "Premium segment"],
    },
    "utrecht": {
        "name": "Utrecht",
        "grondprijs_m2": {"min": 30, "max": 95, "indicatief": 55},
        "agrarisch_ha": 89000,
        "recreatie_potentie": "medium",
        "toerisme_score": 7.0,
        "regelgeving": {
            "bestemmingsplan": "Beperkte ruimte voor nieuwe parken. Utrechtse Heuvelrug beschermd.",
            "max_bouwhoogte": "6 meter (recreatiewoningen), 4 meter (bijgebouwen)",
            "seizoen": "Jaarrond (stedelijk toerisme + natuur)",
            "bijzonderheden": "Utrechtse Heuvelrug Nationaal Park. Loosdrecht voor watersport. Beperkte beschikbaarheid."
        },
        "kenmerken": ["Centraal gelegen", "Utrechtse Heuvelrug", "Loosdrecht", "Beperkt aanbod"],
    },
    "noord-holland": {
        "name": "Noord-Holland",
        "grondprijs_m2": {"min": 35, "max": 120, "indicatief": 70},
        "agrarisch_ha": 96300,
        "recreatie_potentie": "hoog",
        "toerisme_score": 8.0,
        "regelgeving": {
            "bestemmingsplan": "Kustgebied streng gereguleerd. Duingebied extra beschermd.",
            "max_bouwhoogte": "6 meter (kustzone), 8 meter (binnenland)",
            "seizoen": "Mei - September (kust), jaarrond (Amsterdam regio)",
            "bijzonderheden": "Texel en kuststrook zijn premium locaties. Hoge grondprijzen. Amsterdam overshoot naar regio."
        },
        "kenmerken": ["Kust & strand", "Texel", "Amsterdam regio", "Premium grondprijzen", "Internationaal toerisme"],
    },
    "zuid-holland": {
        "name": "Zuid-Holland",
        "grondprijs_m2": {"min": 30, "max": 110, "indicatief": 65},
        "agrarisch_ha": 96900,
        "recreatie_potentie": "medium",
        "toerisme_score": 6.8,
        "regelgeving": {
            "bestemmingsplan": "Beperkte ruimte. Kustzone en Groene Hart hebben restricties.",
            "max_bouwhoogte": "6 meter (recreatiewoningen), 4 meter (bijgebouwen)",
            "seizoen": "Mei - September (kust), jaarrond (steden)",
            "bijzonderheden": "Kustlijn Katwijk-Hoek van Holland populair. Biesbosch voor natuurrecreatie. Dichtstbevolkte provincie."
        },
        "kenmerken": ["Kuststrook", "Biesbosch", "Nabij steden", "Beperkt aanbod"],
    },
    "zeeland": {
        "name": "Zeeland",
        "grondprijs_m2": {"min": 20, "max": 75, "indicatief": 45},
        "agrarisch_ha": 72000,
        "recreatie_potentie": "zeer hoog",
        "toerisme_score": 8.8,
        "regelgeving": {
            "bestemmingsplan": "Sterke recreatietraditie. Deltagebied biedt unieke kansen.",
            "max_bouwhoogte": "7 meter (recreatiewoningen), 5 meter (bijgebouwen)",
            "seizoen": "April - Oktober (sterk seizoensgebonden)",
            "bijzonderheden": "Hoogste recreatiedichtheid van NL. Deltawerken als trekker. Veel bestaande parken te renoveren."
        },
        "kenmerken": ["Strand & zee", "Hoogste recreatiedichtheid", "Seizoensgebonden", "Deltawerken", "Renovatiekansen"],
    },
    "noord-brabant": {
        "name": "Noord-Brabant",
        "grondprijs_m2": {"min": 28, "max": 80, "indicatief": 52},
        "agrarisch_ha": 108200,
        "recreatie_potentie": "hoog",
        "toerisme_score": 7.8,
        "regelgeving": {
            "bestemmingsplan": "Diverse bestemmingsplannen per gemeente. Efteling-regio heeft speciale status.",
            "max_bouwhoogte": "7 meter (recreatiewoningen), 4.5 meter (bijgebouwen)",
            "seizoen": "Jaarrond (attractieparken), mei-september (natuur)",
            "bijzonderheden": "Efteling, Beekse Bergen, Safari Park. Brabantse Wal voor natuur. Stikstof-issues bij veehouderij."
        },
        "kenmerken": ["Efteling regio", "Attractieparken", "Brabantse gezelligheid", "Jaarrond potentieel"],
    },
    "limburg": {
        "name": "Limburg",
        "grondprijs_m2": {"min": 22, "max": 75, "indicatief": 45},
        "agrarisch_ha": 68000,
        "recreatie_potentie": "hoog",
        "toerisme_score": 8.2,
        "regelgeving": {
            "bestemmingsplan": "Heuvelland heeft speciale recreatiezones. Grensoverschrijdende mogelijkheden.",
            "max_bouwhoogte": "7 meter (recreatiewoningen), 5 meter (bijgebouwen)",
            "seizoen": "Jaarrond (Heuvelland), mei-oktober (overig)",
            "bijzonderheden": "Heuvelland is uniek in NL. Drielandenpunt als trekker. Grensoverschrijdend toerisme (BE/DE). Culinaire traditie."
        },
        "kenmerken": ["Heuvelland", "Culinair", "Drielandenpunt", "Grenstoerisme", "Jaarrond attractief"],
    },
}


@location_router.get("/provinces")
async def get_provinces():
    """Alle provincies met indicatieve grondprijzen en recreatie-potentie."""
    result = []
    for pid, p in PROVINCE_DATA.items():
        result.append({
            "id": pid,
            "name": p["name"],
            "grondprijs_m2": p["grondprijs_m2"],
            "recreatie_potentie": p["recreatie_potentie"],
            "toerisme_score": p["toerisme_score"],
            "kenmerken": p["kenmerken"],
        })
    return sorted(result, key=lambda x: x["toerisme_score"], reverse=True)


@location_router.get("/provinces/{province_id}")
async def get_province_detail(province_id: str):
    """Gedetailleerde informatie per provincie."""
    province = PROVINCE_DATA.get(province_id)
    if not province:
        return {"error": "Provincie niet gevonden"}
    return {"id": province_id, **province}


@location_router.get("/grondprijs-vergelijking")
async def get_grondprijs_comparison():
    """Vergelijk grondprijzen van alle provincies."""
    result = []
    for pid, p in PROVINCE_DATA.items():
        result.append({
            "id": pid,
            "name": p["name"],
            "indicatief_m2": p["grondprijs_m2"]["indicatief"],
            "min_m2": p["grondprijs_m2"]["min"],
            "max_m2": p["grondprijs_m2"]["max"],
            "recreatie_potentie": p["recreatie_potentie"],
            "toerisme_score": p["toerisme_score"],
        })
    return sorted(result, key=lambda x: x["indicatief_m2"])


@location_router.get("/investering-calculator")
async def calculate_location_investment(
    province_id: str = "gelderland",
    oppervlakte_m2: int = 5000,
    units: int = 10,
):
    """Bereken indicatieve grondkosten voor een locatie."""
    province = PROVINCE_DATA.get(province_id)
    if not province:
        return {"error": "Provincie niet gevonden"}

    gp = province["grondprijs_m2"]
    grondkosten_min = gp["min"] * oppervlakte_m2
    grondkosten_max = gp["max"] * oppervlakte_m2
    grondkosten_indicatief = gp["indicatief"] * oppervlakte_m2

    return {
        "provincie": province["name"],
        "oppervlakte_m2": oppervlakte_m2,
        "units": units,
        "grondkosten": {
            "min": grondkosten_min,
            "indicatief": grondkosten_indicatief,
            "max": grondkosten_max,
        },
        "kosten_per_unit": {
            "min": round(grondkosten_min / units),
            "indicatief": round(grondkosten_indicatief / units),
            "max": round(grondkosten_max / units),
        },
        "m2_per_unit": round(oppervlakte_m2 / units),
        "recreatie_potentie": province["recreatie_potentie"],
        "toerisme_score": province["toerisme_score"],
        "regelgeving": province["regelgeving"],
        "kenmerken": province["kenmerken"],
    }
