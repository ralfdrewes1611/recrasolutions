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
- Multi-step wizard configurator (Project → Terrain → Products → Quote)
- Drag & drop site planner with snap-to-grid (24px)
- 8 product categories: sanitair, slagbomen, camera's, WiFi, verlichting, betaalsystemen, toegangscontrole, douchelezers
- Real-time CAPEX/OPEX calculation
- AI-powered recommendations
- PDF quote export with RECRA branding
- Zone definition tools
- Project management (save/load/delete)

## What's Been Implemented

### Iteration 1 (April 3, 2026)
- ✅ Products API with 19 seeded products
- ✅ Projects CRUD API
- ✅ Quote calculation API
- ✅ AI recommendations API
- ✅ Floor plan analysis API (OpenAI Vision)
- ✅ PDF quote generation API
- ✅ 4-step wizard navigation
- ✅ Product catalog with category filtering
- ✅ Drag & drop canvas with snap-to-grid
- ✅ Real-time quote sidebar

### Iteration 2 (April 3, 2026)
- ✅ **UI Redesign** - Light theme matching recrasolutions.com (Inter font, green accents #4a9b7f, #2d5a3d)
- ✅ **Douchelezers** - Added 4 new douchelezer products (RECRA specialty product)
- ✅ **Zone Definition Tool** - Polygon drawing on canvas with finish/cancel controls
- ✅ **Project Management** - Save/Load/Delete projects via dialog
- ✅ **Coverage Toggle** - Show/hide product coverage radius
- ✅ 23 total products across 8 categories
- ✅ Header with Projecten, Opslaan buttons
- ✅ Canvas toolbar with Select and Zone tools

## Prioritized Backlog

### P0 - Critical (Done)
- [x] Core configurator flow
- [x] Product placement on canvas
- [x] Quote calculation
- [x] PDF export
- [x] Zone definition tools
- [x] Project save/load functionality
- [x] RECRA branding/look & feel

### P1 - High Priority (Future)
- [ ] User authentication (Free/Pro/Enterprise tiers)
- [ ] Partner/admin portal
- [ ] Floor plan AI auto-detection improvements

### P2 - Medium Priority (Future)
- [ ] CRM integration
- [ ] Lease partner integration (Grenke)
- [ ] White-label support
- [ ] Sharing/collaboration features

### P3 - Nice to Have (Future)
- [ ] AR preview
- [ ] Drone data integration
- [ ] Live sensor simulation
- [ ] Partner marketplace

## Next Tasks
1. User authentication met Free/Pro/Enterprise tiers
2. Partner/admin portal voor projectverdeling
3. Verbeterde AI zone-herkenning
4. Reserveringssysteem integraties
