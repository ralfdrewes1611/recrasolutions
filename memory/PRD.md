# RECRA Solutions — Recreation Project Configurator & Partner Matching Platform

## Origineel Probleem
SaaS platform voor RECRA Solutions met 3 configuratie-flows (Recreatie Infra, Chalet & Stay, FEC & Experience), 2D site planner, product database, partner/leverancier matching, paywall tiers, en Pleisureworld strategic data hook.

## Architectuur
- **Frontend**: React + Tailwind + Shadcn/UI
- **Backend**: FastAPI + MongoDB + Supabase (PostgreSQL)
- **Integraties**: OpenAI GPT-5.2 (Emergent LLM Key), Supabase Analytics

## Code Structuur
### Backend
- `/app/backend/server.py` — Hoofd FastAPI app, Recreatie flow
- `/app/backend/chalet_engine.py` — Chalet & Stay configurator
- `/app/backend/fec_engine.py` — FEC Revenue Engine + PDF Export
- `/app/backend/location_engine.py` — Locatie-intelligentie (provincies, grondprijzen)
- `/app/backend/partner_profiles.py` — Verrijkte leveranciersprofielen + Dynamic Top 3
- `/app/backend/roadmap_engine.py` — "Idee naar Realisatie" fasen-overzicht
- `/app/backend/whitelabel_engine.py` — White-label configuratie (RECRA + Pleisureworld)
- `/app/backend/subsidy_engine.py` — Financiering & Subsidie Check (scoring + AI)
- `/app/backend/supabase_module.py` — Supabase tracking, benchmarks, leads

### Frontend
- `/app/frontend/src/App.js` — Main router, modals, flow state
- `/app/frontend/src/FlowSelector.jsx` — 5 flow kaarten
- `/app/frontend/src/ChaletWizard.jsx` — Chalet & Stay wizard + Subsidie
- `/app/frontend/src/FecWizard.jsx` — FEC Revenue Engine + PDF + Subsidie
- `/app/frontend/src/RoadmapView.jsx` — Roadmap: Idee naar Realisatie
- `/app/frontend/src/SubsidyModule.jsx` — Financiering & Subsidie Check module
- `/app/frontend/src/SupplierProfile.jsx` — Leveranciersprofiel modal
- `/app/frontend/src/components/Step3Products.jsx` — Product selectie (Recreatie)
- `/app/frontend/src/components/Step5Quote.jsx` — Offerte + Roadmap knop

## Wat is gebouwd (voltooid)

### Basis Platform
- [x] 3 configuratie-flows: Recreatie, Chalet, FEC
- [x] 2D Site Planner met drag-and-drop
- [x] Product database met echte leveranciersproducten (49 producten)
- [x] 5 leveranciers: Kunert, Arcabo, BBS, Campsolutions, Ticra Outdoor
- [x] Real product photos (gecrawled van leverancierssites)
- [x] AI-powered terreinanalyse en offerte tekst (GPT-5.2)
- [x] Paywall tiers: Free, Pro, Enterprise
- [x] Platform Dashboard met trends en benchmarks
- [x] Supabase tracking voor analytics en leads

### P0 — Core Features
- [x] Locatie-intelligentie (12 provincies, grondprijzen, regelgeving)
- [x] 14 Ticra Outdoor wellness producten (hottubs, saunas, douches)
- [x] Klikbare leveranciersnamen → SupplierProfile modal
- [x] Click-tracking via Supabase

### P1 — Verrijkte Leveranciers & Dynamiek (10 april 2026)
- [x] Verrijkte profielen voor alle 5 leveranciers (podcasts, quotes, events, USPs, top 3)
- [x] Dynamische "Top 3 meest gekozen" endpoint
- [x] White-label modules: RECRA Solutions + Pleisureworld
- [x] "Idee naar Realisatie" Roadmap mode (4 fasen per flow type)

### P2 — Business Case & Roadmap (10 april 2026)
- [x] FEC PDF Export met volledige Business Case
- [x] Roadmap geïntegreerd in Recreatie, Chalet en FEC
- [x] FlowSelector uitgebreid naar 5 kaarten

### Financiering & Subsidie Check Module (13 april 2026)
- [x] 5-staps intake formulier (organisatie, project, financieel, impact, versterkers)
- [x] Rules-based scoring engine (0-10) met sector fit, projecttype, impact, etc.
- [x] Hard filter: investering < €10K → lage kans
- [x] AI-powered subsidie analyse via GPT-5.2 (kans, toelichting, regelingen, verbeterpunten)
- [x] AI subsidie-aanvraag document generator
- [x] Rechter sidebar integratie in alle 3 configurators
- [x] CTA knoppen: "Laat RECRA dit voor je regelen" + "Plan adviesgesprek"
- [x] Print/PDF export van gegenereerd subsidie document

## API Endpoints
- `GET /api/products` — Alle producten
- `GET /api/location/provinces` — Provincies
- `GET /api/location/evaluate` — Locatie evaluatie
- `GET /api/partners/profiles` — Alle leveranciers
- `GET /api/partners/profiles/{id}` — Leveranciersprofiel
- `GET /api/partners/profiles/{id}/dynamic-top3` — Dynamische top 3
- `POST /api/supabase/partners/track` — Click tracking
- `GET /api/roadmap/phases/{flow_type}` — Roadmap fasen
- `GET /api/roadmap/summary` — Roadmap overzicht
- `GET /api/whitelabel/config` — Actieve branding
- `GET /api/whitelabel/configs` — Alle white-label configs
- `POST /api/fec/pdf` — FEC Business Case PDF
- `POST /api/subsidy/check` — Subsidie scoring (rules-based)
- `POST /api/subsidy/ai-analyse` — AI subsidie analyse (GPT-5.2)
- `POST /api/subsidy/generate-document` — AI subsidie-aanvraag generator
- `POST /api/chalet/calculate` — Chalet prijsberekening
- `GET /api/fec/products` — FEC attracties

## Prioritized Backlog

### P2 (Resterend)
- [ ] Recreatie PDF export verbeteren (vergelijkbaar met FEC business case niveau)

### P3
- [ ] CRM integratie (lead = warm na subsidie check)
- [ ] Offerte automatisch 3 scenario's genereren
- [ ] Follow-up mail na subsidie check
- [ ] Partner portal / Supplier login
- [ ] Auth systeem via Supabase Auth
- [ ] 3D Canvas / AR Preview
- [ ] Benchmark Mode (publiek dashboard)

## Test Iteraties
- Iteratie 19: Real Product Photos & Pricing ✅
- Iteratie 20: Location Intelligence & Ticra Products ✅
- Iteratie 21: Supplier Profiles & Click Tracking ✅
- Iteratie 22: P1/P2 Features (Roadmap, PDF, White-label, Dynamic Top 3) ✅ 100%
- Iteratie 23: Financiering & Subsidie Check Module ✅ 100%
