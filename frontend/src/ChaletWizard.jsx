import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import {
  ArrowLeft, Layers, Square, CornerDownRight, GitMerge, Columns2,
  Minus, Triangle, TrendingUp, Home, Hexagon, ChevronLeft, ChevronRight,
  Bed, Bath, Users, Ruler, Building2, Check, Eye, Settings, FileText,
} from 'lucide-react';
import { Button } from './components/ui/button';
import { Slider } from './components/ui/slider';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

// Stock images per style
const STYLE_IMAGES = {
  modern: [
    'https://images.unsplash.com/photo-1712899227535-e076a4489322?w=800&h=500&fit=crop',
    'https://images.unsplash.com/photo-1645132971658-3ffd441ac6fa?w=800&h=500&fit=crop',
    'https://images.unsplash.com/photo-1522071500372-f0fd8c452178?w=800&h=500&fit=crop',
  ],
  luxe: [
    'https://images.unsplash.com/photo-1610054102966-fc6f9a0a0616?w=800&h=500&fit=crop',
    'https://images.unsplash.com/photo-1762782778316-80b05d151915?w=800&h=500&fit=crop',
    'https://images.unsplash.com/photo-1758745018916-627ad7196524?w=800&h=500&fit=crop',
  ],
  landelijk: [
    'https://images.unsplash.com/photo-1762782778316-80b05d151915?w=800&h=500&fit=crop',
    'https://images.unsplash.com/photo-1610054102966-fc6f9a0a0616?w=800&h=500&fit=crop',
    'https://images.unsplash.com/photo-1522071500372-f0fd8c452178?w=800&h=500&fit=crop',
  ],
};

const VORM_ICONS = {
  alles: Layers, rechthoek: Square, 'l-vorm': CornerDownRight,
  't-vorm': GitMerge, dubbel: Columns2,
};
const DAK_ICONS = {
  alles: Layers, platdak: Minus, zadeldak: Triangle,
  lessenaars: TrendingUp, mansarde: Home, schilddak: Hexagon,
};

export function ChaletWizard({ onBack }) {
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState(null);
  const [activeTab, setActiveTab] = useState('plattegrond');
  const [selectedStijl, setSelectedStijl] = useState('modern');
  const [imageIndex, setImageIndex] = useState(0);

  // Filters
  const [bestemming, setBestemming] = useState('recreatie');
  const [oppRange, setOppRange] = useState([30, 120]);
  const [modelVorm, setModelVorm] = useState('alles');
  const [dakVorm, setDakVorm] = useState('alles');

  // Fetch models
  useEffect(() => {
    const fetchModels = async () => {
      try {
        const params = new URLSearchParams();
        if (bestemming) params.append('bestemming', bestemming);
        if (modelVorm !== 'alles') params.append('model_vorm', modelVorm);
        if (dakVorm !== 'alles') params.append('dak_vorm', dakVorm);
        params.append('min_m2', oppRange[0]);
        params.append('max_m2', oppRange[1]);
        const res = await axios.get(`${API}/chalet/models?${params.toString()}`);
        setModels(res.data);
        if (res.data.length > 0 && !selectedModel) {
          setSelectedModel(res.data[0]);
        } else if (res.data.length > 0 && selectedModel) {
          const still = res.data.find(m => m.id === selectedModel.id);
          if (!still) setSelectedModel(res.data[0]);
        } else if (res.data.length === 0) {
          setSelectedModel(null);
        }
      } catch {
        toast.error('Kon modellen niet laden');
      }
    };
    fetchModels();
  }, [bestemming, modelVorm, dakVorm, oppRange]);

  useEffect(() => { setImageIndex(0); }, [selectedModel, selectedStijl]);

  const images = useMemo(() => {
    return STYLE_IMAGES[selectedStijl] || STYLE_IMAGES.modern;
  }, [selectedStijl]);

  const availableStijlen = selectedModel?.stijlen || ['modern'];

  const prevImage = () => setImageIndex(i => (i - 1 + images.length) % images.length);
  const nextImage = () => setImageIndex(i => (i + 1) % images.length);

  const pricing = selectedModel?.pricing || {};

  return (
    <div className="h-screen w-full flex flex-col overflow-hidden bg-[#FDF9ED]" data-testid="chalet-wizard">
      {/* Header */}
      <header className="h-14 bg-[#244628] flex items-center justify-between px-6 flex-shrink-0">
        <div className="flex items-center gap-3">
          <button onClick={onBack} className="flex items-center gap-2 hover:opacity-80 transition-opacity" data-testid="chalet-back-btn">
            <img src="/recra-logo-white.png" alt="RECRA" className="h-7" />
          </button>
          <span className="text-white/40">|</span>
          <span className="text-[#70C26C] text-sm font-semibold">Chalet & Stay Configurator</span>
        </div>
        <button onClick={onBack} className="text-white/70 hover:text-white text-sm flex items-center gap-1" data-testid="back-to-flows">
          <ArrowLeft size={16} /> Terug naar flows
        </button>
      </header>

      {/* Main 3-column layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* LEFT SIDEBAR — Filters */}
        <div className="w-64 flex-shrink-0 border-r border-[#e5e2d9] bg-[#FFFEF8] overflow-y-auto" data-testid="chalet-filters">
          <div className="p-4 space-y-5">
            {/* BESTEMMING */}
            <div>
              <h3 className="text-[11px] font-bold text-[#333] uppercase tracking-wider mb-2">Bestemming</h3>
              <div className="flex gap-2">
                {['recreatie', 'pre-mantelzorg'].map(b => (
                  <button key={b} onClick={() => setBestemming(b)}
                    className={`text-xs px-3 py-1.5 rounded-md border transition-all ${bestemming === b ? 'bg-[#244628] text-white border-[#244628]' : 'bg-white text-[#555] border-[#e5e2d9] hover:border-[#70C26C]'}`}
                    data-testid={`bestemming-${b}`}
                  >
                    {b === 'recreatie' ? 'Recreatie' : 'Pre-Mantelzorg'}
                  </button>
                ))}
              </div>
            </div>

            {/* OPPERVLAKTE */}
            <div>
              <h3 className="text-[11px] font-bold text-[#333] uppercase tracking-wider mb-2">Oppervlakte (m²)</h3>
              <div className="px-1">
                <div className="flex justify-between text-sm font-semibold text-[#244628] mb-2">
                  <span>{oppRange[0]} <span className="text-xs font-normal text-[#999]">m²</span></span>
                  <span>{oppRange[1]} <span className="text-xs font-normal text-[#999]">m²</span></span>
                </div>
                <Slider
                  value={oppRange}
                  onValueChange={setOppRange}
                  min={30} max={120} step={5}
                  className="[&_[role=slider]]:bg-[#70C26C] [&_[role=slider]]:border-[#70C26C] [&_.bg-primary]:bg-[#70C26C]"
                  data-testid="oppervlakte-slider"
                />
                <div className="flex justify-between text-[10px] text-[#aaa] mt-1">
                  <span>30 m²</span><span>60 m²</span><span>90 m²</span><span>120 m²</span>
                </div>
              </div>
            </div>

            {/* MODEL VORM */}
            <div>
              <h3 className="text-[11px] font-bold text-[#333] uppercase tracking-wider mb-2">Model Vorm</h3>
              <div className="grid grid-cols-5 gap-1">
                {[
                  { id: 'alles', label: 'Alles' },
                  { id: 'rechthoek', label: 'Rechthoek' },
                  { id: 'l-vorm', label: 'L-vorm' },
                  { id: 't-vorm', label: 'T-vorm' },
                  { id: 'dubbel', label: 'Dubbel' },
                ].map(v => {
                  const Icon = VORM_ICONS[v.id] || Layers;
                  const active = modelVorm === v.id;
                  return (
                    <button key={v.id} onClick={() => setModelVorm(v.id)}
                      className={`flex flex-col items-center gap-1 py-2 px-1 rounded-lg border text-[9px] transition-all ${active ? 'bg-[#244628] text-white border-[#244628]' : 'bg-white text-[#666] border-[#e5e2d9] hover:border-[#70C26C]'}`}
                      data-testid={`vorm-${v.id}`}
                    >
                      <Icon size={18} />
                      <span className="leading-tight text-center">{v.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* DAK VORM */}
            <div>
              <h3 className="text-[11px] font-bold text-[#333] uppercase tracking-wider mb-2">Dak Vorm</h3>
              <div className="grid grid-cols-3 gap-1">
                {[
                  { id: 'alles', label: 'Alles' },
                  { id: 'platdak', label: 'Platdak' },
                  { id: 'zadeldak', label: 'Zadeldak' },
                  { id: 'lessenaars', label: 'Lessenaars' },
                  { id: 'mansarde', label: 'Mansarde' },
                  { id: 'schilddak', label: 'Schilddak' },
                ].map(d => {
                  const Icon = DAK_ICONS[d.id] || Layers;
                  const active = dakVorm === d.id;
                  return (
                    <button key={d.id} onClick={() => setDakVorm(d.id)}
                      className={`flex flex-col items-center gap-1 py-2 px-1 rounded-lg border text-[9px] transition-all ${active ? 'bg-[#244628] text-white border-[#244628]' : 'bg-white text-[#666] border-[#e5e2d9] hover:border-[#70C26C]'}`}
                      data-testid={`dak-${d.id}`}
                    >
                      <Icon size={18} />
                      <span className="leading-tight text-center">{d.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* BESCHIKBARE MODELLEN */}
            <div>
              <h3 className="text-[11px] font-bold text-[#333] uppercase tracking-wider mb-2">
                Beschikbare Modellen ({models.length})
              </h3>
              <div className="space-y-1.5">
                {models.map(m => {
                  const isActive = selectedModel?.id === m.id;
                  return (
                    <button key={m.id} onClick={() => setSelectedModel(m)}
                      className={`w-full text-left p-2.5 rounded-lg border transition-all ${isActive ? 'bg-[#244628] text-white border-[#244628]' : 'bg-white text-[#333] border-[#e5e2d9] hover:border-[#70C26C]'}`}
                      data-testid={`model-${m.id}`}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <span className="text-sm font-bold">{m.name}</span>
                          <span className={`text-[10px] ml-1.5 px-1.5 py-0.5 rounded ${isActive ? 'bg-white/20 text-white/80' : 'bg-[#FDF9ED] text-[#888]'}`}>
                            {m.supplier_name}
                          </span>
                        </div>
                        <DakIcon dakVorm={m.dak_vorm} size={14} className={isActive ? 'text-white/60' : 'text-[#ccc]'} />
                      </div>
                      <div className="flex items-center justify-between mt-1">
                        <span className={`text-xs ${isActive ? 'text-white/70' : 'text-[#999]'}`}>{m.oppervlakte_m2} m²</span>
                        <span className="text-sm font-bold">€ {m.basisprijs.toLocaleString('nl-NL')}</span>
                      </div>
                    </button>
                  );
                })}
                {models.length === 0 && (
                  <p className="text-xs text-[#999] text-center py-4">Geen modellen gevonden met deze filters</p>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* CENTER — Main Content */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Model header bar */}
          {selectedModel && (
            <div className="h-12 bg-white border-b border-[#e5e2d9] flex items-center justify-between px-5">
              <div className="flex items-center gap-2 text-sm">
                <span className="font-bold text-[#333]">{selectedModel.name}</span>
                <span className="text-[#aaa]">·</span>
                <span className="text-[#777]">Alle Bestemmingen</span>
                <span className="text-[#aaa]">·</span>
                <span className="text-[#777] capitalize">{selectedModel.dak_vorm}</span>
                <span className="text-[#aaa]">·</span>
                <span className="text-[#777]">{selectedModel.oppervlakte_m2} m²</span>
                <span className="text-[#aaa]">·</span>
                <span className="font-bold text-[#244628]">€ {selectedModel.basisprijs.toLocaleString('nl-NL')}</span>
              </div>
              {/* Tabs */}
              <div className="flex gap-1">
                {[
                  { id: 'plattegrond', label: 'Plattegrond en 3D', icon: Eye },
                  { id: 'specificatie', label: 'Specificatie', icon: FileText },
                  { id: 'samenstellen', label: 'Samenstellen', icon: Settings },
                ].map(tab => (
                  <button key={tab.id} onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full transition-all ${activeTab === tab.id ? 'bg-[#244628] text-white' : 'text-[#777] hover:bg-[#FDF9ED]'}`}
                    data-testid={`tab-${tab.id}`}
                  >
                    <tab.icon size={13} />
                    {tab.label}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Content area */}
          <div className="flex-1 overflow-y-auto p-6">
            {selectedModel ? (
              <div>
                {activeTab === 'plattegrond' && (
                  <PlattegrondTab
                    model={selectedModel}
                    images={images}
                    imageIndex={imageIndex}
                    prevImage={prevImage}
                    nextImage={nextImage}
                    setImageIndex={setImageIndex}
                    selectedStijl={selectedStijl}
                    setSelectedStijl={setSelectedStijl}
                    availableStijlen={availableStijlen}
                  />
                )}
                {activeTab === 'specificatie' && <SpecificatieTab model={selectedModel} />}
                {activeTab === 'samenstellen' && <SamenstellenTab model={selectedModel} />}
              </div>
            ) : (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <Building2 size={48} className="mx-auto mb-4 text-[#ccc]" />
                  <h3 className="text-lg font-semibold text-[#333]">Selecteer een model</h3>
                  <p className="text-sm text-[#777]">Gebruik de filters om een chalet te kiezen</p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* RIGHT SIDEBAR — Pricing */}
        {selectedModel && (
          <div className="w-72 flex-shrink-0 border-l border-[#e5e2d9] bg-[#FFFEF8] overflow-y-auto" data-testid="chalet-pricing">
            <div className="p-5 space-y-5">
              {/* PRIJSOVERZICHT */}
              <div>
                <h3 className="text-[11px] font-bold text-[#333] uppercase tracking-wider mb-3">Prijsoverzicht</h3>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-[#777]">Basisprijs</span>
                    <span className="font-semibold text-[#333]">€ {pricing.basisprijs?.toLocaleString('nl-NL')}</span>
                  </div>
                  <div className="border-t border-[#e5e2d9] pt-2">
                    <div className="flex justify-between text-sm">
                      <span className="font-semibold text-[#333]">Totaal excl. BTW</span>
                      <span className="font-bold text-[#333]">€ {pricing.totaal_excl_btw?.toLocaleString('nl-NL')}</span>
                    </div>
                  </div>
                  <div className="flex justify-between text-xs">
                    <span className="text-[#999]">BTW 21%</span>
                    <span className="text-[#999]">€ {pricing.btw_bedrag?.toLocaleString('nl-NL')}</span>
                  </div>
                  <div className="flex justify-between text-sm pt-1">
                    <span className="font-bold text-[#244628]">Totaal incl. BTW</span>
                    <span className="font-bold text-[#70C26C] text-base">€ {pricing.totaal_incl_btw?.toLocaleString('nl-NL')}</span>
                  </div>
                </div>
              </div>

              {/* OPERATIONAL LEASE */}
              <div className="bg-[#244628] rounded-xl p-4 text-white" data-testid="lease-card">
                <div className="text-xs text-white/70 mb-1 italic">Operational Lease</div>
                <div className="text-2xl font-bold">€ {pricing.lease_monthly?.toLocaleString('nl-NL')}</div>
                <div className="text-xs text-white/60 mt-0.5">per maand / {pricing.lease_months} mnd</div>
              </div>

              <p className="text-[10px] text-[#aaa] leading-relaxed">
                Prijzen zijn indicatief en onder voorbehoud. Transport en fundering niet inbegrepen.
              </p>

              {/* GESELECTEERD */}
              <div className="border-t border-[#e5e2d9] pt-4">
                <h3 className="text-[11px] font-bold text-[#333] uppercase tracking-wider mb-3">Geselecteerd</h3>
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-sm">
                    <Building2 size={14} className="text-[#70C26C]" />
                    <span className="text-[#333]">{selectedModel.name} — {selectedModel.oppervlakte_m2} m²</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <Home size={14} className="text-[#70C26C]" />
                    <span className="text-[#333]">{selectedModel.supplier_name}</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <Eye size={14} className="text-[#70C26C]" />
                    <span className="text-[#333] capitalize">{selectedStijl} Stijl</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <Bed size={14} className="text-[#70C26C]" />
                    <span className="text-[#333]">{selectedModel.slaapkamers} slk, {selectedModel.badkamers} bdk</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ==================== SUB COMPONENTS ====================

function DakIcon({ dakVorm, size = 16, className = '' }) {
  const Icon = DAK_ICONS[dakVorm] || Triangle;
  return <Icon size={size} className={className} />;
}

function PlattegrondTab({ model, images, imageIndex, prevImage, nextImage, setImageIndex, selectedStijl, setSelectedStijl, availableStijlen }) {
  return (
    <div className="max-w-3xl mx-auto space-y-5">
      {/* Image carousel */}
      <div className="relative rounded-xl overflow-hidden bg-[#f0ede6] aspect-[16/10] group">
        <div className="absolute top-3 left-3 z-10">
          <span className="bg-[#244628]/80 text-white text-xs px-2.5 py-1 rounded-full flex items-center gap-1">
            <Building2 size={12} /> {model.supplier_name}
          </span>
        </div>
        <img
          src={images[imageIndex]}
          alt={model.name}
          className="w-full h-full object-cover"
          data-testid="chalet-main-image"
        />
        <button onClick={prevImage} className="absolute left-3 top-1/2 -translate-y-1/2 w-9 h-9 bg-white/80 rounded-full flex items-center justify-center hover:bg-white transition-all opacity-0 group-hover:opacity-100" data-testid="img-prev">
          <ChevronLeft size={18} />
        </button>
        <button onClick={nextImage} className="absolute right-3 top-1/2 -translate-y-1/2 w-9 h-9 bg-white/80 rounded-full flex items-center justify-center hover:bg-white transition-all opacity-0 group-hover:opacity-100" data-testid="img-next">
          <ChevronRight size={18} />
        </button>
        <div className="absolute bottom-3 right-3 bg-black/50 text-white text-xs px-2 py-0.5 rounded">
          {imageIndex + 1} / {images.length}
        </div>
      </div>

      {/* Thumbnails */}
      <div className="flex justify-center gap-2">
        {images.map((img, i) => (
          <button key={i} onClick={() => setImageIndex(i)}
            className={`w-16 h-12 rounded-lg overflow-hidden border-2 transition-all ${i === imageIndex ? 'border-[#244628] ring-1 ring-[#244628]' : 'border-[#e5e2d9] opacity-60 hover:opacity-100'}`}
          >
            <img src={img} alt="" className="w-full h-full object-cover" />
          </button>
        ))}
      </div>

      {/* Style buttons */}
      <div className="flex justify-center gap-2">
        {['modern', 'luxe', 'landelijk'].map(s => {
          const available = availableStijlen.includes(s);
          const active = selectedStijl === s;
          return (
            <button key={s} onClick={() => available && setSelectedStijl(s)}
              className={`px-5 py-2 rounded-lg text-sm font-medium border transition-all flex items-center gap-1.5 ${
                !available ? 'opacity-30 cursor-not-allowed border-[#e5e2d9] text-[#ccc] bg-[#faf9f5]'
                : active ? 'bg-[#244628] text-white border-[#244628]'
                : 'bg-white text-[#555] border-[#e5e2d9] hover:border-[#70C26C]'
              }`}
              disabled={!available}
              data-testid={`stijl-${s}`}
            >
              {active && <Check size={14} />}
              {s.charAt(0).toUpperCase() + s.slice(1)}
            </button>
          );
        })}
      </div>

      {/* Floor plan placeholder */}
      <div>
        <h3 className="text-sm font-bold text-[#333] mb-2">Plattegrond</h3>
        <div className="bg-white border border-[#e5e2d9] rounded-xl p-6">
          <div className="flex items-center justify-center"
            style={{ width: '100%', maxWidth: 500, margin: '0 auto', aspectRatio: `${model.dimensions?.width || 12} / ${model.dimensions?.height || 4}` }}
          >
            <div className="w-full h-full border-2 border-[#244628] rounded-lg relative bg-[#FDF9ED]"
              style={{ minHeight: 120 }}
            >
              {/* Rooms layout */}
              <div className="absolute inset-2 flex gap-1">
                <div className="flex-1 border border-dashed border-[#70C26C] rounded flex items-center justify-center">
                  <span className="text-[10px] text-[#70C26C] font-medium">Woonkamer</span>
                </div>
                {Array.from({ length: model.slaapkamers }).map((_, i) => (
                  <div key={i} className="w-1/5 border border-dashed border-[#8B6914] rounded flex items-center justify-center">
                    <span className="text-[9px] text-[#8B6914] font-medium">Slk {i + 1}</span>
                  </div>
                ))}
                {Array.from({ length: model.badkamers }).map((_, i) => (
                  <div key={`b${i}`} className="w-[12%] border border-dashed border-[#0891b2] rounded flex items-center justify-center">
                    <span className="text-[8px] text-[#0891b2] font-medium">Bad</span>
                  </div>
                ))}
              </div>
              <div className="absolute bottom-1 right-2 text-[9px] text-[#aaa]">
                {model.oppervlakte_m2} m² — {model.dimensions?.width}x{model.dimensions?.height}m
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function SpecificatieTab({ model }) {
  const specs = [
    { label: 'Oppervlakte', value: `${model.oppervlakte_m2} m²`, icon: Ruler },
    { label: 'Slaapkamers', value: model.slaapkamers, icon: Bed },
    { label: 'Badkamers', value: model.badkamers, icon: Bath },
    { label: 'Max personen', value: model.max_personen, icon: Users },
    { label: 'Model vorm', value: model.model_vorm, icon: Square },
    { label: 'Dak vorm', value: model.dak_vorm, icon: Triangle },
    { label: 'Leverancier', value: model.supplier_name, icon: Building2 },
    { label: 'Afmetingen', value: `${model.dimensions?.width}m x ${model.dimensions?.height}m`, icon: Ruler },
  ];
  return (
    <div className="max-w-2xl mx-auto space-y-4">
      <h2 className="text-lg font-bold text-[#333]">Specificaties — {model.name}</h2>
      <p className="text-sm text-[#777]">{model.description}</p>
      <div className="grid grid-cols-2 gap-3">
        {specs.map((s, i) => (
          <div key={i} className="bg-white border border-[#e5e2d9] rounded-xl p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-[#70C26C]/10 flex items-center justify-center">
              <s.icon size={18} className="text-[#70C26C]" />
            </div>
            <div>
              <div className="text-[10px] text-[#999] uppercase tracking-wider">{s.label}</div>
              <div className="text-sm font-semibold text-[#333] capitalize">{s.value}</div>
            </div>
          </div>
        ))}
      </div>
      <div className="bg-white border border-[#e5e2d9] rounded-xl p-4">
        <h3 className="text-sm font-bold text-[#333] mb-2">Beschikbare stijlen</h3>
        <div className="flex gap-2">
          {model.stijlen.map(s => (
            <span key={s} className="px-3 py-1 bg-[#FDF9ED] border border-[#e5e2d9] rounded-full text-xs text-[#555] capitalize">{s}</span>
          ))}
        </div>
      </div>
    </div>
  );
}

function SamenstellenTab({ model }) {
  return (
    <div className="max-w-2xl mx-auto space-y-4">
      <h2 className="text-lg font-bold text-[#333]">Samenstellen — {model.name}</h2>
      <p className="text-sm text-[#777]">Configureer uw {model.name} naar wens. Selecteer opties per categorie.</p>
      {[
        { cat: 'Keuken', options: ['Basis Keuken (incl.)', 'Complete Keuken (+€3.500)', 'Luxe Keuken (+€8.500)'] },
        { cat: 'Badkamer', options: ['Basis Badkamer (incl.)', 'Complete Badkamer (+€2.800)', 'Wellness Badkamer (+€7.500)'] },
        { cat: 'Terras', options: ['Geen Terras', 'Klein Terras 6m² (+€3.200)', 'Groot Terras 15m² (+€8.000)'] },
        { cat: 'Interieur', options: ['Basis Interieur (incl.)', 'Comfort Interieur (+€4.500)', 'Luxe Interieur (+€12.000)'] },
        { cat: 'Klimaat', options: ['Geen', 'CV Verwarming (+€2.200)', 'Warmtepomp + Airco (+€4.800)'] },
        { cat: 'Duurzaamheid', options: ['Standaard', 'Zonnepanelen (+€3.200)', 'Off-Grid Pakket (+€14.000)'] },
      ].map(group => (
        <div key={group.cat} className="bg-white border border-[#e5e2d9] rounded-xl p-4">
          <h3 className="text-sm font-bold text-[#333] mb-2">{group.cat}</h3>
          <div className="grid grid-cols-3 gap-2">
            {group.options.map((opt, i) => (
              <button key={i}
                className={`text-xs p-2.5 rounded-lg border text-left transition-all ${i === 0 ? 'bg-[#244628] text-white border-[#244628]' : 'bg-[#FDF9ED] text-[#555] border-[#e5e2d9] hover:border-[#70C26C]'}`}
              >
                {opt}
              </button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
