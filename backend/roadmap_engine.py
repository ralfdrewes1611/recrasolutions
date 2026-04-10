"""
Roadmap Engine — "Idee naar Realisatie" fasen-overzicht post-configuratie.
Toont stapsgewijze fasen: Ontwerp → Vergunning → Bouw → Exploitatie.
"""
from fastapi import APIRouter
from typing import Optional

roadmap_router = APIRouter(prefix="/roadmap", tags=["Roadmap"])

ROADMAP_PHASES = {
    "recreatie": [
        {
            "id": "ontwerp",
            "fase": 1,
            "titel": "Ontwerp & Planvorming",
            "duur": "4-8 weken",
            "beschrijving": "Definitief terreinontwerp op basis van uw configuratie. Plattegrond, productplaatsing, infrastructuurplan en leveranciersafstemming.",
            "acties": [
                "Terreinontwerp finaliseren met landschapsarchitect",
                "Leveranciers offertes opvragen en vergelijken",
                "Infrastructuurplan (elektra, water, riolering) laten opstellen",
                "Financieringsaanvraag voorbereiden",
            ],
            "deliverables": [
                "Definitief terreinontwerp (2D + 3D)",
                "Offerteboek alle leveranciers",
                "Infrastructuurtekening",
                "Business case document",
            ],
            "kosten_indicatie": "€ 2.500 - € 8.000",
            "betrokken_partijen": ["Landschapsarchitect", "RECRA Solutions", "Leveranciers"],
            "status": "todo",
        },
        {
            "id": "vergunning",
            "fase": 2,
            "titel": "Vergunning & Regelgeving",
            "duur": "8-16 weken",
            "beschrijving": "Bestemmingsplantoets, omgevingsvergunning en eventuele milieueffectrapportage. Wij ondersteunen bij de aanvraag.",
            "acties": [
                "Bestemmingsplan toetsen bij gemeente",
                "Omgevingsvergunning aanvragen",
                "Milieueffectrapportage (indien nodig)",
                "Brandveiligheidsadvies ophalen",
                "Waterschap vergunning controleren",
            ],
            "deliverables": [
                "Omgevingsvergunning",
                "Bestemmingsplantoets rapport",
                "Brandveiligheidsrapport",
                "Eventuele ontheffingen",
            ],
            "kosten_indicatie": "€ 1.500 - € 5.000 (leges)",
            "betrokken_partijen": ["Gemeente", "Adviseur ruimtelijke ordening", "Brandweer"],
            "status": "todo",
        },
        {
            "id": "bouw",
            "fase": 3,
            "titel": "Bouw & Installatie",
            "duur": "8-20 weken",
            "beschrijving": "Grondwerk, infrastructuur aanleggen, producten installeren en terrein inrichten. Projectmanagement door RECRA.",
            "acties": [
                "Grondwerk en fundering",
                "Elektra, water en riolering aanleggen",
                "Sanitair units plaatsen en aansluiten",
                "Camera's, WiFi en slagbomen installeren",
                "Verlichting en betaalsystemen monteren",
                "Terreinverharding en groenvoorziening",
            ],
            "deliverables": [
                "Oplevering terrein",
                "Installatierapporten per leverancier",
                "Testrapport alle systemen",
                "Handleidingen en SLA documenten",
            ],
            "kosten_indicatie": "Conform offerte",
            "betrokken_partijen": ["Aannemer", "Leveranciers", "RECRA Projectmanagement"],
            "status": "todo",
        },
        {
            "id": "exploitatie",
            "fase": 4,
            "titel": "Exploitatie & Optimalisatie",
            "duur": "Doorlopend",
            "beschrijving": "Park operationeel. Monitoring via dashboard, onderhoud via SLA, en continue optimalisatie op basis van data.",
            "acties": [
                "Systemen in bedrijf stellen",
                "Medewerkers trainen",
                "Marketing en boekingssysteem activeren",
                "Maandelijkse performance review via dashboard",
                "Jaarlijks onderhoud volgens SLA",
            ],
            "deliverables": [
                "Operationeel park",
                "Training documentatie",
                "Maandelijkse KPI rapportages",
                "SLA onderhoudscontract actief",
            ],
            "kosten_indicatie": "Lease + SLA conform offerte",
            "betrokken_partijen": ["Parkeigenaar", "RECRA Support", "Leveranciers (SLA)"],
            "status": "todo",
        },
    ],
    "chalet": [
        {
            "id": "ontwerp",
            "fase": 1,
            "titel": "Ontwerp & Modelkeuze",
            "duur": "2-6 weken",
            "beschrijving": "Definitieve modelkeuze, stijlbepaling en samenstelling. 3D visualisatie en offerte bevestiging.",
            "acties": [
                "Model en stijl definitief kiezen",
                "Upgrades en samenstelling bevestigen",
                "3D Matterport tour (indien beschikbaar)",
                "Leverancier offerte bevestigen",
                "Fundament en plaatsing plannen",
            ],
            "deliverables": [
                "Definitieve configuratie met specificaties",
                "3D visualisatie / Matterport",
                "Getekende offerte leverancier",
                "Fundament tekening",
            ],
            "kosten_indicatie": "€ 500 - € 2.000",
            "betrokken_partijen": ["Leverancier", "RECRA Solutions", "Fundament specialist"],
            "status": "todo",
        },
        {
            "id": "vergunning",
            "fase": 2,
            "titel": "Vergunning & Locatie",
            "duur": "4-12 weken",
            "beschrijving": "Plaatsingsvergunning op recreatieterrein, bestemmingsplancheck en eventuele bouwtechnische keuring.",
            "acties": [
                "Bestemmingsplan recreatieterrein controleren",
                "Plaatsingsvergunning aanvragen",
                "Bouwtechnische keuring (bij permanente plaatsing)",
                "Aansluiting nutsvoorzieningen regelen",
            ],
            "deliverables": [
                "Plaatsingsvergunning",
                "Nutsaansluitingen goedgekeurd",
                "Situatietekening op terrein",
            ],
            "kosten_indicatie": "€ 500 - € 2.500 (leges)",
            "betrokken_partijen": ["Gemeente", "Recreatiepark beheer", "Nutsbedrijven"],
            "status": "todo",
        },
        {
            "id": "productie",
            "fase": 3,
            "titel": "Productie & Transport",
            "duur": "5-12 weken",
            "beschrijving": "Productie in de fabriek, kwaliteitscontrole en transport naar de locatie.",
            "acties": [
                "Productie starten bij leverancier",
                "Tussentijdse kwaliteitscontrole",
                "Transport plannen (eigen transport leverancier)",
                "Fundament voorbereiden op locatie",
                "Wellness upgrades bestellen (Ticra Outdoor)",
            ],
            "deliverables": [
                "Productie gereed melding",
                "Kwaliteitsrapport",
                "Transportplanning",
                "Fundament gereed",
            ],
            "kosten_indicatie": "Conform offerte (incl. transport)",
            "betrokken_partijen": ["Leverancier fabriek", "Transportbedrijf", "Locatie beheerder"],
            "status": "todo",
        },
        {
            "id": "plaatsing",
            "fase": 4,
            "titel": "Plaatsing & Oplevering",
            "duur": "1-3 weken",
            "beschrijving": "Plaatsing op locatie, aansluiting nutsvoorzieningen, wellness installatie en eindoplevering.",
            "acties": [
                "Chalet/glamping plaatsen op fundament",
                "Aansluiting elektra, water, riolering",
                "Wellness producten installeren (hottub, sauna)",
                "Eindcontrole en oplevering",
                "Sleuteloverdracht",
            ],
            "deliverables": [
                "Opgeleverd chalet/glamping",
                "Opleverrapport",
                "Garantiebewijzen",
                "SLA onderhoudscontract",
            ],
            "kosten_indicatie": "Incl. in leveranciersprijs",
            "betrokken_partijen": ["Leverancier montageteam", "Installateur", "Parkeigenaar"],
            "status": "todo",
        },
    ],
    "fec": [
        {
            "id": "concept",
            "fase": 1,
            "titel": "Concept & Business Case",
            "duur": "4-8 weken",
            "beschrijving": "Definitief FEC concept uitwerken. Zonering, attractiemix en financieel model valideren.",
            "acties": [
                "FEC concept presentatie voorbereiden",
                "Business case valideren met accountant",
                "Leveranciers shortlist en offertes",
                "Architect inschakelen voor layout",
                "Financiering aanvragen",
            ],
            "deliverables": [
                "FEC Concept Document",
                "Gevalideerde business case",
                "Offertes leveranciers",
                "Architecttekening",
            ],
            "kosten_indicatie": "€ 5.000 - € 15.000",
            "betrokken_partijen": ["Architect", "Accountant", "RECRA Solutions", "Leveranciers"],
            "status": "todo",
        },
        {
            "id": "vergunning",
            "fase": 2,
            "titel": "Vergunning & Brandveiligheid",
            "duur": "8-20 weken",
            "beschrijving": "Omgevingsvergunning, gebruiksvergunning en brandveiligheidskeuring. FEC's hebben extra eisen.",
            "acties": [
                "Omgevingsvergunning aanvragen",
                "Gebruiksvergunning (publieksfunctie)",
                "Brandveiligheidsadvies en keuring",
                "Geluid- en milieuonderzoek",
                "Toegankelijkheidstoets",
            ],
            "deliverables": [
                "Omgevingsvergunning",
                "Gebruiksvergunning",
                "Brandveiligheidsrapport",
                "Milieurapportage",
            ],
            "kosten_indicatie": "€ 3.000 - € 12.000 (leges + advies)",
            "betrokken_partijen": ["Gemeente", "Brandweer", "Milieu-adviseur", "Architect"],
            "status": "todo",
        },
        {
            "id": "bouw",
            "fase": 3,
            "titel": "Bouw & Installatie",
            "duur": "12-24 weken",
            "beschrijving": "Verbouwing, attracties installeren, horeca inrichten en systemen koppelen.",
            "acties": [
                "Verbouwing / afbouw ruimte",
                "Vloerwerk en wandafwerking",
                "Attracties installeren en testen",
                "Horeca inrichting en keukeninstallatie",
                "Ticketing en kassa systemen installeren",
                "Veiligheidstest en TUV keuring",
            ],
            "deliverables": [
                "Opgeleverde FEC ruimte",
                "TUV / veiligheidskeuring attracties",
                "Installatie rapporten",
                "Horecavergunning",
            ],
            "kosten_indicatie": "Conform offerte + verbouwkosten",
            "betrokken_partijen": ["Aannemer", "Leveranciers", "TUV inspecteur", "Horecainstallateur"],
            "status": "todo",
        },
        {
            "id": "exploitatie",
            "fase": 4,
            "titel": "Opening & Groei",
            "duur": "Doorlopend",
            "beschrijving": "Grand opening, marketing activeren en sturen op bezettingsgraad en omzet per m².",
            "acties": [
                "Soft opening voor testpubliek",
                "Grand opening event organiseren",
                "Online marketing en social media",
                "Medewerkers trainen",
                "Maandelijkse revenue review via dashboard",
                "Seizoensgebonden aanpassingen",
            ],
            "deliverables": [
                "Operationele FEC",
                "Marketing plan en materialen",
                "Training documentatie",
                "Maandelijkse P&L rapportage",
            ],
            "kosten_indicatie": "Operationele kosten + marketing",
            "betrokken_partijen": ["FEC eigenaar", "Marketing bureau", "RECRA Support"],
            "status": "todo",
        },
    ],
}


@roadmap_router.get("/phases/{flow_type}")
async def get_roadmap_phases(flow_type: str):
    """Haal roadmap fasen op voor een specifiek flow type."""
    phases = ROADMAP_PHASES.get(flow_type)
    if not phases:
        return {"error": "Flow type niet gevonden", "available": list(ROADMAP_PHASES.keys())}
    return {
        "flow_type": flow_type,
        "total_phases": len(phases),
        "estimated_total_duration": _estimate_total(phases),
        "phases": phases,
    }


def _estimate_total(phases):
    """Bereken geschatte totale doorlooptijd."""
    totals = {"recreatie": "6-12 maanden", "chalet": "3-8 maanden", "fec": "8-16 maanden"}
    return totals.get(phases[0]["id"], "nvt") if phases else "nvt"


@roadmap_router.get("/summary")
async def get_roadmap_summary():
    """Overzicht van alle beschikbare roadmaps."""
    return [
        {
            "flow_type": ft,
            "total_phases": len(phases),
            "phase_names": [p["titel"] for p in phases],
        }
        for ft, phases in ROADMAP_PHASES.items()
    ]
