"""
Supabase Integration Module — Strategic platform features.
Handles: Benchmark tracking, Lead scoring, Scenario comparisons, Session analytics.
"""
import os
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from supabase import create_client, Client

logger = logging.getLogger(__name__)

supabase_router = APIRouter(prefix="/platform", tags=["Platform & Analytics"])

# ==================== SUPABASE CLIENT ====================

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

supabase: Client = None

def get_supabase() -> Client:
    global supabase
    if supabase is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise HTTPException(status_code=500, detail="Supabase not configured")
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase


async def init_supabase_tables():
    """Initialize Supabase tables via REST API. Tables must be created in Supabase dashboard or via SQL."""
    try:
        sb = get_supabase()
        # Test connection by querying
        sb.table("configurator_sessions").select("id").limit(1).execute()
        logger.info("Supabase connection OK — tables accessible")
        return True
    except Exception as e:
        logger.warning(f"Supabase tables not yet created or connection issue: {e}")
        logger.info("Run the SQL migration in Supabase Dashboard → SQL Editor")
        return False


# ==================== SQL MIGRATION (return as string for dashboard) ====================

MIGRATION_SQL = """
-- ============================================
-- RECRA Platform — Supabase Tables
-- ============================================

-- 1. Configurator Sessions (lead scoring + analytics)
CREATE TABLE IF NOT EXISTS configurator_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id TEXT NOT NULL,
    flow_type TEXT NOT NULL CHECK (flow_type IN ('recreatie', 'chalet', 'fec')),
    started_at TIMESTAMPTZ DEFAULT NOW(),
    last_activity TIMESTAMPTZ DEFAULT NOW(),
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'completed', 'abandoned')),
    lead_score INT DEFAULT 0,
    budget_range TEXT,
    phase TEXT DEFAULT 'orientatie' CHECK (phase IN ('orientatie', 'vergelijking', 'concreet')),
    contact_email TEXT,
    contact_name TEXT,
    contact_phone TEXT,
    company_name TEXT,
    notes TEXT
);

-- 2. Configuration Snapshots (what they configured)
CREATE TABLE IF NOT EXISTS configuration_snapshots (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id TEXT NOT NULL,
    flow_type TEXT NOT NULL,
    snapshot_at TIMESTAMPTZ DEFAULT NOW(),
    config_data JSONB NOT NULL DEFAULT '{}',
    total_investment NUMERIC DEFAULT 0,
    total_lease_monthly NUMERIC DEFAULT 0,
    selected_models JSONB DEFAULT '[]',
    selected_suppliers JSONB DEFAULT '[]'
);

-- 3. Benchmark Data (aggregated trends)
CREATE TABLE IF NOT EXISTS benchmark_entries (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    recorded_at TIMESTAMPTZ DEFAULT NOW(),
    flow_type TEXT NOT NULL,
    metric_type TEXT NOT NULL,
    metric_key TEXT NOT NULL,
    metric_value NUMERIC NOT NULL DEFAULT 0,
    meta JSONB DEFAULT '{}'
);

-- 4. Scenarios (saved comparisons)
CREATE TABLE IF NOT EXISTS scenarios (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    name TEXT NOT NULL,
    flow_type TEXT NOT NULL,
    scenario_type TEXT DEFAULT 'basis' CHECK (scenario_type IN ('basis', 'luxe', 'max_bezetting')),
    config_data JSONB NOT NULL DEFAULT '{}',
    total_investment NUMERIC DEFAULT 0,
    total_lease_monthly NUMERIC DEFAULT 0,
    annual_revenue NUMERIC DEFAULT 0,
    roi_years NUMERIC DEFAULT 0,
    cashflow_monthly NUMERIC DEFAULT 0,
    notes TEXT
);

-- 5. Partner/Supplier Preferences (preferred partner tracking)
CREATE TABLE IF NOT EXISTS partner_interactions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    recorded_at TIMESTAMPTZ DEFAULT NOW(),
    supplier_id TEXT NOT NULL,
    supplier_name TEXT NOT NULL,
    flow_type TEXT NOT NULL,
    interaction_type TEXT DEFAULT 'view' CHECK (interaction_type IN ('view', 'select', 'configure', 'quote')),
    session_id TEXT
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_sessions_flow ON configurator_sessions(flow_type);
CREATE INDEX IF NOT EXISTS idx_sessions_status ON configurator_sessions(status);
CREATE INDEX IF NOT EXISTS idx_snapshots_session ON configuration_snapshots(session_id);
CREATE INDEX IF NOT EXISTS idx_benchmark_type ON benchmark_entries(flow_type, metric_type);
CREATE INDEX IF NOT EXISTS idx_scenarios_session ON scenarios(session_id);
CREATE INDEX IF NOT EXISTS idx_partner_supplier ON partner_interactions(supplier_id);

-- Enable Row Level Security (optional, for future auth)
ALTER TABLE configurator_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE configuration_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE benchmark_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE scenarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE partner_interactions ENABLE ROW LEVEL SECURITY;

-- Allow service role full access
CREATE POLICY "Service role full access" ON configurator_sessions FOR ALL USING (true);
CREATE POLICY "Service role full access" ON configuration_snapshots FOR ALL USING (true);
CREATE POLICY "Service role full access" ON benchmark_entries FOR ALL USING (true);
CREATE POLICY "Service role full access" ON scenarios FOR ALL USING (true);
CREATE POLICY "Service role full access" ON partner_interactions FOR ALL USING (true);
"""


# ==================== API ROUTES ====================

@supabase_router.get("/migration-sql")
async def get_migration_sql():
    """Return the SQL migration script to run in Supabase Dashboard."""
    return {"sql": MIGRATION_SQL, "instructions": "Ga naar Supabase Dashboard → SQL Editor → New Query → Plak deze SQL → Run"}


@supabase_router.get("/health")
async def platform_health():
    """Check Supabase connection health."""
    try:
        sb = get_supabase()
        result = sb.table("configurator_sessions").select("id").limit(1).execute()
        return {"status": "connected", "supabase": True, "tables_ready": True}
    except Exception as e:
        return {"status": "not_ready", "supabase": bool(SUPABASE_URL), "error": str(e),
                "action": "Run migration SQL via GET /api/platform/migration-sql"}


# --- Session Tracking (Lead Scoring) ---

@supabase_router.post("/sessions/start")
async def start_session(data: dict):
    """Start a new configurator session for tracking."""
    sb = get_supabase()
    session = {
        "session_id": data.get("session_id"),
        "flow_type": data.get("flow_type", "recreatie"),
        "status": "active",
        "lead_score": 0,
        "phase": "orientatie",
    }
    try:
        result = sb.table("configurator_sessions").insert(session).execute()
        return {"ok": True, "session": result.data[0] if result.data else session}
    except Exception as e:
        logger.error(f"Failed to start session: {e}")
        return {"ok": False, "error": str(e)}


@supabase_router.post("/sessions/update")
async def update_session(data: dict):
    """Update session with lead scoring data."""
    sb = get_supabase()
    session_id = data.get("session_id")
    updates = {
        "last_activity": datetime.now(timezone.utc).isoformat(),
        "lead_score": data.get("lead_score", 0),
        "phase": data.get("phase", "orientatie"),
        "budget_range": data.get("budget_range"),
        "status": data.get("status", "active"),
    }
    # Optional contact info
    for field in ["contact_email", "contact_name", "contact_phone", "company_name"]:
        if data.get(field):
            updates[field] = data[field]

    try:
        result = sb.table("configurator_sessions").update(updates).eq("session_id", session_id).execute()
        return {"ok": True, "updated": len(result.data) if result.data else 0}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# --- Configuration Snapshots ---

@supabase_router.post("/snapshots/save")
async def save_snapshot(data: dict):
    """Save a configuration snapshot."""
    sb = get_supabase()
    snapshot = {
        "session_id": data.get("session_id"),
        "flow_type": data.get("flow_type"),
        "config_data": data.get("config_data", {}),
        "total_investment": data.get("total_investment", 0),
        "total_lease_monthly": data.get("total_lease_monthly", 0),
        "selected_models": data.get("selected_models", []),
        "selected_suppliers": data.get("selected_suppliers", []),
    }
    try:
        result = sb.table("configuration_snapshots").insert(snapshot).execute()
        return {"ok": True, "snapshot_id": result.data[0]["id"] if result.data else None}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# --- Scenarios ---

@supabase_router.post("/scenarios/save")
async def save_scenario(data: dict):
    """Save a scenario comparison."""
    sb = get_supabase()
    scenario = {
        "session_id": data.get("session_id"),
        "name": data.get("name", "Naamloos scenario"),
        "flow_type": data.get("flow_type"),
        "scenario_type": data.get("scenario_type", "basis"),
        "config_data": data.get("config_data", {}),
        "total_investment": data.get("total_investment", 0),
        "total_lease_monthly": data.get("total_lease_monthly", 0),
        "annual_revenue": data.get("annual_revenue", 0),
        "roi_years": data.get("roi_years", 0),
        "cashflow_monthly": data.get("cashflow_monthly", 0),
        "notes": data.get("notes"),
    }
    try:
        result = sb.table("scenarios").insert(scenario).execute()
        return {"ok": True, "scenario": result.data[0] if result.data else None}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@supabase_router.get("/scenarios")
async def get_all_scenarios():
    """Get all scenarios."""
    sb = get_supabase()
    try:
        result = sb.table("scenarios").select("*").order("created_at", desc=True).limit(50).execute()
        return result.data or []
    except Exception as e:
        return []


@supabase_router.get("/scenarios/{session_id}")
async def get_scenarios(session_id: str):
    """Get all scenarios for a session."""
    sb = get_supabase()
    try:
        result = sb.table("scenarios").select("*").eq("session_id", session_id).order("created_at").execute()
        return result.data or []
    except Exception as e:
        return []


# --- Partner Interactions ---

@supabase_router.post("/partners/track")
async def track_partner(data: dict):
    """Track supplier/partner interaction."""
    sb = get_supabase()
    interaction = {
        "supplier_id": data.get("supplier_id"),
        "supplier_name": data.get("supplier_name"),
        "flow_type": data.get("flow_type"),
        "interaction_type": data.get("interaction_type", "view"),
        "session_id": data.get("session_id"),
    }
    try:
        result = sb.table("partner_interactions").insert(interaction).execute()
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# --- Benchmark / Trends Dashboard ---

@supabase_router.post("/benchmark/record")
async def record_benchmark(data: dict):
    """Record a benchmark data point."""
    sb = get_supabase()
    entry = {
        "flow_type": data.get("flow_type"),
        "metric_type": data.get("metric_type"),
        "metric_key": data.get("metric_key"),
        "metric_value": data.get("metric_value", 0),
        "meta": data.get("meta", {}),
    }
    try:
        result = sb.table("benchmark_entries").insert(entry).execute()
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@supabase_router.get("/benchmark/trends")
async def get_benchmark_trends(flow_type: str = None):
    """Get benchmark trends — most chosen models, avg investment, top suppliers."""
    sb = get_supabase()
    try:
        # Most selected models
        query = sb.table("benchmark_entries").select("*")
        if flow_type:
            query = query.eq("flow_type", flow_type)
        result = query.order("recorded_at", desc=True).limit(200).execute()
        entries = result.data or []

        # Aggregate
        model_counts = {}
        supplier_counts = {}
        investments = []

        for e in entries:
            mt = e.get("metric_type")
            mk = e.get("metric_key")
            mv = e.get("metric_value", 0)
            if mt == "model_selected":
                model_counts[mk] = model_counts.get(mk, 0) + 1
            elif mt == "supplier_selected":
                supplier_counts[mk] = supplier_counts.get(mk, 0) + 1
            elif mt == "total_investment":
                investments.append(mv)

        top_models = sorted(model_counts.items(), key=lambda x: -x[1])[:10]
        top_suppliers = sorted(supplier_counts.items(), key=lambda x: -x[1])[:5]
        avg_investment = round(sum(investments) / len(investments)) if investments else 0

        return {
            "total_sessions": len(set(e.get("meta", {}).get("session_id", "") for e in entries)),
            "top_models": [{"name": k, "count": v} for k, v in top_models],
            "top_suppliers": [{"name": k, "count": v} for k, v in top_suppliers],
            "avg_investment": avg_investment,
            "total_data_points": len(entries),
        }
    except Exception as e:
        return {"total_sessions": 0, "top_models": [], "top_suppliers": [], "avg_investment": 0, "error": str(e)}


# --- Lead Overview ---

@supabase_router.get("/leads")
async def get_leads(status: str = None, min_score: int = None):
    """Get leads with filtering."""
    sb = get_supabase()
    try:
        query = sb.table("configurator_sessions").select("*")
        if status:
            query = query.eq("status", status)
        if min_score:
            query = query.gte("lead_score", min_score)
        result = query.order("last_activity", desc=True).limit(50).execute()
        return result.data or []
    except Exception as e:
        return []
