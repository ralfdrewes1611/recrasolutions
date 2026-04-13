# RECRA Solutions — Recreation Project Configurator & Partner Matching Platform

## Origineel Probleem
SaaS platform voor RECRA Solutions met 3 configuratie-flows (Recreatie Infra, Chalet & Stay, FEC & Experience), 2D site planner, product database, partner/leverancier matching, paywall tiers, en Pleisureworld strategic data hook.

## Architectuur
- **Frontend**: React + Tailwind + Shadcn/UI
- **Backend**: FastAPI + MongoDB + Supabase (PostgreSQL)
- **Integraties**: OpenAI GPT-5.2 (Emergent LLM Key), Supabase Analytics

## Code Structuur
### Backend
- `server.py` — Hoofd FastAPI app, Recreatie flow, verbeterde PDF export
- `chalet_engine.py` — Chalet & Stay configurator
- `fec_engine.py` — FEC Revenue Engine + PDF Export
- `location_engine.py` — Locatie-intelligentie
- `partner_profiles.py` — Verrijkte leveranciersprofielen + Dynamic Top 3
- `roadmap_engine.py` — "Idee naar Realisatie" fasen-overzicht
- `whitelabel_engine.py` — White-label configuratie
- `subsidy_engine.py` — Financiering & Subsidie Check
- `crm_engine.py` — CRM leads, follow-up mails, scenario generator
- `supplier_module.py` — Leveranciers CRUD + flow toewijzing + stats
- `supabase_module.py` — Supabase tracking, benchmarks

### Frontend
- `App.js` — Main router, modals, flow state
- `FlowSelector.jsx` — 6 flow kaarten (incl. admin)
- `ChaletWizard.jsx` — Chalet & Stay wizard + Subsidie
- `FecWizard.jsx` — FEC Revenue Engine + PDF + Subsidie
- `RoadmapView.jsx` — Roadmap: Idee naar Realisatie
- `SubsidyModule.jsx` — Subsidie Check + CRM + follow-up
- `ScenarioCompare.jsx` — 3 offerte-scenario's vergelijker
- `SupplierProfile.jsx` — Leveranciersprofiel modal
- `SupplierAdmin.jsx` — Leveranciersbeheer dashboard

## Voltooid

### Basis Platform
- [x] 3 configuratie-flows + 2D Site Planner + Product database
- [x] AI offerte tekst (GPT-5.2) + Paywall tiers + Platform Dashboard
- [x] Locatie-intelligentie + Wellness producten + Click-tracking

### P1 — Leveranciers & Dynamiek
- [x] Verrijkte profielen (5 leveranciers) + Dynamic Top 3
- [x] White-label (RECRA + Pleisureworld) + Roadmap mode

### P2 — Business Case & PDF
- [x] FEC PDF + Recreatie PDF (verbeterd) + Roadmap integratie

### Subsidie & CRM Engine
- [x] 5-staps intake + scoring (0-10) + AI analyse + document generator
- [x] CRM lead management + lead scoring (0-100)
- [x] Follow-up mail generator + 3 offerte-scenario's (AI)

### Leveranciersbeheer (13 april 2026)
- [x] Full CRUD dashboard (toevoegen, bewerken, verwijderen)
- [x] Multi-flow toewijzing per leverancier (recreatie, chalet, fec)
- [x] Categorie management (14 productcategorieën)
- [x] Status systeem (Verified, Compatible, Basis)
- [x] Filter op flow + zoekfunctie + stats dashboard
- [x] Expandable detailweergave (contact, logistiek, categorieën)
- [x] Backend migratie: bestaande leveranciers met flows bijgewerkt

## Prioritized Backlog
### P3
- [ ] Partner portal / Supplier login (leveranciers zelf producten beheren)
- [ ] Auth systeem via Supabase Auth
- [ ] Real email sending (Resend/SendGrid)
- [ ] CRM dashboard voor sales team
- [ ] 3D Canvas / AR Preview
- [ ] Benchmark Mode (publiek dashboard)

## Test Iteraties
- Iteratie 19-21: Core features ✅
- Iteratie 22: Roadmap, PDF, White-label, Dynamic Top 3 ✅ 100%
- Iteratie 23: Subsidie Check Module ✅ 100%
- Iteratie 24: CRM, Scenario's, Follow-up Mail, Verbeterde PDF ✅ 100%
- Iteratie 25: Leveranciersbeheer Dashboard (CRUD + Flows) ✅ 100%
