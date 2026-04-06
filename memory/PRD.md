# RECRA Solutions Configurator Platform - PRD

## Original Problem Statement
AI-gedreven configurator & offerteplatform voor RECRA Solutions: recreatieparken, campings en outdoor hospitality.

## Architecture
- **Frontend**: React 19 + Tailwind CSS + Shadcn UI
- **Backend**: FastAPI (Python) — server.py + ai_services.py + supplier_module.py
- **Database**: MongoDB (27 producten, 5 leveranciers)
- **AI**: OpenAI GPT-5.2 via Emergent Integrations (for quote text & floorplan only; recommendations are rule-based)

## Implemented Features

### Core Platform
- 5-stappen wizard: Project > Terrein > Producten > Energie > Offerte
- **3 Configuratie Flows**: Recreatie Infra, Chalet & Stay, FEC & Experience
- Flow-specifieke productfiltering per branche
- Canvas met zones, dekking toggle, snap-to-grid (24px)
- Click-to-place + custom pointer drag + selectie + verplaatsing
- Icoon | 2D toggle (op-schaal rechthoeken)
- Project CRUD, PDF offerte export, RECRA branding

### Producten (27 stuks, echte producten)
- **Sanitair** (3): Compact 3x6m, Medium 6x8m, Premium 8x12m
- **Slagboom** (3): Nice M5BAR, Nice M5BAR + Kentekenherkenning, Premium Toegangspoort
- **Camera** (6): UniFi G5 Bullet, Dome Ultra, Pro, Turret Ultra, AI LPR, **UNVR Pro** (NEW)
- **Toegangscontrole** (4): UniFi Access Hub, UA-Lite, UA-Pro, Starter Kit
- **WiFi** (4): UniFi AP Indoor/Outdoor, Mesh, **USW-Lite-8-PoE** (NEW)
- **Verlichting** (2): Solar LED Pad, Slimme Lichtmast
- **Betaalsystemen** (2): Adyen Betaalterminal, Self-Service Kiosk
- **Douchelezers** (3): Basis, Pro, Enterprise

### Leveranciers & Logistiek
- 5 leveranciers met GPS-coördinaten (Nice Benelux, UI.com, Sanitec, Adyen, Van Loon)
- Haversine afstandsberekening (hemelsbreed * 1.3 = wegafstand)
- Reiskosten: startfee + km-prijs * afstand * 2 (heen+terug) + uurtarief * reistijd * 2
- Partner matching gesorteerd op verified status + afstand
- Reiskosten per categorie in offerte (dichtstbijzijnde leverancier per productcategorie)

### Paywall (Free / Pro / Enterprise)
- **Free**: Configurator, AI aanbevelingen, projecten opslaan
- **Pro**: + PDF export, AI offertetekst
- **Enterprise**: + Partner matching, Leveranciers dashboard
- Upgrade modal met plan-selectie

### AI & Automatisering
- **Rule-based AI Advisor** (lichtgewicht, geen GPT-calls):
  - Sanitair: 1 unit per 20 standplaatsen
  - WiFi: 1 AP per 30 standplaatsen
  - Camera: minimaal bij toegangswegen
  - Slagboom: bij > 10 standplaatsen
  - Verlichting: altijd adviseren
  - Betaalsysteem: bij sanitair zonder douchelezer
  - Kentekenherkenning: bij slagboom + camera
  - Mesh WiFi: bij > 50 standplaatsen
- Excel/CSV import met AI kolom-matching (GPT-5.2)
- Website scraper met AI productextractie (GPT-5.2)
- Smart plattegrond analyse (Vision, GPT-5.2)
- AI offertetekst generatie (GPT-5.2)

### Codebase Refactoring
- App.js: 1885 → 852 regels (-55%)
- 5 losse step-componenten: Step1ProjectDetails, Step2Terrain, Step3Products, Step4Energy, Step5Quote
- Gedeelde constanten (categoryIcons, categoryColors) geëxporteerd vanuit Step3Products

### Labels & Terminologie
- "Investering" (geen CAPEX), "Operational Lease" (geen OPEX)
- "60 maanden incl. SLA" zichtbaar als tekst
- Adyen-only (geen muntautomaten)

## Backlog

### P1 - High
- [ ] Energie stap: hybrid/offgrid berekening (zonnepanelen, accu's, warmtepomp) - functioneel maken
- [ ] RECRA Logo (PNG/SVG nodig van gebruiker)
- [ ] Product scraper: 2D/3D afbeelding generatie per product

### P2 - Medium
- [ ] Partner portal: leveranciers uploaden productcatalogus
- [ ] Auth systeem (echte login/registratie voor paywall persistentie)
- [ ] Deel configuratie via URL
- [ ] 3D canvas weergave

### P3 - Future
- [ ] AR preview, CRM integratie, Grenke lease, White-label
