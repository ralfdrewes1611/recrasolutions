import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import {
  Beer, ChevronRight, ChevronLeft, ArrowLeft, Plus, Minus, Sparkles,
  AlertTriangle, TrendingUp, Coffee, CreditCard, Tv, Sandwich, Sun,
  Gamepad2, Building2, Users, Download, Lock, Trophy, X, ShoppingCart,
} from 'lucide-react';
import { Button } from './components/ui/button';
import { Input } from './components/ui/input';
import { Label } from './components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './components/ui/select';
import SupplierProfile from './SupplierProfile';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const CATEGORY_META = {
  kassa: { label: 'Kassa & POS', icon: CreditCard, color: '#244628' },
  bestelzuil: { label: 'Bestelzuilen', icon: Tv, color: '#0ea5e9' },
  vending: { label: 'Vending', icon: Coffee, color: '#7c3aed' },
  bar_inrichting: { label: 'Bar Inrichting', icon: Beer, color: '#b45309' },
  meubilair: { label: 'Meubilair', icon: Users, color: '#10b981' },
  pub_games: { label: 'Pub Games', icon: Gamepad2, color: '#8b5cf6' },
  keuken: { label: 'Keuken', icon: Sandwich, color: '#f97316' },
  terras: { label: 'Terras', icon: Sun, color: '#06b6d4' },
};

const STEPS = [
  { id: 1, title: 'Concept', icon: Building2 },
  { id: 2, title: 'Inrichting', icon: ShoppingCart },
  { id: 3, title: 'Revenue', icon: TrendingUp },
];

const SUPPLIER_PROFILE_MAP = {
  'Eijsink': 'eijsink',
};

export default function HorecaWizard({ onBack, onOpenEijsinkPage }) {
  const [step, setStep] = useState(1);
  const [products, setProducts] = useState([]);
  const [top5, setTop5] = useState([]);
  const [selected, setSelected] = useState([]); // [{ product_id, quantity }]
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [revenueReport, setRevenueReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [profilePartnerId, setProfilePartnerId] = useState(null);
  const [project, setProject] = useState({
    name: 'Nieuwe Horeca Configuratie',
    setting: 'park',
    style: 'casual',
    total_area_m2: 200,
    seats_target: 60,
    operating_hours: 8,
    operating_days: 30,
    avg_spend_per_guest: 18,
  });

  useEffect(() => {
    axios.get(`${API}/horeca/products`).then(r => setProducts(r.data)).catch(() => {});
    axios.get(`${API}/horeca/top5`).then(r => setTop5(r.data)).catch(() => {});
  }, []);

  const productById = useMemo(() => {
    const m = {};
    products.forEach(p => { m[p.id] = p; });
    return m;
  }, [products]);

  const selectedItems = useMemo(() => selected.map(s => ({
    ...s,
    product: productById[s.product_id],
  })).filter(x => x.product), [selected, productById]);

  const totalInvestment = selectedItems.reduce((sum, it) =>
    sum + (it.product.price_purchase + it.product.installation_cost) * it.quantity, 0);
  const totalLease = selectedItems.reduce((sum, it) =>
    sum + (it.product.price_lease_monthly || 0) * it.quantity, 0);

  const filteredProducts = useMemo(() => {
    if (selectedCategory === 'all') return products;
    return products.filter(p => p.category === selectedCategory);
  }, [products, selectedCategory]);

  function addProduct(product_id) {
    setSelected(prev => {
      const existing = prev.find(s => s.product_id === product_id);
      if (existing) {
        return prev.map(s => s.product_id === product_id ? { ...s, quantity: s.quantity + 1 } : s);
      }
      return [...prev, { product_id, quantity: 1 }];
    });
  }
  function removeProduct(product_id) {
    setSelected(prev => {
      const existing = prev.find(s => s.product_id === product_id);
      if (!existing) return prev;
      if (existing.quantity <= 1) return prev.filter(s => s.product_id !== product_id);
      return prev.map(s => s.product_id === product_id ? { ...s, quantity: s.quantity - 1 } : s);
    });
  }

  async function calculateRevenue() {
    if (selected.length === 0) {
      toast.error('Selecteer eerst minimaal één product');
      return;
    }
    setLoading(true);
    try {
      const r = await axios.post(`${API}/horeca/calculate-revenue`, {
        products: selected,
        operating_hours: project.operating_hours,
        operating_days: project.operating_days,
        project,
      });
      setRevenueReport(r.data);
      setStep(3);
    } catch (e) {
      toast.error('Kon revenue niet berekenen');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-[#FDF9ED]" data-testid="horeca-wizard">
      {/* Header */}
      <header className="bg-[#244628] text-white px-6 py-4 sticky top-0 z-30 shadow-md">
        <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <button onClick={onBack} className="p-2 hover:bg-white/10 rounded-lg transition-colors" data-testid="horeca-back-btn">
              <ArrowLeft size={20} />
            </button>
            <div className="flex items-center gap-2">
              <Beer size={24} className="text-[#fbbf24]" />
              <div>
                <h1 className="text-base font-bold">Horeca & Bar</h1>
                <p className="text-xs text-white/70">Bar / kassa / bestelzuilen / pub games configurator</p>
              </div>
            </div>
          </div>
          <div className="hidden md:flex items-center gap-2">
            {STEPS.map((s) => {
              const Icon = s.icon;
              const active = step === s.id;
              const done = step > s.id;
              return (
                <div key={s.id} className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs ${active ? 'bg-[#fbbf24] text-[#244628] font-semibold' : done ? 'bg-white/20 text-white' : 'bg-white/5 text-white/50'}`}>
                  <Icon size={14} />
                  <span>{s.title}</span>
                </div>
              );
            })}
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto p-6">
        {/* Step 1: Concept */}
        {step === 1 && (
          <div className="max-w-2xl mx-auto" data-testid="horeca-step-1">
            <h2 className="text-2xl font-bold text-[#244628] mb-2">Concept & Locatie</h2>
            <p className="text-sm text-[#777] mb-6">Vertel ons over je horeca-concept. Dit bepaalt de aanbevelingen en omzetberekeningen.</p>

            <div className="space-y-5 bg-white rounded-2xl p-6 border border-[#e5e2d9]">
              <div>
                <Label htmlFor="name">Naam project</Label>
                <Input id="name" data-testid="horeca-input-name"
                  value={project.name}
                  onChange={(e) => setProject({ ...project, name: e.target.value })} />
              </div>

              <div>
                <Label>Setting</Label>
                <Select value={project.setting} onValueChange={(v) => setProject({ ...project, setting: v })}>
                  <SelectTrigger data-testid="horeca-select-setting"><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="park">Recreatiepark / Vakantiepark</SelectItem>
                    <SelectItem value="camping">Camping</SelectItem>
                    <SelectItem value="standalone">Stand-alone (sportbar / café)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label>Stijl</Label>
                <Select value={project.style} onValueChange={(v) => setProject({ ...project, style: v })}>
                  <SelectTrigger data-testid="horeca-select-style"><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="casual">Casual Pub / Café</SelectItem>
                    <SelectItem value="sports_bar">Sports Bar</SelectItem>
                    <SelectItem value="beach_bar">Beach / Strand-paviljoen</SelectItem>
                    <SelectItem value="premium">Premium Restaurant</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="area">Oppervlakte (m²)</Label>
                  <Input id="area" type="number" data-testid="horeca-input-area"
                    value={project.total_area_m2}
                    onChange={(e) => setProject({ ...project, total_area_m2: Number(e.target.value) })} />
                </div>
                <div>
                  <Label htmlFor="seats">Aantal zitplaatsen</Label>
                  <Input id="seats" type="number" data-testid="horeca-input-seats"
                    value={project.seats_target}
                    onChange={(e) => setProject({ ...project, seats_target: Number(e.target.value) })} />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label>Uur/dag</Label>
                  <Input type="number" data-testid="horeca-input-hours"
                    value={project.operating_hours}
                    onChange={(e) => setProject({ ...project, operating_hours: Number(e.target.value) })} />
                </div>
                <div>
                  <Label>Dagen/maand</Label>
                  <Input type="number" data-testid="horeca-input-days"
                    value={project.operating_days}
                    onChange={(e) => setProject({ ...project, operating_days: Number(e.target.value) })} />
                </div>
                <div>
                  <Label>Besteding/gast</Label>
                  <Input type="number" data-testid="horeca-input-spend"
                    value={project.avg_spend_per_guest}
                    onChange={(e) => setProject({ ...project, avg_spend_per_guest: Number(e.target.value) })} />
                </div>
              </div>
            </div>

            <div className="flex justify-end mt-6">
              <Button onClick={() => setStep(2)} data-testid="horeca-next-step1"
                className="bg-[#244628] hover:bg-[#244628]/90 text-white">
                Volgende: Inrichting <ChevronRight size={16} className="ml-1" />
              </Button>
            </div>
          </div>
        )}

        {/* Step 2: Inrichting */}
        {step === 2 && (
          <div data-testid="horeca-step-2">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-2xl font-bold text-[#244628]">Inrichting samenstellen</h2>
                <p className="text-sm text-[#777]">Kies kassa-systemen, bar-inrichting, pub games, meubilair en meer.</p>
              </div>
              <div className="text-right">
                <div className="text-xs text-[#777]">Totale investering</div>
                <div className="text-xl font-bold text-[#244628]">€ {totalInvestment.toLocaleString('nl-NL')}</div>
                <div className="text-xs text-[#b45309] font-medium">Vanaf € {Math.round(totalLease).toLocaleString('nl-NL')} per maand</div>
              </div>
            </div>

            {/* Featured Top 5 */}
            {top5.length > 0 && (
              <div className="bg-gradient-to-r from-[#fef3c7] to-[#fde68a] rounded-2xl p-5 mb-5 border border-[#f59e0b]/30">
                <div className="flex items-center gap-2 mb-3">
                  <Trophy size={18} className="text-[#b45309]" />
                  <h3 className="font-bold text-[#244628]">Top 5 omzetdrijvers (€/m²)</h3>
                </div>
                <div className="grid grid-cols-2 lg:grid-cols-5 gap-3">
                  {top5.map(t => (
                    <button key={t.id} onClick={() => addProduct(t.id)} data-testid={`horeca-top5-${t.id}`}
                      className="text-left bg-white rounded-xl p-3 hover:shadow-md transition-shadow border border-[#fcd34d]">
                      <div className="text-xs text-[#777]">{CATEGORY_META[t.category]?.label}</div>
                      <div className="text-sm font-semibold text-[#244628] line-clamp-2">{t.name}</div>
                      <div className="text-xs text-[#10b981] font-medium mt-1">€ {t.revenue_per_m2}/m² mnd</div>
                      <div className="text-xs text-[#b45309] mt-0.5">Vanaf € {Math.round(t.lease_monthly)}/mnd</div>
                    </button>
                  ))}
                </div>
              </div>
            )}

            <div className="flex flex-wrap gap-2 mb-5">
              <button onClick={() => setSelectedCategory('all')} data-testid="horeca-cat-all"
                className={`px-4 py-2 rounded-full text-xs font-medium border transition-colors ${selectedCategory === 'all' ? 'bg-[#244628] text-white border-[#244628]' : 'bg-white text-[#244628] border-[#e5e2d9]'}`}>
                Alle ({products.length})
              </button>
              {Object.entries(CATEGORY_META).map(([key, meta]) => {
                const Icon = meta.icon;
                const count = products.filter(p => p.category === key).length;
                if (count === 0) return null;
                return (
                  <button key={key} onClick={() => setSelectedCategory(key)} data-testid={`horeca-cat-${key}`}
                    className={`px-4 py-2 rounded-full text-xs font-medium border transition-colors flex items-center gap-1.5 ${selectedCategory === key ? 'text-white border-transparent' : 'bg-white border-[#e5e2d9]'}`}
                    style={selectedCategory === key ? { backgroundColor: meta.color } : { color: meta.color }}>
                    <Icon size={14} /> {meta.label} ({count})
                  </button>
                );
              })}
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredProducts.map(p => {
                const meta = CATEGORY_META[p.category] || { color: '#777', icon: ShoppingCart };
                const Icon = meta.icon;
                const sel = selected.find(s => s.product_id === p.id);
                const hasProfile = SUPPLIER_PROFILE_MAP[p.supplier];
                return (
                  <div key={p.id} className="bg-white rounded-2xl p-4 border border-[#e5e2d9] hover:shadow-md transition-shadow" data-testid={`horeca-product-${p.id}`}>
                    <div className="flex items-start justify-between gap-2 mb-2">
                      <div className="flex items-center gap-1.5 text-xs font-medium" style={{ color: meta.color }}>
                        <Icon size={14} />
                        {meta.label}
                      </div>
                      <span className="text-xs px-2 py-0.5 rounded-full bg-[#f5f5f0] text-[#777]">{p.tier}</span>
                    </div>
                    <h3 className="font-bold text-sm text-[#244628] mb-1 line-clamp-2">{p.name}</h3>
                    <p className="text-xs text-[#777] mb-3 line-clamp-3">{p.description}</p>
                    <div className="flex items-center gap-2 mb-3">
                      <button onClick={() => {
                        if (p.supplier === 'Eijsink' && onOpenEijsinkPage) onOpenEijsinkPage();
                        else if (hasProfile) setProfilePartnerId(hasProfile);
                      }} data-testid={`horeca-supplier-${p.supplier}`}
                        className={`text-xs ${(p.supplier === 'Eijsink' || hasProfile) ? 'text-[#244628] font-semibold underline cursor-pointer hover:text-[#70C26C]' : 'text-[#777]'}`}>
                        {p.supplier}
                      </button>
                    </div>
                    <div className="space-y-1 text-xs mb-3">
                      <div className="flex justify-between"><span className="text-[#777]">Investering</span><span className="font-semibold">€ {p.price_purchase.toLocaleString('nl-NL')}</span></div>
                      <div className="flex justify-between"><span className="text-[#777]">Lease/mnd</span><span className="font-semibold text-[#b45309]">Vanaf € {Math.round(p.price_lease_monthly).toLocaleString('nl-NL')}</span></div>
                      <div className="flex justify-between"><span className="text-[#777]">Omzet/uur</span><span className="font-semibold text-[#10b981]">€ {p.revenue_per_hour}</span></div>
                      <div className="flex justify-between"><span className="text-[#777]">Footprint</span><span>{p.footprint_m2} m²</span></div>
                    </div>
                    <div className="flex items-center justify-between gap-2">
                      {sel ? (
                        <div className="flex items-center gap-2 flex-1">
                          <Button size="sm" variant="outline" onClick={() => removeProduct(p.id)} data-testid={`horeca-decrease-${p.id}`}
                            className="h-8 w-8 p-0"><Minus size={14} /></Button>
                          <span className="font-bold text-[#244628] flex-1 text-center">{sel.quantity}</span>
                          <Button size="sm" variant="outline" onClick={() => addProduct(p.id)} data-testid={`horeca-increase-${p.id}`}
                            className="h-8 w-8 p-0"><Plus size={14} /></Button>
                        </div>
                      ) : (
                        <Button size="sm" onClick={() => addProduct(p.id)} data-testid={`horeca-add-${p.id}`}
                          className="bg-[#244628] hover:bg-[#244628]/90 text-white w-full">
                          <Plus size={14} className="mr-1" /> Toevoegen
                        </Button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="flex justify-between mt-8 pb-12">
              <Button variant="outline" onClick={() => setStep(1)} data-testid="horeca-back-step2">
                <ChevronLeft size={16} className="mr-1" /> Terug
              </Button>
              <Button onClick={calculateRevenue} disabled={loading || selected.length === 0} data-testid="horeca-calc-revenue"
                className="bg-[#b45309] hover:bg-[#b45309]/90 text-white">
                {loading ? 'Berekenen...' : 'Bereken omzet & ROI'} <TrendingUp size={16} className="ml-2" />
              </Button>
            </div>
          </div>
        )}

        {/* Step 3: Revenue */}
        {step === 3 && revenueReport && (
          <div data-testid="horeca-step-3">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-2xl font-bold text-[#244628]">Business Case</h2>
                <p className="text-sm text-[#777]">{project.name} — {project.setting} — {selectedItems.length} producten</p>
              </div>
              <Button variant="outline" onClick={() => setStep(2)} data-testid="horeca-edit-config">
                <ChevronLeft size={16} className="mr-1" /> Aanpassen
              </Button>
            </div>

            {/* Hero metrics */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
              <MetricCard label="Investering" value={`€ ${revenueReport.total_investment.toLocaleString('nl-NL')}`} color="#b45309" />
              <MetricCard label="Omzet / maand" value={`€ ${revenueReport.total_monthly_revenue.toLocaleString('nl-NL')}`} color="#10b981" />
              <MetricCard label="Break-even" value={`${revenueReport.break_even_months} mnd`} color="#244628" />
              <MetricCard label="€ / m² / mnd" value={`€ ${revenueReport.revenue_per_m2_month.toLocaleString('nl-NL')}`} color="#8b5cf6" />
            </div>

            {/* Lease box (frontend toont alleen "Vanaf €XXX per maand") */}
            <div className="bg-[#244628] text-white rounded-2xl p-6 mb-6">
              <div className="flex items-center gap-2 mb-3">
                <Lock size={16} className="text-[#fbbf24]" />
                <h3 className="font-bold text-[#fbbf24]">Operational Lease Optie</h3>
              </div>
              <div className="text-3xl font-bold mb-1">Vanaf € {Math.round(revenueReport.total_lease_monthly).toLocaleString('nl-NL')} per maand</div>
              <p className="text-xs text-white/70 mb-3">Inclusief installatie, SLA-onderhoud en service. Looptijd 60 maanden.</p>
              <div className="grid grid-cols-2 gap-2 text-sm pt-3 border-t border-white/10">
                <div>
                  <div className="text-xs text-white/60">Netto winst/maand</div>
                  <div className="font-bold text-[#70C26C]">€ {Math.round(revenueReport.total_monthly_revenue - revenueReport.total_lease_monthly).toLocaleString('nl-NL')}</div>
                </div>
                <div>
                  <div className="text-xs text-white/60">Jaarlijkse winst</div>
                  <div className="font-bold text-[#70C26C]">€ {Math.round((revenueReport.total_monthly_revenue - revenueReport.total_lease_monthly) * 12).toLocaleString('nl-NL')}</div>
                </div>
              </div>
            </div>

            {/* Top performers */}
            {revenueReport.top_performers && revenueReport.top_performers.length > 0 && (
              <div className="bg-white rounded-2xl p-5 mb-6 border border-[#e5e2d9]">
                <h3 className="font-bold text-[#244628] mb-3 flex items-center gap-2">
                  <Trophy size={18} className="text-[#b45309]" /> Top performers
                </h3>
                <div className="space-y-2">
                  {revenueReport.top_performers.map((tp, i) => (
                    <div key={i} className="flex items-center justify-between p-3 bg-[#fafaf7] rounded-lg">
                      <div className="flex-1">
                        <div className="font-semibold text-sm">{tp.product_name}</div>
                        <div className="text-xs text-[#777]">{tp.supplier} — ROI {tp.roi_months} mnd</div>
                      </div>
                      <div className="text-right">
                        <div className="font-bold text-[#10b981]">€ {tp.monthly_revenue.toLocaleString('nl-NL')}</div>
                        <div className="text-xs text-[#777]">/ maand</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Suggestions */}
            {revenueReport.suggestions && revenueReport.suggestions.length > 0 && (
              <div className="bg-white rounded-2xl p-5 mb-6 border border-[#e5e2d9]">
                <h3 className="font-bold text-[#244628] mb-3 flex items-center gap-2">
                  <Sparkles size={18} className="text-[#fbbf24]" /> Aanbevelingen
                </h3>
                <div className="space-y-2">
                  {revenueReport.suggestions.map((s, i) => (
                    <div key={i} className={`flex gap-3 p-3 rounded-lg ${s.type === 'warning' ? 'bg-[#fffbeb] border border-[#fcd34d]' : 'bg-[#fafaf7]'}`}>
                      {s.type === 'warning' ? <AlertTriangle size={16} className="text-[#f59e0b] flex-shrink-0 mt-0.5" /> : <Sparkles size={16} className="text-[#fbbf24] flex-shrink-0 mt-0.5" />}
                      <div>
                        <div className="font-semibold text-sm text-[#244628]">{s.title}</div>
                        <div className="text-xs text-[#777] mt-0.5">{s.description}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* All products table */}
            <div className="bg-white rounded-2xl p-5 mb-12 border border-[#e5e2d9] overflow-x-auto">
              <h3 className="font-bold text-[#244628] mb-3">Alle producten</h3>
              <table className="w-full text-sm">
                <thead className="text-xs text-[#777] uppercase">
                  <tr className="border-b border-[#e5e2d9]">
                    <th className="text-left py-2">Product</th>
                    <th className="text-left py-2">Leverancier</th>
                    <th className="text-right py-2">Investering</th>
                    <th className="text-right py-2">Lease/mnd</th>
                    <th className="text-right py-2">Omzet/mnd</th>
                    <th className="text-right py-2">ROI</th>
                  </tr>
                </thead>
                <tbody>
                  {revenueReport.all_products.map((p, i) => (
                    <tr key={i} className="border-b border-[#f5f5f0]">
                      <td className="py-2">{p.product_name}</td>
                      <td className="py-2 text-[#777]">{p.supplier}</td>
                      <td className="text-right py-2">€ {p.investment.toLocaleString('nl-NL')}</td>
                      <td className="text-right py-2 text-[#b45309]">€ {Math.round(p.lease_monthly).toLocaleString('nl-NL')}</td>
                      <td className="text-right py-2 text-[#10b981] font-semibold">€ {p.monthly_revenue.toLocaleString('nl-NL')}</td>
                      <td className="text-right py-2">{p.roi_months} mnd</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {profilePartnerId && (
        <SupplierProfile partnerId={profilePartnerId} onClose={() => setProfilePartnerId(null)} />
      )}
    </div>
  );
}

function MetricCard({ label, value, color }) {
  return (
    <div className="bg-white rounded-2xl p-4 border border-[#e5e2d9]">
      <div className="text-xs text-[#777] uppercase tracking-wider">{label}</div>
      <div className="text-xl font-bold mt-1" style={{ color }}>{value}</div>
    </div>
  );
}
