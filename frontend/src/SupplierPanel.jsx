import React, { useState, useEffect } from 'react';
import { toast } from 'sonner';
import axios from 'axios';
import {
  Truck, MapPin, Star, Shield, CheckCircle2,
  Plus, X, Edit2, Trash2, Loader2, ChevronDown, ChevronUp
} from 'lucide-react';
import { Button } from './components/ui/button';
import { Input } from './components/ui/input';
import { Label } from './components/ui/label';
import { Badge } from './components/ui/badge';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const STATUS_COLORS = {
  verified: { bg: '#70C26C20', text: '#244628', label: 'Verified' },
  compatible: { bg: '#f59e0b20', text: '#92400e', label: 'Compatible' },
  basic: { bg: '#e5e2d9', text: '#777777', label: 'Basis' },
};

export function SupplierPanel({ projectLat, projectLng, onClose }) {
  const [suppliers, setSuppliers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    name: '', address: '', lat: 52.0, lng: 5.0,
    categories: [], price_per_km: 0.45, start_fee: 75,
    hourly_rate_travel: 65, verified_status: 'basic',
    contact_email: '',
  });

  const fetchSuppliers = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API}/suppliers/match`, {
        project_lat: projectLat,
        project_lng: projectLng,
      });
      setSuppliers(res.data);
    } catch {
      const res = await axios.get(`${API}/suppliers`);
      setSuppliers(res.data.map(s => ({ supplier: s, travel: null })));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchSuppliers(); }, [projectLat, projectLng]);

  const addSupplier = async () => {
    try {
      await axios.post(`${API}/suppliers`, form);
      toast.success('Leverancier toegevoegd');
      setShowForm(false);
      setForm({ name: '', address: '', lat: 52.0, lng: 5.0, categories: [], price_per_km: 0.45, start_fee: 75, hourly_rate_travel: 65, verified_status: 'basic', contact_email: '' });
      fetchSuppliers();
    } catch (err) {
      toast.error('Fout bij toevoegen');
    }
  };

  const deleteSupplier = async (id) => {
    try {
      await axios.delete(`${API}/suppliers/${id}`);
      toast.success('Leverancier verwijderd');
      fetchSuppliers();
    } catch {
      toast.error('Fout bij verwijderen');
    }
  };

  const toggleCategory = (cat) => {
    setForm(prev => ({
      ...prev,
      categories: prev.categories.includes(cat)
        ? prev.categories.filter(c => c !== cat)
        : [...prev.categories, cat],
    }));
  };

  const CATEGORIES = ['slagboom', 'camera', 'sanitair', 'wifi', 'verlichting', 'betaalsysteem', 'toegangscontrole', 'douchelezer'];

  return (
    <div className="space-y-3" data-testid="supplier-panel">
      <div className="flex items-center justify-between">
        <h3 className="font-bold text-[#333333] flex items-center gap-2">
          <Truck size={18} className="text-[#70C26C]" /> Leveranciers
        </h3>
        <Button variant="ghost" size="sm" onClick={() => setShowForm(!showForm)}>
          {showForm ? <X size={14} /> : <Plus size={14} />}
        </Button>
      </div>

      {showForm && (
        <div className="p-3 bg-white rounded-xl border border-[#e5e2d9] space-y-2" data-testid="supplier-form">
          <Input placeholder="Naam" value={form.name} onChange={e => setForm(p => ({...p, name: e.target.value}))} className="h-8 text-sm" />
          <Input placeholder="Adres" value={form.address} onChange={e => setForm(p => ({...p, address: e.target.value}))} className="h-8 text-sm" />
          <div className="grid grid-cols-2 gap-2">
            <Input type="number" step="0.001" placeholder="Lat" value={form.lat} onChange={e => setForm(p => ({...p, lat: parseFloat(e.target.value) || 52}))} className="h-8 text-sm" />
            <Input type="number" step="0.001" placeholder="Lng" value={form.lng} onChange={e => setForm(p => ({...p, lng: parseFloat(e.target.value) || 5}))} className="h-8 text-sm" />
          </div>
          <div className="flex flex-wrap gap-1">
            {CATEGORIES.map(cat => (
              <button key={cat} onClick={() => toggleCategory(cat)} className={`text-[10px] px-2 py-0.5 rounded-full border ${form.categories.includes(cat) ? 'bg-[#70C26C] text-white border-[#70C26C]' : 'bg-white text-[#777777] border-[#e5e2d9]'}`}>
                {cat}
              </button>
            ))}
          </div>
          <div className="grid grid-cols-3 gap-2">
            <Input type="number" step="0.01" placeholder="EUR/km" value={form.price_per_km} onChange={e => setForm(p => ({...p, price_per_km: parseFloat(e.target.value) || 0}))} className="h-8 text-xs" />
            <Input type="number" placeholder="Startfee" value={form.start_fee} onChange={e => setForm(p => ({...p, start_fee: parseFloat(e.target.value) || 0}))} className="h-8 text-xs" />
            <Input type="number" placeholder="EUR/uur" value={form.hourly_rate_travel} onChange={e => setForm(p => ({...p, hourly_rate_travel: parseFloat(e.target.value) || 0}))} className="h-8 text-xs" />
          </div>
          <Button onClick={addSupplier} disabled={!form.name.trim()} className="w-full bg-[#70C26C] text-white h-8 text-sm">
            Toevoegen
          </Button>
        </div>
      )}

      {loading ? (
        <div className="text-center py-4"><Loader2 size={20} className="animate-spin mx-auto text-[#70C26C]" /></div>
      ) : (
        <div className="space-y-2">
          {suppliers.map((item, i) => {
            const s = item.supplier || item;
            const t = item.travel;
            const status = STATUS_COLORS[s.verified_status] || STATUS_COLORS.basic;
            return (
              <div key={s.id || i} className="p-3 bg-white rounded-xl border border-[#e5e2d9]" data-testid={`supplier-${s.id}`}>
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-sm text-[#333333] truncate">{s.name}</span>
                      <span className="text-[9px] px-1.5 py-0.5 rounded-full font-medium" style={{ backgroundColor: status.bg, color: status.text }}>
                        {status.label}
                      </span>
                    </div>
                    {s.address && <div className="text-[10px] text-[#777777] flex items-center gap-1 mt-0.5"><MapPin size={10} />{s.address}</div>}
                    <div className="flex gap-1 mt-1 flex-wrap">
                      {(s.categories || []).map(c => (
                        <span key={c} className="text-[9px] bg-[#FDF9ED] text-[#777777] px-1.5 py-0.5 rounded">{c}</span>
                      ))}
                    </div>
                  </div>
                  <Button variant="ghost" size="icon" className="w-6 h-6 text-red-400" onClick={() => deleteSupplier(s.id)}>
                    <Trash2 size={12} />
                  </Button>
                </div>
                {t && (
                  <div className="mt-2 pt-2 border-t border-[#e5e2d9] grid grid-cols-3 gap-1 text-center">
                    <div>
                      <div className="text-[9px] text-[#777777]">Afstand</div>
                      <div className="text-xs font-bold text-[#333333]">{t.distance_km} km</div>
                    </div>
                    <div>
                      <div className="text-[9px] text-[#777777]">Reistijd</div>
                      <div className="text-xs font-bold text-[#333333]">{Math.round(t.travel_time_hours * 60)} min</div>
                    </div>
                    <div>
                      <div className="text-[9px] text-[#777777]">Reiskosten</div>
                      <div className="text-xs font-bold text-[#70C26C]">EUR {t.total_travel_cost.toLocaleString()}</div>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
          {suppliers.length === 0 && (
            <p className="text-xs text-[#777777] text-center py-3">Geen leveranciers gevonden. Voeg er een toe.</p>
          )}
        </div>
      )}
    </div>
  );
}
