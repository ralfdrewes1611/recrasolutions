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
- 22 producten in 8 categorieen (Muntautomaat verwijderd, alleen Adyen)
- Canvas met zones, dekking toggle, snap-to-grid (24px)
- AI aanbevelingen, plattegrond analyse (Vision), PDF offerte export
- Project CRUD (opslaan/laden/verwijderen)
- RECRA branding: Cream #FDF9ED, Dark Olive #244628, Bright Green #70C26C

### Iteratie 4-5 (April 4, 2026)
- "CAPEX" -> "Investering" / "Aankoopkosten"
- "OPEX" -> "Operational Lease" met zichtbare tekst "60 maanden incl. SLA"
- Sanitair configurator in Step 5 (Adyen, 4 modules)
- Click-to-place mechanisme
- Realistische sanitair maten: 3x6m, 6x8m, 8x12m
- Rechthoekige standplaatsen: 8x10m normaal, 12x15m XL
- Rondrit wegenloop (4 wegzones)

### Iteratie 6 (April 4, 2026)
- **Custom pointer drag**: Muisknop ingedrukt houden op product icoon, slepen naar canvas, loslaten = geplaatst
- **Drag ghost**: Visueel preview-element dat de cursor volgt tijdens slepen
- **Icoon | 2D toggle**: Duidelijke schakelknop in canvas toolbar
- **2D weergave**: Producten als op-schaal rechthoeken (CANVAS_SCALE=10px/m) met afmetingen erin
- **Icoon weergave**: Compacte 48x48 iconen (legacy)
- **Afmetingen op kaarten**: 3x6m, 6x8m, 8x12m etc. getoond naast prijs
- **Partner toekomst**: Gebruiker wil data van partners ontvangen om producten toe te voegen

## Prioritized Backlog

### P0 - Done
- [x] Core wizard flow + Canvas + Drag/Click-to-place
- [x] Investering/Operational Lease labels
- [x] Sanitair samenstelling in offerte
- [x] 2D toggle + op-schaal weergave
- [x] Realistische afmetingen
- [x] Pointer-based drag

### P1 - High Priority
- [ ] Dynamisch terrein: layout past zich aan op geuploade plattegrond
- [ ] Energie stap: volledige hybrid/offgrid berekening
- [ ] RECRA Logo integratie (PNG/SVG nodig)
- [ ] App.js opsplitsen in componenten

### P2 - Medium Priority
- [ ] Partner portal: data ontvangen van leveranciers voor producten
- [ ] Authenticatie (Free/Pro/Enterprise)
- [ ] Deel configuratie via unieke URL

### P3 - Nice to Have
- [ ] AR preview, Drone data, Live sensors
- [ ] CRM integratie, Grenke lease, White-label
