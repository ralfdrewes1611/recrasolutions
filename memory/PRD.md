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
- Drag & drop site planner with snap-to-grid (24px)
- 8 product categories: sanitair, slagbomen, camera's, WiFi, verlichting, betaalsystemen, toegangscontrole, douchelezers
- Real-time CAPEX / Operational Lease calculation
- AI-powered recommendations
- PDF quote export with RECRA branding
- Zone definition tools
- Project management (save/load/delete)
- Modular sanitair configuration in quote step
- Only Adyen payment terminals (no coin machines)

## What's Been Implemented

### Iteration 1-2 (April 3, 2026)
- Products API with 22 seeded products (Muntautomaat removed)
- Projects CRUD API
- Quote calculation API
- AI recommendations API (rule-based + GPT-5.2)
- Floor plan analysis API (OpenAI Vision)
- PDF quote generation API
- 5-step wizard navigation
- Product catalog with category filtering
- Drag & drop canvas with snap-to-grid
- Real-time quote sidebar
- UI Redesign - Light theme matching recrasolutions.com
- Douchelezers - 3 douchelezer products
- Zone Definition Tool - Polygon drawing on canvas
- Project Management - Save/Load/Delete projects
- Coverage Toggle - Show/hide product coverage radius

### Iteration 4 (April 4, 2026)
- **Drag & Drop Fix** - Fixed empty state overlay blocking drag events (pointer-events-none)
- **OPEX -> Operational Lease** - Renamed throughout app and PDF, with tooltip "60 maanden incl. SLA"
- **Muntautomaat Removed** - Purged from DB seed and existing databases on startup
- **Sanitair Configurator** - Moved to Step 5 (Offerte) with modular options:
  - Extra douches (+EUR 2.500)
  - Familiecabine (+EUR 3.000)
  - Warmtepomp (+EUR 4.500)
  - Zonneboiler (+EUR 3.500)
- **Drag Feedback** - Visual border change + "Laat hier los" text when dragging over canvas
- **Adyen Only** - All payment via Adyen contactless (PIN/Apple Pay/Google Pay)

## Prioritized Backlog

### P0 - Critical (Done)
- [x] Core configurator flow
- [x] Product placement on canvas (drag & drop working)
- [x] Quote calculation
- [x] PDF export
- [x] Zone definition tools
- [x] Project save/load functionality
- [x] RECRA branding/look & feel
- [x] Operational Lease terminology
- [x] Adyen-only payments (no coin machines)
- [x] Modular sanitair configuration in offerte

### P1 - High Priority
- [ ] AI Auto-Layout - AI-generated terrain layout with road and pitches
- [ ] 2D Top-Down Product View Toggle on canvas
- [ ] RECRA Logo integration (need PNG/SVG from user)
- [ ] Energy step - full calculation logic with hybrid/offgrid options
- [ ] App.js refactoring into smaller components

### P2 - Medium Priority
- [ ] User authentication (Free/Pro/Enterprise tiers)
- [ ] Partner/admin portal
- [ ] Share configuration via unique URL

### P3 - Nice to Have
- [ ] AR preview
- [ ] Drone data integration
- [ ] Live sensor simulation
- [ ] CRM integration
- [ ] Lease partner integration (Grenke)
- [ ] White-label support
