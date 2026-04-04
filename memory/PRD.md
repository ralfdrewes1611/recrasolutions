# RECRA Solutions Configurator Platform - PRD

## Original Problem Statement
Een geavanceerde AI-gedreven configurator & offerteplatform voor RECRA Solutions, gericht op recreatieparken, campings en outdoor hospitality. Klanten configureren hun terrein, plaatsen producten op een plattegrond en ontvangen realtime een offerte + technisch plan.

## Architecture
- **Frontend**: React 19 + Tailwind CSS + Shadcn UI
- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **AI**: OpenAI GPT-5.2 via Emergent Integrations

## What's Been Implemented

### Core (Iteratie 1-3)
- 5-stappen wizard: Project > Terrein > Producten > Energie > Offerte
- 22 producten in 8 categorieen (alleen Adyen betaalterminals)
- Canvas met zones, dekking toggle, snap-to-grid (24px)
- AI aanbevelingen, plattegrond analyse (Vision), PDF offerte export
- Project CRUD, RECRA branding

### Iteratie 4-5
- "CAPEX" -> "Investering" / "Aankoopkosten"
- "OPEX" -> "Operational Lease" met zichtbare "60 maanden incl. SLA"
- Sanitair configurator in Step 5 (Adyen, 4 modules)
- Click-to-place, realistische maten, rechthoekige standplaatsen

### Iteratie 6
- Custom pointer drag (sidebar -> canvas) met ghost preview
- Icoon | 2D toggle knop in toolbar
- Producten als op-schaal rechthoeken (CANVAS_SCALE=10px/m)

### Iteratie 7 (April 4, 2026)
- **Selectie gefixt**: selectedProduct gewist na plaatsing, geen dubbel plaatsen meer
- **Geplaatste producten selecteerbaar**: Mousedown op canvas-item toont groene ring + draaien/verwijderen
- **Verplaatsbaar**: Mousedown + slepen verplaatst product met grid-snapping
- **Schaal-instelling**: In Step 2 bij geuploade plattegrond — meters per blokje instellen
- **Deselecteren**: Klik op lege canvas wist selectie

## Prioritized Backlog

### P0 - Done
- [x] Core wizard, canvas, drag/click-to-place
- [x] Selectie + verplaatsing geplaatste items
- [x] 2D toggle + op-schaal weergave
- [x] Schaal-instelling voor plattegronden
- [x] Investering/Operational Lease labels
- [x] Sanitair samenstelling in offerte

### P1 - High Priority
- [ ] Product scraper (Excel/website import) met 2D maten per product
- [ ] Dynamisch terrein: layout past zich aan op geuploade plattegrond
- [ ] Energie stap: volledige hybrid/offgrid berekening
- [ ] RECRA Logo (PNG/SVG nodig)
- [ ] App.js opsplitsen in componenten

### P2 - Medium Priority
- [ ] Partner portal: leveranciers leveren producten aan met specs + maten
- [ ] 2D -> 3D configurator weergave
- [ ] Auth (Free/Pro/Enterprise)
- [ ] Deel configuratie via URL

### P3 - Nice to Have
- [ ] AR preview, Drone data, Live sensors
- [ ] CRM integratie, Grenke lease, White-label
