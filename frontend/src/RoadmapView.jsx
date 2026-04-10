import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  ArrowLeft, PenTool, FileCheck, Hammer, TrendingUp, ChevronRight,
  CheckCircle2, Clock, Users, FileText, Coins,
} from 'lucide-react';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const PHASE_ICONS = [PenTool, FileCheck, Hammer, TrendingUp];
const PHASE_COLORS = ['#2563eb', '#f59e0b', '#10b981', '#244628'];

export function RoadmapView({ flowType, onBack, projectSummary }) {
  const [roadmap, setRoadmap] = useState(null);
  const [expandedPhase, setExpandedPhase] = useState(null);

  useEffect(() => {
    axios.get(`${API}/roadmap/phases/${flowType}`)
      .then(r => setRoadmap(r.data))
      .catch(() => {});
  }, [flowType]);

  if (!roadmap) {
    return (
      <div className="min-h-screen bg-[#FDF9ED] flex items-center justify-center">
        <div className="text-[#777] text-sm">Roadmap laden...</div>
      </div>
    );
  }

  const flowLabels = { recreatie: 'Recreatie Infra', chalet: 'Chalet & Stay', fec: 'FEC & Experience' };

  return (
    <div className="min-h-screen bg-[#FDF9ED]" data-testid="roadmap-view">
      <header className="bg-[#244628] text-white px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button onClick={onBack} className="hover:opacity-80 transition-opacity" data-testid="roadmap-back">
              <ArrowLeft size={20} />
            </button>
            <div>
              <div className="text-sm font-bold">Idee naar Realisatie</div>
              <div className="text-xs text-white/60">{flowLabels[flowType] || flowType}</div>
            </div>
          </div>
          <div className="text-xs text-white/50">
            Geschatte doorlooptijd: {roadmap.estimated_total_duration || '6-12 maanden'}
          </div>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-6 py-8">
        {/* Project summary if available */}
        {projectSummary && (
          <div className="bg-white border border-[#e5e2d9] rounded-2xl p-5 mb-8" data-testid="roadmap-project-summary">
            <div className="text-xs text-[#999] uppercase tracking-wider mb-2">Uw Configuratie</div>
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm font-bold text-[#333]">{projectSummary.name || 'Project'}</div>
                <div className="text-xs text-[#777]">{projectSummary.details || ''}</div>
              </div>
              {projectSummary.investment && (
                <div className="text-right">
                  <div className="text-xs text-[#999]">Investering</div>
                  <div className="text-lg font-bold text-[#244628]">€ {projectSummary.investment.toLocaleString('nl-NL')}</div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Timeline */}
        <div className="space-y-0">
          {roadmap.phases.map((phase, i) => {
            const Icon = PHASE_ICONS[i] || TrendingUp;
            const color = PHASE_COLORS[i] || '#244628';
            const isExpanded = expandedPhase === phase.id;
            const isLast = i === roadmap.phases.length - 1;

            return (
              <div key={phase.id} className="relative" data-testid={`roadmap-phase-${phase.id}`}>
                {/* Timeline connector */}
                {!isLast && (
                  <div className="absolute left-6 top-14 bottom-0 w-0.5 bg-[#e5e2d9]" />
                )}

                <button
                  onClick={() => setExpandedPhase(isExpanded ? null : phase.id)}
                  className="w-full text-left"
                  data-testid={`roadmap-toggle-${phase.id}`}
                >
                  <div className="flex items-start gap-4 p-4 rounded-2xl hover:bg-white/80 transition-all">
                    {/* Phase circle */}
                    <div className="relative z-10 flex-shrink-0">
                      <div
                        className="w-12 h-12 rounded-xl flex items-center justify-center shadow-sm"
                        style={{ backgroundColor: `${color}15`, border: `2px solid ${color}30` }}
                      >
                        <Icon size={22} style={{ color }} />
                      </div>
                    </div>

                    {/* Phase content */}
                    <div className="flex-1 min-w-0 pt-1">
                      <div className="flex items-center gap-3 mb-1">
                        <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full" style={{ color, backgroundColor: `${color}12` }}>
                          Fase {phase.fase}
                        </span>
                        <span className="text-xs text-[#999] flex items-center gap-1">
                          <Clock size={11} /> {phase.duur}
                        </span>
                      </div>
                      <h3 className="text-base font-bold text-[#333]">{phase.titel}</h3>
                      <p className="text-sm text-[#777] mt-0.5">{phase.beschrijving}</p>

                      <div className="flex items-center gap-4 mt-2 text-xs text-[#999]">
                        <span className="flex items-center gap-1"><Coins size={11} /> {phase.kosten_indicatie}</span>
                        <span className="flex items-center gap-1"><Users size={11} /> {phase.betrokken_partijen.length} partijen</span>
                      </div>
                    </div>

                    {/* Expand indicator */}
                    <ChevronRight
                      size={18}
                      className={`text-[#ccc] mt-3 flex-shrink-0 transition-transform ${isExpanded ? 'rotate-90' : ''}`}
                    />
                  </div>
                </button>

                {/* Expanded detail */}
                {isExpanded && (
                  <div className="ml-16 mr-4 mb-6 space-y-4" data-testid={`roadmap-detail-${phase.id}`}>
                    {/* Acties */}
                    <div className="bg-white rounded-xl border border-[#e5e2d9] p-4">
                      <h4 className="text-xs font-bold text-[#333] uppercase tracking-wider mb-3">Actiepunten</h4>
                      <div className="space-y-2">
                        {phase.acties.map((actie, j) => (
                          <div key={j} className="flex items-start gap-2.5">
                            <div className="w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5" style={{ backgroundColor: `${color}15` }}>
                              <span className="text-[9px] font-bold" style={{ color }}>{j + 1}</span>
                            </div>
                            <span className="text-sm text-[#555]">{actie}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Deliverables */}
                    <div className="bg-white rounded-xl border border-[#e5e2d9] p-4">
                      <h4 className="text-xs font-bold text-[#333] uppercase tracking-wider mb-3 flex items-center gap-1.5">
                        <FileText size={13} className="text-[#70C26C]" /> Deliverables
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {phase.deliverables.map((d, j) => (
                          <span key={j} className="text-xs bg-[#70C26C]/10 text-[#244628] px-3 py-1.5 rounded-full flex items-center gap-1.5">
                            <CheckCircle2 size={11} className="text-[#70C26C]" /> {d}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Betrokken partijen */}
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="text-[10px] text-[#999] uppercase tracking-wider">Betrokken:</span>
                      {phase.betrokken_partijen.map((p, j) => (
                        <span key={j} className="text-[10px] bg-white border border-[#e5e2d9] text-[#555] px-2.5 py-1 rounded-full">
                          {p}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* CTA */}
        <div className="mt-8 bg-[#244628] rounded-2xl p-6 text-center text-white" data-testid="roadmap-cta">
          <h3 className="text-lg font-bold mb-2">Klaar om te starten?</h3>
          <p className="text-sm text-white/70 mb-4">
            Neem contact op met RECRA Solutions voor een vrijblijvend gesprek over uw project.
          </p>
          <div className="flex items-center justify-center gap-3">
            <a href="mailto:info@recrasolutions.com" className="bg-[#70C26C] text-[#244628] px-6 py-2.5 rounded-xl text-sm font-bold hover:bg-[#5fb35b] transition-colors" data-testid="roadmap-contact">
              Neem Contact Op
            </a>
            <button onClick={onBack} className="text-white/60 hover:text-white text-sm underline" data-testid="roadmap-back-config">
              Terug naar configurator
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
