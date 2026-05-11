import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import {
  ArrowLeft, Layers, Square, CornerDownRight, GitMerge, Columns2,
  Minus, Triangle, TrendingUp, Home, Hexagon, ChevronLeft, ChevronRight,
  Bed, Bath, Users, Ruler, Building2, Check, Eye, Settings, FileText,
  Tent, Factory, Sparkles, Package, Award, Map,
} from 'lucide-react';
import { Slider } from './components/ui/slider';
import SupplierProfile from './SupplierProfile';
import { SubsidyModule } from './SubsidyModule';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const VORM_ICONS = {
  alles: Layers, rechthoek: Square, 'l-vorm': CornerDownRight,
  't-vorm': GitMerge, dubbel: Columns2,
};
const DAK_ICONS = {
  alles: Layers, platdak: Minus, zadeldak: Triangle,
  lessenaars: TrendingUp, mansarde: Home, schilddak: Hexagon,
};

const FALLBACK_IMAGES = [
  'https://arcabo.nl/wp-content/uploads/1-New-Bay-A-buitenzijde-2024-uitgelicht.png',
  'https://campsolutions.com/wp-content/uploads/2020/12/Scherm%C2%ADafbeelding-2025-12-08-om-15.52.21-min-e1765205821482.png',
  'https://ucarecdn.com/76932055-baf1-402d-bedb-68e5b903160e/-/format/auto/-/resize/800x500/',
];

export function ChaletWizard({ onBack, onRoadmap }) {
  const [models, setModels] = useState([]);
  const [suppliers, setSuppliers] = useState([]);
  const [selectedModel, setSelectedModel] = useState(null);
  const [activeTab, setActiveTab] = useState('plattegrond');
  const [selectedStijl, setSelectedStijl] = useState('modern');
  const [imageIndex, setImageIndex] = useState(0);
  const [upgradeSelections, setUpgradeSelections] = useState({});
  const [upgradePricing, setUpgradePricing] = useState(null);
  const [showSubsidy, setShowSubsidy] = useState(false);

  // Filters
  const [bestemming, setBestemming] = useState('recreatie');
  const [oppRange, setOppRange] = useState([5, 120]);
  const [modelVorm, setModelVorm] = useState('alles');
  const [dakVorm, setDakVorm] = useState('alles');
  const [categorie, setCategorie] = useState('alles');
  const [supplierId, setSupplierId] = useState('alles');
  const [viewMode, setViewMode] = useState('configurator'); // 'configurator' or 'inspiratie'
  const [supplierProfileId, setSupplierProfileId] = useState(null);

  const SUPPLIER_MAP = { 'Kunert Group': 'kunert-group', 'Arcabo': 'arcabo', 'BBS Systeembouw': 'bbs-systeembouw', 'Campsolutions': 'campsolutions', 'Ticra Outdoor': 'ticra-outdoor', 'Madino': 'madino' };
  const openSupplierProfile = (name) => setSupplierProfileId(SUPPLIER_MAP[name] || null);

  // Fetch suppliers once
  useEffect(() => {
    axios.get(`${API}/chalet/suppliers`).then(r => setSuppliers(r.data)).catch(() => {});
  }, []);

  // Fetch models on filter change
  useEffect(() => {
    const fetchModels = async () => {
      try {
        const params = new URLSearchParams();
        if (bestemming) params.append('bestemming', bestemming);
        if (modelVorm !== 'alles') params.append('model_vorm', modelVorm);
        if (dakVorm !== 'alles') params.append('dak_vorm', dakVorm);
        if (categorie !== 'alles') params.append('categorie', categorie);
        if (supplierId !== 'alles') params.append('supplier_id', supplierId);
        params.append('min_m2', oppRange[0]);
        params.append('max_m2', oppRange[1]);
        const res = await axios.get(`${API}/chalet/models?${params.toString()}`);
        setModels(res.data);
        if (res.data.length > 0 && (!selectedModel || !res.data.find(m => m.id === selectedModel.id))) {
          setSelectedModel(res.data[0]);
        } else if (res.data.length === 0) {
          setSelectedModel(null);
        }
      } catch {
        toast.error('Kon modellen niet laden');
      }
    };
    fetchModels();
  }, [bestemming, modelVorm, dakVorm, oppRange, categorie, supplierId]);

  useEffect(() => { setImageIndex(0); }, [selectedModel, selectedStijl]);

  // Reset upgrades when model changes
  useEffect(() => {
    setUpgradeSelections({});
    setUpgradePricing(null);
  }, [selectedModel?.id]);

  // Recalculate pricing when upgrades change
  useEffect(() => {
    if (!selectedModel || Object.keys(upgradeSelections).length === 0) {
      setUpgradePricing(null);
      return;
    }
    axios.post(`${API}/chalet/calculate-with-upgrades`, {
      model_id: selectedModel.id,
      upgrades: upgradeSelections,
    }).then(res => setUpgradePricing(res.data)).catch(() => {});
  }, [upgradeSelections, selectedModel?.id]);

  const images = useMemo(() => {
    if (!selectedModel?.images) return FALLBACK_IMAGES;
    return selectedModel.images[selectedStijl] || selectedModel.images.modern || FALLBACK_IMAGES;
  }, [selectedModel, selectedStijl]);

  const availableStijlen = selectedModel?.stijlen || ['modern'];
  const prevImage = () => setImageIndex(i => (i - 1 + images.length) % images.length);
  const nextImage = () => setImageIndex(i => (i + 1) % images.length);
  const pricing = upgradePricing?.pricing || selectedModel?.pricing || {};

  // Count per category
  const chaletCount = models.filter(m => m.categorie === 'chalet').length;
  const glampingCount = models.filter(m => m.categorie === 'glamping').length;

  return (
    <>
    <div className="h-screen w-full flex flex-col overflow-hidden bg-[#FDF9ED]" data-testid="chalet-wizard">
      {/* Header */}
      <header className="h-14 bg-[#244628] flex items-center justify-between px-6 flex-shrink-0">
        <div className="flex items-center gap-3">
          <button onClick={onBack} className="flex items-center gap-2 hover:opacity-80 transition-opacity" data-testid="chalet-back-btn">
            <img src="/recra-logo-white.png" alt="RECRA" className="h-7" onError={e => { e.target.style.display = 'none'; }} />
            <span className="text-white font-bold text-lg tracking-wide">RECRA</span>
          </button>
          <span className="text-white/40">|</span>
          <span className="text-[#70C26C] text-sm font-semibold">Chalet & Stay Configurator</span>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={() => setShowSubsidy(!showSubsidy)}
            className={`text-xs px-3 py-1.5 rounded-full flex items-center gap-1.5 transition-all ${showSubsidy ? 'bg-[#f59e0b] text-white font-bold' : 'text-white/70 hover:text-white'}`}
            data-testid="chalet-subsidy-btn">
            <TrendingUp size={13} /> Subsidie Check
          </button>
          <button onClick={() => setViewMode('configurator')}
            className={`text-xs px-3 py-1.5 rounded-full flex items-center gap-1.5 transition-all ${viewMode === 'configurator' ? 'bg-[#70C26C] text-[#244628] font-bold' : 'text-white/70 hover:text-white'}`}
            data-testid="mode-configurator">
            <Settings size={13} /> Configurator
          </button>
          <button onClick={() => setViewMode('inspiratie')}
            className={`text-xs px-3 py-1.5 rounded-full flex items-center gap-1.5 transition-all ${viewMode === 'inspiratie' ? 'bg-[#70C26C] text-[#244628] font-bold' : 'text-white/70 hover:text-white'}`}
            data-testid="mode-inspiratie">
            <Sparkles size={13} /> Inspiratie Pakketten
          </button>
        </div>
        <button onClick={onBack} className="text-white/70 hover:text-white text-sm flex items-center gap-1" data-testid="back-to-flows">
          <ArrowLeft size={16} /> Terug naar flows
        </button>
      </header>

      {/* Main content */}
      {viewMode === 'inspiratie' ? (
        <InspiratieView onSelectModel={(model) => { setSelectedModel(model); setViewMode('configurator'); setActiveTab('plattegrond'); }} />
      ) : (
      <div className="flex-1 flex overflow-hidden">
        {/* LEFT SIDEBAR — Filters */}
        <div className="w-[270px] flex-shrink-0 border-r border-[#e5e2d9] bg-[#FFFEF8] overflow-y-auto" data-testid="chalet-filters">
          <div className="p-4 space-y-4">
            {/* CATEGORIE */}
            <div>
              <h3 className="text-[11px] font-bold text-[#333] uppercase tracking-wider mb-2">Categorie</h3>
              <div className="flex gap-1.5">
                {[
                  { id: 'alles', label: 'Alles', icon: Layers },
                  { id: 'chalet', label: `Chalets`, icon: Building2 },
                  { id: 'glamping', label: `Glamping`, icon: Tent },
                ].map(c => (
                  <button key={c.id} onClick={() => setCategorie(c.id)}
                    className={`flex-1 flex items-center justify-center gap-1.5 text-xs px-2 py-2 rounded-lg border transition-all ${categorie === c.id ? 'bg-[#244628] text-white border-[#244628]' : 'bg-white text-[#555] border-[#e5e2d9] hover:border-[#70C26C]'}`}
                    data-testid={`cat-${c.id}`}
                  >
                    <c.icon size={13} />
                    {c.label}
                  </button>
                ))}
              </div>
            </div>

            {/* LEVERANCIER */}
            <div>
              <h3 className="text-[11px] font-bold text-[#333] uppercase tracking-wider mb-2">Leverancier</h3>
              <div className="flex flex-wrap gap-1.5">
                <button onClick={() => setSupplierId('alles')}
                  className={`text-xs px-2.5 py-1.5 rounded-md border transition-all ${supplierId === 'alles' ? 'bg-[#244628] text-white border-[#244628]' : 'bg-white text-[#555] border-[#e5e2d9] hover:border-[#70C26C]'}`}
                  data-testid="supplier-alles"
                >Alle</button>
                {suppliers.map(s => (
                  <button key={s.id} onClick={() => setSupplierId(s.id)}
                    className={`text-xs px-2.5 py-1.5 rounded-md border transition-all flex items-center gap-1 ${supplierId === s.id ? 'bg-[#244628] text-white border-[#244628]' : 'bg-white text-[#555] border-[#e5e2d9] hover:border-[#70C26C]'}`}
                    data-testid={`supplier-${s.id}`}
                  >
                    {s.pleisureworld_partner && <Award size={10} className={supplierId === s.id ? 'text-[#70C26C]' : 'text-[#8B6914]'} />}
                    {s.name}
                  </button>
                ))}
              </div>
            </div>

            {/* BESTEMMING */}
            <div>
              <h3 className="text-[11px] font-bold text-[#333] uppercase tracking-wider mb-2">Bestemming</h3>
              <div className="flex gap-2">
                <button
                  className="text-xs px-3 py-1.5 rounded-md border bg-[#244628] text-white border-[#244628]"
                  data-testid="bestemming-recreatie"
                >
                  Recreatie
                </button>
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
                <Slider value={oppRange} onValueChange={setOppRange} min={5} max={120} step={5}
                  className="[&_[role=slider]]:bg-[#70C26C] [&_[role=slider]]:border-[#70C26C]"
                  data-testid="oppervlakte-slider" />
                <div className="flex justify-between text-[10px] text-[#aaa] mt-1">
                  <span>5</span><span>30</span><span>60</span><span>90</span><span>120</span>
                </div>
              </div>
            </div>

            {/* MODEL VORM */}
            <div>
              <h3 className="text-[11px] font-bold text-[#333] uppercase tracking-wider mb-2">Model Vorm</h3>
              <div className="grid grid-cols-5 gap-1">
                {[
                  { id: 'alles', label: 'Alles' }, { id: 'rechthoek', label: 'Rechthoek' },
                  { id: 'l-vorm', label: 'L-vorm' }, { id: 't-vorm', label: 'T-vorm' },
                  { id: 'dubbel', label: 'Dubbel' },
                ].map(v => {
                  const Icon = VORM_ICONS[v.id] || Layers;
                  return (
                    <button key={v.id} onClick={() => setModelVorm(v.id)}
                      className={`flex flex-col items-center gap-1 py-2 px-1 rounded-lg border text-[9px] transition-all ${modelVorm === v.id ? 'bg-[#244628] text-white border-[#244628]' : 'bg-white text-[#666] border-[#e5e2d9] hover:border-[#70C26C]'}`}
                      data-testid={`vorm-${v.id}`}
                    >
                      <Icon size={16} /><span className="leading-tight text-center">{v.label}</span>
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
                  { id: 'alles', label: 'Alles' }, { id: 'platdak', label: 'Platdak' },
                  { id: 'zadeldak', label: 'Zadeldak' }, { id: 'lessenaars', label: 'Lessenaars' },
                  { id: 'mansarde', label: 'Mansarde' }, { id: 'schilddak', label: 'Schilddak' },
                ].map(d => {
                  const Icon = DAK_ICONS[d.id] || Layers;
                  return (
                    <button key={d.id} onClick={() => setDakVorm(d.id)}
                      className={`flex flex-col items-center gap-1 py-2 px-1 rounded-lg border text-[9px] transition-all ${dakVorm === d.id ? 'bg-[#244628] text-white border-[#244628]' : 'bg-white text-[#666] border-[#e5e2d9] hover:border-[#70C26C]'}`}
                      data-testid={`dak-${d.id}`}
                    >
                      <Icon size={16} /><span className="leading-tight text-center">{d.label}</span>
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
              <div className="space-y-1.5 max-h-[400px] overflow-y-auto pr-1">
                {models.map(m => {
                  const isActive = selectedModel?.id === m.id;
                  const isGlamping = m.categorie === 'glamping';
                  return (
                    <button key={m.id} onClick={() => { setSelectedModel(m); setActiveTab('plattegrond'); }}
                      className={`w-full text-left p-2.5 rounded-lg border transition-all ${isActive ? 'bg-[#244628] text-white border-[#244628]' : 'bg-white text-[#333] border-[#e5e2d9] hover:border-[#70C26C]'}`}
                      data-testid={`model-${m.id}`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-1.5 min-w-0">
                          {isGlamping ? <Tent size={13} className={isActive ? 'text-white/60' : 'text-[#2D6A4F]'} /> : <Building2 size={13} className={isActive ? 'text-white/60' : 'text-[#8B6914]'} />}
                          <span className="text-sm font-bold truncate">{m.name}</span>
                        </div>
                        <DakIcon dakVorm={m.dak_vorm} size={13} className={isActive ? 'text-white/50' : 'text-[#ccc]'} />
                      </div>
                      <div className="flex items-center gap-1.5 mt-0.5">
                        <span
                          role="button"
                          tabIndex={0}
                          className={`text-[10px] px-1.5 py-0.5 rounded hover:underline cursor-pointer ${isActive ? 'bg-white/20 text-white/80' : 'bg-[#FDF9ED] text-[#777]'}`}
                          onClick={(e) => { e.stopPropagation(); openSupplierProfile(m.supplier_name); }}
                          onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.stopPropagation(); e.preventDefault(); openSupplierProfile(m.supplier_name); } }}
                          data-testid={`model-supplier-${m.id}`}
                        >
                          {m.supplier_name}
                        </span>
                        <span className={`text-[10px] ${isActive ? 'text-white/60' : 'text-[#aaa]'}`}>{m.oppervlakte_m2} m²</span>
                      </div>
                      <div className="flex items-center justify-between mt-1">
                        <span className={`text-[10px] ${isActive ? 'text-white/60' : 'text-[#999]'}`}>{m.slaapkamers} slk · {m.badkamers} bdk · {m.max_personen}p</span>
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
        <div className="flex-1 flex flex-col overflow-hidden min-w-0">
          {selectedModel && (
            <div className="h-12 bg-white border-b border-[#e5e2d9] flex items-center justify-between px-5 flex-shrink-0">
              <div className="flex items-center gap-2 text-sm min-w-0 mr-4">
                <span className="font-bold text-[#333] truncate">{selectedModel.name}</span>
                <span className="text-[#aaa] flex-shrink-0">·</span>
                <span className="text-[#777] flex-shrink-0">{selectedModel.supplier_name}</span>
                <span className="text-[#aaa] flex-shrink-0">·</span>
                <span className="text-[#777] capitalize flex-shrink-0">{selectedModel.dak_vorm}</span>
                <span className="text-[#aaa] flex-shrink-0">·</span>
                <span className="text-[#777] flex-shrink-0">{selectedModel.oppervlakte_m2} m²</span>
                <span className="text-[#aaa] flex-shrink-0">·</span>
                <span className="font-bold text-[#244628] flex-shrink-0">€ {selectedModel.basisprijs.toLocaleString('nl-NL')}</span>
              </div>
              <div className="flex gap-1 flex-shrink-0">
                {[
                  { id: 'plattegrond', label: 'Plattegrond en 3D', icon: Eye },
                  { id: 'specificatie', label: 'Specificatie', icon: FileText },
                  { id: 'samenstellen', label: 'Samenstellen', icon: Settings },
                ].map(tab => (
                  <button key={tab.id} onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full transition-all whitespace-nowrap ${activeTab === tab.id ? 'bg-[#244628] text-white' : 'text-[#777] hover:bg-[#FDF9ED]'}`}
                    data-testid={`tab-${tab.id}`}
                  >
                    <tab.icon size={13} />{tab.label}
                  </button>
                ))}
              </div>
            </div>
          )}

          <div className="flex-1 overflow-y-auto p-6">
            {selectedModel ? (
              <>
                {activeTab === 'plattegrond' && (
                  <PlattegrondTab model={selectedModel} images={images} imageIndex={imageIndex}
                    prevImage={prevImage} nextImage={nextImage} setImageIndex={setImageIndex}
                    selectedStijl={selectedStijl} setSelectedStijl={setSelectedStijl} availableStijlen={availableStijlen} />
                )}
                {activeTab === 'specificatie' && <SpecificatieTab model={selectedModel} />}
                {activeTab === 'samenstellen' && <SamenstellenTab model={selectedModel} selections={upgradeSelections} onSelect={setUpgradeSelections} onSupplierClick={openSupplierProfile} />}
              </>
            ) : (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <Building2 size={48} className="mx-auto mb-4 text-[#ccc]" />
                  <h3 className="text-lg font-semibold text-[#333]">Selecteer een model</h3>
                  <p className="text-sm text-[#777]">Gebruik de filters links om een chalet of glamping model te kiezen</p>
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
                  {pricing.upgrades_total > 0 && (
                    <div className="flex justify-between text-sm">
                      <span className="text-[#70C26C]">Upgrades</span>
                      <span className="font-semibold text-[#70C26C]">+ € {pricing.upgrades_total?.toLocaleString('nl-NL')}</span>
                    </div>
                  )}
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

              {onRoadmap && (
                <button onClick={onRoadmap} className="w-full flex items-center justify-center gap-2 text-xs font-medium text-[#244628] border border-[#244628] rounded-xl py-2.5 hover:bg-[#244628] hover:text-white transition-all" data-testid="chalet-roadmap-btn">
                  <Map size={14} /> Idee naar Realisatie
                </button>
              )}

              {/* GESELECTEERD */}
              <div className="border-t border-[#e5e2d9] pt-4">
                <h3 className="text-[11px] font-bold text-[#333] uppercase tracking-wider mb-3">Geselecteerd</h3>
                <div className="space-y-2.5">
                  <div className="flex items-center gap-2.5 text-sm">
                    {selectedModel.categorie === 'glamping' ? <Tent size={14} className="text-[#2D6A4F]" /> : <Building2 size={14} className="text-[#70C26C]" />}
                    <span className="text-[#333]">{selectedModel.name} — {selectedModel.oppervlakte_m2} m²</span>
                  </div>
                  <div className="flex items-center gap-2.5 text-sm">
                    <Factory size={14} className="text-[#70C26C]" />
                    <button onClick={() => openSupplierProfile(selectedModel.supplier_name)} className="text-[#244628] font-medium hover:underline flex items-center gap-1" data-testid="supplier-profile-link">
                      {selectedModel.supplier_name}
                      <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M7 17L17 7M17 7H7M17 7V17"/></svg>
                    </button>
                  </div>
                  <div className="flex items-center gap-2.5 text-sm">
                    <Eye size={14} className="text-[#70C26C]" />
                    <span className="text-[#333] capitalize">{selectedStijl} Stijl</span>
                  </div>
                  <div className="flex items-center gap-2.5 text-sm">
                    <Bed size={14} className="text-[#70C26C]" />
                    <span className="text-[#333]">{selectedModel.slaapkamers} slk, {selectedModel.badkamers} bdk</span>
                  </div>
                  <div className="flex items-center gap-2.5 text-sm">
                    <Users size={14} className="text-[#70C26C]" />
                    <span className="text-[#333]">Max {selectedModel.max_personen} personen</span>
                  </div>
                  <div className="flex items-center gap-2.5 text-sm">
                    <Ruler size={14} className="text-[#70C26C]" />
                    <span className="text-[#333] capitalize">{selectedModel.model_vorm} · {selectedModel.dak_vorm}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
      )}
    </div>
    {supplierProfileId && (
      <SupplierProfile partnerId={supplierProfileId} onClose={() => setSupplierProfileId(null)} />
    )}
    {showSubsidy && (
      <div className="fixed right-0 top-14 bottom-0 w-80 bg-[#FFFEF8] border-l border-[#e5e2d9] z-40 shadow-xl" data-testid="chalet-subsidy-panel">
        <SubsidyModule
          onClose={() => setShowSubsidy(false)}
          projectContext={{
            sector: 'Recreatie',
            projectomschrijving: selectedModel ? `${selectedModel.name} (${selectedModel.supplier_name})` : '',
          }}
        />
      </div>
    )}
    </>
  );
}

// ==================== INSPIRATIE VIEW ====================

function InspiratieView({ onSelectModel }) {
  const [pakketten, setPakketten] = useState([]);
  const [selectedPakket, setSelectedPakket] = useState(null);
  const [pakketDetail, setPakketDetail] = useState(null);

  useEffect(() => {
    axios.get(`${API}/chalet/inspiratie`).then(r => setPakketten(r.data)).catch(() => {});
  }, []);

  useEffect(() => {
    if (selectedPakket) {
      axios.get(`${API}/chalet/inspiratie/${selectedPakket}`).then(r => setPakketDetail(r.data)).catch(() => {});
    } else {
      setPakketDetail(null);
    }
  }, [selectedPakket]);

  if (pakketDetail) {
    return (
      <div className="flex-1 overflow-y-auto p-6">
        <div className="max-w-4xl mx-auto space-y-6">
          <button onClick={() => setSelectedPakket(null)} className="text-sm text-[#777] hover:text-[#333] flex items-center gap-1" data-testid="back-to-pakketten">
            <ArrowLeft size={14} /> Terug naar pakketten
          </button>

          <div className="flex items-start justify-between">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs px-2 py-0.5 rounded-full text-white font-medium" style={{ backgroundColor: pakketDetail.badge_color }}>
                  {pakketDetail.badge}
                </span>
              </div>
              <h1 className="text-2xl font-bold text-[#244628]">{pakketDetail.name}</h1>
              <p className="text-sm text-[#777] mt-1">{pakketDetail.subtitle}</p>
            </div>
            <div className="text-right">
              <div className="text-xs text-[#999]">Totaal incl. BTW</div>
              <div className="text-2xl font-bold text-[#70C26C]">€ {pakketDetail.totals?.total_investment_incl_btw?.toLocaleString('nl-NL')}</div>
              <div className="text-xs text-[#777]">Lease: € {pakketDetail.totals?.total_lease_monthly?.toLocaleString('nl-NL')}/mnd</div>
            </div>
          </div>

          <p className="text-sm text-[#555] bg-white border border-[#e5e2d9] rounded-xl p-4">{pakketDetail.description}</p>

          <div className="space-y-3">
            <h3 className="text-sm font-bold text-[#333] uppercase tracking-wider">Modellen in dit pakket ({pakketDetail.totals?.total_units} units)</h3>
            {pakketDetail.enriched_models?.map((item, i) => (
              <div key={i} className="bg-white border border-[#e5e2d9] rounded-xl p-4 flex items-center justify-between hover:shadow-sm transition-shadow">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-lg bg-[#244628]/10 flex items-center justify-center">
                    {item.model.categorie === 'glamping' ? <Tent size={20} className="text-[#2D6A4F]" /> : <Building2 size={20} className="text-[#8B6914]" />}
                  </div>
                  <div>
                    <div className="text-sm font-bold text-[#333]">{item.quantity}x {item.model.name}</div>
                    <div className="text-xs text-[#999]">{item.model.supplier_name} · {item.model.oppervlakte_m2} m² · {item.model.slaapkamers} slk</div>
                    {item.upgrade_details?.length > 0 && (
                      <div className="flex gap-1 mt-1 flex-wrap">
                        {item.upgrade_details.map((u, j) => (
                          <span key={j} className="text-[9px] px-1.5 py-0.5 rounded bg-[#70C26C]/10 text-[#2D6A4F]">{u.name}</span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-bold text-[#333]">€ {item.line_total?.toLocaleString('nl-NL')}</div>
                  <div className="text-xs text-[#999]">€ {item.line_lease?.toLocaleString('nl-NL')}/mnd</div>
                </div>
              </div>
            ))}
          </div>

          <div className="bg-[#244628] rounded-xl p-5 text-white">
            <h3 className="text-sm font-bold mb-3 flex items-center gap-2"><Award size={16} className="text-[#70C26C]" /> Highlights</h3>
            <div className="grid grid-cols-2 gap-2">
              {pakketDetail.highlights?.map((h, i) => (
                <div key={i} className="flex items-center gap-2 text-sm text-white/90">
                  <Check size={14} className="text-[#70C26C]" /> {h}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-6">
      <div className="max-w-4xl mx-auto space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-[#244628]">Inspiratie Pakketten</h1>
          <p className="text-sm text-[#777] mt-1">
            Samen met leveranciers samengestelde concepten — direct doorrekenen in de configurator.
          </p>
        </div>
        <div className="grid grid-cols-3 gap-4">
          {pakketten.map(p => (
            <button key={p.id} onClick={() => setSelectedPakket(p.id)}
              className="bg-white border border-[#e5e2d9] rounded-xl p-5 text-left hover:shadow-md transition-all group"
              data-testid={`pakket-${p.id}`}
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-[10px] px-2 py-0.5 rounded-full text-white font-medium" style={{ backgroundColor: p.badge_color }}>
                  {p.badge}
                </span>
                <Package size={16} className="text-[#ccc] group-hover:text-[#70C26C] transition-colors" />
              </div>
              <h3 className="text-base font-bold text-[#333] mb-1">{p.name}</h3>
              <p className="text-xs text-[#777] mb-3">{p.subtitle}</p>
              <div className="flex items-center justify-between pt-3 border-t border-[#f0ede6]">
                <span className="text-xs text-[#999]">{p.total_units} units</span>
                <span className="text-sm font-bold text-[#244628]">~ € {p.estimated_investment?.toLocaleString('nl-NL')}</span>
              </div>
              <div className="mt-2 flex gap-1 flex-wrap">
                {p.highlights?.slice(0, 2).map((h, i) => (
                  <span key={i} className="text-[9px] px-1.5 py-0.5 rounded-full bg-[#FDF9ED] text-[#777] border border-[#e5e2d9]">{h}</span>
                ))}
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

// ==================== SUB COMPONENTS ====================

function DakIcon({ dakVorm, size = 16, className = '' }) {
  const Icon = DAK_ICONS[dakVorm] || Triangle;
  return <Icon size={size} className={className} />;
}

/* Glamping tent floor plan — open ruimte, canvas vorm, geen harde kamers */
function GlampingFloorPlan({ model }) {
  const w = model.dimensions?.width || 8;
  const h = model.dimensions?.height || 5;
  const isDome = model.name.toLowerCase().includes('dome');
  const isHat = model.name.toLowerCase().includes('hat');
  const hasWC = model.badkamers > 0;
  const slk = model.slaapkamers;

  // SVG based layout for glamping
  const svgW = 400;
  const svgH = Math.round(svgW * (h / w));
  const pad = 15;
  const innerW = svgW - pad * 2;
  const innerH = svgH - pad * 2;

  return (
    <div className="flex items-center justify-center" style={{ maxWidth: 480, margin: '0 auto' }}>
      <svg viewBox={`0 0 ${svgW} ${svgH + 30}`} className="w-full" style={{ maxHeight: 320 }}>
        {/* Canvas/tent outline */}
        {isDome ? (
          <ellipse cx={svgW / 2} cy={svgH / 2} rx={innerW / 2} ry={innerH / 2}
            fill="#f0ede6" stroke="#2D6A4F" strokeWidth="2.5" strokeDasharray="8 4" />
        ) : isHat ? (
          <>
            <polygon points={`${svgW/2},${pad - 5} ${svgW - pad},${svgH - pad} ${pad},${svgH - pad}`}
              fill="#f0ede6" stroke="#2D6A4F" strokeWidth="2.5" strokeDasharray="8 4" />
          </>
        ) : (
          <rect x={pad} y={pad} width={innerW} height={innerH} rx="8"
            fill="#f0ede6" stroke="#2D6A4F" strokeWidth="2.5" strokeDasharray="8 4" />
        )}

        {/* Open leefruimte label */}
        <text x={svgW / 2} y={svgH * 0.35} textAnchor="middle" fill="#2D6A4F" fontSize="13" fontWeight="600">
          Leefruimte
        </text>
        <text x={svgW / 2} y={svgH * 0.35 + 16} textAnchor="middle" fill="#2D6A4F" fontSize="10" opacity="0.6">
          open ruimte
        </text>

        {/* Slaapruimtes — als gestippelde zones aan de zijkant */}
        {slk > 0 && Array.from({ length: slk }).map((_, i) => {
          const zoneW = innerW * 0.22;
          const zoneH = innerH * 0.35;
          const x = isDome
            ? svgW / 2 - (slk * zoneW * 0.6) / 2 + i * zoneW * 1.1
            : pad + 12 + i * (zoneW + 8);
          const y = isDome ? svgH * 0.55 : svgH - pad - zoneH - 8;
          return (
            <g key={i}>
              <rect x={x} y={y} width={zoneW} height={zoneH} rx="4"
                fill="rgba(139,105,20,0.08)" stroke="#8B6914" strokeWidth="1.5" strokeDasharray="4 3" />
              <text x={x + zoneW / 2} y={y + zoneH / 2 - 4} textAnchor="middle" fill="#8B6914" fontSize="9" fontWeight="600">
                Slaapruimte {slk > 1 ? i + 1 : ''}
              </text>
              {/* Bed icon */}
              <rect x={x + zoneW / 2 - 10} y={y + zoneH / 2 + 4} width="20" height="8" rx="2"
                fill="none" stroke="#8B6914" strokeWidth="1" opacity="0.5" />
            </g>
          );
        })}

        {/* Sanitair zone — alleen als badkamers > 0 */}
        {hasWC && (
          <g>
            <rect x={svgW - pad - innerW * 0.18 - 8} y={svgH - pad - innerH * 0.3 - 8}
              width={innerW * 0.18} height={innerH * 0.3} rx="4"
              fill="rgba(8,145,178,0.08)" stroke="#0891b2" strokeWidth="1.5" strokeDasharray="4 3" />
            <text x={svgW - pad - innerW * 0.09 - 8} y={svgH - pad - innerH * 0.15 - 4}
              textAnchor="middle" fill="#0891b2" fontSize="9" fontWeight="600">Sanitair</text>
          </g>
        )}

        {/* Terras/ingang indicatie */}
        {!isDome && !isHat && (
          <g>
            <line x1={svgW / 2 - 25} y1={pad} x2={svgW / 2 + 25} y2={pad}
              stroke="#70C26C" strokeWidth="4" strokeLinecap="round" />
            <text x={svgW / 2} y={pad - 5} textAnchor="middle" fill="#70C26C" fontSize="8">INGANG</text>
          </g>
        )}

        {/* Afmetingen */}
        <text x={svgW / 2} y={svgH + 20} textAnchor="middle" fill="#aaa" fontSize="10">
          {model.oppervlakte_m2} m² — {w}x{h}m
        </text>
      </svg>
    </div>
  );
}

/* Chalet floor plan — traditionele kamer-indeling */
function ChaletFloorPlan({ model }) {
  const w = model.dimensions?.width || 12;
  const h = model.dimensions?.height || 4;

  return (
    <div className="flex items-center justify-center" style={{ width: '100%', maxWidth: 500, margin: '0 auto', aspectRatio: `${w} / ${h}` }}>
      <div className="w-full h-full border-2 border-[#244628] rounded-lg relative bg-[#FDF9ED]" style={{ minHeight: 100 }}>
        <div className="absolute inset-2 flex gap-1">
          <div className="flex-1 border border-dashed border-[#70C26C] rounded flex items-center justify-center">
            <span className="text-[10px] text-[#70C26C] font-medium">Woonkamer</span>
          </div>
          {Array.from({ length: model.slaapkamers }).map((_, i) => (
            <div key={i} className="w-1/5 border border-dashed border-[#8B6914] rounded flex items-center justify-center">
              <span className="text-[9px] text-[#8B6914] font-medium">Slk {i + 1}</span>
            </div>
          ))}
          {model.badkamers > 0 && Array.from({ length: model.badkamers }).map((_, i) => (
            <div key={`b${i}`} className="w-[12%] border border-dashed border-[#0891b2] rounded flex items-center justify-center">
              <span className="text-[8px] text-[#0891b2] font-medium">Bad</span>
            </div>
          ))}
        </div>
        <div className="absolute bottom-1 right-2 text-[9px] text-[#aaa]">
          {model.oppervlakte_m2} m² — {w}x{h}m
        </div>
      </div>
    </div>
  );
}

function PlattegrondTab({ model, images, imageIndex, prevImage, nextImage, setImageIndex, selectedStijl, setSelectedStijl, availableStijlen }) {
  return (
    <div className="max-w-3xl mx-auto space-y-5">
      {/* Image carousel */}
      <div className="relative rounded-xl overflow-hidden bg-[#f0ede6] aspect-[16/10] group">
        <div className="absolute top-3 left-3 z-10 flex gap-2">
          <span className="bg-[#244628]/80 text-white text-xs px-2.5 py-1 rounded-full flex items-center gap-1">
            {model.categorie === 'glamping' ? <Tent size={12} /> : <Building2 size={12} />}
            {model.supplier_name}
          </span>
          <span className="bg-white/80 text-[#333] text-xs px-2.5 py-1 rounded-full capitalize">
            {model.categorie}
          </span>
        </div>
        <img src={images[imageIndex]} alt={model.name} className="w-full h-full object-cover" data-testid="chalet-main-image" />
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
              disabled={!available} data-testid={`stijl-${s}`}
            >
              {active && <Check size={14} />}
              {s.charAt(0).toUpperCase() + s.slice(1)}
            </button>
          );
        })}
      </div>

      {/* Floor plan */}
      <div>
        <h3 className="text-sm font-bold text-[#333] mb-2">Plattegrond</h3>
        <div className="bg-white border border-[#e5e2d9] rounded-xl p-6">
          {model.categorie === 'glamping' ? (
            <GlampingFloorPlan model={model} />
          ) : (
            <ChaletFloorPlan model={model} />
          )}
        </div>
      </div>

      {/* Description */}
      <div className="bg-white border border-[#e5e2d9] rounded-xl p-4">
        <p className="text-sm text-[#555] leading-relaxed">{model.description}</p>
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
    { label: 'Leverancier', value: model.supplier_name, icon: Factory },
    { label: 'Afmetingen', value: `${model.dimensions?.width}m x ${model.dimensions?.height}m`, icon: Ruler },
    { label: 'Categorie', value: model.categorie, icon: model.categorie === 'glamping' ? Tent : Building2 },
  ];
  return (
    <div className="max-w-2xl mx-auto space-y-4">
      <h2 className="text-lg font-bold text-[#333]">Specificaties — {model.name}</h2>
      <p className="text-sm text-[#777]">{model.description}</p>
      <div className="grid grid-cols-3 gap-3">
        {specs.map((s, i) => (
          <div key={i} className="bg-white border border-[#e5e2d9] rounded-xl p-3 flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-[#70C26C]/10 flex items-center justify-center flex-shrink-0">
              <s.icon size={16} className="text-[#70C26C]" />
            </div>
            <div className="min-w-0">
              <div className="text-[10px] text-[#999] uppercase tracking-wider">{s.label}</div>
              <div className="text-sm font-semibold text-[#333] capitalize truncate">{s.value}</div>
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
      <div className="bg-white border border-[#e5e2d9] rounded-xl p-4">
        <h3 className="text-sm font-bold text-[#333] mb-2">Bestemmingen</h3>
        <div className="flex gap-2">
          {model.bestemmingen.map(b => (
            <span key={b} className="px-3 py-1 bg-[#FDF9ED] border border-[#e5e2d9] rounded-full text-xs text-[#555] capitalize">{b}</span>
          ))}
        </div>
      </div>
    </div>
  );
}

function SamenstellenTab({ model, selections, onSelect, onSupplierClick }) {
  const [options, setOptions] = useState({});

  useEffect(() => {
    axios.get(`${API}/chalet/upgrade-options/${model.categorie}`).then(res => setOptions(res.data)).catch(() => {});
  }, [model.categorie]);

  const handleSelect = (catKey, optionId) => {
    onSelect(prev => ({ ...prev, [catKey]: optionId }));
  };

  const categoryLabels = {
    keuken: 'Keuken', badkamer: 'Badkamer', terras: 'Terras — Madino', interieur: 'Interieur',
    klimaat: 'Klimaat', duurzaamheid: 'Duurzaamheid', sanitair: 'Sanitair',
    inrichting: 'Inrichting', vlonder: 'Vlonder / Fundament', verlichting: 'Verlichting',
    wellness: 'Wellness — Ticra Outdoor',
  };

  const categoryIcons = { wellness: 'droplets' };

  return (
    <div className="max-w-2xl mx-auto space-y-4">
      <h2 className="text-lg font-bold text-[#333]">Samenstellen — {model.name}</h2>
      <p className="text-sm text-[#777]">
        Selecteer upgrades per categorie. De prijs wordt direct bijgewerkt in het overzicht rechts.
      </p>
      {Object.entries(options).map(([catKey, catOptions]) => {
        const selected = selections[catKey] || catOptions[0]?.id;
        const isWellness = catKey === 'wellness';
        const isTerras = catKey === 'terras';
        const hasImages = isWellness || isTerras;
        const supplierTag = isWellness ? 'Ticra Outdoor' : (isTerras ? 'Madino' : null);
        const tagColor = isWellness ? '#8B5E3C' : '#10b981';
        return (
          <div key={catKey} className="bg-white border border-[#e5e2d9] rounded-xl p-4" data-testid={`upgrade-${catKey}`}>
            <h3 className="text-sm font-bold text-[#333] mb-2 flex items-center gap-2">
              {categoryLabels[catKey] || catKey}
              {supplierTag && (
                <button
                  onClick={() => onSupplierClick && onSupplierClick(supplierTag)}
                  className="text-[10px] font-normal px-2 py-0.5 rounded-full hover:opacity-80 transition-opacity cursor-pointer"
                  style={{ backgroundColor: `${tagColor}1A`, color: tagColor }}
                  data-testid={`supplier-tag-${catKey}`}
                >
                  {supplierTag}
                </button>
              )}
            </h3>
            <div className={`grid gap-2 ${hasImages ? 'grid-cols-2' : 'grid-cols-3'}`}>
              {catOptions.map(opt => {
                const isActive = selected === opt.id;
                return (
                  <button key={opt.id} onClick={() => handleSelect(catKey, opt.id)}
                    className={`text-left rounded-lg border transition-all overflow-hidden ${isActive ? 'bg-[#244628] text-white border-[#244628] ring-1 ring-[#70C26C]' : 'bg-[#FDF9ED] text-[#555] border-[#e5e2d9] hover:border-[#70C26C]'}`}
                    data-testid={`opt-${opt.id}`}
                  >
                    {hasImages && opt.image && (
                      <div className="w-full h-24 bg-[#f0ede6] overflow-hidden">
                        <img src={opt.image} alt={opt.name} className="w-full h-full object-cover" loading="lazy" />
                      </div>
                    )}
                    <div className="p-2.5">
                      <div className="text-xs font-semibold">{opt.name}</div>
                      <div className={`text-[10px] mt-0.5 ${isActive ? 'text-white/70' : 'text-[#999]'}`}>{opt.description}</div>
                      {opt.supplier && opt.supplier !== '' && (
                        <button className={`text-[10px] mt-0.5 italic hover:underline ${isActive ? 'text-white/50' : 'text-[#bbb]'}`}
                          onClick={(e) => { e.stopPropagation(); if (onSupplierClick) onSupplierClick(opt.supplier); }}>
                          {opt.supplier}
                        </button>
                      )}
                      {opt.price > 0 && (
                        <div className={`text-xs font-bold mt-1 ${isActive ? 'text-[#70C26C]' : 'text-[#70C26C]'}`}>
                          + € {opt.price.toLocaleString('nl-NL')}
                        </div>
                      )}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
}
