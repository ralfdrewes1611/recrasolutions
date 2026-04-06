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
- Denken in plaatsen / units
- Focus: kosten + infra
- 5-stappen wizard: Project > Terrein > Producten > Energie > Offerte

### FEC = Revenue Engineering (binnen, m²/m³, omzet gestuurd)
- Denken in ruimte + omzet
- Focus: € per m² / m³
- 4-stappen wizard: Locatie > Zones > Attracties > Revenue Dashboard
- **Interactive canvas**: drag & resize zones, m² auto-berekening

## Implemented Features

### Core Platform
- Flow Selector met 3 flows + RECRA logo (wit/donker PNG)
- Paywall (Free/Pro/Enterprise) met upgrade modal
- RECRA branding: #244628 header, #FDF9ED achtergrond, #70C26C accenten

### Recreatie & Chalet Configurator
- 27 echte producten (UniFi cameras, Nice slagbomen, sanitair, WiFi, etc.)
- Custom pointer-based drag & click-to-place 2D canvas
- Haversine leveranciersmatching met reiskosten per categorie
- Rule-based AI advisor (8 regels)
- Functionele energie stap (zonnepanelen, accu's, warmtepomp, terugverdientijd)
- PDF offerte export met reiskosten

### FEC Revenue Engine
- 14 FEC producten over 5 categorieën (Arcade, Karting, Interactive, Indoor Play, F&B)
- 5 FEC leveranciers (X-Wall, Shuffly, Heemskerk Play, Pro Karting, Time Mission)
- Revenue Engine: daily/monthly revenue, ROI, break-even per product
- Top 5 Geldverdieners gesorteerd op €/m²/maand
- **Interactive Canvas** (NIEUW):
  - Zone drag: versleep zones naar gewenste positie
  - Zone resize: sleep rechtsonder hoek om formaat aan te passen
  - m² auto-sync: pixel afmetingen ↔ vierkante meters bidirectioneel
  - Zone selectie met ring, delete knop, resize handle
  - Canvas boundaries check (zones blijven binnen canvas)
- Zone-types: Entree, Arcade, Karting, Interactive, Indoor Play, Horeca, Routing
- FEC AI Rules (8 regels): horeca advies, karting flag, capaciteit check, etc.
- Business Case sidebar met live investering, omzet/mnd, break-even
- Cross-sell naar Recreatie/Chalet

### Codebase (goed gestructureerd)
- App.js: ~880 regels
- FecWizard.jsx: ~670 regels
- fec_engine.py: ~340 regels
- 5 step-componenten + FlowSelector + SupplierPanel

## Backlog

### P1 - High
- [ ] Auth systeem (login/registratie voor paywall persistentie)
- [ ] FEC PDF export met business case

### P2 - Medium
- [ ] Partner portal: leveranciers uploaden productcatalogus
- [ ] Deel configuratie via URL
- [ ] 3D canvas weergave
- [ ] Geocoding (adres → lat/lng automatisch)

### P3 - Future
- [ ] AR preview, CRM integratie, Grenke lease, White-label
- [ ] Benchmark Mode (vergelijk met branche-gemiddelden)
