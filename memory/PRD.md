# RECRA Solutions — PRD

## Original Problem Statement
SaaS platform: Recreation Project Configurator & Partner Matching Platform.
- 4 configurator flows: Recreatie Infra, Chalet & Stay, FEC & Experience, Horeca & Bar
- FEC + Horeca Revenue Engines
- 2D site planner canvas
- Real product database with tiered suppliers
- Partner/Supplier logistics + matching
- Paywall: Free / Pro / Enterprise
- Pleisureworld strategic hooks: trends, benchmarks, partner ecosystem, scenario compare, white-label, location intel, CRM, subsidie, lease engine

## User Language
Dutch — always reply in Dutch.

## Login Credentials
`AdminRECRA` / `Welkom123$` — see `/app/memory/test_credentials.md`.

## Lease Formula (deterministic, never expose to UI)
`monthly = (investment + max(investment * 0.10, 500)) * 0.0219`
Frontend MUST display only "Vanaf €XXX per maand".

## Architecture
- `/app/backend/server.py` — main FastAPI app, Recreatie flow, quote gen
- `/app/backend/auth_engine.py` — JWT auth
- `/app/backend/fec_engine.py` — FEC products + revenue engine
- `/app/backend/horeca_engine.py` — Horeca products + revenue engine
- `/app/backend/chalet_engine.py` — chalet config (terras now Madino-branded)
- `/app/backend/subsidy_engine.py` — funding check
- `/app/backend/crm_engine.py` — leads + AI 3-scenario
- `/app/backend/supplier_module.py` — supplier CRUD
- `/app/backend/partner_profiles.py` — rich profiles, **MongoDB-backed**, full CRUD admin endpoints
- `/app/frontend/src/App.js` — router (>1000 lines, refactor candidate)
- `/app/frontend/src/FlowSelector.jsx` — 8 tiles (recreatie / chalet / fec / horeca / dashboard / roadmap / admin-suppliers / admin-partners)
- `/app/frontend/src/HorecaWizard.jsx` — Horeca wizard
- `/app/frontend/src/ChaletWizard.jsx` — Chalet (now Madino terras chip + Ticra wellness chip)
- `/app/frontend/src/EijsinkPartnerPage.jsx` — full-page Eijsink partner
- `/app/frontend/src/SupplierProfile.jsx` — modal for other partners
- `/app/frontend/src/PartnerProfileAdmin.jsx` — admin CRUD UI ✅ NEW
- `/app/frontend/src/SupplierAdmin.jsx` — supplier CRUD
- `/app/frontend/src/SubsidyModule.jsx` — funding sticky sidebar
- `/app/frontend/src/LoginScreen.jsx` — auth gate

## Stack
React + FastAPI + MongoDB + Supabase Postgres. JWT auth. OpenAI GPT via Emergent LLM Key.

## Implemented Modules
- Recreatie Infra wizard (5-step) + 2D canvas + PDF
- Chalet & Stay wizard with chalet model picker + Ticra wellness + **Madino terras** ✅
- FEC & Experience wizard (revenue engine, zones, AI advisor, PDF)
- Horeca & Bar wizard (revenue engine, 32 products, lease/ROI calc)
- Subsidie Check
- CRM lead engine + 3-scenario quote generator
- Supplier Admin Dashboard
- JWT Login Gate
- Rich Partner Profiles (Ticra, Kunert, Arcabo, CampSolutions, BBS, Eijsink, **Madino**) — MongoDB-backed
- **Partner Profile Admin** with full CRUD (May 2026) ✅

## Roadmap
### P1
- UX wireframe / pricing strategy (Basic/Pro/Premium) — user provides
- Apply deterministic lease formula across Recreatie + Chalet
- Return 404 (not 200+error) for not-found partner endpoints

### P2
- Partner portal: supplier login to upload own product photos and view leads
- Resend / SendGrid integration for Subsidy follow-up emails
- Refactor `App.js` (>1000 lines)
- Split partner_profiles.py seed data to `seed_partners.py`
- Extract `lease_utils.py` (shared formula)
- Hero image upload in partner admin (currently URL only)

### P3
- 3D Canvas / AR Preview
- Benchmark Mode public view

## Known Issues
- ESC key does not close SupplierProfile modal (a11y nice-to-have)

## Test Reports
`iteration_22.json` … `iteration_29.json` — all PASS
