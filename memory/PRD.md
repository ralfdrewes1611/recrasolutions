# RECRA Solutions Configurator Platform - PRD

## Original Problem Statement
AI-gedreven configurator & offerteplatform voor RECRA Solutions: recreatieparken, campings en outdoor hospitality.

## Architecture
- **Frontend**: React 19 + Tailwind CSS + Shadcn UI
- **Backend**: FastAPI (Python) — server.py + ai_services.py + supplier_module.py + fec_engine.py + chalet_engine.py + supabase_module.py
- **Database**: MongoDB (producten/projecten) + Supabase PostgreSQL (analytics/leads/scenarios/benchmark)
- **AI**: OpenAI GPT-5.2 via Emergent Integrations

## Fundamental Architecture Split

### Recreatie = Asset Placement (buiten, terrein, infra)
- 5-stappen wizard: Project > Terrein > Producten > Energie > Offerte

### Chalet & Stay = Accommodation Configurator (dedicated ChaletWizard)
- 3-kolom layout: Filters (links) > Fotocarrousel + Plattegrond (midden) > Prijsoverzicht (rechts)
- 26 modellen van 4 leveranciers: Kunert Group (8), Arcabo (6), BBS Systeembouw (3), Campsolutions (9 glamping)
- Filters: Categorie, Leverancier, Bestemming, Oppervlakte, Model Vorm, Dak Vorm
- Stijlen: Modern / Luxe / Landelijk
- Pricing: Basisprijs + BTW 21% + Operational Lease (60 mnd)
- Aparte plattegronden: SVG tent voor glamping (open ruimte), kamer-indeling voor chalets

### FEC = Revenue Engineering (binnen, m²/m³, omzet gestuurd)
- 4-stappen wizard: Locatie > Zones > Attracties > Revenue Dashboard
- 17 FEC producten + 6 leveranciers

### Platform Dashboard (NEW — Supabase)
- **Trends & Benchmark**: KPIs, meest gekozen modellen/leveranciers, gem. investering
- **Lead Scoring**: Funnel (oriëntatie/vergelijking/concreet), lead details, budget, fase
- **Scenario Vergelijking**: Basis/Luxe/Max Bezetting met ROI, cashflow, investering
- Data via Supabase PostgreSQL (5 tabellen: sessions, snapshots, benchmarks, scenarios, partner_interactions)

## Supabase Integration (08 apr 2026)
- URL: https://ehhmmysmxbbrdvceyicw.supabase.co
- 5 tabellen: configurator_sessions, configuration_snapshots, benchmark_entries, scenarios, partner_interactions
- APIs: /api/platform/sessions, /api/platform/benchmark, /api/platform/scenarios, /api/platform/leads, /api/platform/partners

## Backlog

### P0
- [ ] Auth systeem (login/registratie via Supabase Auth)
- [ ] Samenstellen tab dynamisch (upgrade opties updaten prijs live)

### P1
- [ ] Inspiratie → Realisatie funnel (pre-set configuraties vanuit artikelen)
- [ ] "Van idee naar realisatie" roadmap (ontwerp → vergunning → bouw → exploitatie)
- [ ] Preferred Partner posities (leveranciers premium zichtbaarheid)
- [ ] FEC PDF export met business case

### P2
- [ ] White-label modules (Pleisureworld eigen branded versies)
- [ ] Locatie-intelligentie (grondprijzen, regelgeving, toeristische aantrekkelijkheid)
- [ ] Geocoding (adres naar lat/lng)
- [ ] Partner portal

### P3
- [ ] 3D Canvas / AR Preview / CRM / Benchmark Mode
