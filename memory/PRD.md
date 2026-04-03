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
- 7 product categories: sanitair, slagbomen, camera's, WiFi, verlichting, betaalsystemen, toegangscontrole
- Real-time CAPEX/OPEX calculation
- AI-powered recommendations
- PDF quote export with RECRA branding

## What's Been Implemented (April 3, 2026)
### Backend
- ✅ Products API with 19 seeded products
- ✅ Projects CRUD API
- ✅ Quote calculation API (CAPEX/OPEX/Installation)
- ✅ AI recommendations API (rule-based + OpenAI GPT-5.2)
- ✅ Floor plan analysis API (OpenAI Vision)
- ✅ PDF quote generation API

### Frontend
- ✅ Dark theme UI with RECRA branding (blue #0ea5e9, green #10b981)
- ✅ 4-step wizard navigation
- ✅ Project configuration (name, type, spots)
- ✅ Floor plan upload with AI analysis
- ✅ Product catalog with category filtering
- ✅ Drag & drop canvas with snap-to-grid
- ✅ Coverage radius visualization
- ✅ Real-time quote sidebar
- ✅ AI recommendations panel
- ✅ PDF export functionality

## Prioritized Backlog

### P0 - Critical (Done)
- [x] Core configurator flow
- [x] Product placement on canvas
- [x] Quote calculation
- [x] PDF export

### P1 - High Priority (Future)
- [ ] Zone definition tools (polygon drawing)
- [ ] Floor plan AI auto-detection improvements
- [ ] Project list/load functionality
- [ ] Partner/admin portal

### P2 - Medium Priority (Future)
- [ ] User authentication (Free/Pro/Enterprise tiers)
- [ ] CRM integration
- [ ] Lease partner integration (Grenke)
- [ ] White-label support

### P3 - Nice to Have (Future)
- [ ] AR preview
- [ ] Drone data integration
- [ ] Live sensor simulation
- [ ] Partner marketplace

## Next Tasks
1. Improve AI recommendation accuracy
2. Add zone definition polygon tool
3. Implement project list/load from database
4. Add user authentication tiers
