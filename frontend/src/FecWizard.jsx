import React, { useState, useEffect, useMemo, useCallback, useRef } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import {
  Building2, Gamepad2, Users, DollarSign, TrendingUp, ChevronRight, ChevronLeft,
  Plus, Minus, Sparkles, AlertTriangle, Zap, Trophy, ArrowRight,
  LayoutGrid, Coffee, Car, Sword, Baby, Ticket, Route, X, Download, Lock,
  Check, Package, Map,
} from 'lucide-react';
import { Button } from './components/ui/button';
import { Input } from './components/ui/input';
import { Label } from './components/ui/label';
import { ScrollArea } from './components/ui/scroll-area';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './components/ui/select';
import { SubsidyModule } from './SubsidyModule';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const CATEGORY_META = {
  arcade: { label: 'Arcade & Games', icon: Gamepad2, color: '#8b5cf6' },
  karting: { label: 'Karting', icon: Car, color: '#ef4444' },
  interactive: { label: 'Interactive Experiences', icon: Sword, color: '#f59e0b' },
  indoor_play: { label: 'Indoor Speelparadijs', icon: Baby, color: '#10b981' },
  horeca: { label: 'Food & Beverage', icon: Coffee, color: '#f97316' },
};

const ZONE_META = {
  entree: { label: 'Entree & Ticketing', icon: Ticket, color: '#6366f1' },
  arcade: { label: 'Arcade & Games', icon: Gamepad2, color: '#8b5cf6' },
  karting: { label: 'Karting', icon: Car, color: '#ef4444' },
  interactive: { label: 'Interactive', icon: Sword, color: '#f59e0b' },
  indoor_play: { label: 'Indoor Play', icon: Baby, color: '#10b981' },
  horeca: { label: 'Food & Beverage', icon: Coffee, color: '#f97316' },
  routing: { label: 'Routing & Looppad', icon: Route, color: '#94a3b8' },
};

const FEC_STEPS = [
  { id: 1, title: 'Locatie', icon: Building2 },
  { id: 2, title: 'Zones', icon: LayoutGrid },
  { id: 3, title: 'Attracties', icon: Gamepad2 },
  { id: 4, title: 'Revenue', icon: TrendingUp },
];

export function FecWizard({ onBack, userTier }) {
  const [step, setStep] = useState(1);
  const [fecProducts, setFecProducts] = useState([]);
  const [top5, setTop5] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showRoadmap, setShowRoadmap] = useState(false);
  const [showSubsidy, setShowSubsidy] = useState(false);
  const [project, setProject] = useState({
    total_area_m2: 500,
    ceiling_height_m: 5.0,
    target_audience: 'families',
    budget_range: 'midrange',
    address: '',
    operating_hours: 10,
    operating_days: 30,
    zones: [],
  });
  const [selectedProducts, setSelectedProducts] = useState([]);
  const [revenueReport, setRevenueReport] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedZone, setSelectedZone] = useState(null);
  const [dragState, setDragState] = useState(null); // { zoneId, offsetX, offsetY }
  const [resizeState, setResizeState] = useState(null); // { zoneId, startX, startY, startW, startH }
  const canvasRef = useRef(null);

  // Canvas dimensions
  const CANVAS_W = Math.max(700, Math.sqrt(project.total_area_m2) * 22);
  const CANVAS_H = Math.max(450, Math.sqrt(project.total_area_m2) * 15);
  const PX_PER_M2 = (CANVAS_W * CANVAS_H) / project.total_area_m2;

  const pxToM2 = (w, h) => Math.round((w * h) / PX_PER_M2);
  const m2ToPx = (m2) => {
    const side = Math.sqrt(m2 * PX_PER_M2);
    return { w: Math.round(side * 1.4), h: Math.round(side / 1.4) };
  };

  useEffect(() => {
    axios.get(`${API}/fec/products`).then(r => setFecProducts(r.data)).catch(() => {});
    axios.get(`${API}/fec/top5`).then(r => setTop5(r.data)).catch(() => {});
  }, []);

  const calculateRevenue = useCallback(async () => {
    if (selectedProducts.length === 0) { setRevenueReport(null); return; }
    try {
      const res = await axios.post(`${API}/fec/calculate-revenue`, {
        products: selectedProducts.map(sp => ({ product_id: sp.product_id, quantity: sp.quantity })),
        operating_hours: project.operating_hours,
        operating_days: project.operating_days,
        project: { total_area_m2: project.total_area_m2, ceiling_height_m: project.ceiling_height_m, zones: project.zones },
      });
      setRevenueReport(res.data);
    } catch { setRevenueReport(null); }
  }, [selectedProducts, project.operating_hours, project.operating_days, project.total_area_m2, project.ceiling_height_m, project.zones]);

  useEffect(() => { calculateRevenue(); }, [calculateRevenue]);

  const totalFootprint = selectedProducts.reduce((s, sp) => {
    const p = fecProducts.find(fp => fp.id === sp.product_id);
    return s + (p ? p.footprint_m2 * sp.quantity : 0);
  }, 0);
  const zoneArea = project.zones.reduce((s, z) => s + z.area_m2, 0);
  const remainingM2 = project.total_area_m2 - zoneArea;

  const addProduct = (productId) => {
    const existing = selectedProducts.find(sp => sp.product_id === productId);
    if (existing) {
      setSelectedProducts(prev => prev.map(sp => sp.product_id === productId ? { ...sp, quantity: sp.quantity + 1 } : sp));
    } else {
      setSelectedProducts(prev => [...prev, { product_id: productId, quantity: 1 }]);
    }
    const p = fecProducts.find(fp => fp.id === productId);
    if (p) toast.success(`${p.name} toegevoegd`);
  };

  const removeProduct = (productId) => {
    const existing = selectedProducts.find(sp => sp.product_id === productId);
    if (existing && existing.quantity > 1) {
      setSelectedProducts(prev => prev.map(sp => sp.product_id === productId ? { ...sp, quantity: sp.quantity - 1 } : sp));
    } else {
      setSelectedProducts(prev => prev.filter(sp => sp.product_id !== productId));
    }
  };

  const addZone = (type) => {
    const meta = ZONE_META[type];
    const { w, h } = m2ToPx(50);
    // Stack zones with offset so they don't overlap
    const offsetIdx = project.zones.length;
    const x = 20 + (offsetIdx % 3) * (w + 16);
    const y = 20 + Math.floor(offsetIdx / 3) * (h + 16);
    const newZone = {
      id: `zone-${Date.now()}`, type, name: meta.label, area_m2: 50,
      expected_capacity: 20, color: meta.color,
      x, y, w, h,
    };
    setProject(prev => ({ ...prev, zones: [...prev.zones, newZone] }));
  };

  const updateZone = (zoneId, updates) => {
    setProject(prev => ({ ...prev, zones: prev.zones.map(z => z.id === zoneId ? { ...z, ...updates } : z) }));
  };

  const removeZone = (zoneId) => {
    setProject(prev => ({ ...prev, zones: prev.zones.filter(z => z.id !== zoneId) }));
    if (selectedZone === zoneId) setSelectedZone(null);
  };

  // ============ DRAG LOGIC ============
  const handleZoneMouseDown = useCallback((e, zone) => {
    e.stopPropagation();
    e.preventDefault();
    const rect = canvasRef.current.getBoundingClientRect();
    setDragState({ zoneId: zone.id, offsetX: e.clientX - rect.left - zone.x, offsetY: e.clientY - rect.top - zone.y });
    setSelectedZone(zone.id);
  }, []);

  useEffect(() => {
    if (!dragState) return;
    const handleMove = (e) => {
      const rect = canvasRef.current.getBoundingClientRect();
      const zone = project.zones.find(z => z.id === dragState.zoneId);
      if (!zone) return;
      const newX = Math.max(0, Math.min(CANVAS_W - zone.w, e.clientX - rect.left - dragState.offsetX));
      const newY = Math.max(0, Math.min(CANVAS_H - zone.h, e.clientY - rect.top - dragState.offsetY));
      setProject(prev => ({ ...prev, zones: prev.zones.map(z => z.id === dragState.zoneId ? { ...z, x: Math.round(newX), y: Math.round(newY) } : z) }));
    };
    const handleUp = () => setDragState(null);
    document.addEventListener('mousemove', handleMove);
    document.addEventListener('mouseup', handleUp);
    return () => { document.removeEventListener('mousemove', handleMove); document.removeEventListener('mouseup', handleUp); };
  }, [dragState, CANVAS_W, CANVAS_H, project.zones]);

  // ============ RESIZE LOGIC ============
  const handleResizeMouseDown = useCallback((e, zone) => {
    e.stopPropagation();
    e.preventDefault();
    setResizeState({ zoneId: zone.id, startX: e.clientX, startY: e.clientY, startW: zone.w, startH: zone.h });
    setSelectedZone(zone.id);
  }, []);

  useEffect(() => {
    if (!resizeState) return;
    const handleMove = (e) => {
      const dx = e.clientX - resizeState.startX;
      const dy = e.clientY - resizeState.startY;
      const newW = Math.max(60, resizeState.startW + dx);
      const newH = Math.max(40, resizeState.startH + dy);
      const newM2 = pxToM2(newW, newH);
      setProject(prev => ({ ...prev, zones: prev.zones.map(z =>
        z.id === resizeState.zoneId ? { ...z, w: Math.round(newW), h: Math.round(newH), area_m2: Math.max(5, newM2) } : z
      ) }));
    };
    const handleUp = () => setResizeState(null);
    document.addEventListener('mousemove', handleMove);
    document.addEventListener('mouseup', handleUp);
    return () => { document.removeEventListener('mousemove', handleMove); document.removeEventListener('mouseup', handleUp); };
  }, [resizeState]);

  // Deselect on canvas click
  const handleCanvasClick = (e) => {
    if (e.target === canvasRef.current) setSelectedZone(null);
  };

  const filteredProducts = selectedCategory === 'all' ? fecProducts : fecProducts.filter(p => p.category === selectedCategory);

  const exportFecPDF = async () => {
    if (selectedProducts.length === 0) { toast.error('Selecteer eerst attracties'); return; }
    try {
      setLoading(true);
      const res = await axios.post(`${API}/fec/pdf`, {
        products: selectedProducts.map(sp => ({ product_id: sp.product_id, quantity: sp.quantity })),
        operating_hours: project.operating_hours,
        operating_days: project.operating_days,
        project: {
          total_area_m2: project.total_area_m2,
          ceiling_height_m: project.ceiling_height_m,
          target_audience: project.target_audience,
          zones: project.zones,
        },
      });
      const printWindow = window.open('', '_blank');
      printWindow.document.write(res.data.html);
      printWindow.document.close();
      printWindow.focus();
      setTimeout(() => printWindow.print(), 500);
      toast.success('Business Case PDF gegenereerd');
    } catch {
      toast.error('Kon PDF niet genereren');
    } finally {
      setLoading(false);
    }
  };

  if (showRoadmap) {
    const { RoadmapView } = require('./RoadmapView');
    return (
      <RoadmapView
        flowType="fec"
        onBack={() => setShowRoadmap(false)}
        projectSummary={revenueReport ? {
          name: 'FEC Business Case',
          details: `${project.total_area_m2}m² · ${selectedProducts.length} attracties · ${project.target_audience}`,
          investment: revenueReport.total_investment,
        } : null}
      />
    );
  }

  return (
    <div className="h-screen w-full flex flex-col overflow-hidden bg-[#FDF9ED]">
      {/* Header */}
      <header className="h-16 bg-[#244628] flex items-center justify-between px-6 flex-shrink-0">
        <div className="flex items-center gap-4">
          <button onClick={onBack} className="flex items-center gap-2 hover:opacity-80" data-testid="fec-back-btn">
            <img src="/recra-logo-white.png" alt="RECRA Solutions" className="h-8" />
          </button>
          <span className="text-white/40">|</span>
          <span className="text-[#f59e0b] text-sm font-medium">FEC & Experience</span>
          <span className="bg-[#f59e0b]/20 text-[#f59e0b] text-xs px-2 py-0.5 rounded-full font-medium">Revenue Engine</span>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={() => setShowSubsidy(!showSubsidy)}
            className={`text-xs flex items-center gap-1 px-3 py-1.5 rounded-full transition-all ${showSubsidy ? 'bg-[#f59e0b] text-white font-bold' : 'text-white/60 hover:text-white hover:bg-white/10'}`}
            data-testid="fec-subsidy-btn">
            <TrendingUp size={14} /> Subsidie Check
          </button>
          <button onClick={() => setShowRoadmap(true)}
            className="text-white/60 hover:text-white text-xs flex items-center gap-1 px-3 py-1.5 rounded-full hover:bg-white/10 transition-all"
            data-testid="fec-roadmap-btn">
            <Map size={14} /> Roadmap
          </button>
          <button onClick={exportFecPDF} disabled={selectedProducts.length === 0 || loading}
            className="text-white/90 hover:text-white text-xs flex items-center gap-1 px-3 py-1.5 rounded-full bg-[#f59e0b] hover:bg-[#e68a00] disabled:opacity-40 transition-all font-medium"
            data-testid="fec-pdf-btn">
            <Download size={14} /> {loading ? 'Genereren...' : 'Business Case PDF'}
          </button>
        </div>
      </header>

      <div className="flex-1 flex overflow-hidden">
        {/* Left Sidebar - Steps & Input */}
        <div className="w-80 flex-shrink-0 border-r border-[#e5e2d9] bg-[#FFFEF8] flex flex-col">
          {/* Step Navigation */}
          <div className="p-3 border-b border-[#e5e2d9]">
            <div className="flex gap-1">
              {FEC_STEPS.map((s) => {
                const Icon = s.icon;
                const isActive = step === s.id;
                const isDone = step > s.id;
                return (
                  <button key={s.id} onClick={() => setStep(s.id)}
                    className={`flex-1 flex flex-col items-center gap-1 p-2 rounded-lg transition-all text-center ${isActive ? 'bg-[#f59e0b]/10 border border-[#f59e0b]/30' : isDone ? 'bg-[#f59e0b]/5' : 'hover:bg-[#FDF9ED]'}`}
                    data-testid={`fec-step-${s.id}`}
                  >
                    <div className={`w-7 h-7 rounded-lg flex items-center justify-center ${isActive || isDone ? 'bg-[#f59e0b] text-white' : 'bg-[#e5e2d9] text-[#777]'}`}>
                      {isDone ? <Check size={14} /> : <Icon size={14} />}
                    </div>
                    <span className={`text-[10px] font-medium ${isActive ? 'text-[#f59e0b]' : 'text-[#777]'}`}>{s.title}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Step Content */}
          <ScrollArea className="flex-1 p-4">
            {step === 1 && (
              <div className="space-y-4" data-testid="fec-step-1-content">
                <h3 className="font-bold text-[#333] text-sm">FEC Locatie & Ruimte</h3>
                <div>
                  <Label className="text-sm text-[#333]">Totale oppervlakte (m²)</Label>
                  <Input type="number" value={project.total_area_m2} onChange={(e) => setProject(prev => ({ ...prev, total_area_m2: parseInt(e.target.value) || 100 }))}
                    className="mt-1 bg-white border-[#e5e2d9]" data-testid="fec-area-input" />
                </div>
                <div>
                  <Label className="text-sm text-[#333]">Plafondhoogte (m)</Label>
                  <Input type="number" step="0.5" value={project.ceiling_height_m} onChange={(e) => setProject(prev => ({ ...prev, ceiling_height_m: parseFloat(e.target.value) || 3 }))}
                    className="mt-1 bg-white border-[#e5e2d9]" data-testid="fec-ceiling-input" />
                  <p className="text-[10px] text-[#777] mt-1">Volume: {Math.round(project.total_area_m2 * project.ceiling_height_m).toLocaleString()} m³</p>
                </div>
                <div>
                  <Label className="text-sm text-[#333]">Doelgroep</Label>
                  <Select value={project.target_audience} onValueChange={(v) => setProject(prev => ({ ...prev, target_audience: v }))}>
                    <SelectTrigger className="mt-1 bg-white border-[#e5e2d9]" data-testid="fec-audience-select">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="bg-white">
                      <SelectItem value="families">Families met kinderen</SelectItem>
                      <SelectItem value="teens">Tieners & jongvolwassenen</SelectItem>
                      <SelectItem value="all_ages">Alle leeftijden</SelectItem>
                      <SelectItem value="corporate">Zakelijk / teambuilding</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <Label className="text-sm text-[#333]">Openingsuren/dag</Label>
                    <Input type="number" value={project.operating_hours} onChange={(e) => setProject(prev => ({ ...prev, operating_hours: parseFloat(e.target.value) || 8 }))}
                      className="mt-1 bg-white border-[#e5e2d9]" data-testid="fec-hours-input" />
                  </div>
                  <div>
                    <Label className="text-sm text-[#333]">Dagen/maand</Label>
                    <Input type="number" value={project.operating_days} onChange={(e) => setProject(prev => ({ ...prev, operating_days: parseInt(e.target.value) || 25 }))}
                      className="mt-1 bg-white border-[#e5e2d9]" data-testid="fec-days-input" />
                  </div>
                </div>
                <div>
                  <Label className="text-sm text-[#333]">Adres</Label>
                  <Input value={project.address} onChange={(e) => setProject(prev => ({ ...prev, address: e.target.value }))}
                    className="mt-1 bg-white border-[#e5e2d9]" placeholder="Straat, Stad" data-testid="fec-address-input" />
                </div>
              </div>
            )}

            {step === 2 && (
              <div className="space-y-4" data-testid="fec-step-2-content">
                <h3 className="font-bold text-[#333] text-sm">Zones Indelen</h3>
                <p className="text-xs text-[#777]">Bouw eerst uw zones voordat u attracties selecteert.</p>

                <div className="grid grid-cols-2 gap-2">
                  {Object.entries(ZONE_META).map(([type, meta]) => {
                    const Icon = meta.icon;
                    const hasZone = project.zones.some(z => z.type === type);
                    return (
                      <button key={type} onClick={() => addZone(type)}
                        className={`p-2.5 rounded-xl border-2 text-left transition-all bg-white ${hasZone ? 'border-current opacity-60' : 'border-[#e5e2d9] hover:border-current'}`}
                        style={{ '--tw-border-opacity': 1, borderColor: hasZone ? meta.color : undefined }}
                        data-testid={`add-zone-${type}`}
                      >
                        <Icon size={18} style={{ color: meta.color }} />
                        <div className="text-[11px] font-medium text-[#333] mt-1">{meta.label}</div>
                      </button>
                    );
                  })}
                </div>

                {project.zones.length > 0 && (
                  <div className="space-y-2">
                    <div className="flex justify-between text-xs text-[#777]">
                      <span>{project.zones.length} zones</span>
                      <span>{zoneArea}m² / {project.total_area_m2}m²</span>
                    </div>
                    {project.zones.map((zone) => {
                      const meta = ZONE_META[zone.type];
                      const Icon = meta?.icon || Package;
                      const isSelected = selectedZone === zone.id;
                      return (
                        <div key={zone.id} className={`p-2.5 rounded-lg border bg-white transition-all ${isSelected ? 'ring-2 ring-offset-1' : ''}`} style={{ borderColor: zone.color + '40', '--tw-ring-color': zone.color }} data-testid={`zone-item-${zone.id}`}>
                          <div className="flex items-center justify-between mb-2">
                            <button className="flex items-center gap-2" onClick={() => setSelectedZone(isSelected ? null : zone.id)}>
                              <Icon size={14} style={{ color: zone.color }} />
                              <span className="text-xs font-medium text-[#333]">{zone.name}</span>
                            </button>
                            <Button variant="ghost" size="icon" className="h-6 w-6 text-[#777] hover:text-red-500" onClick={() => removeZone(zone.id)}>
                              <X size={12} />
                            </Button>
                          </div>
                          <div className="flex gap-2">
                            <div className="flex-1">
                              <Label className="text-[10px] text-[#777]">m²</Label>
                              <Input type="number" value={zone.area_m2} onChange={(e) => {
                                const newM2 = parseInt(e.target.value) || 10;
                                const { w, h } = m2ToPx(newM2);
                                updateZone(zone.id, { area_m2: newM2, w, h });
                              }}
                                className="h-7 text-xs bg-white border-[#e5e2d9]" />
                            </div>
                            <div className="flex-1">
                              <Label className="text-[10px] text-[#777]">Capaciteit</Label>
                              <Input type="number" value={zone.expected_capacity} onChange={(e) => updateZone(zone.id, { expected_capacity: parseInt(e.target.value) || 0 })}
                                className="h-7 text-xs bg-white border-[#e5e2d9]" />
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}

                {/* Zone area bar */}
                {project.zones.length > 0 && (
                  <div className="rounded-lg overflow-hidden h-6 flex" data-testid="zone-bar">
                    {project.zones.map(z => (
                      <div key={z.id} style={{ width: `${Math.max(2, (z.area_m2 / project.total_area_m2) * 100)}%`, backgroundColor: z.color }}
                        className={`h-full flex items-center justify-center cursor-pointer transition-opacity ${selectedZone && selectedZone !== z.id ? 'opacity-40' : ''}`}
                        onClick={() => setSelectedZone(selectedZone === z.id ? null : z.id)}>
                        <span className="text-[8px] text-white font-bold truncate px-1">{z.area_m2}m²</span>
                      </div>
                    ))}
                    {remainingM2 > 0 && (
                      <div style={{ width: `${(remainingM2 / project.total_area_m2) * 100}%` }} className="h-full bg-[#e5e2d9] flex items-center justify-center">
                        <span className="text-[8px] text-[#777] font-bold">{Math.round(remainingM2)}m²</span>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}

            {step === 3 && (
              <div className="space-y-3" data-testid="fec-step-3-content">
                <h3 className="font-bold text-[#333] text-sm">Top Geldverdieners</h3>

                {/* Top 5 highlight */}
                {top5.length > 0 && (
                  <div className="p-3 rounded-xl bg-[#f59e0b]/10 border border-[#f59e0b]/20">
                    <div className="flex items-center gap-2 mb-2">
                      <Trophy size={16} className="text-[#f59e0b]" />
                      <span className="text-xs font-bold text-[#333]">Top 5 per m² omzet</span>
                    </div>
                    <div className="space-y-1">
                      {top5.map((p, i) => (
                        <button key={p.id} onClick={() => addProduct(p.id)}
                          className="w-full flex items-center justify-between p-1.5 rounded-lg hover:bg-white/80 transition-all text-left"
                          data-testid={`top5-${i}`}
                        >
                          <div className="flex items-center gap-2">
                            <span className="text-[10px] font-bold text-[#f59e0b] w-4">#{i + 1}</span>
                            <span className="text-xs text-[#333] font-medium truncate">{p.name}</span>
                          </div>
                          <span className="text-[10px] font-bold text-[#f59e0b]">€{p.revenue_per_m2}/m²</span>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* Category filter */}
                <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                  <SelectTrigger className="bg-white border-[#e5e2d9]" data-testid="fec-category-select">
                    <SelectValue placeholder="Alle categorieën" />
                  </SelectTrigger>
                  <SelectContent className="bg-white">
                    <SelectItem value="all">Alle categorieën</SelectItem>
                    {Object.entries(CATEGORY_META).map(([key, meta]) => (
                      <SelectItem key={key} value={key}>{meta.label}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>

                {/* Products */}
                <div className="space-y-2">
                  {filteredProducts.map((product) => {
                    const meta = CATEGORY_META[product.category] || { icon: Package, color: '#777', label: product.category };
                    const Icon = meta.icon;
                    const selected = selectedProducts.find(sp => sp.product_id === product.id);
                    return (
                      <div key={product.id}
                        className={`p-3 rounded-xl border-2 bg-white transition-all ${selected ? 'border-[#f59e0b] bg-[#f59e0b]/5' : 'border-[#e5e2d9] hover:border-[#f59e0b]/50'}`}
                        data-testid={`fec-product-${product.id}`}
                      >
                        <div className="flex items-start gap-2.5">
                          <div className="w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0" style={{ backgroundColor: `${meta.color}15` }}>
                            <Icon size={18} style={{ color: meta.color }} />
                          </div>
                          <div className="flex-1 min-w-0">
                            <div className="font-semibold text-xs text-[#333] truncate">{product.name}</div>
                            <div className="text-[10px] text-[#777] line-clamp-1">{product.supplier} — {product.footprint_m2}m²</div>
                            <div className="flex items-center gap-3 mt-1">
                              <span className="text-xs font-bold text-[#f59e0b]">€{product.revenue_per_hour}/uur</span>
                              <span className="text-[10px] text-[#777]">ROI {product.roi_months} mnd</span>
                              <span className="text-[10px] text-[#777]">Lease €{product.price_lease_monthly}/mnd</span>
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center gap-2 mt-2">
                          {selected ? (
                            <div className="flex items-center gap-2 flex-1">
                              <Button variant="outline" size="icon" className="h-7 w-7 border-[#e5e2d9]" onClick={() => removeProduct(product.id)}>
                                <Minus size={12} />
                              </Button>
                              <span className="text-sm font-bold text-[#333] w-6 text-center">{selected.quantity}</span>
                              <Button variant="outline" size="icon" className="h-7 w-7 border-[#e5e2d9]" onClick={() => addProduct(product.id)}>
                                <Plus size={12} />
                              </Button>
                              <span className="text-[10px] text-[#777] ml-auto">€{(product.price_purchase * selected.quantity).toLocaleString()}</span>
                            </div>
                          ) : (
                            <Button size="sm" className="w-full h-7 bg-[#f59e0b] hover:bg-[#e68a00] text-white text-xs" onClick={() => addProduct(product.id)}>
                              <Plus size={12} className="mr-1" /> Toevoegen — €{product.price_purchase.toLocaleString()}
                            </Button>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {step === 4 && (
              <div className="space-y-4" data-testid="fec-step-4-content">
                <h3 className="font-bold text-[#333] text-sm">Revenue Dashboard</h3>

                {revenueReport ? (
                  <>
                    {/* Key metrics */}
                    <div className="grid grid-cols-2 gap-2">
                      <div className="p-3 rounded-xl bg-[#f59e0b]/10 border border-[#f59e0b]/20">
                        <div className="text-[10px] text-[#777]">Investering</div>
                        <div className="font-bold text-[#f59e0b]" data-testid="fec-total-investment">€ {revenueReport.total_investment.toLocaleString()}</div>
                      </div>
                      <div className="p-3 rounded-xl bg-[#10b981]/10 border border-[#10b981]/20">
                        <div className="text-[10px] text-[#777]">Omzet/maand</div>
                        <div className="font-bold text-[#10b981]" data-testid="fec-monthly-revenue">€ {revenueReport.total_monthly_revenue.toLocaleString()}</div>
                      </div>
                      <div className="p-3 rounded-xl bg-[#244628]/10 border border-[#244628]/20">
                        <div className="text-[10px] text-[#777]">Break-even</div>
                        <div className="font-bold text-[#244628]" data-testid="fec-breakeven">{revenueReport.break_even_months} mnd</div>
                      </div>
                      <div className="p-3 rounded-xl bg-[#8b5cf6]/10 border border-[#8b5cf6]/20">
                        <div className="text-[10px] text-[#777]">€/m²/maand</div>
                        <div className="font-bold text-[#8b5cf6]" data-testid="fec-rev-per-m2">€ {revenueReport.revenue_per_m2_month.toLocaleString()}</div>
                      </div>
                    </div>

                    {/* Lease option */}
                    {revenueReport.total_lease_monthly > 0 && (
                      <div className="p-3 rounded-xl bg-white border border-[#e5e2d9]">
                        <div className="text-xs font-bold text-[#333] mb-1.5">Operational Lease</div>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-[#777]">Totaal lease/maand</span>
                          <span className="font-bold text-[#f59e0b]" data-testid="fec-lease-monthly">€ {revenueReport.total_lease_monthly.toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between text-xs text-[#777]">
                          <span>Netto winst/mnd (omzet - lease)</span>
                          <span className="font-bold text-[#10b981]">€ {(revenueReport.total_monthly_revenue - revenueReport.total_lease_monthly).toLocaleString()}</span>
                        </div>
                        <p className="text-[10px] text-[#777] mt-1.5">60 maanden incl. SLA onderhoudscontract</p>
                      </div>
                    )}

                    {/* Top performers */}
                    <div className="p-3 rounded-xl bg-white border border-[#e5e2d9]">
                      <div className="flex items-center gap-2 mb-2">
                        <Trophy size={16} className="text-[#f59e0b]" />
                        <span className="font-bold text-xs text-[#333]">Top Performers</span>
                      </div>
                      <div className="space-y-1.5">
                        {revenueReport.top_performers.map((p, i) => (
                          <div key={i} className="flex items-center justify-between p-2 rounded-lg bg-[#FDF9ED]">
                            <div>
                              <div className="text-xs font-medium text-[#333]">{p.product_name}</div>
                              <div className="text-[10px] text-[#777]">{p.category} — ROI {p.roi_months} mnd</div>
                              {p.lease_monthly > 0 && <div className="text-[10px] text-[#f59e0b]">Lease €{p.lease_monthly}/mnd</div>}
                            </div>
                            <div className="text-right">
                              <div className="text-xs font-bold text-[#10b981]">€{p.monthly_revenue.toLocaleString()}/mnd</div>
                              <div className="text-[10px] text-[#777]">€{p.revenue_per_m2}/m²</div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* AI Suggestions */}
                    {revenueReport.suggestions?.length > 0 && (
                      <div className="space-y-2">
                        <div className="flex items-center gap-2">
                          <Sparkles size={16} className="text-[#f59e0b]" />
                          <span className="font-bold text-xs text-[#333]">AI Advies</span>
                        </div>
                        {revenueReport.suggestions.map((s, i) => (
                          <div key={i} className={`p-2.5 rounded-lg border bg-white ${s.type === 'warning' ? 'border-amber-300' : s.type === 'optimization' ? 'border-[#10b981]' : 'border-[#f59e0b]'}`} data-testid={`fec-suggestion-${i}`}>
                            <div className="flex items-start gap-2">
                              {s.type === 'warning' ? <AlertTriangle size={14} className="text-amber-500 mt-0.5" /> : <Zap size={14} className="text-[#f59e0b] mt-0.5" />}
                              <div>
                                <div className="text-xs font-medium text-[#333]">{s.title}</div>
                                <div className="text-[10px] text-[#777] mt-0.5">{s.description}</div>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Cross-sell */}
                    <div className="p-3 rounded-xl bg-[#244628] text-white">
                      <div className="text-xs font-medium text-white/80 mb-2">Volgende stappen</div>
                      <button onClick={exportFecPDF} disabled={loading}
                        className="flex items-center gap-2 text-[#f59e0b] text-xs hover:underline mb-1 w-full" data-testid="fec-export-pdf-step4">
                        <Download size={12} /> Download Business Case PDF
                      </button>
                      <button onClick={() => setShowRoadmap(true)}
                        className="flex items-center gap-2 text-[#70C26C] text-xs hover:underline mb-1 w-full" data-testid="fec-roadmap-step4">
                        <Map size={12} /> Bekijk Roadmap: Idee naar Realisatie
                      </button>
                      <div className="h-px bg-white/10 my-2" />
                      <button onClick={onBack} className="flex items-center gap-2 text-white/50 text-xs hover:underline" data-testid="fec-crosssell-recreatie">
                        <ArrowRight size={12} /> Bekijk Recreatie Infra voor buitenuitbreiding
                      </button>
                      <button onClick={onBack} className="flex items-center gap-2 text-white/50 text-xs hover:underline mt-1" data-testid="fec-crosssell-chalet">
                        <ArrowRight size={12} /> Overweeg Chalet & Stay voor verblijfsomzet
                      </button>
                    </div>
                  </>
                ) : (
                  <div className="text-center py-8 text-[#777]">
                    <TrendingUp size={32} className="mx-auto mb-2 opacity-50" />
                    <p className="text-xs">Selecteer attracties om de omzetberekening te zien</p>
                  </div>
                )}
              </div>
            )}
          </ScrollArea>

          {/* Navigation */}
          <div className="p-4 border-t border-[#e5e2d9] flex gap-2">
            <Button variant="outline" onClick={() => setStep(prev => Math.max(1, prev - 1))} disabled={step === 1} className="flex-1 border-[#e5e2d9] bg-white" data-testid="fec-prev-btn">
              <ChevronLeft size={16} className="mr-1" /> Vorige
            </Button>
            <Button onClick={() => setStep(prev => Math.min(4, prev + 1))} disabled={step === 4} className="flex-1 bg-[#f59e0b] hover:bg-[#e68a00] text-white" data-testid="fec-next-btn">
              Volgende <ChevronRight size={16} className="ml-1" />
            </Button>
          </div>
        </div>

        {/* Main Canvas - FEC Floor Plan (Interactive Drag & Resize) */}
        <div className="flex-1 flex flex-col overflow-hidden">
          <div className="h-12 bg-white border-b border-[#e5e2d9] flex items-center justify-between px-4">
            <div className="flex items-center gap-3">
              <span className="text-sm text-[#777]">FEC Layout — {project.total_area_m2}m² / {project.ceiling_height_m}m hoog</span>
              {selectedZone && (
                <span className="text-xs text-[#f59e0b] bg-[#f59e0b]/10 px-2 py-0.5 rounded-full">
                  Zone geselecteerd — versleep of resize
                </span>
              )}
            </div>
            <div className="flex items-center gap-3 text-xs text-[#777]">
              <span>Zones: {zoneArea}m²</span>
              <span className={remainingM2 < 0 ? 'text-red-500 font-bold' : ''}>Vrij: {Math.max(0, Math.round(remainingM2))}m²</span>
            </div>
          </div>

          <div className="flex-1 overflow-auto bg-[#FDF9ED] p-4">
            <div ref={canvasRef}
              className="relative bg-white rounded-xl shadow-lg mx-auto border-2 border-[#e5e2d9] select-none"
              style={{
                width: CANVAS_W, height: CANVAS_H, minWidth: 600,
                backgroundImage: 'linear-gradient(to right, rgba(0,0,0,0.02) 1px, transparent 1px), linear-gradient(to bottom, rgba(0,0,0,0.02) 1px, transparent 1px)',
                backgroundSize: '24px 24px',
              }}
              onClick={handleCanvasClick}
              data-testid="fec-canvas"
            >
              {/* Interactive zones */}
              {project.zones.map((zone) => {
                const meta = ZONE_META[zone.type];
                const Icon = meta?.icon || Package;
                const isSelected = selectedZone === zone.id;
                const isDragging = dragState?.zoneId === zone.id;
                const isResizing = resizeState?.zoneId === zone.id;

                return (
                  <div key={zone.id}
                    className={`absolute rounded-xl border-2 flex flex-col items-center justify-center select-none transition-shadow ${isDragging ? 'cursor-grabbing shadow-2xl z-20 opacity-90' : isResizing ? 'z-20' : isSelected ? 'cursor-grab shadow-lg z-10 ring-2 ring-offset-2' : 'cursor-grab hover:shadow-md z-0'}`}
                    style={{
                      left: zone.x, top: zone.y, width: zone.w, height: zone.h,
                      backgroundColor: `${zone.color}18`, borderColor: `${zone.color}${isSelected ? 'cc' : '60'}`,
                      '--tw-ring-color': zone.color,
                    }}
                    onMouseDown={(e) => handleZoneMouseDown(e, zone)}
                    data-testid={`fec-canvas-zone-${zone.id}`}
                  >
                    <Icon size={Math.min(zone.w, zone.h) * 0.25} style={{ color: zone.color }} className="pointer-events-none" />
                    <span className="text-xs font-bold mt-1 pointer-events-none" style={{ color: zone.color }}>{zone.name}</span>
                    <span className="text-[10px] text-[#777] pointer-events-none">{zone.area_m2}m²</span>

                    {/* Resize handle (bottom-right corner) */}
                    <div
                      className={`absolute bottom-0 right-0 w-5 h-5 cursor-se-resize rounded-tl-lg rounded-br-xl transition-opacity ${isSelected ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'}`}
                      style={{ backgroundColor: zone.color }}
                      onMouseDown={(e) => handleResizeMouseDown(e, zone)}
                      data-testid={`fec-resize-${zone.id}`}
                    >
                      <svg width="12" height="12" viewBox="0 0 12 12" className="absolute bottom-0.5 right-0.5 text-white">
                        <path d="M10 2L2 10M10 6L6 10M10 10L10 10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                      </svg>
                    </div>

                    {/* Delete button (top-right) */}
                    {isSelected && (
                      <button
                        className="absolute -top-2 -right-2 w-5 h-5 bg-red-500 text-white rounded-full flex items-center justify-center shadow-md hover:bg-red-600 z-30"
                        onClick={(e) => { e.stopPropagation(); removeZone(zone.id); }}
                        data-testid={`fec-delete-zone-${zone.id}`}
                      >
                        <X size={10} />
                      </button>
                    )}
                  </div>
                );
              })}

              {/* Empty state */}
              {project.zones.length === 0 && (
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                  <div className="text-center max-w-sm p-8">
                    <LayoutGrid size={32} className="mx-auto mb-2 text-[#e5e2d9]" />
                    <h3 className="font-semibold text-[#333] mb-2">Bouw uw FEC layout</h3>
                    <p className="text-sm text-[#777]">Voeg zones toe in Stap 2 en versleep ze op het canvas.</p>
                  </div>
                </div>
              )}

              {/* Revenue hotspots */}
              {revenueReport && revenueReport.top_performers.length > 0 && (
                <div className="absolute top-2 right-2 bg-white/90 backdrop-blur-sm rounded-lg p-2 border border-[#e5e2d9] shadow-sm pointer-events-none">
                  <div className="text-[10px] font-bold text-[#333] mb-1 flex items-center gap-1">
                    <DollarSign size={10} className="text-[#f59e0b]" /> Hotspots
                  </div>
                  {revenueReport.top_performers.slice(0, 3).map((p, i) => (
                    <div key={i} className="text-[9px] text-[#777] flex items-center gap-1">
                      <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: CATEGORY_META[p.category]?.color || '#777' }} />
                      {p.product_name.split(' ').slice(0, 2).join(' ')} — €{p.revenue_per_m2}/m²
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Sidebar - Quick Revenue Summary */}
        <div className="w-72 flex-shrink-0 border-l border-[#e5e2d9] bg-[#FFFEF8] flex flex-col">
          <div className="p-3 border-b border-[#e5e2d9]">
            <div className="flex items-center gap-2">
              <TrendingUp size={16} className="text-[#f59e0b]" />
              <span className="font-bold text-sm text-[#333]">Business Case</span>
            </div>
          </div>
          <ScrollArea className="flex-1 p-4">
            <div className="space-y-3">
              {/* Selected products summary */}
              {selectedProducts.length > 0 ? (
                <>
                  <div className="space-y-1.5">
                    {selectedProducts.map((sp) => {
                      const p = fecProducts.find(fp => fp.id === sp.product_id);
                      if (!p) return null;
                      const meta = CATEGORY_META[p.category] || { icon: Package, color: '#777' };
                      const Icon = meta.icon;
                      return (
                        <div key={sp.product_id} className="flex items-center justify-between p-2 rounded-lg bg-white border border-[#e5e2d9]">
                          <div className="flex items-center gap-2">
                            <div className="w-7 h-7 rounded flex items-center justify-center" style={{ backgroundColor: `${meta.color}15` }}>
                              <Icon size={12} style={{ color: meta.color }} />
                            </div>
                            <div>
                              <div className="text-[10px] font-medium text-[#333] truncate max-w-[120px]">{p.name}</div>
                              <div className="text-[9px] text-[#777]">{sp.quantity}x — €{(p.price_purchase * sp.quantity).toLocaleString()} | Lease €{((p.price_lease_monthly || 0) * sp.quantity).toLocaleString()}/mnd</div>
                            </div>
                          </div>
                          <div className="text-right">
                            <div className="text-[10px] font-bold text-[#10b981]">€{(p.revenue_per_hour * sp.quantity * project.operating_hours).toLocaleString()}/dag</div>
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  {revenueReport && (
                    <div className="p-3 rounded-xl bg-[#244628] text-white">
                      <div className="flex justify-between mb-1">
                        <span className="text-white/80 text-xs">Investering</span>
                        <span className="font-bold text-sm">€{revenueReport.total_investment.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between mb-1">
                        <span className="text-white/80 text-xs">Omzet/mnd</span>
                        <span className="font-bold text-sm text-[#70C26C]">€{revenueReport.total_monthly_revenue.toLocaleString()}</span>
                      </div>
                      {revenueReport.total_lease_monthly > 0 && (
                        <div className="flex justify-between mb-1">
                          <span className="text-white/80 text-xs">Lease/mnd</span>
                          <span className="text-sm text-[#f59e0b]">€{revenueReport.total_lease_monthly.toLocaleString()}</span>
                        </div>
                      )}
                      <div className="h-px bg-white/20 my-1.5" />
                      <div className="flex justify-between">
                        <span className="text-white/80 text-xs">Break-even</span>
                        <span className="font-bold text-[#f59e0b]">{revenueReport.break_even_months} maanden</span>
                      </div>
                    </div>
                  )}
                </>
              ) : (
                <div className="text-center py-8 text-[#777]">
                  <DollarSign size={24} className="mx-auto mb-2 opacity-50" />
                  <p className="text-xs">Selecteer attracties voor de business case</p>
                </div>
              )}
            </div>
          </ScrollArea>
        </div>
      </div>

      {/* Subsidie Panel */}
      {showSubsidy && (
        <div className="w-80 flex-shrink-0 border-l border-[#e5e2d9] bg-[#FFFEF8]" data-testid="fec-subsidy-panel">
          <SubsidyModule
            onClose={() => setShowSubsidy(false)}
            projectContext={{
              sector: 'Recreatie',
              projectomschrijving: `FEC ${project.total_area_m2}m² — ${selectedProducts.length} attracties`,
              investering: revenueReport ? (revenueReport.total_investment > 100000 ? '> €100K' : revenueReport.total_investment > 25000 ? '€25K - €100K' : '€10K - €25K') : '',
            }}
          />
        </div>
      )}
    </div>
  );
}
