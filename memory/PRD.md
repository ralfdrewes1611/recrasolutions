# RECRA Solutions Configurator Platform - PRD

## Original Problem Statement
AI-gedreven configurator & offerteplatform voor RECRA Solutions: recreatieparken, campings en outdoor hospitality.

## Architecture
- **Frontend**: React 19 + Tailwind CSS + Shadcn UI
- **Backend**: FastAPI (Python) — server.py + ai_services.py + supplier_module.py + fec_engine.py
- **Database**: MongoDB (27 recreatie producten, 5 recreatie leveranciers + 14 FEC producten, 5 FEC leveranciers)
- **AI**: OpenAI GPT-5.2 via Emergent Integrations (quote text & floorplan); Rule-based AI for recommendations

## Fundamental Architecture Split

### Recreatie + Chalet = Asset Placement (buiten, terrein, infra)
- 5-stappen wizard: Project > Terrein > Producten > Energie > Offerte

### FEC = Revenue Engineering (binnen, m²/m³, omzet gestuurd)
- 4-stappen wizard: Locatie > Zones > Attracties > Revenue Dashboard
- Interactive canvas: drag & resize zones, m² auto-berekening
- Revenue engine + lease pricing

## Implemented Features

### FEC Revenue Engine
- 14 FEC producten met lease pricing (price_lease_monthly) over 5 categorieën
- Correctie: **X-Wall Battle Arena** (geen klimwand)
- 5 FEC leveranciers: X-Wall (battle arena's), Shuffly, Heemskerk Play, Pro Karting, Time Mission
- Revenue Engine: daily/monthly revenue, ROI, break-even, lease per product
- **Operational Lease in dashboard**: totaal lease/mnd, netto winst (omzet - lease)
- Top Performers met lease per product
- Business Case sidebar met lease breakdown
- Interactive Canvas: drag & resize zones
- FEC AI Rules (8 regels)

### Recreatie & Chalet Configurator
- 27 echte producten, custom pointer-based drag & click-to-place 2D canvas
- Haversine leveranciersmatching, energie stap, PDF export

### Platform
- 3 flows (Recreatie, Chalet, FEC), RECRA logo, Paywall (Free/Pro/Enterprise)

## Backlog

### P1
- [ ] Auth systeem (login/registratie voor paywall persistentie)
- [ ] FEC PDF export met business case

### P2
- [ ] Partner portal, Deel configuratie via URL, 3D canvas, Geocoding

### P3
- [ ] AR preview, CRM, Grenke lease, White-label, Benchmark Mode
