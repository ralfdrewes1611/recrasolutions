import React, { useState } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import {
  X, Loader2, Sparkles, Check, Star, TrendingUp,
  ChevronDown, ChevronUp, DollarSign, Clock,
} from 'lucide-react';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const TIER_STYLES = [
  { border: '#e5e2d9', bg: '#fafaf7', accent: '#777', badge: 'Budget', badgeBg: '#f0ede6' },
  { border: '#70C26C', bg: '#f0fdf4', accent: '#244628', badge: 'Populair', badgeBg: '#70C26C' },
  { border: '#f59e0b', bg: '#fffbeb', accent: '#92400e', badge: 'Premium', badgeBg: '#f59e0b' },
];

export function ScenarioCompare({ flowType, projectDescription, investmentRange, onClose }) {
  const [scenarios, setScenarios] = useState(null);
  const [loading, setLoading] = useState(false);
  const [expandedIdx, setExpandedIdx] = useState(1); // Standaard expanded by default

  const generate = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API}/crm/scenarios/generate`, {
        flow_type: flowType || 'recreatie',
        project_beschrijving: projectDescription || 'Recreatiepark configuratie',
        investering_range: investmentRange || '€25K - €100K',
      });
      setScenarios(res.data.scenarios);
      toast.success(`${res.data.source === 'ai' ? 'AI' : 'Standaard'} scenario's gegenereerd`);
    } catch {
      toast.error('Scenario generatie mislukt');
    } finally {
      setLoading(false);
    }
  };

  if (!scenarios) {
    return (
      <div className="bg-white border border-[#e5e2d9] rounded-2xl p-5" data-testid="scenario-trigger">
        <div className="text-center">
          <Sparkles className="text-[#f59e0b] mx-auto mb-3" size={28} />
          <h3 className="text-sm font-bold text-[#333] mb-1">3 Offerte Scenario's</h3>
          <p className="text-xs text-[#777] mb-4">
            Budget, Standaard & Premium — vergelijk en kies de beste optie voor uw park.
          </p>
          <button
            onClick={generate}
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 text-xs font-medium bg-[#244628] text-white rounded-xl py-3 hover:bg-[#1a341d] disabled:opacity-50 transition-all"
            data-testid="generate-scenarios-btn"
          >
            {loading ? <><Loader2 size={14} className="animate-spin" /> Scenario's genereren...</> : <><Sparkles size={14} /> Genereer 3 scenario's</>}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div data-testid="scenario-results">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-bold text-[#333] flex items-center gap-1.5">
          <Sparkles size={14} className="text-[#f59e0b]" /> Offerte Scenario's
        </h3>
        {onClose && (
          <button onClick={onClose} className="text-[#999] hover:text-[#333]" data-testid="close-scenarios">
            <X size={16} />
          </button>
        )}
      </div>

      <div className="space-y-3">
        {scenarios.map((sc, i) => {
          const style = TIER_STYLES[i] || TIER_STYLES[0];
          const isExpanded = expandedIdx === i;

          return (
            <div
              key={sc.naam}
              className="rounded-xl overflow-hidden transition-all"
              style={{ border: `2px solid ${style.border}`, background: style.bg }}
              data-testid={`scenario-${i}`}
            >
              {/* Header */}
              <button
                onClick={() => setExpandedIdx(isExpanded ? -1 : i)}
                className="w-full text-left p-4"
                data-testid={`scenario-toggle-${i}`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span
                      className="text-[9px] font-bold uppercase px-2 py-0.5 rounded-full"
                      style={{
                        background: i === 1 ? style.badgeBg : `${style.badgeBg}20`,
                        color: i === 1 ? 'white' : style.accent,
                      }}
                    >
                      {style.badge}
                    </span>
                    <span className="text-sm font-bold" style={{ color: style.accent }}>
                      {sc.naam}
                    </span>
                  </div>
                  {isExpanded ? <ChevronUp size={16} className="text-[#999]" /> : <ChevronDown size={16} className="text-[#999]" />}
                </div>

                <p className="text-xs text-[#777] mt-1">{sc.beschrijving}</p>

                {/* Key metrics */}
                <div className="flex items-center gap-4 mt-3">
                  <div className="flex items-center gap-1">
                    <DollarSign size={12} className="text-[#70C26C]" />
                    <span className="text-xs font-bold" style={{ color: style.accent }}>
                      € {(sc.investering || 0).toLocaleString('nl-NL')}
                    </span>
                  </div>
                  <div className="flex items-center gap-1">
                    <TrendingUp size={12} className="text-[#f59e0b]" />
                    <span className="text-[10px] text-[#777]">
                      € {(sc.lease_maand || 0).toLocaleString('nl-NL')}/mnd
                    </span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Clock size={12} className="text-[#2563eb]" />
                    <span className="text-[10px] text-[#777]">
                      {sc.terugverdientijd_maanden || 0} mnd
                    </span>
                  </div>
                </div>
              </button>

              {/* Expanded content */}
              {isExpanded && (
                <div className="px-4 pb-4 space-y-3 border-t" style={{ borderColor: `${style.border}50` }}>
                  {/* Products */}
                  <div className="pt-3">
                    <div className="text-[9px] text-[#999] uppercase tracking-wider mb-1.5">Producten</div>
                    <div className="flex flex-wrap gap-1.5">
                      {(sc.producten || []).map((p, j) => (
                        <span key={j} className="text-[10px] bg-white border border-[#e5e2d9] text-[#555] px-2 py-1 rounded-full flex items-center gap-1">
                          <Check size={9} className="text-[#70C26C]" /> {p}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Voordelen */}
                  {sc.voordelen?.length > 0 && (
                    <div>
                      <div className="text-[9px] text-[#999] uppercase tracking-wider mb-1.5">Voordelen</div>
                      <div className="space-y-1">
                        {sc.voordelen.map((v, j) => (
                          <div key={j} className="text-[10px] text-[#555] flex items-start gap-1.5">
                            <Star size={10} className="text-[#f59e0b] mt-0.5 flex-shrink-0" /> {v}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Geschikt voor */}
                  {sc.geschikt_voor && (
                    <div className="text-[10px] text-[#777] bg-white/60 border border-[#e5e2d9] rounded-lg p-2">
                      Geschikt voor: <span className="font-medium text-[#333]">{sc.geschikt_voor}</span>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Regenerate */}
      <button
        onClick={generate}
        disabled={loading}
        className="w-full mt-3 text-center text-[10px] text-[#999] hover:text-[#555] py-2 flex items-center justify-center gap-1"
        data-testid="regenerate-scenarios"
      >
        {loading ? <Loader2 size={10} className="animate-spin" /> : <Sparkles size={10} />} Opnieuw genereren
      </button>
    </div>
  );
}
