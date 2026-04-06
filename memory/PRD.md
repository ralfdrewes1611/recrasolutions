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
- Eigen product catalog, leveranciers, revenue engine

## Implemented Features

### Core Platform
- Flow Selector met 3 flows + RECRA logo
- Paywall (Free/Pro/Enterprise) met upgrade modal
- RECRA branding: #244628 header, #FDF9ED achtergrond, #70C26C accenten

### Recreatie & Chalet Configurator
- 27 echte producten (UniFi cameras, Nice slagbomen, sanitair, WiFi, etc.)
- Custom pointer-based drag & click-to-place 2D canvas
- Haversine leveranciersmatching met reiskosten per categorie
- Rule-based AI advisor (8 regels)
- Functionele energie stap (zonnepanelen, accu's, warmtepomp, etc.)
- PDF offerte export

### FEC Revenue Engine (NIEUW)
- **14 FEC producten** over 5 categorieën:
  - Arcade & Games: Shuffleboard, Arcade Wall, Air Hockey
  - Karting: Elektrische Kartbaan (8 karts), Mini Kart Track
  - Interactive: X-Wall Klimwand, Escape Room, VR Experience
  - Indoor Play: Mega Speeltoestel, Toddler Zone, Trampoline Park
  - Food & Beverage: Snackbar, Drinks Station, Premium Restaurant
- **5 FEC leveranciers**: X-Wall, Shuffly, Heemskerk Play, Pro Karting, Time Mission
- **Revenue Engine**: daily_revenue, monthly_revenue, ROI, break-even per product
- **Top 5 Geldverdieners**: gesorteerd op €/m²/maand
- **Zone-based layout**: Entree, Arcade, Karting, Interactive, Indoor Play, Horeca, Routing
- **FEC AI Rules** (8 regels):
  - Geen horeca → +30% omzet advies
  - Karting → high revenue flag
  - Lage capaciteit → high turnover suggestie
  - Geen interactive → verblijftijd advies
  - Plafondhoogte check
  - Onbenutte ruimte signalering
  - Entree zone advies
  - Cross-sell naar Recreatie/Chalet bij grote locaties
- **Canvas**: zone-gebaseerd met kleuren, hotspot indicators (€/m²)
- **Business Case sidebar**: live investering, omzet/mnd, break-even

### Codebase
- App.js: ~870 regels (was 1885)
- FecWizard.jsx: ~390 regels
- fec_engine.py: ~340 regels
- 5 step-componenten + FlowSelector + SupplierPanel

## Backlog

### P1 - High
- [ ] Auth systeem (login/registratie voor paywall persistentie)
- [ ] FEC zone drag/resize op canvas (interactieve indeling)

### P2 - Medium
- [ ] Partner portal: leveranciers uploaden productcatalogus
- [ ] Deel configuratie via URL
- [ ] 3D canvas weergave
- [ ] FEC PDF export met business case

### P3 - Future
- [ ] AR preview, CRM integratie, Grenke lease, White-label
