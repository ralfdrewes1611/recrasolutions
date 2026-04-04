# RECRA Solutions Configurator Platform - PRD

## Original Problem Statement
Een geavanceerde AI-gedreven configurator & offerteplatform voor RECRA Solutions, gericht op recreatieparken, campings en outdoor hospitality. Klanten configureren hun terrein, plaatsen producten op een plattegrond en ontvangen realtime een offerte + technisch plan.

## Architecture
- **Frontend**: React 19 + Tailwind CSS + Shadcn UI
- **Backend**: FastAPI (Python) — server.py + ai_services.py
- **Database**: MongoDB
- **AI**: OpenAI GPT-5.2 via Emergent Integrations (tekst + Vision)

## What's Been Implemented

### Core (Iteratie 1-3)
- 5-stappen wizard: Project > Terrein > Producten > Energie > Offerte
- 22 producten in 8 categorieen (alleen Adyen betaalterminals)
- Canvas met zones, dekking toggle, snap-to-grid (24px)
- AI aanbevelingen (rule-based + GPT-5.2)
- PDF offerte export met RECRA branding
- Project CRUD (opslaan/laden/verwijderen)
- RECRA branding: Cream #FDF9ED, Dark Olive #244628, Bright Green #70C26C

### Iteratie 4-7 (April 4, 2026)
- "CAPEX" -> "Investering", "OPEX" -> "Operational Lease" (60 mnd incl. SLA)
- Sanitair configurator in Step 5 (Adyen, 4 modules)
- Click-to-place + custom pointer drag met ghost preview
- Selectie + verplaatsing geplaatste items op canvas
- Icoon | 2D toggle: op-schaal rechthoeken (CANVAS_SCALE=10px/m)
- Realistische sanitair maten: 3x6m, 6x8m, 8x12m
- Rechthoekige standplaatsen: 8x10m normaal, 12x15m XL met rondrit
- Schaal-instelling voor geuploade plattegronden

### Iteratie 8 (April 4, 2026) — AI Automatisering
- **Excel/CSV Import**: Upload productlijst → AI herkent kolommen → preview → bevestig import
  - Endpoint: POST /api/ai/import-products + /api/ai/import-products/confirm
  - Component: ProductImportPanel.jsx
- **Website Scraper**: Voer URL in → AI extraheert productinfo uit de pagina
  - Endpoint: POST /api/ai/scrape-products
- **Smart Plattegrond Analyse**: Upload tekening → GPT-5.2 Vision detecteert zones, schat standplaatsen
  - Endpoint: POST /api/ai/analyze-floorplan-smart
  - Button in Step 2 na upload
- **AI Offertetekst**: Genereer professionele Nederlandse offertetekst
  - Endpoint: POST /api/ai/generate-quote-text
  - Component: AIQuoteText.jsx in Step 5

## Prioritized Backlog

### P0 - Done
- [x] Core wizard + canvas + drag/click-to-place + selectie + verplaatsing
- [x] 2D toggle + op-schaal weergave + realistische afmetingen
- [x] Investering/Operational Lease labels
- [x] Sanitair samenstelling in offerte
- [x] AI product import (Excel/CSV + Website scraper)
- [x] AI plattegrond analyse (Vision)
- [x] AI offertetekst generatie
- [x] Schaal-instelling voor plattegronden

### P1 - High Priority
- [ ] Product scraper uitbreiden: 2D→3D afbeelding generatie per product
- [ ] Dynamisch terrein: layout past zich aan op geuploade plattegrond (ipv grid)
- [ ] Energie stap: volledige hybrid/offgrid berekening
- [ ] RECRA Logo (PNG/SVG nodig van klant)
- [ ] App.js opsplitsen in componenten

### P2 - Medium Priority
- [ ] Partner portal: leveranciers leveren producten aan met specs + maten
- [ ] Auth (Free/Pro/Enterprise)
- [ ] Deel configuratie via unieke URL
- [ ] 3D canvas weergave

### P3 - Nice to Have
- [ ] AR preview, Drone data, Live sensors
- [ ] CRM integratie, Grenke lease, White-label
