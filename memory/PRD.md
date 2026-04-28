# RECRA Solutions — PRD

## Original Problem Statement
SaaS platform: Recreation Project Configurator & Partner Matching Platform.
- 3 (now 4) configurator flows: Recreatie Infra, Chalet & Stay, FEC & Experience, Horeca & Bar
- FEC + Horeca Revenue Engines
- 2D site planner canvas (Recreatie + FEC)
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
Frontend MUST display only "Vanaf €XXX per maand". No raw 0.0219, 2.19%, 0.10 margin, etc.

## Architecture
- `/app/backend/server.py` — main FastAPI app, Recreatie flow, quote gen
- `/app/backend/auth_engine.py` — JWT auth (AdminRECRA seed)
- `/app/backend/fec_engine.py` — FEC products + revenue engine
- `/app/backend/horeca_engine.py` — Horeca products + revenue engine ✅ NEW
- `/app/backend/chalet_engine.py` — chalet config
- `/app/backend/subsidy_engine.py` — funding check
- `/app/backend/crm_engine.py` — leads + 3-scenario AI
- `/app/backend/supplier_module.py` — supplier CRUD + matching
- `/app/backend/partner_profiles.py` — rich profiles (ticra, kunert, arcabo, campsolutions, bbs, eijsink ✅ NEW)
- `/app/frontend/src/App.js` — router + global state (>1000 lines, refactor candidate)
- `/app/frontend/src/FlowSelector.jsx` — 7 tiles (recreatie / chalet / fec / horeca / dashboard / roadmap / admin-suppliers)
- `/app/frontend/src/HorecaWizard.jsx` — 3-step Horeca configurator ✅ NEW
- `/app/frontend/src/SupplierProfile.jsx` — modal used by Recreatie + Horeca (and others)
- `/app/frontend/src/SupplierAdmin.jsx` — supplier CRUD dashboard
- `/app/frontend/src/SubsidyModule.jsx` — funding sticky sidebar
- `/app/frontend/src/LoginScreen.jsx` — auth gate

## Stack
React + FastAPI + MongoDB (products/projects/suppliers) + Supabase Postgres (leads, sessions, benchmarks).
JWT auth, OpenAI GPT via Emergent LLM Key.

## Implemented Modules (status: live)
- Recreatie Infra wizard (5-step) + 2D canvas + PDF export
- Chalet & Stay wizard with chalet model picker
- FEC & Experience wizard (revenue engine, zones, AI advisor, PDF)
- **Horeca & Bar wizard** (revenue engine, 32 products, lease/ROI calc, AI tips) — Feb 2026
- Subsidie Check (5-step intake + AI document gen)
- CRM lead engine + 3-scenario quote generator
- Supplier Admin Dashboard (CRUD)
- JWT Login Gate
- Rich Supplier Profiles (Ticra, Kunert, Arcabo, CampSolutions, BBS, **Eijsink** — Feb 2026)

## Roadmap
### P1
- UX wireframe / pricing strategie (Basic/Pro/Premium) for Lease Engine — user provides
- Apply deterministic lease formula across Recreatie + Chalet flows (only Horeca + FEC currently use it explicitly)

### P2
- Partner portal: supplier login to upload own product photos and view leads
- Resend / SendGrid integration for Subsidy follow-up emails
- Refactor `App.js` (split into hooks/sub-routers, currently >1000 lines)
- Extract HORECA_PRODUCTS / FEC_PRODUCTS to JSON seed files
- Shared `lease_utils.py` for the deterministic formula (currently duplicated)

### P3
- 3D Canvas / AR Preview
- Benchmark Mode public view
- Pydantic request models on /horeca/calculate-revenue (currently raw dict)

## Known Issues
- ESC key does not close SupplierProfile modal (a11y nice-to-have, not blocking)
- `App.js` >1000 lines

## Test Reports
`/app/test_reports/iteration_22.json` … `iteration_27.json` (all 100% pass)
