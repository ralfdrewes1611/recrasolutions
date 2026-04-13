"""
Financiering & Subsidie Check Engine
Rules-based scoring + AI-powered analyse en document generator.
"""
import os
import json
import logging
import uuid
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from emergentintegrations.llm.chat import LlmChat, UserMessage

logger = logging.getLogger("subsidy")
subsidy_router = APIRouter(prefix="/subsidy", tags=["Subsidie"])


class SubsidyIntake(BaseModel):
    sector: str
    rechtsvorm: str
    projectomschrijving: str
    doel: str
    investering: str
    eigen_investering: str
    gebruikers: str
    samenwerking: str
    duurzaamheid: str


class SubsidyScore(BaseModel):
    score: float
    kans: str
    breakdown: dict
    subsidie_range: str
    advies: str


def calculate_score(intake: SubsidyIntake) -> dict:
    """Rules-based scoring (0-10)."""
    breakdown = {}

    # Hard filter
    if intake.investering == "< €10K":
        return {
            "score": 1.0,
            "kans": "laag",
            "breakdown": {"hard_filter": "Investering < €10K — lage kans op subsidie"},
            "subsidie_range": "€0 - €5.000",
            "advies": "lease",
            "filtered": True,
        }

    # Sector fit (0-2)
    sector_scores = {"recreatie": 2, "zorg": 2, "kinderopvang": 2, "overig": 1}
    sector_score = sector_scores.get(intake.sector.lower(), 1)
    breakdown["sector_fit"] = {"score": sector_score, "max": 2, "label": "Sector match"}

    # Projecttype (0-2)
    doel_scores = {
        "digitaliseren": 2, "zorg / welzijn verbeteren": 2,
        "beleving verbeteren": 1.5, "kosten besparen": 1,
    }
    doel_score = doel_scores.get(intake.doel.lower(), 1)
    breakdown["projecttype"] = {"score": doel_score, "max": 2, "label": "Projectdoel"}

    # Investering (0-2)
    inv_scores = {"€10K - €25K": 1, "€25K - €100K": 2, "> €100K": 2}
    inv_score = inv_scores.get(intake.investering, 0)
    breakdown["investering"] = {"score": inv_score, "max": 2, "label": "Investeringsniveau"}

    # Impact (0-2)
    impact_scores = {"< 100": 0, "100 - 1.000": 1, "1.000 - 10.000": 2, "> 10.000": 2}
    impact_score = impact_scores.get(intake.gebruikers, 0)
    breakdown["impact"] = {"score": impact_score, "max": 2, "label": "Bereik / impact"}

    # Samenwerking (0-1)
    collab_score = 1 if intake.samenwerking.lower() == "ja" else 0
    breakdown["samenwerking"] = {"score": collab_score, "max": 1, "label": "Samenwerking"}

    # Duurzaamheid (0-1)
    sustain_score = 1 if intake.duurzaamheid.lower() == "ja" else 0
    breakdown["duurzaamheid"] = {"score": sustain_score, "max": 1, "label": "Duurzaamheid"}

    total = sector_score + doel_score + inv_score + impact_score + collab_score + sustain_score

    if total <= 4:
        kans = "laag"
        subsidie_range = "€0 - €5.000"
        advies = "lease"
    elif total <= 7:
        kans = "middel"
        subsidie_range = "€5.000 - €20.000"
        advies = "hybride"
    else:
        kans = "hoog"
        subsidie_range = "€10.000 - €50.000"
        advies = "subsidie + financiering"

    return {
        "score": round(total, 1),
        "kans": kans,
        "breakdown": breakdown,
        "subsidie_range": subsidie_range,
        "advies": advies,
        "filtered": False,
    }


@subsidy_router.post("/check")
async def subsidy_check(intake: SubsidyIntake):
    """Stap 1: Rules-based score berekening."""
    result = calculate_score(intake)
    return result


@subsidy_router.post("/ai-analyse")
async def ai_analyse(intake: SubsidyIntake):
    """Stap 2: AI-powered subsidie analyse met GPT-5.2."""
    rules_result = calculate_score(intake)

    llm_key = os.environ.get("EMERGENT_LLM_KEY")
    if not llm_key:
        return {**rules_result, "ai_analyse": None, "ai_error": "AI niet geconfigureerd"}

    prompt = f"""Analyseer onderstaande invoer en geef een subsidie-inschatting.

Input:
- sector: {intake.sector}
- rechtsvorm: {intake.rechtsvorm}
- project: {intake.projectomschrijving}
- doel: {intake.doel}
- investering: {intake.investering}
- impact: {intake.gebruikers}
- samenwerking: {intake.samenwerking}
- duurzaamheid: {intake.duurzaamheid}
- score: {rules_result['score']}/10

Geef output in JSON:

{{
  "kans": "laag/middel/hoog",
  "score": "X/10",
  "toelichting": "korte zakelijke uitleg waarom",
  "subsidie_range": "€X - €X",
  "advies": "beste route: koop / lease / hybride",
  "verbeterpunten": [
    "punt 1",
    "punt 2"
  ],
  "regelingen": [
    "naam van mogelijke regeling 1",
    "naam van mogelijke regeling 2"
  ]
}}

Schrijf zakelijk, concreet en in begrijpelijke taal.
Geen garanties geven. Geef alleen valide JSON terug, geen markdown formatting."""

    try:
        chat = LlmChat(
            api_key=llm_key,
            session_id=f"subsidy-analyse-{uuid.uuid4()}",
            system_message="Je bent een subsidie-expert die projecten analyseert voor Nederlandse subsidies en financieringsregelingen."
        ).with_model("openai", "gpt-5.2")
        
        response = await chat.send_message(UserMessage(text=prompt))

        text = response.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        ai_data = json.loads(text)
        return {**rules_result, "ai_analyse": ai_data}

    except json.JSONDecodeError:
        return {**rules_result, "ai_analyse": {"raw": text if 'text' in dir() else "Parse error"}}
    except Exception as e:
        logger.error(f"AI analyse fout: {e}")
        return {**rules_result, "ai_analyse": None, "ai_error": str(e)}


@subsidy_router.post("/generate-document")
async def generate_subsidy_document(intake: SubsidyIntake):
    """Stap 3: AI document generator — volledige subsidie-aanvraag."""
    llm_key = os.environ.get("EMERGENT_LLM_KEY")
    if not llm_key:
        return {"error": "AI niet geconfigureerd (EMERGENT_LLM_KEY ontbreekt)"}

    prompt = f"""Schrijf een subsidieaanvraag op basis van:

- project: {intake.projectomschrijving}
- sector: {intake.sector}
- doel: {intake.doel}
- impact: {intake.gebruikers}
- investering: {intake.investering}
- rechtsvorm: {intake.rechtsvorm}
- samenwerking: {intake.samenwerking}
- duurzaamheid: {intake.duurzaamheid}

Structuur:
1. Projectomschrijving
2. Probleemstelling
3. Oplossing
4. Impact
5. Financieel
6. Waarom subsidie nodig

Schrijf formeel, beleidsgericht en overtuigend. In het Nederlands.
Gebruik professionele taal geschikt voor subsidieverstrekkers."""

    try:
        chat = LlmChat(
            api_key=llm_key,
            session_id=f"subsidy-document-{uuid.uuid4()}",
            system_message="Je bent een professionele subsidie-aanvraag schrijver die formele documenten opstelt voor Nederlandse subsidieverstrekkers."
        ).with_model("openai", "gpt-5.2")
        
        response = await chat.send_message(UserMessage(text=prompt))

        return {"document": response, "status": "success"}

    except Exception as e:
        logger.error(f"Document generatie fout: {e}")
        return {"error": str(e), "status": "failed"}
