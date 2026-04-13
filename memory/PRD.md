# RECRA Solutions — Recreation Project Configurator & Partner Matching Platform

## Origineel Probleem
SaaS platform voor RECRA Solutions met 3 configuratie-flows (Recreatie Infra, Chalet & Stay, FEC & Experience), 2D site planner, product database, partner/leverancier matching, paywall tiers, en Pleisureworld strategic data hook.

## Architectuur
- **Frontend**: React + Tailwind + Shadcn/UI
- **Backend**: FastAPI + MongoDB + Supabase (PostgreSQL)
- **Integraties**: OpenAI GPT-5.2 (Emergent LLM Key), Supabase Analytics

## Code Structuur
### Backend
- `/app/backend/server.py` — Hoofd FastAPI app, Recreatie flow, verbeterde PDF export
- `/app/backend/chalet_engine.py` — Chalet & Stay configurator
- `/app/backend/fec_engine.py` — FEC Revenue Engine + PDF Export
- `/app/backend/location_engine.py` — Locatie-intelligentie (provincies, grondprijzen)
- `/app/backend/partner_profiles.py` — Verrijkte leveranciersprofielen + Dynamic Top 3
- `/app/backend/roadmap_engine.py` — "Idee naar Realisatie" fasen-overzicht
- `/app/backend/whitelabel_engine.py` — White-label configuratie (RECRA + Pleisureworld)
- `/app/backend/subsidy_engine.py` — Financiering & Subsidie Check (scoring + AI)
- `/app/backend/crm_engine.py` — CRM leads, follow-up mails, scenario generator
- `/app/backend/supabase_module.py` — Supabase tracking, benchmarks, leads

### Frontend
- `/app/frontend/src/App.js` — Main router, modals, flow state
- `/app/frontend/src/FlowSelector.jsx` — 5 flow kaarten
- `/app/frontend/src/ChaletWizard.jsx` — Chalet & Stay wizard + Subsidie
- `/app/frontend/src/FecWizard.jsx` — FEC Revenue Engine + PDF + Subsidie
- `/app/frontend/src/RoadmapView.jsx` — Roadmap: Idee naar Realisatie
- `/app/frontend/src/SubsidyModule.jsx` — Subsidie Check + CRM contactformulier + follow-up
- `/app/frontend/src/ScenarioCompare.jsx` — 3 offerte-scenario's vergelijker
- `/app/frontend/src/SupplierProfile.jsx` — Leveranciersprofiel modal
- `/app/frontend/src/components/Step5Quote.jsx` — Offerte + Roadmap + Scenario's

## Wat is gebouwd (voltooid)

### Basis Platform
- [x] 3 configuratie-flows: Recreatie, Chalet, FEC
- [x] 2D Site Planner met drag-and-drop
- [x] Product database (49 producten, 5 leveranciers)
- [x] Real product photos (gecrawled)
- [x] AI-powered terreinanalyse (GPT-5.2)
- [x] Paywall tiers: Free, Pro, Enterprise
- [x] Platform Dashboard

### P0 — Core Features
- [x] Locatie-intelligentie (12 provincies)
- [x] 14 Ticra Outdoor wellness producten
- [x] Klikbare leveranciers + click-tracking

### P1 — Leveranciers & Dynamiek
- [x] Verrijkte profielen alle 5 leveranciers
- [x] Dynamische Top 3 endpoint
- [x] White-label modules (RECRA + Pleisureworld)
- [x] "Idee naar Realisatie" Roadmap mode

### P2 — Business Case & PDF
- [x] FEC PDF Export met Business Case
- [x] Recreatie PDF Export verbeterd (metrics, categorieën, lease, branding)
- [x] Roadmap geïntegreerd in alle flows

### Financiering & Subsidie Check
- [x] 5-staps intake formulier
- [x] Rules-based scoring engine (0-10)
- [x] AI-powered subsidie analyse (GPT-5.2)
- [x] AI subsidie-aanvraag document generator
- [x] Rechter sidebar in alle 3 configurators

### CRM & Conversie Engine (13 april 2026)
- [x] CRM lead management (opslaan na subsidie check)
- [x] Lead scoring (0-100): email+telefoon+bedrijf+project+subsidie+kans+investering
- [x] Follow-up mail generator (professionele HTML template met RECRA branding)
- [x] 3 automatische offerte-scenario's (Budget/Standaard/Premium) via GPT-5.2
- [x] ScenarioCompare component in Recreatie Step5
- [x] Contactformulier in SubsidyModule (naam, email, telefoon, bedrijf)
- [x] Follow-up mail preview na lead opslag

## API Endpoints
### Core
- `GET /api/products`, `POST /api/quote/pdf`, `POST /api/chalet/calculate`
- `GET /api/fec/products`, `POST /api/fec/pdf`

### Platform
- `GET /api/location/provinces`, `GET /api/location/evaluate`
- `GET /api/partners/profiles/{id}`, `GET /api/partners/profiles/{id}/dynamic-top3`
- `POST /api/supabase/partners/track`
- `GET /api/roadmap/phases/{flow_type}`
- `GET /api/whitelabel/config`, `GET /api/whitelabel/configs`

### Subsidie & CRM
- `POST /api/subsidy/check` — Rules-based scoring
- `POST /api/subsidy/ai-analyse` — AI subsidie analyse
- `POST /api/subsidy/generate-document` — Subsidie-aanvraag generator
- `POST /api/crm/leads` — Lead aanmaken + lead score
- `GET /api/crm/leads` — Leads ophalen
- `POST /api/crm/leads/{id}/follow-up` — Follow-up mail genereren
- `POST /api/crm/follow-up/generate` — Follow-up mail (zonder lead)
- `POST /api/crm/scenarios/generate` — 3 offerte-scenario's

## Prioritized Backlog

### P3
- [ ] Partner portal / Supplier login
- [ ] Auth systeem via Supabase Auth
- [ ] 3D Canvas / AR Preview
- [ ] Benchmark Mode (publiek dashboard)
- [ ] Real email sending (Resend/SendGrid integratie)
- [ ] CRM dashboard voor sales team

## Test Iteraties
- Iteratie 19-21: Core features ✅
- Iteratie 22: P1/P2 (Roadmap, PDF, White-label, Dynamic Top 3) ✅ 100%
- Iteratie 23: Subsidie Check Module ✅ 100%
- Iteratie 24: CRM, Scenario's, Follow-up Mail, Verbeterde PDF ✅ 100%
