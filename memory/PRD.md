# RECRA Solutions Configurator Platform - PRD

## Original Problem Statement
AI-gedreven configurator & offerteplatform voor RECRA Solutions: recreatieparken, campings en outdoor hospitality.

## Architecture
- **Frontend**: React 19 + Tailwind CSS + Shadcn UI
- **Backend**: FastAPI (Python) — server.py + ai_services.py
- **Database**: MongoDB (25 producten)
- **AI**: OpenAI GPT-5.2 via Emergent Integrations

## Implemented Features

### Core Platform
- 5-stappen wizard: Project > Terrein > Producten > Energie > Offerte
- Canvas met zones, dekking toggle, snap-to-grid (24px)
- Click-to-place + custom pointer drag + selectie + verplaatsing
- Icoon | 2D toggle (op-schaal rechthoeken)
- Project CRUD, PDF offerte export, RECRA branding

### Producten (25 stuks, echte producten)
- **Sanitair** (3): Compact 3x6m, Medium 6x8m, Premium 8x12m
- **Slagboom** (3): Nice M5BAR, Nice M5BAR + Kentekenherkenning, Premium Toegangspoort
- **Camera** (5): UniFi G5 Bullet, Dome Ultra, Pro, Turret Ultra, AI LPR
- **Toegangscontrole** (4): UniFi Access Hub, UA-Lite, UA-Pro, Starter Kit
- **WiFi** (2): UniFi AP Indoor/Outdoor
- **Verlichting** (2): Solar LED Pad, Slimme Lichtmast
- **Betaalsystemen** (2): Adyen Betaalterminal, Adyen + Reserveringssysteem
- **Douchelezers** (3): Basis, Pro, Enterprise

### AI Automatisering
- Excel/CSV import met AI kolom-matching
- Website scraper met AI productextractie
- Smart plattegrond analyse (Vision)
- AI offertetekst generatie
- AI aanbevelingen (rule-based + GPT-5.2)

### Labels & Terminologie
- "Investering" (geen CAPEX), "Operational Lease" (geen OPEX)
- "60 maanden incl. SLA" zichtbaar als tekst
- Adyen-only (geen muntautomaten)

## Backlog

### P1 - High
- [ ] Energie stap: hybrid/offgrid berekening (zonnepanelen, accu's, warmtepomp)
- [ ] Dynamisch terrein: layout past zich aan op plattegrond
- [ ] RECRA Logo (PNG/SVG nodig)
- [ ] App.js opsplitsen in componenten
- [ ] Product scraper: 2D/3D afbeelding generatie per product

### P2 - Medium
- [ ] Partner portal: leveranciers uploaden productcatalogus
- [ ] Auth (Free/Pro/Enterprise)
- [ ] Deel configuratie via URL
- [ ] 3D canvas weergave

### P3 - Future
- [ ] AR preview, CRM integratie, Grenke lease, White-label
