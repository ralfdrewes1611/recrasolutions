import React, { useState } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import {
  X, ChevronRight, ChevronLeft, Sparkles, Loader2, FileText,
  TrendingUp, Shield, Zap, Users, Leaf, Handshake,
  Download, Phone, CheckCircle2, AlertTriangle, ArrowRight,
  Mail, Building, User,
} from 'lucide-react';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const STEPS = [
  { id: 'organisatie', label: 'Organisatie', icon: Shield },
  { id: 'project', label: 'Project', icon: Zap },
  { id: 'financieel', label: 'Financieel', icon: TrendingUp },
  { id: 'impact', label: 'Impact', icon: Users },
  { id: 'versterkers', label: 'Versterkers', icon: Leaf },
];

const INITIAL = {
  sector: '', rechtsvorm: '', projectomschrijving: '', doel: '',
  investering: '', eigen_investering: '', gebruikers: '',
  samenwerking: '', duurzaamheid: '',
};

function RadioGroup({ options, value, onChange, name }) {
  return (
    <div className="grid grid-cols-2 gap-2">
      {options.map(opt => (
        <button
          key={opt}
          type="button"
          onClick={() => onChange(opt)}
          data-testid={`${name}-${opt.toLowerCase().replace(/[^a-z0-9]/g, '-')}`}
          className={`text-left text-xs px-3 py-2.5 rounded-lg border transition-all ${
            value === opt
              ? 'border-[#244628] bg-[#244628] text-white font-medium'
              : 'border-[#e5e2d9] bg-white text-[#555] hover:border-[#244628]/30'
          }`}
        >
          {opt}
        </button>
      ))}
    </div>
  );
}

function ScoreBar({ score, maxScore = 10 }) {
  const pct = (score / maxScore) * 100;
  const color = score <= 4 ? '#ef4444' : score <= 7 ? '#f59e0b' : '#10b981';
  return (
    <div className="relative h-2.5 bg-[#f0ede6] rounded-full overflow-hidden">
      <div
        className="absolute left-0 top-0 h-full rounded-full transition-all duration-700"
        style={{ width: `${pct}%`, backgroundColor: color }}
      />
    </div>
  );
}

function KansLabel({ kans }) {
  const cfg = {
    laag: { color: '#ef4444', bg: '#fef2f2', label: 'LAAG' },
    middel: { color: '#f59e0b', bg: '#fffbeb', label: 'MIDDEL' },
    hoog: { color: '#10b981', bg: '#f0fdf4', label: 'HOOG' },
  }[kans] || { color: '#777', bg: '#f5f5f5', label: kans?.toUpperCase() };
  return (
    <span
      className="text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider"
      style={{ color: cfg.color, backgroundColor: cfg.bg }}
      data-testid="kans-label"
    >
      {cfg.label}
    </span>
  );
}

export function SubsidyModule({ onClose, projectContext }) {
  const [step, setStep] = useState(0);
  const [form, setForm] = useState({ ...INITIAL, ...projectContext });
  const [result, setResult] = useState(null);
  const [aiResult, setAiResult] = useState(null);
  const [document, setDocument] = useState(null);
  const [loading, setLoading] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);
  const [docLoading, setDocLoading] = useState(false);
  const [contact, setContact] = useState({ naam: '', email: '', telefoon: '', bedrijf: '' });
  const [leadSaved, setLeadSaved] = useState(false);
  const [followUpHtml, setFollowUpHtml] = useState(null);
  const [savingLead, setSavingLead] = useState(false);

  const set = (key, val) => setForm(prev => ({ ...prev, [key]: val }));

  const canProceed = () => {
    if (step === 0) return form.sector && form.rechtsvorm;
    if (step === 1) return form.projectomschrijving && form.doel;
    if (step === 2) return form.investering && form.eigen_investering;
    if (step === 3) return form.gebruikers;
    if (step === 4) return form.samenwerking && form.duurzaamheid;
    return true;
  };

  const submitCheck = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API}/subsidy/check`, form);
      setResult(res.data);
      toast.success('Subsidie check voltooid');
    } catch {
      toast.error('Fout bij subsidie check');
    } finally {
      setLoading(false);
    }
  };

  const runAiAnalyse = async () => {
    setAiLoading(true);
    try {
      const res = await axios.post(`${API}/subsidy/ai-analyse`, form);
      setAiResult(res.data.ai_analyse);
      if (res.data.ai_analyse) toast.success('AI analyse voltooid');
      else toast.error(res.data.ai_error || 'AI analyse mislukt');
    } catch {
      toast.error('AI analyse mislukt');
    } finally {
      setAiLoading(false);
    }
  };

  const generateDocument = async () => {
    setDocLoading(true);
    try {
      const res = await axios.post(`${API}/subsidy/generate-document`, form);
      if (res.data.status === 'success') {
        setDocument(res.data.document);
        toast.success('Subsidie-aanvraag gegenereerd');
      } else {
        toast.error(res.data.error || 'Document generatie mislukt');
      }
    } catch {
      toast.error('Document generatie mislukt');
    } finally {
      setDocLoading(false);
    }
  };

  const saveLead = async () => {
    if (!contact.naam || !contact.email) { toast.error('Vul naam en e-mail in'); return; }
    setSavingLead(true);
    try {
      await axios.post(`${API}/crm/leads`, {
        ...contact,
        flow_type: form.sector?.toLowerCase() || 'recreatie',
        bron: 'subsidie_check',
        project_beschrijving: form.projectomschrijving,
        subsidie_score: result?.score,
        subsidie_kans: result?.kans,
        subsidie_range: result?.subsidie_range,
        investering: form.investering,
      });
      setLeadSaved(true);
      toast.success('Gegevens opgeslagen — wij nemen contact op');

      // Generate follow-up email
      const fRes = await axios.post(`${API}/crm/follow-up/generate`, {
        naam: contact.naam,
        email: contact.email,
        subsidie_score: result?.score,
        subsidie_kans: result?.kans,
        subsidie_range: result?.subsidie_range,
        project_beschrijving: form.projectomschrijving,
        investering: form.investering,
      });
      setFollowUpHtml(fRes.data.email_html);
    } catch {
      toast.error('Opslaan mislukt');
    } finally {
      setSavingLead(false);
    }
  };

  const nextStep = () => {
    if (step < 4) setStep(step + 1);
    else submitCheck();
  };

  // RESULTS VIEW
  if (result) {
    return (
      <div className="flex flex-col h-full" data-testid="subsidy-results">
        {/* Header */}
        <div className="bg-[#244628] text-white p-4 flex-shrink-0">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-bold">Subsidie Check Resultaat</h2>
            <button onClick={onClose} className="text-white/50 hover:text-white" data-testid="close-subsidy-results">
              <X size={18} />
            </button>
          </div>
          <div className="flex items-center gap-3">
            <KansLabel kans={result.kans} />
            <span className="text-2xl font-bold">{result.score}/10</span>
          </div>
          <ScoreBar score={result.score} />
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {/* Subsidie range */}
          <div className="bg-white border border-[#e5e2d9] rounded-xl p-4" data-testid="subsidie-range">
            <div className="text-[10px] text-[#999] uppercase tracking-wider mb-1">Verwachte bijdrage</div>
            <div className="text-xl font-bold text-[#244628]">{result.subsidie_range}</div>
            <div className="text-xs text-[#777] mt-1">Beste aanpak: <span className="font-medium text-[#333]">{result.advies}</span></div>
          </div>

          {/* Score breakdown */}
          <div className="bg-white border border-[#e5e2d9] rounded-xl p-4" data-testid="score-breakdown">
            <div className="text-[10px] text-[#999] uppercase tracking-wider mb-3">Score Opbouw</div>
            <div className="space-y-2">
              {Object.entries(result.breakdown).map(([key, val]) => {
                if (typeof val === 'string') return (
                  <div key={key} className="text-xs text-[#ef4444] flex items-center gap-1.5">
                    <AlertTriangle size={12} /> {val}
                  </div>
                );
                return (
                  <div key={key} className="flex items-center justify-between">
                    <span className="text-xs text-[#555]">{val.label}</span>
                    <div className="flex items-center gap-2">
                      <div className="w-16 h-1.5 bg-[#f0ede6] rounded-full overflow-hidden">
                        <div className="h-full rounded-full bg-[#70C26C]" style={{ width: `${(val.score / val.max) * 100}%` }} />
                      </div>
                      <span className="text-[10px] font-mono text-[#999] w-8">{val.score}/{val.max}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* AI Analyse */}
          {!aiResult ? (
            <button
              onClick={runAiAnalyse}
              disabled={aiLoading}
              className="w-full flex items-center justify-center gap-2 text-xs font-medium bg-[#244628] text-white rounded-xl py-3 hover:bg-[#1a341d] transition-all disabled:opacity-50"
              data-testid="run-ai-analyse"
            >
              {aiLoading ? <><Loader2 size={14} className="animate-spin" /> AI analyseert...</> : <><Sparkles size={14} /> AI Subsidie Analyse</>}
            </button>
          ) : (
            <div className="bg-white border border-[#70C26C]/30 rounded-xl p-4 space-y-3" data-testid="ai-analyse-result">
              <div className="flex items-center gap-1.5 text-xs font-bold text-[#244628]">
                <Sparkles size={13} className="text-[#70C26C]" /> AI Analyse
              </div>

              {aiResult.toelichting && (
                <p className="text-xs text-[#555] leading-relaxed">{aiResult.toelichting}</p>
              )}

              {aiResult.subsidie_range && (
                <div className="text-sm font-bold text-[#244628]">AI schatting: {aiResult.subsidie_range}</div>
              )}

              {aiResult.regelingen?.length > 0 && (
                <div>
                  <div className="text-[10px] text-[#999] uppercase tracking-wider mb-1.5">Mogelijke regelingen</div>
                  <div className="flex flex-wrap gap-1.5">
                    {aiResult.regelingen.map((r, i) => (
                      <span key={i} className="text-[10px] bg-[#70C26C]/10 text-[#244628] px-2 py-1 rounded-full">{r}</span>
                    ))}
                  </div>
                </div>
              )}

              {aiResult.verbeterpunten?.length > 0 && (
                <div>
                  <div className="text-[10px] text-[#999] uppercase tracking-wider mb-1.5">Verbeter je kans</div>
                  <div className="space-y-1">
                    {aiResult.verbeterpunten.map((v, i) => (
                      <div key={i} className="text-xs text-[#555] flex items-start gap-1.5">
                        <CheckCircle2 size={12} className="text-[#f59e0b] mt-0.5 flex-shrink-0" />
                        {v}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Document generator */}
          {!document ? (
            <button
              onClick={generateDocument}
              disabled={docLoading}
              className="w-full flex items-center justify-center gap-2 text-xs font-medium border border-[#244628] text-[#244628] rounded-xl py-3 hover:bg-[#244628] hover:text-white transition-all disabled:opacity-50"
              data-testid="generate-document"
            >
              {docLoading ? <><Loader2 size={14} className="animate-spin" /> Document genereren...</> : <><FileText size={14} /> Genereer subsidie-aanvraag</>}
            </button>
          ) : (
            <div className="bg-white border border-[#e5e2d9] rounded-xl p-4" data-testid="subsidy-document">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-1.5 text-xs font-bold text-[#244628]">
                  <FileText size={13} className="text-[#70C26C]" /> Subsidie-aanvraag
                </div>
                <button
                  onClick={() => {
                    const w = window.open('', '_blank');
                    w.document.write(`<html><head><style>body{font-family:'Segoe UI',sans-serif;max-width:700px;margin:40px auto;padding:20px;color:#333;line-height:1.7;} h1,h2,h3{color:#244628;} @media print{body{margin:0;padding:20px;}}</style></head><body>${document.replace(/\n/g,'<br/>')}</body></html>`);
                    w.document.close();
                    w.print();
                  }}
                  className="text-[10px] text-[#70C26C] hover:underline flex items-center gap-1"
                  data-testid="print-document"
                >
                  <Download size={11} /> Print / PDF
                </button>
              </div>
              <div className="text-xs text-[#555] leading-relaxed whitespace-pre-line max-h-60 overflow-y-auto">
                {document}
              </div>
            </div>
          )}

          {/* Contact form / CRM Lead */}
          {!leadSaved ? (
            <div className="bg-[#244628] rounded-xl p-4 space-y-3" data-testid="subsidy-cta">
              <div className="text-xs text-white font-medium">Laat uw gegevens achter</div>
              <div className="text-[10px] text-white/50">Wij nemen binnen 24 uur contact op met een persoonlijk advies.</div>
              <input
                value={contact.naam} onChange={e => setContact(c => ({ ...c, naam: e.target.value }))}
                placeholder="Naam *" data-testid="contact-naam"
                className="w-full text-xs px-3 py-2 rounded-lg bg-white/10 border border-white/15 text-white placeholder-white/30 focus:outline-none focus:border-[#70C26C]"
              />
              <input
                value={contact.email} onChange={e => setContact(c => ({ ...c, email: e.target.value }))}
                placeholder="E-mail *" type="email" data-testid="contact-email"
                className="w-full text-xs px-3 py-2 rounded-lg bg-white/10 border border-white/15 text-white placeholder-white/30 focus:outline-none focus:border-[#70C26C]"
              />
              <div className="flex gap-2">
                <input
                  value={contact.telefoon} onChange={e => setContact(c => ({ ...c, telefoon: e.target.value }))}
                  placeholder="Telefoon" data-testid="contact-telefoon"
                  className="flex-1 text-xs px-3 py-2 rounded-lg bg-white/10 border border-white/15 text-white placeholder-white/30 focus:outline-none focus:border-[#70C26C]"
                />
                <input
                  value={contact.bedrijf} onChange={e => setContact(c => ({ ...c, bedrijf: e.target.value }))}
                  placeholder="Bedrijf" data-testid="contact-bedrijf"
                  className="flex-1 text-xs px-3 py-2 rounded-lg bg-white/10 border border-white/15 text-white placeholder-white/30 focus:outline-none focus:border-[#70C26C]"
                />
              </div>
              <button
                onClick={saveLead} disabled={savingLead || !contact.naam || !contact.email}
                className="w-full flex items-center justify-center gap-2 text-xs font-bold bg-[#70C26C] text-white rounded-lg py-2.5 hover:bg-[#5fb35b] transition-all disabled:opacity-40"
                data-testid="save-lead-btn"
              >
                {savingLead ? <><Loader2 size={14} className="animate-spin" /> Opslaan...</> : <><Handshake size={14} /> Laat RECRA dit voor je regelen</>}
              </button>
              <a href="mailto:info@recrasolutions.com?subject=Plan%20adviesgesprek"
                className="w-full flex items-center justify-center gap-2 text-xs font-medium text-white/60 border border-white/15 rounded-lg py-2 hover:bg-white/10 transition-all"
                data-testid="cta-plan-gesprek"
              >
                <Phone size={12} /> Of bel direct: +31 634200253
              </a>
            </div>
          ) : (
            <div className="space-y-3">
              <div className="bg-[#f0fdf4] border border-[#86efac] rounded-xl p-4 text-center" data-testid="lead-saved">
                <CheckCircle2 size={24} className="text-[#10b981] mx-auto mb-2" />
                <div className="text-sm font-bold text-[#244628]">Bedankt, {contact.naam}!</div>
                <div className="text-xs text-[#555] mt-1">Wij nemen zo snel mogelijk contact met u op.</div>
              </div>

              {followUpHtml && (
                <div className="bg-white border border-[#e5e2d9] rounded-xl p-3" data-testid="follow-up-preview">
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-[10px] text-[#999] uppercase tracking-wider flex items-center gap-1"><Mail size={10} /> Follow-up mail preview</div>
                    <button
                      onClick={() => {
                        const w = window.open('', '_blank');
                        w.document.write(followUpHtml);
                        w.document.close();
                      }}
                      className="text-[10px] text-[#70C26C] hover:underline"
                      data-testid="view-followup"
                    >
                      Bekijk volledig
                    </button>
                  </div>
                  <div className="text-[10px] text-[#555]">
                    Aan: {contact.email}<br />
                    Onderwerp: Uw subsidie-check resultaat — {result?.kans} kans
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Reset */}
          <button
            onClick={() => { setResult(null); setAiResult(null); setDocument(null); setStep(0); }}
            className="w-full text-center text-[10px] text-[#999] hover:text-[#555] py-2"
            data-testid="reset-subsidy"
          >
            Opnieuw berekenen
          </button>
        </div>
      </div>
    );
  }

  // INTAKE FORM
  return (
    <div className="flex flex-col h-full" data-testid="subsidy-module">
      {/* Header */}
      <div className="bg-[#244628] text-white p-4 flex-shrink-0">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-sm font-bold">Financiering & Subsidie Check</h2>
            <p className="text-[10px] text-white/50 mt-0.5">Ontdek of uw project in aanmerking komt</p>
          </div>
          <button onClick={onClose} className="text-white/50 hover:text-white" data-testid="close-subsidy">
            <X size={18} />
          </button>
        </div>

        {/* Step indicator */}
        <div className="flex items-center gap-1 mt-3">
          {STEPS.map((s, i) => (
            <div key={s.id} className="flex items-center flex-1">
              <div className={`h-1 flex-1 rounded-full transition-all ${i <= step ? 'bg-[#70C26C]' : 'bg-white/15'}`} />
            </div>
          ))}
        </div>
        <div className="flex items-center gap-1.5 mt-2">
          {React.createElement(STEPS[step].icon, { size: 13, className: 'text-[#70C26C]' })}
          <span className="text-[10px] text-white/60">Stap {step + 1}/5 — {STEPS[step].label}</span>
        </div>
      </div>

      {/* Form */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {step === 0 && (
          <>
            <div>
              <label className="text-[10px] text-[#999] uppercase tracking-wider block mb-2">Wat is uw type organisatie?</label>
              <RadioGroup name="sector" options={['Recreatie', 'Zorg', 'Kinderopvang', 'Overig']} value={form.sector} onChange={v => set('sector', v)} />
            </div>
            <div>
              <label className="text-[10px] text-[#999] uppercase tracking-wider block mb-2">Rechtsvorm</label>
              <RadioGroup name="rechtsvorm" options={['BV', 'VOF', 'Stichting', 'Anders']} value={form.rechtsvorm} onChange={v => set('rechtsvorm', v)} />
            </div>
          </>
        )}

        {step === 1 && (
          <>
            <div>
              <label className="text-[10px] text-[#999] uppercase tracking-wider block mb-2">Wat wilt u realiseren?</label>
              <textarea
                value={form.projectomschrijving}
                onChange={e => set('projectomschrijving', e.target.value.slice(0, 200))}
                maxLength={200}
                rows={3}
                placeholder="Beschrijf kort uw project..."
                className="w-full text-xs border border-[#e5e2d9] rounded-lg px-3 py-2.5 bg-white text-[#333] placeholder-[#bbb] focus:outline-none focus:border-[#244628] resize-none"
                data-testid="project-beschrijving"
              />
              <div className="text-right text-[9px] text-[#bbb] mt-0.5">{form.projectomschrijving.length}/200</div>
            </div>
            <div>
              <label className="text-[10px] text-[#999] uppercase tracking-wider block mb-2">Wat is het hoofddoel?</label>
              <RadioGroup name="doel" options={['Beleving verbeteren', 'Kosten besparen', 'Digitaliseren', 'Zorg / welzijn verbeteren']} value={form.doel} onChange={v => set('doel', v)} />
            </div>
          </>
        )}

        {step === 2 && (
          <>
            <div>
              <label className="text-[10px] text-[#999] uppercase tracking-wider block mb-2">Wat is de totale investering?</label>
              <RadioGroup name="investering" options={['< €10K', '€10K - €25K', '€25K - €100K', '> €100K']} value={form.investering} onChange={v => set('investering', v)} />
            </div>
            <div>
              <label className="text-[10px] text-[#999] uppercase tracking-wider block mb-2">Bent u bereid zelf te investeren?</label>
              <RadioGroup name="eigen-investering" options={['Ja', 'Nee', 'Deels']} value={form.eigen_investering} onChange={v => set('eigen_investering', v)} />
            </div>
          </>
        )}

        {step === 3 && (
          <div>
            <label className="text-[10px] text-[#999] uppercase tracking-wider block mb-2">Hoeveel gebruikers / bezoekers?</label>
            <RadioGroup name="gebruikers" options={['< 100', '100 - 1.000', '1.000 - 10.000', '> 10.000']} value={form.gebruikers} onChange={v => set('gebruikers', v)} />
          </div>
        )}

        {step === 4 && (
          <>
            <div>
              <label className="text-[10px] text-[#999] uppercase tracking-wider block mb-2">Werkt u samen met andere partijen?</label>
              <RadioGroup name="samenwerking" options={['Ja', 'Nee']} value={form.samenwerking} onChange={v => set('samenwerking', v)} />
            </div>
            <div>
              <label className="text-[10px] text-[#999] uppercase tracking-wider block mb-2">Zit er een duurzaam component in het project?</label>
              <RadioGroup name="duurzaamheid" options={['Ja', 'Nee']} value={form.duurzaamheid} onChange={v => set('duurzaamheid', v)} />
            </div>
          </>
        )}
      </div>

      {/* Navigation */}
      <div className="p-4 border-t border-[#e5e2d9] flex gap-2 flex-shrink-0">
        {step > 0 && (
          <button
            onClick={() => setStep(step - 1)}
            className="flex items-center gap-1 text-xs text-[#777] hover:text-[#333] px-3 py-2"
            data-testid="subsidy-prev"
          >
            <ChevronLeft size={14} /> Terug
          </button>
        )}
        <button
          onClick={nextStep}
          disabled={!canProceed() || loading}
          className="flex-1 flex items-center justify-center gap-1.5 text-xs font-medium bg-[#244628] text-white rounded-xl py-2.5 hover:bg-[#1a341d] disabled:opacity-40 transition-all"
          data-testid="subsidy-next"
        >
          {loading ? (
            <><Loader2 size={14} className="animate-spin" /> Berekenen...</>
          ) : step < 4 ? (
            <>Volgende <ChevronRight size={14} /></>
          ) : (
            <>Bereken subsidie kans <ArrowRight size={14} /></>
          )}
        </button>
      </div>
    </div>
  );
}
