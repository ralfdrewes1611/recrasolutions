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
- **3 Configuratie Flows**: Recreatie Infra (27 prod), Chalet & Stay (24 prod), FEC & Experience (21 prod)
- Flow-specifieke productfiltering per branche
- Canvas met zones, dekking toggle, snap-to-grid (24px)
- Click-to-place + custom pointer drag + selectie + verplaatsing
- Icoon | 2D toggle (op-schaal rechthoeken)
- Project CRUD, PDF offerte export
- **RECRA Logo** geïntegreerd (wit/donker PNG versies)
- RECRA branding: #244628 header, #FDF9ED achtergrond, #70C26C accenten

### Producten (27 stuks, echte producten)
- Sanitair (3), Slagboom (3), Camera (6 incl. UNVR Pro), Toegangscontrole (4), WiFi (4 incl. USW-Lite-8-PoE), Verlichting (2), Betaalsystemen (2), Douchelezers (3)

### Leveranciers & Logistiek
- 5 leveranciers met GPS-coördinaten
- Haversine afstandsberekening (hemelsbreed * 1.3 = wegafstand)
- Reiskosten: startfee + km-prijs * afstand * 2 + uurtarief * reistijd * 2
- Per-categorie reiskosten in offerte (dichtstbijzijnde leverancier)

### Paywall (Free / Pro / Enterprise)
- **Free**: Configurator, AI aanbevelingen, projecten opslaan
- **Pro**: + PDF export, AI offertetekst
- **Enterprise**: + Partner matching, Leveranciers dashboard
- Upgrade modal met plan-selectie

### Energie Stap (Functioneel)
- 3 modi: Netaansluiting, Hybrid, Off-Grid
- **Zonnepanelen**: 450Wp/stuk, €320/panel, 3.5 zonuren NL, dekking %, aanbevolen panelen
- **Accu-opslag**: LiFePO4 5kWh/unit, €2800/unit, autonomie-uren, aanbevolen units
- **Warmtepomp**: COP 3.5, €8500, jaarlijkse besparing kWh
- **Zonneboiler**: 300L, €3200
- **Wateropvang & hergebruik**: €12000
- **Windturbine**: 3kW micro, €6500
- Investering overzicht met terugverdientijd en jaarlijkse besparing
- Energie-investering geïntegreerd in offerte totaal

### AI & Automatisering
- **Rule-based AI Advisor** (8 regels, geen GPT-calls): sanitair, wifi, camera, slagboom, verlichting, betaalsysteem, kentekenherkenning, mesh wifi
- Excel/CSV import met AI kolom-matching (GPT-5.2)
- Smart plattegrond analyse (Vision, GPT-5.2)
- AI offertetekst generatie (GPT-5.2)

### Codebase
- App.js: 1885 → ~870 regels (-54%)
- 5 step-componenten + FlowSelector + SupplierPanel

## Backlog

### P1 - High
- [ ] Auth systeem (login/registratie voor paywall persistentie)
- [ ] Deel configuratie via URL

### P2 - Medium
- [ ] Partner portal: leveranciers uploaden productcatalogus
- [ ] Product scraper: 2D afbeeldingen per product
- [ ] 3D canvas weergave

### P3 - Future
- [ ] AR preview, CRM integratie, Grenke lease, White-label
