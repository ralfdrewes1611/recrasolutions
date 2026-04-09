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
- **Echte productfoto's** per model vanuit leverancier-websites (chaletskunert.nl, arcabo.nl, campsolutions.com, bbssysteembouw.nl)
- **Samenstellen tab**: Upgrade categorien per type (chalet: 6 categorien, glamping: 4 categorien) met dynamische prijsberekening
- **Inspiratie Pakketten**: 3 vooraf geconfigureerde concepten (Glamping Tour, Luxe Chaletpark, Starter Budget)
- **Pleisureworld Partner badges**: Award icoon bij preferred suppliers

### FEC = Revenue Engineering (binnen, m2/m3, omzet gestuurd)
- 4-stappen wizard: Locatie > Zones > Attracties > Revenue Dashboard
- 17 FEC producten + 6 leveranciers

### Platform Dashboard (Supabase)
- **Trends & Benchmark**: KPIs, meest gekozen modellen/leveranciers, gem. investering
- **Lead Scoring**: Funnel (orientatie/vergelijking/concreet), lead details, budget, fase
- **Scenario Vergelijking**: Basis/Luxe/Max Bezetting met ROI, cashflow, investering
- Data via Supabase PostgreSQL (5 tabellen)

## Supabase Integration (08 apr 2026)
- URL: https://ehhmmysmxbbrdvceyicw.supabase.co
- 5 tabellen: configurator_sessions, configuration_snapshots, benchmark_entries, scenarios, partner_interactions

## Completed Features
- [x] Recreatie Infra 5-stappen wizard
- [x] FEC Business Simulator
- [x] Chalet & Stay Configurator met 26 modellen van 4 leveranciers
- [x] Echte productfoto's van leverancier-websites (09 apr 2026)
- [x] Samenstellen tab met dynamische prijsberekening (09 apr 2026)
- [x] Inspiratie Pakketten (3 presets) (09 apr 2026)
- [x] Pleisureworld Partner badges (09 apr 2026)
- [x] Supabase Platform Dashboard
- [x] Glamping SVG plattegronden (tent/dome outlines)

## Backlog

### P1
- [ ] Auth systeem (login/registratie via Supabase Auth) — user zei: kan later
- [ ] White-label modules voor Pleisureworld
- [ ] Locatie-intelligentie (grondprijzen, regelgeving, afstand doelgroep)

### P2
- [ ] "Idee naar Realisatie" Roadmap mode (ontwerp > vergunning > bouw > exploitatie)
- [ ] FEC PDF Export met Business Case
- [ ] Partner portal / Supplier login

### P3
- [ ] 3D Canvas / AR Preview
- [ ] CRM integratie
- [ ] Benchmark Mode
