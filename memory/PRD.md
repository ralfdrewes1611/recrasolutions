# RECRA Solutions Configurator Platform - PRD

## Original Problem Statement
AI-gedreven configurator & offerteplatform voor RECRA Solutions: recreatieparken, campings en outdoor hospitality.

## Architecture
- **Frontend**: React 19 + Tailwind CSS + Shadcn UI
- **Backend**: FastAPI — server.py + chalet_engine.py + fec_engine.py + location_engine.py + partner_profiles.py + supabase_module.py
- **Database**: MongoDB (producten/projecten) + Supabase PostgreSQL (analytics/leads/scenarios/benchmark)
- **AI**: OpenAI GPT-5.2 via Emergent Integrations

## Core Modules

### Recreatie Infra (5-stappen wizard)
- **Locatie-intelligentie**: 12 provincies met grondprijzen, regelgeving, toerisme scores
- **Wellness — Ticra Outdoor**: 14 producten met echte productfoto's
- **Klikbare leveranciersnamen** met categorie-labels op productkaarten

### Chalet & Stay Configurator
- 26 modellen van 5 leveranciers met echte productfoto's
- **Samenstellen tab** incl. Wellness (Ticra Outdoor hottubs/sauna's/buitendouches)
- **Inspiratie Pakketten**: 3 presets
- **Klikbare leveranciersnamen** in modellen, rechterpaneel, en samenstellen tab

### Partner/Leverancier Profielen
- **5 leveranciersprofielen**: Ticra Outdoor (rijk voorbeeld), Kunert Group, Arcabo, Campsolutions, BBS Systeembouw
- **Ticra profiel bevat**: Pleisureworld Preferred Partner badge, Leisure Talk Podcast (#14 met Richard Otten), Trendwatcher quote, Top 3 meest gekozen producten, Evenementen & Deelname, USPs, Website/Blog links
- **Click tracking**: profile_view, website_click, blog_click, podcast_click via Supabase

### FEC Business Simulator
- 17 FEC producten + 6 leveranciers

### Platform Dashboard (Supabase)
- Trends & Benchmark, Lead Scoring, Scenario Vergelijking

## Leveranciers
- **Kunert Group** — 8 chalets (Pleisureworld Partner sinds 2023)
- **Arcabo** — 6 chalets (Pleisureworld Partner sinds 2024)
- **BBS Systeembouw** — 3 vakantiewoningen
- **Campsolutions** — 9 glamping
- **Ticra Outdoor** — 14 wellness (Pleisureworld Preferred Partner sinds 2024)

## Completed Features
- [x] Recreatie Infra 5-stappen wizard
- [x] FEC Business Simulator
- [x] Chalet & Stay Configurator met 26 modellen
- [x] Echte productfoto's van leverancier-websites
- [x] Samenstellen tab met dynamische prijsberekening
- [x] Inspiratie Pakketten (3 presets)
- [x] Pleisureworld Partner badges
- [x] Supabase Platform Dashboard
- [x] Locatie-intelligentie (12 provincies)
- [x] Ticra Outdoor wellness producten (14 producten)
- [x] **Partner/Leverancier Profielen** — 5 profielen met klikbare leveranciersnamen (10 apr 2026)
- [x] **Ticra rijke profielpagina** — Podcast, trendwatcher quote, top 3, evenementen (10 apr 2026)
- [x] **Click tracking** — profile_view, website, blog, podcast (10 apr 2026)
- [x] **Categorie-labels** op productkaarten in Recreatie (10 apr 2026)

## Backlog

### P1
- [ ] Auth systeem (login/registratie via Supabase Auth)
- [ ] White-label modules voor Pleisureworld
- [ ] Leveranciersprofielen verrijken (Kunert, Arcabo, Campsolutions, BBS — zelfde niveau als Ticra)

### P2
- [ ] "Idee naar Realisatie" Roadmap mode
- [ ] FEC PDF Export met Business Case
- [ ] Partner portal / Supplier login

### P3
- [ ] 3D Canvas / AR Preview
- [ ] CRM integratie
- [ ] Benchmark Mode
