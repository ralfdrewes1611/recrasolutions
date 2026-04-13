import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import {
  ArrowLeft, Plus, Pencil, Trash2, Search, X, Check,
  Building2, MapPin, Mail, Phone, Globe, Shield,
  ChevronDown, ChevronUp, Loader2, Filter,
  Tent, Home, Gamepad2, Save,
} from 'lucide-react';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const FLOW_OPTIONS = [
  { id: 'recreatie', label: 'Recreatie Infra', icon: Tent, color: '#70C26C' },
  { id: 'chalet', label: 'Chalet & Stay', icon: Home, color: '#2563eb' },
  { id: 'fec', label: 'FEC & Experience', icon: Gamepad2, color: '#f59e0b' },
];

const STATUS_OPTIONS = [
  { id: 'verified', label: 'Verified', color: '#10b981' },
  { id: 'compatible', label: 'Compatible', color: '#f59e0b' },
  { id: 'basic', label: 'Basis', color: '#999' },
];

const CATEGORY_OPTIONS = [
  'slagboom', 'camera', 'sanitair', 'wifi', 'betaalsysteem',
  'verlichting', 'toegangscontrole', 'douchelezer', 'wellness',
  'chalets', 'glamping', 'tiny_house', 'attracties', 'horeca',
];

const EMPTY_FORM = {
  name: '', address: '', lat: 52.0, lng: 5.0,
  categories: [], flows: [], price_per_km: 0.45, start_fee: 75,
  hourly_rate_travel: 65, avg_speed_kmh: 80, verified_status: 'basic',
  contact_email: '', contact_phone: '', website: '', notes: '',
};

function FlowBadge({ flowId, small }) {
  const f = FLOW_OPTIONS.find(o => o.id === flowId);
  if (!f) return null;
  const Icon = f.icon;
  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full font-medium ${small ? 'text-[9px] px-1.5 py-0.5' : 'text-[10px] px-2 py-1'}`}
      style={{ backgroundColor: `${f.color}15`, color: f.color, border: `1px solid ${f.color}30` }}
    >
      <Icon size={small ? 9 : 11} /> {f.label}
    </span>
  );
}

function StatusBadge({ status }) {
  const s = STATUS_OPTIONS.find(o => o.id === status) || STATUS_OPTIONS[2];
  return (
    <span className="text-[9px] font-bold uppercase px-2 py-0.5 rounded-full" style={{ color: s.color, backgroundColor: `${s.color}15` }}>
      {s.label}
    </span>
  );
}

function MultiSelect({ options, selected, onChange, label }) {
  return (
    <div>
      <label className="text-[10px] text-[#999] uppercase tracking-wider block mb-1.5">{label}</label>
      <div className="flex flex-wrap gap-1.5">
        {options.map(opt => {
          const isSelected = selected.includes(typeof opt === 'string' ? opt : opt.id);
          const id = typeof opt === 'string' ? opt : opt.id;
          const lbl = typeof opt === 'string' ? opt : opt.label;
          const Icon = typeof opt === 'object' ? opt.icon : null;
          return (
            <button
              key={id}
              type="button"
              onClick={() => onChange(isSelected ? selected.filter(s => s !== id) : [...selected, id])}
              className={`text-[10px] px-2.5 py-1.5 rounded-lg border transition-all flex items-center gap-1 ${
                isSelected
                  ? 'border-[#244628] bg-[#244628] text-white font-medium'
                  : 'border-[#e5e2d9] bg-white text-[#555] hover:border-[#244628]/30'
              }`}
              data-testid={`select-${id}`}
            >
              {Icon && <Icon size={10} />}
              {lbl}
            </button>
          );
        })}
      </div>
    </div>
  );
}

function SupplierForm({ initial, onSave, onCancel, saving }) {
  const [form, setForm] = useState(initial || EMPTY_FORM);
  const set = (k, v) => setForm(prev => ({ ...prev, [k]: v }));

  return (
    <div className="space-y-4 p-5" data-testid="supplier-form">
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="text-[10px] text-[#999] uppercase tracking-wider block mb-1">Naam *</label>
          <input value={form.name} onChange={e => set('name', e.target.value)} placeholder="Bedrijfsnaam"
            className="w-full text-xs border border-[#e5e2d9] rounded-lg px-3 py-2 bg-white focus:outline-none focus:border-[#244628]" data-testid="form-name" />
        </div>
        <div>
          <label className="text-[10px] text-[#999] uppercase tracking-wider block mb-1">Adres</label>
          <input value={form.address} onChange={e => set('address', e.target.value)} placeholder="Stad, Land"
            className="w-full text-xs border border-[#e5e2d9] rounded-lg px-3 py-2 bg-white focus:outline-none focus:border-[#244628]" data-testid="form-address" />
        </div>
      </div>

      <div className="grid grid-cols-3 gap-3">
        <div>
          <label className="text-[10px] text-[#999] uppercase tracking-wider block mb-1">E-mail</label>
          <input value={form.contact_email} onChange={e => set('contact_email', e.target.value)} type="email" placeholder="info@..."
            className="w-full text-xs border border-[#e5e2d9] rounded-lg px-3 py-2 bg-white focus:outline-none focus:border-[#244628]" data-testid="form-email" />
        </div>
        <div>
          <label className="text-[10px] text-[#999] uppercase tracking-wider block mb-1">Telefoon</label>
          <input value={form.contact_phone} onChange={e => set('contact_phone', e.target.value)} placeholder="+31..."
            className="w-full text-xs border border-[#e5e2d9] rounded-lg px-3 py-2 bg-white focus:outline-none focus:border-[#244628]" data-testid="form-phone" />
        </div>
        <div>
          <label className="text-[10px] text-[#999] uppercase tracking-wider block mb-1">Website</label>
          <input value={form.website} onChange={e => set('website', e.target.value)} placeholder="https://..."
            className="w-full text-xs border border-[#e5e2d9] rounded-lg px-3 py-2 bg-white focus:outline-none focus:border-[#244628]" data-testid="form-website" />
        </div>
      </div>

      <MultiSelect options={FLOW_OPTIONS} selected={form.flows} onChange={v => set('flows', v)} label="Configurator flows *" />
      <MultiSelect options={CATEGORY_OPTIONS} selected={form.categories} onChange={v => set('categories', v)} label="Product categorieën" />

      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="text-[10px] text-[#999] uppercase tracking-wider block mb-1">Status</label>
          <div className="flex gap-1.5">
            {STATUS_OPTIONS.map(s => (
              <button key={s.id} type="button" onClick={() => set('verified_status', s.id)}
                className={`text-[10px] px-3 py-1.5 rounded-lg border transition-all ${
                  form.verified_status === s.id ? 'border-[#244628] bg-[#244628] text-white' : 'border-[#e5e2d9] text-[#555]'
                }`} data-testid={`status-${s.id}`}>
                {s.label}
              </button>
            ))}
          </div>
        </div>
        <div>
          <label className="text-[10px] text-[#999] uppercase tracking-wider block mb-1">Coordinaten</label>
          <div className="flex gap-2">
            <input value={form.lat} onChange={e => set('lat', parseFloat(e.target.value) || 0)} type="number" step="0.0001" placeholder="Lat"
              className="flex-1 text-xs border border-[#e5e2d9] rounded-lg px-3 py-2 bg-white focus:outline-none focus:border-[#244628]" data-testid="form-lat" />
            <input value={form.lng} onChange={e => set('lng', parseFloat(e.target.value) || 0)} type="number" step="0.0001" placeholder="Lng"
              className="flex-1 text-xs border border-[#e5e2d9] rounded-lg px-3 py-2 bg-white focus:outline-none focus:border-[#244628]" data-testid="form-lng" />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-4 gap-2">
        <div>
          <label className="text-[10px] text-[#999] uppercase block mb-1">€/km</label>
          <input value={form.price_per_km} onChange={e => set('price_per_km', parseFloat(e.target.value) || 0)} type="number" step="0.01"
            className="w-full text-xs border border-[#e5e2d9] rounded-lg px-2 py-2 bg-white focus:outline-none focus:border-[#244628]" data-testid="form-price-km" />
        </div>
        <div>
          <label className="text-[10px] text-[#999] uppercase block mb-1">Startkosten</label>
          <input value={form.start_fee} onChange={e => set('start_fee', parseFloat(e.target.value) || 0)} type="number"
            className="w-full text-xs border border-[#e5e2d9] rounded-lg px-2 py-2 bg-white focus:outline-none focus:border-[#244628]" data-testid="form-start-fee" />
        </div>
        <div>
          <label className="text-[10px] text-[#999] uppercase block mb-1">€/uur reis</label>
          <input value={form.hourly_rate_travel} onChange={e => set('hourly_rate_travel', parseFloat(e.target.value) || 0)} type="number"
            className="w-full text-xs border border-[#e5e2d9] rounded-lg px-2 py-2 bg-white focus:outline-none focus:border-[#244628]" data-testid="form-hourly-rate" />
        </div>
        <div>
          <label className="text-[10px] text-[#999] uppercase block mb-1">Gem. km/h</label>
          <input value={form.avg_speed_kmh} onChange={e => set('avg_speed_kmh', parseFloat(e.target.value) || 0)} type="number"
            className="w-full text-xs border border-[#e5e2d9] rounded-lg px-2 py-2 bg-white focus:outline-none focus:border-[#244628]" data-testid="form-avg-speed" />
        </div>
      </div>

      <div>
        <label className="text-[10px] text-[#999] uppercase tracking-wider block mb-1">Notities</label>
        <textarea value={form.notes} onChange={e => set('notes', e.target.value)} rows={2} placeholder="Interne notities..."
          className="w-full text-xs border border-[#e5e2d9] rounded-lg px-3 py-2 bg-white focus:outline-none focus:border-[#244628] resize-none" data-testid="form-notes" />
      </div>

      <div className="flex items-center gap-2 pt-2">
        <button onClick={() => onSave(form)} disabled={saving || !form.name}
          className="flex-1 flex items-center justify-center gap-2 text-xs font-medium bg-[#244628] text-white rounded-xl py-2.5 hover:bg-[#1a341d] disabled:opacity-40 transition-all"
          data-testid="form-save">
          {saving ? <><Loader2 size={14} className="animate-spin" /> Opslaan...</> : <><Save size={14} /> Opslaan</>}
        </button>
        <button onClick={onCancel} className="text-xs text-[#999] hover:text-[#333] px-4 py-2.5" data-testid="form-cancel">
          Annuleren
        </button>
      </div>
    </div>
  );
}

export function SupplierAdmin({ onBack }) {
  const [suppliers, setSuppliers] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [flowFilter, setFlowFilter] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [saving, setSaving] = useState(false);
  const [expandedId, setExpandedId] = useState(null);

  const fetchData = useCallback(async () => {
    try {
      const [supRes, statsRes] = await Promise.all([
        axios.get(`${API}/suppliers${flowFilter ? `?flow=${flowFilter}` : ''}`),
        axios.get(`${API}/suppliers/stats`),
      ]);
      setSuppliers(supRes.data);
      setStats(statsRes.data);
    } catch { toast.error('Fout bij laden leveranciers'); }
    finally { setLoading(false); }
  }, [flowFilter]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleSave = async (form) => {
    setSaving(true);
    try {
      if (editingId) {
        await axios.put(`${API}/suppliers/${editingId}`, form);
        toast.success('Leverancier bijgewerkt');
      } else {
        await axios.post(`${API}/suppliers`, form);
        toast.success('Leverancier toegevoegd');
      }
      setShowForm(false);
      setEditingId(null);
      fetchData();
    } catch { toast.error('Opslaan mislukt'); }
    finally { setSaving(false); }
  };

  const handleDelete = async (id, name) => {
    if (!window.confirm(`Weet u zeker dat u "${name}" wilt verwijderen?`)) return;
    try {
      await axios.delete(`${API}/suppliers/${id}`);
      toast.success('Leverancier verwijderd');
      fetchData();
    } catch { toast.error('Verwijderen mislukt'); }
  };

  const startEdit = (supplier) => {
    setEditingId(supplier.id);
    setShowForm(true);
  };

  const filtered = suppliers.filter(s =>
    s.name.toLowerCase().includes(search.toLowerCase()) ||
    s.address?.toLowerCase().includes(search.toLowerCase()) ||
    s.categories?.some(c => c.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div className="min-h-screen bg-[#FDF9ED]" data-testid="supplier-admin">
      {/* Header */}
      <header className="bg-[#244628] text-white px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button onClick={onBack} className="hover:opacity-80" data-testid="admin-back">
              <ArrowLeft size={20} />
            </button>
            <div>
              <div className="text-sm font-bold">Leveranciersbeheer</div>
              <div className="text-[10px] text-white/50">Toevoegen, bewerken en configurator-toewijzing</div>
            </div>
          </div>
          <button onClick={() => { setShowForm(true); setEditingId(null); }}
            className="flex items-center gap-1.5 text-xs font-medium bg-[#70C26C] text-white px-4 py-2 rounded-xl hover:bg-[#5fb35b] transition-all"
            data-testid="add-supplier-btn">
            <Plus size={14} /> Leverancier toevoegen
          </button>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-6 py-6">
        {/* Stats */}
        {stats && (
          <div className="grid grid-cols-5 gap-3 mb-6" data-testid="supplier-stats">
            <div className="bg-white border border-[#e5e2d9] rounded-xl p-4 text-center">
              <div className="text-[10px] text-[#999] uppercase">Totaal</div>
              <div className="text-2xl font-bold text-[#244628]">{stats.total}</div>
            </div>
            {FLOW_OPTIONS.map(f => (
              <div key={f.id} className="bg-white border border-[#e5e2d9] rounded-xl p-4 text-center">
                <div className="text-[10px] text-[#999] uppercase">{f.label}</div>
                <div className="text-2xl font-bold" style={{ color: f.color }}>{stats.per_flow[f.id] || 0}</div>
              </div>
            ))}
            <div className="bg-white border border-[#e5e2d9] rounded-xl p-4 text-center">
              <div className="text-[10px] text-[#999] uppercase">Verified</div>
              <div className="text-2xl font-bold text-[#10b981]">{stats.per_status.verified || 0}</div>
            </div>
          </div>
        )}

        {/* Form */}
        {showForm && (
          <div className="bg-white border border-[#e5e2d9] rounded-2xl mb-6 overflow-hidden" data-testid="supplier-form-wrapper">
            <div className="bg-[#fafaf7] px-5 py-3 border-b border-[#e5e2d9] flex items-center justify-between">
              <span className="text-xs font-bold text-[#333]">
                {editingId ? 'Leverancier bewerken' : 'Nieuwe leverancier'}
              </span>
              <button onClick={() => { setShowForm(false); setEditingId(null); }} className="text-[#999] hover:text-[#333]">
                <X size={16} />
              </button>
            </div>
            <SupplierForm
              initial={editingId ? suppliers.find(s => s.id === editingId) : EMPTY_FORM}
              onSave={handleSave}
              onCancel={() => { setShowForm(false); setEditingId(null); }}
              saving={saving}
            />
          </div>
        )}

        {/* Filters */}
        <div className="flex items-center gap-3 mb-4">
          <div className="relative flex-1">
            <Search size={14} className="absolute left-3 top-2.5 text-[#bbb]" />
            <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Zoek leverancier, categorie of locatie..."
              className="w-full text-xs border border-[#e5e2d9] rounded-xl pl-9 pr-3 py-2.5 bg-white focus:outline-none focus:border-[#244628]"
              data-testid="supplier-search" />
          </div>
          <div className="flex items-center gap-1.5">
            <Filter size={13} className="text-[#999]" />
            <button onClick={() => setFlowFilter('')}
              className={`text-[10px] px-2.5 py-1.5 rounded-lg border transition-all ${!flowFilter ? 'border-[#244628] bg-[#244628] text-white' : 'border-[#e5e2d9] text-[#555]'}`}
              data-testid="filter-all">Alle</button>
            {FLOW_OPTIONS.map(f => (
              <button key={f.id} onClick={() => setFlowFilter(flowFilter === f.id ? '' : f.id)}
                className={`text-[10px] px-2.5 py-1.5 rounded-lg border transition-all flex items-center gap-1 ${flowFilter === f.id ? 'border-[#244628] bg-[#244628] text-white' : 'border-[#e5e2d9] text-[#555]'}`}
                data-testid={`filter-${f.id}`}>
                <f.icon size={10} /> {f.label}
              </button>
            ))}
          </div>
        </div>

        {/* Table */}
        {loading ? (
          <div className="flex items-center justify-center py-20 text-[#999] text-sm">
            <Loader2 size={20} className="animate-spin mr-2" /> Laden...
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-20 text-[#999] text-sm" data-testid="no-suppliers">
            Geen leveranciers gevonden
          </div>
        ) : (
          <div className="space-y-2">
            {filtered.map(sup => (
              <div key={sup.id} className="bg-white border border-[#e5e2d9] rounded-xl overflow-hidden hover:border-[#244628]/20 transition-all" data-testid={`supplier-row-${sup.id}`}>
                <div className="flex items-center gap-4 px-5 py-4 cursor-pointer" onClick={() => setExpandedId(expandedId === sup.id ? null : sup.id)}>
                  {/* Status dot */}
                  <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{
                    backgroundColor: STATUS_OPTIONS.find(s => s.id === sup.verified_status)?.color || '#999'
                  }} />

                  {/* Name & address */}
                  <div className="min-w-0 flex-1">
                    <div className="text-sm font-bold text-[#333] flex items-center gap-2">
                      {sup.name}
                      <StatusBadge status={sup.verified_status} />
                    </div>
                    <div className="text-[10px] text-[#999] flex items-center gap-1 mt-0.5">
                      <MapPin size={9} /> {sup.address || 'Geen adres'}
                    </div>
                  </div>

                  {/* Flows */}
                  <div className="flex items-center gap-1 flex-shrink-0">
                    {(sup.flows || []).map(f => <FlowBadge key={f} flowId={f} small />)}
                    {(!sup.flows || sup.flows.length === 0) && <span className="text-[9px] text-[#ccc]">Geen flows</span>}
                  </div>

                  {/* Categories count */}
                  <div className="text-[10px] text-[#999] flex-shrink-0 w-20 text-right">
                    {sup.categories?.length || 0} cat.
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-1 flex-shrink-0">
                    <button onClick={e => { e.stopPropagation(); startEdit(sup); }}
                      className="p-1.5 rounded-lg hover:bg-[#f0ede6] text-[#999] hover:text-[#244628] transition-all"
                      data-testid={`edit-${sup.id}`}>
                      <Pencil size={14} />
                    </button>
                    <button onClick={e => { e.stopPropagation(); handleDelete(sup.id, sup.name); }}
                      className="p-1.5 rounded-lg hover:bg-[#fef2f2] text-[#999] hover:text-[#ef4444] transition-all"
                      data-testid={`delete-${sup.id}`}>
                      <Trash2 size={14} />
                    </button>
                  </div>

                  {expandedId === sup.id ? <ChevronUp size={16} className="text-[#ccc]" /> : <ChevronDown size={16} className="text-[#ccc]" />}
                </div>

                {/* Expanded details */}
                {expandedId === sup.id && (
                  <div className="px-5 pb-4 border-t border-[#f0ede6] pt-3 space-y-3" data-testid={`detail-${sup.id}`}>
                    <div className="grid grid-cols-4 gap-4 text-xs">
                      <div>
                        <span className="text-[10px] text-[#999] uppercase block">Contact</span>
                        <div className="flex items-center gap-1 mt-1 text-[#555]"><Mail size={11} /> {sup.contact_email || '-'}</div>
                        <div className="flex items-center gap-1 mt-0.5 text-[#555]"><Phone size={11} /> {sup.contact_phone || '-'}</div>
                        {sup.website && <div className="flex items-center gap-1 mt-0.5 text-[#2563eb]">
                          <Globe size={11} /> <a href={sup.website} target="_blank" rel="noopener noreferrer" className="hover:underline">{sup.website}</a>
                        </div>}
                      </div>
                      <div>
                        <span className="text-[10px] text-[#999] uppercase block">Logistiek</span>
                        <div className="mt-1 text-[#555]">€ {sup.price_per_km}/km · € {sup.start_fee} start</div>
                        <div className="text-[#555]">€ {sup.hourly_rate_travel}/uur · {sup.avg_speed_kmh} km/h</div>
                      </div>
                      <div>
                        <span className="text-[10px] text-[#999] uppercase block">Categorieën</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {(sup.categories || []).map(c => (
                            <span key={c} className="text-[9px] bg-[#f0ede6] text-[#555] px-2 py-0.5 rounded-full">{c}</span>
                          ))}
                        </div>
                      </div>
                      <div>
                        <span className="text-[10px] text-[#999] uppercase block">Configurators</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {(sup.flows || []).map(f => <FlowBadge key={f} flowId={f} />)}
                        </div>
                      </div>
                    </div>
                    {sup.notes && (
                      <div className="text-[10px] text-[#999] bg-[#fafaf7] rounded-lg p-2">
                        <span className="font-medium">Notities:</span> {sup.notes}
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
