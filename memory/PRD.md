# RECRA Solutions Configurator Platform - PRD

## Original Problem Statement
AI-gedreven configurator & offerteplatform voor RECRA Solutions: recreatieparken, campings en outdoor hospitality.

## Architecture
- **Frontend**: React 19 + Tailwind CSS + Shadcn UI
- **Backend**: FastAPI (Python) — server.py + ai_services.py + supplier_module.py + fec_engine.py + chalet_engine.py
- **Database**: MongoDB (35 recreatie producten incl. 8 IK informatiezuilen, 5 recreatie leveranciers + 17 FEC producten incl. 3 IK kiosken, 6 FEC leveranciers + 10 chalet modellen, 2 chalet leveranciers)
- **AI**: OpenAI GPT-5.2 via Emergent Integrations (quote text & floorplan); Rule-based AI for recommendations

## Fundamental Architecture Split

### Recreatie = Asset Placement (buiten, terrein, infra)
- 5-stappen wizard: Project > Terrein > Producten > Energie > Offerte

### Chalet & Stay = Accommodation Configurator (dedicated ChaletWizard)
- Gebaseerd op projectadmin.nl referentie
- 3-kolom layout: Filters (links) > Fotocarrousel + Plattegrond (midden) > Prijsoverzicht (rechts)
- Filters: Bestemming, Oppervlakte slider, Model Vorm (5), Dak Vorm (6)
- 10 modellen van 2 leveranciers (Kunert Group, Arcabo)
- Stijlen: Modern / Luxe / Landelijk
- Tabs: Plattegrond en 3D, Specificatie, Samenstellen
- Prijsoverzicht: Basisprijs, BTW 21%, Totaal incl. BTW, Operational Lease (60 mnd)

### FEC = Revenue Engineering (binnen, m²/m³, omzet gestuurd)
- 4-stappen wizard: Locatie > Zones > Attracties > Revenue Dashboard
- Interactive canvas: drag & resize zones, m² auto-berekening
- Revenue engine + lease pricing

## Implemented Features

### Chalet & Stay Configurator (NEW — 08 apr 2026)
- 10 chalet modellen: Plat 12/18, Zadel 12/18, L-Plat 16, Lessenaars 14, Mansarde 20, Schilddak 15, T-Vorm 22, Dubbel 24
- 2 leveranciers: Kunert Group, Arcabo
- Filters: bestemming (recreatie/pre-mantelzorg), oppervlakte (30-120 m²), model vorm (rechthoek/L-vorm/T-vorm/dubbel), dak vorm (platdak/zadeldak/lessenaars/mansarde/schilddak)
- Stijlen per model: Modern, Luxe, Landelijk (niet alle stijlen beschikbaar per model)
- Pricing engine: basisprijs + BTW 21% + operational lease (1.8% factor, 60 maanden)
- Geselecteerd samenvatting: model, m², leverancier, stijl, slk/bdk
- Tabs: Plattegrond (carrousel + plattegrond), Specificatie (specs grid), Samenstellen (opties keuken/badkamer/terras/interieur/klimaat/duurzaamheid)

### FEC Revenue Engine
- 17 FEC producten met lease pricing (price_lease_monthly) over 6 categorieën
- Correctie: **X-Wall Battle Arena** (geen klimwand)
- 6 FEC leveranciers: X-Wall, Shuffly, Heemskerk Play, Pro Karting, Time Mission, IK Display Solutions
- 3 IK indoor kiosken (entree categorie): 21.5" tilted, 43" landscape tilted, 55" portrait
- Revenue Engine: daily/monthly revenue, ROI, break-even, lease per product
- **Operational Lease in dashboard**: totaal lease/mnd, netto winst (omzet - lease)
- Top Performers met lease per product
- Business Case sidebar met lease breakdown
- Interactive Canvas: drag & resize zones
- FEC AI Rules (8 regels)

### Recreatie Configurator
- 35 echte producten incl. 8 IK Display Solutions informatiezuilen & kiosken
- Nieuwe categorie: **Informatiezuilen & Kiosken** (5 outdoor + 3 indoor)
- Custom pointer-based drag & click-to-place 2D canvas
- Haversine leveranciersmatching, energie stap, PDF export

### Platform
- 3 flows (Recreatie, Chalet, FEC), RECRA logo, Paywall (Free/Pro/Enterprise)

## Backlog

### P0
- [ ] Auth systeem (login/registratie voor paywall persistentie)

### P1
- [ ] FEC PDF export met business case
- [ ] Geocoding (adres -> lat/lng)

### P2
- [ ] Partner portal, Deel configuratie via URL, 3D canvas

### P3
- [ ] AR preview, CRM, Grenke lease, White-label, Benchmark Mode
