"""
CRM Engine — Lead management, follow-up mails, scenario opslag.
Leads worden warm na subsidie check of offerte-aanvraag.
"""
import os
import json
import uuid
import logging
from datetime import datetime, timezone
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from emergentintegrations.llm.chat import LlmChat, UserMessage

logger = logging.getLogger("crm")
crm_router = APIRouter(prefix="/crm", tags=["CRM & Leads"])


class LeadCreate(BaseModel):
    naam: str
    email: str
    telefoon: Optional[str] = ""
    bedrijf: Optional[str] = ""
    flow_type: str = "recreatie"
    bron: str = "subsidie_check"
    project_beschrijving: Optional[str] = ""
    subsidie_score: Optional[float] = None
    subsidie_kans: Optional[str] = None
    subsidie_range: Optional[str] = None
    investering: Optional[str] = None
    notities: Optional[str] = ""


class ScenarioRequest(BaseModel):
    flow_type: str
    project_beschrijving: str
    investering_range: str
    doelgroep: Optional[str] = "families"
    extra_wensen: Optional[str] = ""


# In-memory lead store (backed by Supabase when available)
_leads_store = []


def _try_supabase_save(table: str, data: dict):
    """Probeer op te slaan in Supabase, fail silently."""
    try:
        from supabase_module import get_supabase
        sb = get_supabase()
        sb.table(table).insert(data).execute()
        return True
    except Exception as e:
        logger.warning(f"Supabase save failed ({table}): {e}")
        return False


@crm_router.post("/leads")
async def create_lead(lead: LeadCreate):
    """Nieuwe lead aanmaken (warm na subsidie check / offerte)."""
    lead_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    lead_data = {
        "id": lead_id,
        "naam": lead.naam,
        "email": lead.email,
        "telefoon": lead.telefoon,
        "bedrijf": lead.bedrijf,
        "flow_type": lead.flow_type,
        "bron": lead.bron,
        "project_beschrijving": lead.project_beschrijving,
        "subsidie_score": lead.subsidie_score,
        "subsidie_kans": lead.subsidie_kans,
        "subsidie_range": lead.subsidie_range,
        "investering": lead.investering,
        "notities": lead.notities,
        "status": "nieuw",
        "lead_score": _calculate_lead_score(lead),
        "created_at": now,
        "follow_up_sent": False,
    }

    _leads_store.append(lead_data)

    # Save to Supabase
    _try_supabase_save("configurator_sessions", {
        "session_id": lead_id,
        "flow_type": lead.flow_type,
        "status": "completed",
        "lead_score": lead_data["lead_score"],
        "budget_range": lead.investering,
        "contact_email": lead.email,
        "contact_name": lead.naam,
        "contact_phone": lead.telefoon,
        "company_name": lead.bedrijf,
        "notes": lead.project_beschrijving,
        "phase": "concreet",
    })

    return {
        "id": lead_id,
        "lead_score": lead_data["lead_score"],
        "status": "nieuw",
        "message": "Lead succesvol aangemaakt",
    }


def _calculate_lead_score(lead: LeadCreate) -> int:
    """Bereken lead score (0-100) op basis van completeness + subsidie score."""
    score = 0
    if lead.email:
        score += 20
    if lead.telefoon:
        score += 15
    if lead.bedrijf:
        score += 10
    if lead.project_beschrijving:
        score += 10
    if lead.subsidie_score is not None:
        score += 15
    if lead.subsidie_kans == "hoog":
        score += 20
    elif lead.subsidie_kans == "middel":
        score += 10
    if lead.investering in ["> €100K", "€25K - €100K"]:
        score += 10
    return min(score, 100)


@crm_router.get("/leads")
async def get_leads(status: str = None):
    """Alle leads ophalen, optioneel gefilterd op status."""
    leads = _leads_store
    if status:
        leads = [l for l in leads if l["status"] == status]
    return sorted(leads, key=lambda x: x["created_at"], reverse=True)


@crm_router.get("/leads/{lead_id}")
async def get_lead(lead_id: str):
    """Specifieke lead ophalen."""
    lead = next((l for l in _leads_store if l["id"] == lead_id), None)
    if not lead:
        return {"error": "Lead niet gevonden"}
    return lead


@crm_router.post("/leads/{lead_id}/status")
async def update_lead_status(lead_id: str, status: str):
    """Lead status bijwerken."""
    lead = next((l for l in _leads_store if l["id"] == lead_id), None)
    if not lead:
        return {"error": "Lead niet gevonden"}
    lead["status"] = status
    return lead


# ===================== FOLLOW-UP MAIL =====================

@crm_router.post("/leads/{lead_id}/follow-up")
async def generate_follow_up(lead_id: str):
    """Genereer gepersonaliseerde follow-up mail voor een lead."""
    lead = next((l for l in _leads_store if l["id"] == lead_id), None)
    if not lead:
        return {"error": "Lead niet gevonden"}

    email_html = _generate_follow_up_html(lead)
    lead["follow_up_sent"] = True
    lead["follow_up_at"] = datetime.now(timezone.utc).isoformat()

    return {
        "email_html": email_html,
        "subject": f"Uw subsidie-check resultaat — {lead['subsidie_kans'] or 'analyse'} kans",
        "to": lead["email"],
        "naam": lead["naam"],
    }


@crm_router.post("/follow-up/generate")
async def generate_follow_up_from_data(data: dict):
    """Genereer follow-up mail direct vanuit subsidie resultaten (zonder lead opslaan)."""
    email_html = _generate_follow_up_html(data)
    return {
        "email_html": email_html,
        "subject": f"Uw subsidie-check resultaat — {data.get('subsidie_kans', 'analyse')} kans",
    }


def _generate_follow_up_html(lead_data: dict) -> str:
    """Genereer professionele follow-up email HTML."""
    naam = lead_data.get("naam", "")
    kans = lead_data.get("subsidie_kans", "middel")
    score = lead_data.get("subsidie_score", 0)
    subsidie_range = lead_data.get("subsidie_range", "€5.000 - €20.000")
    project = lead_data.get("project_beschrijving", "uw project")
    investering = lead_data.get("investering", "")

    kans_color = {"laag": "#ef4444", "middel": "#f59e0b", "hoog": "#10b981"}.get(kans, "#f59e0b")

    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family:'Segoe UI',Arial,sans-serif;margin:0;padding:0;background:#f5f5f0;">
<div style="max-width:600px;margin:0 auto;background:white;">

  <div style="background:#244628;padding:32px 24px;text-align:center;">
    <div style="color:white;font-size:22px;font-weight:bold;letter-spacing:2px;">RECRA</div>
    <div style="color:#70C26C;font-size:11px;margin-top:2px;">SOLUTIONS</div>
  </div>

  <div style="padding:32px 24px;">
    <p style="color:#333;font-size:15px;line-height:1.6;">Beste {naam},</p>
    <p style="color:#555;font-size:14px;line-height:1.7;">
      Bedankt voor het invullen van de Financiering & Subsidie Check via ons platform.
      Hieronder vindt u een samenvatting van de analyse.
    </p>

    <div style="background:#fafaf7;border:1px solid #e5e2d9;border-radius:12px;padding:20px;margin:24px 0;">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
        <span style="background:{kans_color};color:white;padding:4px 16px;border-radius:20px;font-size:12px;font-weight:bold;text-transform:uppercase;">
          {kans} kans
        </span>
        <span style="font-size:20px;font-weight:bold;color:#244628;">{score}/10</span>
      </div>

      <table style="width:100%;font-size:13px;color:#555;">
        <tr style="border-bottom:1px solid #e5e2d9;">
          <td style="padding:8px 0;">Verwachte subsidie</td>
          <td style="padding:8px 0;text-align:right;font-weight:bold;color:#244628;">{subsidie_range}</td>
        </tr>
        <tr style="border-bottom:1px solid #e5e2d9;">
          <td style="padding:8px 0;">Investering</td>
          <td style="padding:8px 0;text-align:right;">{investering}</td>
        </tr>
        <tr>
          <td style="padding:8px 0;">Project</td>
          <td style="padding:8px 0;text-align:right;">{project[:80]}</td>
        </tr>
      </table>
    </div>

    <p style="color:#555;font-size:14px;line-height:1.7;">
      Op basis van uw profiel zien wij goede mogelijkheden voor subsidie en/of financiering.
      Wij helpen u graag verder met een persoonlijk adviesgesprek.
    </p>

    <div style="text-align:center;margin:28px 0;">
      <a href="mailto:info@recrasolutions.com?subject=Subsidie%20adviesgesprek%20-%20{naam}"
         style="display:inline-block;background:#70C26C;color:white;padding:12px 32px;border-radius:8px;text-decoration:none;font-size:14px;font-weight:bold;">
        Plan een adviesgesprek
      </a>
    </div>

    <p style="color:#999;font-size:12px;line-height:1.6;">
      Dit is een automatisch gegenereerde e-mail op basis van uw subsidie-check.
      De genoemde bedragen zijn indicatief en onder voorbehoud.
    </p>
  </div>

  <div style="background:#244628;padding:20px 24px;text-align:center;">
    <div style="color:white;font-size:11px;">RECRA Solutions — info@recrasolutions.com — +31 634200253</div>
    <div style="color:white;font-size:10px;opacity:0.5;margin-top:4px;">Powered by Pleisureworld x RECRA Solutions</div>
  </div>

</div>
</body>
</html>"""


# ===================== 3 SCENARIO'S GENERATOR =====================

@crm_router.post("/scenarios/generate")
async def generate_scenarios(req: ScenarioRequest):
    """Genereer 3 offerte-scenario's: Budget, Standaard, Premium."""
    llm_key = os.environ.get("EMERGENT_LLM_KEY")
    if not llm_key:
        return _fallback_scenarios(req)

    prompt = f"""Genereer 3 offerte-scenario's voor een recreatieproject.

Context:
- Flow type: {req.flow_type}
- Project: {req.project_beschrijving}
- Budget range: {req.investering_range}
- Doelgroep: {req.doelgroep}
- Extra wensen: {req.extra_wensen or 'geen'}

Genereer precies 3 scenario's in JSON array format:

[
  {{
    "naam": "Budget",
    "beschrijving": "Korte beschrijving van het budget scenario",
    "investering": 25000,
    "lease_maand": 500,
    "terugverdientijd_maanden": 24,
    "producten": ["Product 1", "Product 2", "Product 3"],
    "voordelen": ["Voordeel 1", "Voordeel 2"],
    "nadelen": ["Nadeel 1"],
    "geschikt_voor": "Starters en kleine parken"
  }},
  {{
    "naam": "Standaard",
    "beschrijving": "Korte beschrijving",
    "investering": 50000,
    "lease_maand": 950,
    "terugverdientijd_maanden": 18,
    "producten": ["Product 1", "Product 2", "Product 3", "Product 4"],
    "voordelen": ["Voordeel 1", "Voordeel 2", "Voordeel 3"],
    "nadelen": ["Nadeel 1"],
    "geschikt_voor": "Middelgrote parken"
  }},
  {{
    "naam": "Premium",
    "beschrijving": "Korte beschrijving",
    "investering": 100000,
    "lease_maand": 1800,
    "terugverdientijd_maanden": 14,
    "producten": ["Product 1", "Product 2", "Product 3", "Product 4", "Product 5"],
    "voordelen": ["Voordeel 1", "Voordeel 2", "Voordeel 3", "Voordeel 4"],
    "nadelen": [],
    "geschikt_voor": "Grote parken en resorts"
  }}
]

Maak de scenario's realistisch en relevant voor de {req.flow_type} sector.
Gebruik Nederlandse productnamen en bedragen.
Geef alleen valide JSON terug, geen markdown."""

    try:
        chat = LlmChat(
            api_key=llm_key,
            session_id=f"scenario-{uuid.uuid4()}",
            system_message="Je bent een recreatie-expert die offerte-scenario's genereert voor parkeigenaren."
        ).with_model("openai", "gpt-5.2")

        response = await chat.send_message(UserMessage(text=prompt))
        text = response.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        scenarios = json.loads(text)
        return {"scenarios": scenarios, "source": "ai"}

    except Exception as e:
        logger.error(f"Scenario generatie fout: {e}")
        return _fallback_scenarios(req)


def _fallback_scenarios(req: ScenarioRequest) -> dict:
    """Statische fallback scenario's als AI niet beschikbaar is."""
    base_inv = 25000
    if "€25K" in req.investering_range or "€100K" in req.investering_range:
        base_inv = 50000
    elif "> €100K" in req.investering_range:
        base_inv = 100000

    scenarios = [
        {
            "naam": "Budget",
            "beschrijving": "Basisuitrusting voor een kostenefficiënte start. Essentiële producten zonder luxe extras.",
            "investering": int(base_inv * 0.5),
            "lease_maand": int(base_inv * 0.5 / 60),
            "terugverdientijd_maanden": 24,
            "producten": ["Sanitair unit basis", "Slagboom systeem", "WiFi basis"],
            "voordelen": ["Laagste investering", "Snelle installatie", "Basis functionaliteit"],
            "nadelen": ["Beperkte capaciteit", "Geen premium features"],
            "geschikt_voor": "Starters en kleine parken",
        },
        {
            "naam": "Standaard",
            "beschrijving": "Compleet pakket met goede balans tussen prijs en kwaliteit. Meest gekozen door parkeigenaren.",
            "investering": base_inv,
            "lease_maand": int(base_inv / 60),
            "terugverdientijd_maanden": 18,
            "producten": ["Sanitair unit compleet", "Slagboom + camera", "WiFi premium", "Verlichting LED"],
            "voordelen": ["Goede prijs-kwaliteit", "Uitbreidbaar", "Meest populair", "SLA onderhoud"],
            "nadelen": ["Middelmatig budget nodig"],
            "geschikt_voor": "Middelgrote parken",
        },
        {
            "naam": "Premium",
            "beschrijving": "All-inclusive pakket met alle premium features. Maximale gastbeleving en omzet per standplaats.",
            "investering": int(base_inv * 2),
            "lease_maand": int(base_inv * 2 / 60),
            "terugverdientijd_maanden": 14,
            "producten": ["Sanitair unit luxe", "Smart slagboom + ANPR camera", "WiFi enterprise", "LED verlichting", "Betaalsysteem contactloos", "Wellness hottub"],
            "voordelen": ["Maximale gastbeleving", "Hoogste omzet/standplaats", "Compleet pakket", "Premium uitstraling"],
            "nadelen": [],
            "geschikt_voor": "Grote parken en resorts",
        },
    ]
    return {"scenarios": scenarios, "source": "statisch"}
