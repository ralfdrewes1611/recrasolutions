# RECRA Solutions Configurator Platform - PRD

## Original Problem Statement
AI-gedreven configurator & offerteplatform voor RECRA Solutions: recreatieparken, campings en outdoor hospitality.

## Architecture
- **Frontend**: React 19 + Tailwind CSS + Shadcn UI
- **Backend**: FastAPI (Python) — server.py + chalet_engine.py + fec_engine.py + location_engine.py + supabase_module.py
- **Database**: MongoDB (producten/projecten) + Supabase PostgreSQL (analytics/leads/scenarios/benchmark)
- **AI**: OpenAI GPT-5.2 via Emergent Integrations

## Core Modules

### Recreatie Infra (5-stappen wizard)
- Project > Terrein > Producten > Energie > Offerte
- **Locatie-intelligentie**: 12 provincies met grondprijzen (€15-€120/m²), regelgeving, toerisme scores
- **Wellness — Ticra Outdoor**: 14 producten (5 hottubs, 5 sauna's, 4 buitendouches) met echte productfoto's

### Chalet & Stay Configurator
- 26 modellen van 5 leveranciers: Kunert Group (8), Arcabo (6), BBS Systeembouw (3), Campsolutions (9), + Ticra Outdoor (wellness)
- Echte productfoto's per model vanuit leverancier-websites
- **Samenstellen tab**: Upgrade categorien incl. Wellness (Ticra Outdoor hottubs/sauna's/buitendouches)
- **Inspiratie Pakketten**: 3 presets (Glamping Tour, Luxe Chaletpark, Starter Budget)
- **Pleisureworld Partner badges**

### FEC Business Simulator (4 stappen)
- Locatie > Zones > Attracties > Revenue Dashboard
- 17 FEC producten + 6 leveranciers

### Platform Dashboard (Supabase)
- Trends & Benchmark, Lead Scoring, Scenario Vergelijking

## Leveranciers
- **Kunert Group** — 8 chaletmodellen (chaletskunert.nl)
- **Arcabo** — 6 chaletmodellen (arcabo.nl)
- **BBS Systeembouw** — 3 vakantiewoningen (bbssysteembouw.nl)
- **Campsolutions** — 9 glamping tenten/lodges (campsolutions.com)
- **Ticra Outdoor** — 14 wellness producten: hottubs (€2.995-€8.995), sauna's (€3.295-€14.395), buitendouches (€695-€3.354) (ticraoutdoor.com)

## Completed Features
- [x] Recreatie Infra 5-stappen wizard
- [x] FEC Business Simulator
- [x] Chalet & Stay Configurator met 26 modellen
- [x] Echte productfoto's van leverancier-websites
- [x] Samenstellen tab met dynamische prijsberekening
- [x] Inspiratie Pakketten (3 presets)
- [x] Pleisureworld Partner badges
- [x] Supabase Platform Dashboard
- [x] Glamping SVG plattegronden
- [x] Pre-Mantelzorg verwijderd, Emergent badge verborgen
- [x] **Locatie-intelligentie** — 12 provincies met grondprijzen, regelgeving, toerisme scores (10 apr 2026)
- [x] **Ticra Outdoor wellness producten** — 14 producten in Recreatie + Chalet Samenstellen (10 apr 2026)

## Backlog

### P1
- [ ] Auth systeem (login/registratie via Supabase Auth)
- [ ] White-label modules voor Pleisureworld
- [ ] Locatie-detail uitbreiden (afstand doelgroep, specifieke gemeenten)

### P2
- [ ] "Idee naar Realisatie" Roadmap mode
- [ ] FEC PDF Export met Business Case
- [ ] Partner portal / Supplier login

### P3
- [ ] 3D Canvas / AR Preview
- [ ] CRM integratie
- [ ] Benchmark Mode
