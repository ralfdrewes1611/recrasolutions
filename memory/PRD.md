# RECRA Solutions Configurator Platform - PRD

## Original Problem Statement
Een geavanceerde AI-gedreven configurator & offerteplatform voor RECRA Solutions, gericht op recreatieparken, campings en outdoor hospitality. Een schaalbare tool waarin klanten zelfstandig hun terrein kunnen configureren, producten kunnen plaatsen op een plattegrond en realtime een offerte + technisch plan ontvangen.

## Architecture
- **Frontend**: React 19 + Tailwind CSS + Shadcn UI
- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **AI**: OpenAI GPT-5.2 via Emergent Integrations

## User Personas
1. **Park Manager** - Configures their recreation park with products
2. **Sales Representative** - Uses tool for customer quotes
3. **Technical Planner** - Plans product placement and coverage

## Core Requirements
- Multi-step wizard configurator (Project > Terrein > Producten > Energie > Offerte)
- Drag & drop AND click-to-place site planner with snap-to-grid (24px)
- 8 product categories: sanitair, slagbomen, camera's, WiFi, verlichting, betaalsystemen, toegangscontrole, douchelezers
- Real-time Investering / Operational Lease calculation (60 mnd incl. SLA)
- AI-powered recommendations
- PDF quote export with RECRA branding
- Zone definition tools
- Project management (save/load/delete)
- Modular sanitair configuration in quote step (Adyen only)
- Realistic product dimensions (sanitair: 3x6m, 6x8m, 8x12m)
- Realistic pitch sizes (normal: 8x10m=80m2, XL: 12x15m=180m2)

## What's Been Implemented

### Iteration 1-2 (April 3, 2026)
- Products API with 22 seeded products
- Projects CRUD API, Quote calculation API
- AI recommendations API (rule-based + GPT-5.2)
- Floor plan analysis API (OpenAI Vision)
- PDF quote generation API
- 5-step wizard, Product catalog with filtering
- Canvas with zones and coverage toggle

### Iteration 4 (April 4, 2026)
- Drag & Drop fix (pointer-events-none on empty state)
- OPEX -> Operational Lease renamed
- Muntautomaat removed from DB
- Sanitair configurator moved to Step 5

### Iteration 5 (April 4, 2026)
- **Click-to-place**: Click product in sidebar, then click canvas to place
- **"CAPEX" removed**: Sidebar now shows "Investering", Step 5 shows "Aankoopkosten"
- **Lease text visible**: "60 mnd incl. SLA" shown as text, not tooltip
- **Realistic sanitair dimensions**: Compact 3x6m, Medium 6x8m, Premium 8x12m
- **Rectangular pitches**: AI layout generates 8x10m normal and 12x15m XL pitches
- **Road loop**: 4 road zones (Hoofdweg, Weg links, Weg rechts, Weg onder)
- **Product dimensions shown**: On product cards next to price
- **Canvas cursor**: Changes to copy cursor when click-to-place is active

## Prioritized Backlog

### P0 - Critical (Done)
- [x] Core configurator flow
- [x] Product placement (drag + click-to-place)
- [x] Quote calculation
- [x] PDF export
- [x] Zone definition tools
- [x] Project save/load
- [x] RECRA branding
- [x] Operational Lease terminology (no CAPEX/OPEX)
- [x] Adyen-only payments
- [x] Modular sanitair configuration
- [x] Realistic dimensions

### P1 - High Priority
- [ ] Dynamic terrain: layout adapts to uploaded plattegrond instead of static grid
- [ ] 2D Top-Down Product View Toggle on canvas
- [ ] RECRA Logo integration (need PNG/SVG)
- [ ] Energy step - full calculation with hybrid/offgrid components
- [ ] App.js refactoring into smaller components

### P2 - Medium Priority
- [ ] User authentication (Free/Pro/Enterprise)
- [ ] Partner/admin portal
- [ ] Share configuration via unique URL

### P3 - Nice to Have
- [ ] AR preview, Drone data, Live sensors
- [ ] CRM integration, Grenke lease, White-label
