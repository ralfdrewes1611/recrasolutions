import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  ArrowLeft, BarChart3, Users, TrendingUp, Building2, Tent,
  DollarSign, Target, Activity, ChevronRight, Eye,
} from 'lucide-react';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export function PlatformDashboard({ onBack }) {
  const [trends, setTrends] = useState(null);
  const [leads, setLeads] = useState([]);
  const [scenarios, setScenarios] = useState([]);
  const [activeTab, setActiveTab] = useState('trends');

  useEffect(() => {
    const load = async () => {
      try {
        const [tRes, lRes] = await Promise.all([
          axios.get(`${API}/platform/benchmark/trends`),
          axios.get(`${API}/platform/leads`),
        ]);
        setTrends(tRes.data);
        setLeads(lRes.data);
      } catch { /* tables might be empty */ }
    };
    load();
  }, []);

  const tabs = [
    { id: 'trends', label: 'Trends & Benchmark', icon: BarChart3 },
    { id: 'leads', label: 'Lead Scoring', icon: Users },
    { id: 'scenarios', label: 'Scenario\'s', icon: Target },
  ];

  return (
    <div className="h-screen w-full flex flex-col overflow-hidden bg-[#FDF9ED]" data-testid="platform-dashboard">
      {/* Header */}
      <header className="h-14 bg-[#244628] flex items-center justify-between px-6 flex-shrink-0">
        <div className="flex items-center gap-3">
          <button onClick={onBack} className="hover:opacity-80 transition-opacity" data-testid="dash-back-btn">
            <span className="text-white font-bold text-lg tracking-wide">RECRA</span>
          </button>
          <span className="text-white/40">|</span>
          <span className="text-[#70C26C] text-sm font-semibold">Platform Dashboard</span>
        </div>
        <div className="flex items-center gap-1">
          {tabs.map(tab => (
            <button key={tab.id} onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-1.5 text-xs px-4 py-2 rounded-full transition-all ${activeTab === tab.id ? 'bg-[#70C26C] text-[#244628] font-bold' : 'text-white/70 hover:text-white'}`}
              data-testid={`dash-tab-${tab.id}`}
            >
              <tab.icon size={14} />{tab.label}
            </button>
          ))}
        </div>
        <button onClick={onBack} className="text-white/70 hover:text-white text-sm flex items-center gap-1" data-testid="dash-back">
          <ArrowLeft size={16} /> Terug
        </button>
      </header>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6">
        {activeTab === 'trends' && <TrendsTab trends={trends} />}
        {activeTab === 'leads' && <LeadsTab leads={leads} />}
        {activeTab === 'scenarios' && <ScenariosTab />}
      </div>
    </div>
  );
}

// ==================== TRENDS TAB ====================

function TrendsTab({ trends }) {
  const t = trends || {};
  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-[#244628]">Marktinzichten & Benchmarks</h1>
        <p className="text-sm text-[#777] mt-1">Live data uit de configurator — welke modellen, leveranciers en investeringen zijn trending.</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-4 gap-4">
        <KpiCard icon={Activity} label="Sessies" value={t.total_sessions || 0} color="#70C26C" />
        <KpiCard icon={BarChart3} label="Datapunten" value={t.total_data_points || 0} color="#0891b2" />
        <KpiCard icon={DollarSign} label="Gem. Investering" value={`€${(t.avg_investment || 0).toLocaleString('nl-NL')}`} color="#8B6914" />
        <KpiCard icon={TrendingUp} label="Top Modellen" value={t.top_models?.length || 0} color="#244628" />
      </div>

      {/* Top Models & Suppliers */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-white border border-[#e5e2d9] rounded-xl p-5">
          <h3 className="text-sm font-bold text-[#333] uppercase tracking-wider mb-4 flex items-center gap-2">
            <Building2 size={16} className="text-[#70C26C]" /> Meest Gekozen Modellen
          </h3>
          {t.top_models?.length > 0 ? (
            <div className="space-y-3">
              {t.top_models.map((m, i) => (
                <div key={i} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="w-6 h-6 rounded-full bg-[#244628] text-white text-xs flex items-center justify-center font-bold">{i + 1}</span>
                    <span className="text-sm font-medium text-[#333]">{m.name}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-24 h-2 bg-[#f0ede6] rounded-full overflow-hidden">
                      <div className="h-full bg-[#70C26C] rounded-full" style={{ width: `${Math.min(100, (m.count / Math.max(1, t.top_models[0]?.count || 1)) * 100)}%` }} />
                    </div>
                    <span className="text-xs text-[#999] w-8 text-right">{m.count}x</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState text="Nog geen modelkeuzes geregistreerd" />
          )}
        </div>

        <div className="bg-white border border-[#e5e2d9] rounded-xl p-5">
          <h3 className="text-sm font-bold text-[#333] uppercase tracking-wider mb-4 flex items-center gap-2">
            <Tent size={16} className="text-[#70C26C]" /> Meest Gekozen Leveranciers
          </h3>
          {t.top_suppliers?.length > 0 ? (
            <div className="space-y-3">
              {t.top_suppliers.map((s, i) => (
                <div key={i} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="w-6 h-6 rounded-full bg-[#8B6914] text-white text-xs flex items-center justify-center font-bold">{i + 1}</span>
                    <span className="text-sm font-medium text-[#333]">{s.name}</span>
                  </div>
                  <span className="text-xs text-[#999]">{s.count}x</span>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState text="Nog geen leverancierskeuzes geregistreerd" />
          )}
        </div>
      </div>

      {/* Placeholder for future charts */}
      <div className="bg-white border border-[#e5e2d9] rounded-xl p-6">
        <h3 className="text-sm font-bold text-[#333] uppercase tracking-wider mb-3 flex items-center gap-2">
          <TrendingUp size={16} className="text-[#70C26C]" /> Investering per m² — Trend
        </h3>
        <div className="h-48 flex items-center justify-center bg-[#FDF9ED] rounded-lg border border-dashed border-[#e5e2d9]">
          <div className="text-center">
            <BarChart3 size={32} className="mx-auto mb-2 text-[#ccc]" />
            <p className="text-sm text-[#999]">Grafiek wordt automatisch gevuld naarmate meer configuraties worden opgeslagen</p>
            <p className="text-xs text-[#ccc] mt-1">Gemiddelde investering, prijsontwikkeling per categorie, NL/BE/DE vergelijking</p>
          </div>
        </div>
      </div>
    </div>
  );
}

// ==================== LEADS TAB ====================

function LeadsTab({ leads }) {
  const phaseColors = {
    orientatie: { bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200' },
    vergelijking: { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200' },
    concreet: { bg: 'bg-green-50', text: 'text-green-700', border: 'border-green-200' },
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-[#244628]">Lead Scoring & Opvolging</h1>
        <p className="text-sm text-[#777] mt-1">Wie configureert wat, budgetrange en fase — pure business intelligence.</p>
      </div>

      {/* Lead funnel summary */}
      <div className="grid grid-cols-3 gap-4">
        <FunnelCard phase="Oriëntatie" count={leads.filter(l => l.phase === 'orientatie').length} total={leads.length} color="#3b82f6" />
        <FunnelCard phase="Vergelijking" count={leads.filter(l => l.phase === 'vergelijking').length} total={leads.length} color="#d97706" />
        <FunnelCard phase="Concreet" count={leads.filter(l => l.phase === 'concreet').length} total={leads.length} color="#16a34a" />
      </div>

      {/* Leads table */}
      <div className="bg-white border border-[#e5e2d9] rounded-xl overflow-hidden">
        <div className="px-5 py-3 border-b border-[#e5e2d9] flex items-center justify-between">
          <h3 className="text-sm font-bold text-[#333]">Recente Leads ({leads.length})</h3>
        </div>
        {leads.length > 0 ? (
          <div className="divide-y divide-[#f0ede6]">
            {leads.map((lead, i) => {
              const pc = phaseColors[lead.phase] || phaseColors.orientatie;
              return (
                <div key={i} className="px-5 py-3 flex items-center justify-between hover:bg-[#FDF9ED] transition-colors">
                  <div className="flex items-center gap-4">
                    <div className="w-9 h-9 rounded-full bg-[#244628] text-white flex items-center justify-center text-xs font-bold">
                      {lead.lead_score || 0}
                    </div>
                    <div>
                      <div className="text-sm font-medium text-[#333]">
                        {lead.contact_name || lead.company_name || lead.session_id}
                      </div>
                      <div className="text-xs text-[#999] flex items-center gap-2">
                        <span className="capitalize">{lead.flow_type}</span>
                        {lead.budget_range && <span>· {lead.budget_range}</span>}
                        {lead.contact_email && <span>· {lead.contact_email}</span>}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className={`text-[10px] px-2 py-0.5 rounded-full ${pc.bg} ${pc.text} ${pc.border} border capitalize`}>
                      {lead.phase}
                    </span>
                    <span className={`text-[10px] px-2 py-0.5 rounded-full ${lead.status === 'completed' ? 'bg-green-50 text-green-700' : lead.status === 'abandoned' ? 'bg-red-50 text-red-700' : 'bg-gray-50 text-gray-600'}`}>
                      {lead.status}
                    </span>
                    <ChevronRight size={14} className="text-[#ccc]" />
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="p-8"><EmptyState text="Nog geen leads — data wordt automatisch verzameld via de configurators" /></div>
        )}
      </div>
    </div>
  );
}

// ==================== SCENARIOS TAB ====================

function ScenariosTab() {
  const [scenarios, setScenarios] = useState([]);

  useEffect(() => {
    axios.get(`${API}/platform/scenarios`).then(res => setScenarios(res.data || [])).catch(() => {});
  }, []);

  const typeLabels = { basis: 'Basis', luxe: 'Luxe', max_bezetting: 'Max Bezetting' };
  const typeColors = { basis: '#3b82f6', luxe: '#8B6914', max_bezetting: '#16a34a' };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-[#244628]">Scenario Vergelijking</h1>
        <p className="text-sm text-[#777] mt-1">Vergelijk investeringsscenario's: basis, luxe en maximale bezetting met ROI en cashflow.</p>
      </div>

      {scenarios.length > 0 ? (
        <div className="grid grid-cols-3 gap-4">
          {scenarios.map((s, i) => (
            <div key={i} className="bg-white border border-[#e5e2d9] rounded-xl p-5 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-bold text-[#333]">{s.name}</h3>
                <span className="text-[10px] px-2 py-0.5 rounded-full border font-medium" style={{ color: typeColors[s.scenario_type], borderColor: typeColors[s.scenario_type], backgroundColor: `${typeColors[s.scenario_type]}10` }}>
                  {typeLabels[s.scenario_type] || s.scenario_type}
                </span>
              </div>
              <div className="space-y-2">
                <ScenarioRow label="Investering" value={`€${(s.total_investment || 0).toLocaleString('nl-NL')}`} />
                <ScenarioRow label="Lease/mnd" value={`€${(s.total_lease_monthly || 0).toLocaleString('nl-NL')}`} />
                <ScenarioRow label="Omzet/jaar" value={`€${(s.annual_revenue || 0).toLocaleString('nl-NL')}`} />
                <ScenarioRow label="ROI" value={`${s.roi_years || 0} jaar`} highlight />
                <ScenarioRow label="Cashflow/mnd" value={`€${(s.cashflow_monthly || 0).toLocaleString('nl-NL')}`} highlight />
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white border border-[#e5e2d9] rounded-xl p-12">
          <div className="text-center">
            <Target size={48} className="mx-auto mb-4 text-[#ccc]" />
            <h3 className="text-lg font-semibold text-[#333]">Nog geen scenario's opgeslagen</h3>
            <p className="text-sm text-[#777] mt-2 max-w-md mx-auto">
              Scenario's worden automatisch aangemaakt wanneer gebruikers configuraties vergelijken (Basis vs Luxe vs Max Bezetting).
            </p>
            <div className="mt-6 grid grid-cols-3 gap-3 max-w-lg mx-auto">
              {['Basis Park', 'Luxe Upgrade', 'Max Bezetting'].map((name, i) => (
                <div key={i} className="bg-[#FDF9ED] border border-dashed border-[#e5e2d9] rounded-lg p-3 text-center">
                  <div className="text-xs font-bold text-[#244628]">{name}</div>
                  <div className="text-[10px] text-[#999] mt-1">{['10 chalets, basis', '10 chalets, luxe', '15 chalets, max'][i]}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ==================== SHARED COMPONENTS ====================

function KpiCard({ icon: Icon, label, value, color }) {
  return (
    <div className="bg-white border border-[#e5e2d9] rounded-xl p-4 flex items-center gap-4">
      <div className="w-12 h-12 rounded-xl flex items-center justify-center" style={{ backgroundColor: `${color}15` }}>
        <Icon size={22} style={{ color }} />
      </div>
      <div>
        <div className="text-[10px] text-[#999] uppercase tracking-wider">{label}</div>
        <div className="text-xl font-bold text-[#333]">{value}</div>
      </div>
    </div>
  );
}

function FunnelCard({ phase, count, total, color }) {
  const pct = total > 0 ? Math.round((count / total) * 100) : 0;
  return (
    <div className="bg-white border border-[#e5e2d9] rounded-xl p-4">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-bold text-[#333]">{phase}</span>
        <span className="text-2xl font-bold" style={{ color }}>{count}</span>
      </div>
      <div className="w-full h-2 bg-[#f0ede6] rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all" style={{ width: `${pct}%`, backgroundColor: color }} />
      </div>
      <span className="text-[10px] text-[#999] mt-1 block">{pct}% van alle leads</span>
    </div>
  );
}

function ScenarioRow({ label, value, highlight }) {
  return (
    <div className="flex justify-between text-sm">
      <span className="text-[#777]">{label}</span>
      <span className={highlight ? 'font-bold text-[#244628]' : 'font-semibold text-[#333]'}>{value}</span>
    </div>
  );
}

function EmptyState({ text }) {
  return (
    <div className="text-center py-6">
      <Eye size={24} className="mx-auto mb-2 text-[#ddd]" />
      <p className="text-sm text-[#999]">{text}</p>
    </div>
  );
}
