import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import {
  ArrowLeft, Plus, Pencil, Trash2, Save, X, Loader2, Search,
  Award, Mic, Quote, Trophy, CheckCircle2, Calendar, Image as ImageIcon,
  Eye, Globe,
} from 'lucide-react';
import { Button } from './components/ui/button';
import { Input } from './components/ui/input';
import { Label } from './components/ui/label';
import { Textarea } from './components/ui/textarea';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const EMPTY_PROFILE = {
  id: '',
  name: '',
  tagline: '',
  description: '',
  website: '',
  logo: '',
  hero_image: '',
  categorieen: [],
  pleisureworld_partner: false,
  pleisureworld_badge: '',
  pleisureworld_sinds: '',
  blog_url: '',
  blog_titel: '',
  podcast: { titel: '', beschrijving: '', url: '', duur: '', gast: '' },
  trendwatcher_quote: { tekst: '', auteur: '', functie: '' },
  stats: { parken_actief: '', jaren_ervaring: '', producten_geinstalleerd: '', klanttevredenheid: '' },
  deelname: [],
  top_producten: [],
  usps: [],
};

export function PartnerProfileAdmin({ onBack, onPreview }) {
  const [profiles, setProfiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [editing, setEditing] = useState(null); // null | profile-object | EMPTY_PROFILE for new
  const [saving, setSaving] = useState(false);

  const load = useCallback(() => {
    setLoading(true);
    axios.get(`${API}/partners/admin/profiles`).then(r => {
      setProfiles(r.data || []);
    }).catch(() => toast.error('Kon profielen niet laden'))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => { load(); }, [load]);

  const filtered = profiles.filter(p =>
    !search || p.name.toLowerCase().includes(search.toLowerCase()) || (p.id || '').includes(search.toLowerCase())
  );

  const handleSave = async () => {
    if (!editing.name) { toast.error('Naam is verplicht'); return; }
    setSaving(true);
    try {
      const isNew = !editing.id || !profiles.find(p => p.id === editing.id);
      if (isNew) {
        const r = await axios.post(`${API}/partners/admin/profiles`, editing);
        if (r.data.error) { toast.error(r.data.error); return; }
        toast.success('Partner aangemaakt');
      } else {
        const r = await axios.put(`${API}/partners/admin/profiles/${editing.id}`, editing);
        if (r.data.error) { toast.error(r.data.error); return; }
        toast.success('Partner bijgewerkt');
      }
      setEditing(null);
      load();
    } catch (e) {
      toast.error('Opslaan mislukt: ' + (e.response?.data?.detail || e.message));
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id, name) => {
    if (!window.confirm(`Weet je zeker dat je "${name}" wilt verwijderen?`)) return;
    try {
      await axios.delete(`${API}/partners/admin/profiles/${id}`);
      toast.success('Partner verwijderd');
      load();
    } catch (e) {
      toast.error('Verwijderen mislukt');
    }
  };

  if (editing) {
    return (
      <PartnerEditor
        profile={editing}
        onChange={setEditing}
        onCancel={() => setEditing(null)}
        onSave={handleSave}
        saving={saving}
      />
    );
  }

  return (
    <div className="min-h-screen bg-[#FDF9ED]" data-testid="partner-admin">
      <header className="bg-[#244628] text-white px-6 py-4 sticky top-0 z-30 shadow-md">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <button onClick={onBack} className="flex items-center gap-2 text-sm hover:bg-white/10 px-3 py-1.5 rounded-lg" data-testid="partner-admin-back">
            <ArrowLeft size={16} /> Terug
          </button>
          <div className="text-xs text-white/60 tracking-widest hidden md:block">PARTNER PROFIELEN BEHEER</div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-6 py-10">
        <div className="flex items-center gap-3 mb-3">
          <div className="h-px w-8 bg-[#70C26C]" />
          <span className="text-xs font-mono tracking-widest text-[#70C26C]">BEHEER</span>
        </div>
        <div className="flex items-end justify-between gap-4 flex-wrap mb-8">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold text-[#244628] tracking-tight">Partner profielen</h1>
            <p className="text-sm text-[#777] mt-1">Beheer rijke partner-profielen — voeg een nieuwe partner toe of werk een bestaande bij.</p>
          </div>
          <Button onClick={() => setEditing({ ...EMPTY_PROFILE })} className="bg-[#244628] hover:bg-[#244628]/90 text-white" data-testid="partner-admin-new">
            <Plus size={16} className="mr-2" /> Nieuwe partner
          </Button>
        </div>

        <div className="relative mb-6">
          <Search size={16} className="absolute left-3 top-2.5 text-[#999]" />
          <Input
            placeholder="Zoek op naam of id..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="pl-9 bg-white"
            data-testid="partner-admin-search"
          />
        </div>

        {loading ? (
          <div className="text-center py-12 text-[#777]"><Loader2 className="animate-spin inline" /> Laden...</div>
        ) : (
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {filtered.map(p => (
              <div key={p.id} className="bg-white rounded-2xl border border-[#e5e2d9] overflow-hidden hover:shadow-md transition-shadow" data-testid={`partner-card-${p.id}`}>
                {p.hero_image ? (
                  <div className="h-32 bg-[#f0ede6] overflow-hidden relative">
                    <img src={p.hero_image} alt={p.name} className="w-full h-full object-cover" loading="lazy" />
                    {p.pleisureworld_partner && (
                      <div className="absolute top-2 left-2 bg-[#70C26C] text-[#244628] text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1">
                        <Award size={10} /> {p.pleisureworld_badge || 'Partner'}
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="h-32 bg-[#f5f5f0] flex items-center justify-center text-[#999]">
                    <ImageIcon size={32} />
                  </div>
                )}
                <div className="p-4">
                  <div className="text-[10px] text-[#999] uppercase tracking-wide mb-1">{p.id}</div>
                  <h3 className="font-bold text-[#244628] mb-1">{p.name}</h3>
                  <p className="text-xs text-[#777] line-clamp-2 mb-3">{p.tagline}</p>
                  <div className="flex flex-wrap gap-1 mb-3">
                    {(p.categorieen || []).slice(0, 3).map((c, i) => (
                      <span key={i} className="text-[10px] bg-[#fafaf7] text-[#555] px-2 py-0.5 rounded-full border border-[#e5e2d9]">{c}</span>
                    ))}
                  </div>
                  <div className="flex items-center gap-1.5">
                    {onPreview && (
                      <Button size="sm" variant="outline" onClick={() => onPreview(p.id)} className="flex-1 h-8 text-xs" data-testid={`partner-preview-${p.id}`}>
                        <Eye size={12} className="mr-1" /> Bekijk
                      </Button>
                    )}
                    <Button size="sm" variant="outline" onClick={() => setEditing({ ...EMPTY_PROFILE, ...p })} className="flex-1 h-8 text-xs" data-testid={`partner-edit-${p.id}`}>
                      <Pencil size={12} className="mr-1" /> Bewerken
                    </Button>
                    <Button size="sm" variant="outline" onClick={() => handleDelete(p.id, p.name)} className="h-8 w-8 p-0 text-red-600 hover:bg-red-50 border-red-200" data-testid={`partner-delete-${p.id}`}>
                      <Trash2 size={12} />
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function PartnerEditor({ profile, onChange, onCancel, onSave, saving }) {
  const update = (patch) => onChange({ ...profile, ...patch });
  const updateNested = (key, patch) => onChange({ ...profile, [key]: { ...profile[key], ...patch } });

  const addCategorie = (val) => {
    if (!val.trim()) return;
    update({ categorieen: [...(profile.categorieen || []), val.trim()] });
  };
  const removeCategorie = (i) => {
    update({ categorieen: profile.categorieen.filter((_, idx) => idx !== i) });
  };
  const addUsp = () => update({ usps: [...(profile.usps || []), ''] });
  const updateUsp = (i, v) => update({ usps: profile.usps.map((u, idx) => idx === i ? v : u) });
  const removeUsp = (i) => update({ usps: profile.usps.filter((_, idx) => idx !== i) });

  const addDeelname = () => update({ deelname: [...(profile.deelname || []), { event: '', type: '' }] });
  const updateDeelname = (i, patch) => update({ deelname: profile.deelname.map((d, idx) => idx === i ? { ...d, ...patch } : d) });
  const removeDeelname = (i) => update({ deelname: profile.deelname.filter((_, idx) => idx !== i) });

  const addTopProduct = () => update({ top_producten: [...(profile.top_producten || []), { id: '', name: '', prijs: 0, image: '', reden: '', configuraties: 0 }] });
  const updateTopProduct = (i, patch) => update({ top_producten: profile.top_producten.map((p, idx) => idx === i ? { ...p, ...patch } : p) });
  const removeTopProduct = (i) => update({ top_producten: profile.top_producten.filter((_, idx) => idx !== i) });

  const isNew = !profile.id;

  return (
    <div className="min-h-screen bg-[#FDF9ED]" data-testid="partner-editor">
      <header className="bg-[#244628] text-white px-6 py-4 sticky top-0 z-30 shadow-md">
        <div className="max-w-4xl mx-auto flex items-center justify-between gap-3">
          <button onClick={onCancel} className="flex items-center gap-2 text-sm hover:bg-white/10 px-3 py-1.5 rounded-lg" data-testid="partner-editor-cancel">
            <ArrowLeft size={16} /> Annuleren
          </button>
          <div className="text-sm font-semibold">{isNew ? 'Nieuwe partner' : `Bewerken: ${profile.name}`}</div>
          <Button onClick={onSave} disabled={saving} className="bg-[#70C26C] hover:bg-[#5fb35b] text-[#244628] font-semibold" data-testid="partner-editor-save">
            {saving ? <><Loader2 size={14} className="animate-spin mr-2" /> Opslaan...</> : <><Save size={14} className="mr-2" /> Opslaan</>}
          </Button>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-6 py-8 space-y-8">
        {/* Basis */}
        <Section title="Basisgegevens" icon={Globe}>
          <Row>
            <Field label="ID (slug)" hint="Leeg laten voor auto-genereren bij nieuwe partner">
              <Input value={profile.id} onChange={e => update({ id: e.target.value })} placeholder="madino" disabled={!isNew} data-testid="editor-id" />
            </Field>
            <Field label="Naam *">
              <Input value={profile.name} onChange={e => update({ name: e.target.value })} placeholder="Madino" data-testid="editor-name" />
            </Field>
          </Row>
          <Field label="Tagline">
            <Input value={profile.tagline} onChange={e => update({ tagline: e.target.value })} data-testid="editor-tagline" />
          </Field>
          <Field label="Beschrijving">
            <Textarea rows={5} value={profile.description} onChange={e => update({ description: e.target.value })} data-testid="editor-description" />
          </Field>
          <Row>
            <Field label="Website"><Input value={profile.website} onChange={e => update({ website: e.target.value })} placeholder="https://..." /></Field>
            <Field label="Logo URL"><Input value={profile.logo} onChange={e => update({ logo: e.target.value })} placeholder="https://..." /></Field>
          </Row>
          <Field label="Hero image URL (groot)">
            <Input value={profile.hero_image} onChange={e => update({ hero_image: e.target.value })} placeholder="https://..." data-testid="editor-hero" />
          </Field>
          {profile.hero_image && (
            <div className="h-32 rounded-xl bg-[#f0ede6] overflow-hidden">
              <img src={profile.hero_image} alt="Preview" className="w-full h-full object-cover" />
            </div>
          )}
        </Section>

        {/* Pleisureworld */}
        <Section title="Pleisureworld Partnership" icon={Award}>
          <Row>
            <Field label="Partner?">
              <label className="flex items-center gap-2 text-sm cursor-pointer">
                <input type="checkbox" checked={profile.pleisureworld_partner} onChange={e => update({ pleisureworld_partner: e.target.checked })} />
                Pleisureworld preferred partner
              </label>
            </Field>
            <Field label="Badge tekst"><Input value={profile.pleisureworld_badge} onChange={e => update({ pleisureworld_badge: e.target.value })} placeholder="Preferred Partner" /></Field>
            <Field label="Partner sinds"><Input value={profile.pleisureworld_sinds} onChange={e => update({ pleisureworld_sinds: e.target.value })} placeholder="2026" /></Field>
          </Row>
          <Row>
            <Field label="Blog URL"><Input value={profile.blog_url} onChange={e => update({ blog_url: e.target.value })} placeholder="https://..." /></Field>
            <Field label="Blog titel"><Input value={profile.blog_titel} onChange={e => update({ blog_titel: e.target.value })} /></Field>
          </Row>
        </Section>

        {/* Categorieen */}
        <Section title="Categorieën" icon={CheckCircle2}>
          <div className="flex flex-wrap gap-2 mb-3">
            {(profile.categorieen || []).map((c, i) => (
              <span key={i} className="inline-flex items-center gap-1 text-xs bg-[#fafaf7] border border-[#e5e2d9] px-2 py-1 rounded-full">
                {c}
                <button onClick={() => removeCategorie(i)}><X size={12} /></button>
              </span>
            ))}
          </div>
          <Input
            placeholder="Type een categorie en druk Enter..."
            onKeyDown={e => { if (e.key === 'Enter') { addCategorie(e.target.value); e.target.value = ''; e.preventDefault(); } }}
          />
        </Section>

        {/* Stats */}
        <Section title="Statistieken" icon={Trophy}>
          <Row>
            <Field label="Parken/Locaties"><Input value={profile.stats?.parken_actief || ''} onChange={e => updateNested('stats', { parken_actief: e.target.value })} placeholder="75+" /></Field>
            <Field label="Jaren ervaring"><Input value={profile.stats?.jaren_ervaring || ''} onChange={e => updateNested('stats', { jaren_ervaring: e.target.value })} placeholder="12+" /></Field>
          </Row>
          <Row>
            <Field label="Producten geïnstalleerd"><Input value={profile.stats?.producten_geinstalleerd || ''} onChange={e => updateNested('stats', { producten_geinstalleerd: e.target.value })} placeholder="1.800+" /></Field>
            <Field label="Klanttevredenheid"><Input value={profile.stats?.klanttevredenheid || ''} onChange={e => updateNested('stats', { klanttevredenheid: e.target.value })} placeholder="4.7/5" /></Field>
          </Row>
        </Section>

        {/* Podcast */}
        <Section title="Podcast (Leisure Talk)" icon={Mic}>
          <Field label="Titel"><Input value={profile.podcast?.titel || ''} onChange={e => updateNested('podcast', { titel: e.target.value })} /></Field>
          <Field label="Beschrijving"><Textarea rows={3} value={profile.podcast?.beschrijving || ''} onChange={e => updateNested('podcast', { beschrijving: e.target.value })} /></Field>
          <Row>
            <Field label="URL"><Input value={profile.podcast?.url || ''} onChange={e => updateNested('podcast', { url: e.target.value })} /></Field>
            <Field label="Duur"><Input value={profile.podcast?.duur || ''} onChange={e => updateNested('podcast', { duur: e.target.value })} placeholder="33 min" /></Field>
          </Row>
          <Field label="Gast"><Input value={profile.podcast?.gast || ''} onChange={e => updateNested('podcast', { gast: e.target.value })} /></Field>
        </Section>

        {/* Trendwatcher quote */}
        <Section title="Trendwatcher Quote" icon={Quote}>
          <Field label="Quote tekst"><Textarea rows={4} value={profile.trendwatcher_quote?.tekst || ''} onChange={e => updateNested('trendwatcher_quote', { tekst: e.target.value })} /></Field>
          <Row>
            <Field label="Auteur"><Input value={profile.trendwatcher_quote?.auteur || ''} onChange={e => updateNested('trendwatcher_quote', { auteur: e.target.value })} placeholder="Richard Otten" /></Field>
            <Field label="Functie"><Input value={profile.trendwatcher_quote?.functie || ''} onChange={e => updateNested('trendwatcher_quote', { functie: e.target.value })} placeholder="Trendwatcher Recreatie & Hospitality" /></Field>
          </Row>
        </Section>

        {/* USPs */}
        <Section title="USPs / Sterke punten" icon={CheckCircle2}>
          <div className="space-y-2">
            {(profile.usps || []).map((u, i) => (
              <div key={i} className="flex items-center gap-2">
                <Input value={u} onChange={e => updateUsp(i, e.target.value)} />
                <Button size="sm" variant="outline" onClick={() => removeUsp(i)} className="text-red-600"><X size={14} /></Button>
              </div>
            ))}
          </div>
          <Button size="sm" variant="outline" onClick={addUsp} className="mt-2"><Plus size={14} className="mr-1" /> USP toevoegen</Button>
        </Section>

        {/* Top producten */}
        <Section title="Top 3 producten" icon={Trophy}>
          {(profile.top_producten || []).map((p, i) => (
            <div key={i} className="bg-white border border-[#e5e2d9] rounded-xl p-4 mb-3 space-y-2">
              <Row>
                <Field label="Product naam"><Input value={p.name} onChange={e => updateTopProduct(i, { name: e.target.value })} /></Field>
                <Field label="Prijs (€)"><Input type="number" value={p.prijs} onChange={e => updateTopProduct(i, { prijs: Number(e.target.value) })} /></Field>
              </Row>
              <Field label="Image URL"><Input value={p.image} onChange={e => updateTopProduct(i, { image: e.target.value })} /></Field>
              <Row>
                <Field label="Reden (waarom top)"><Input value={p.reden} onChange={e => updateTopProduct(i, { reden: e.target.value })} /></Field>
                <Field label="# Configuraties"><Input type="number" value={p.configuraties} onChange={e => updateTopProduct(i, { configuraties: Number(e.target.value) })} /></Field>
              </Row>
              <div className="flex justify-end">
                <Button size="sm" variant="outline" onClick={() => removeTopProduct(i)} className="text-red-600"><Trash2 size={12} className="mr-1" /> Verwijderen</Button>
              </div>
            </div>
          ))}
          <Button size="sm" variant="outline" onClick={addTopProduct}><Plus size={14} className="mr-1" /> Product toevoegen</Button>
        </Section>

        {/* Events */}
        <Section title="Events / Deelname" icon={Calendar}>
          {(profile.deelname || []).map((d, i) => (
            <Row key={i}>
              <Field label="Event"><Input value={d.event} onChange={e => updateDeelname(i, { event: e.target.value })} /></Field>
              <Field label="Rol/Type"><Input value={d.type} onChange={e => updateDeelname(i, { type: e.target.value })} /></Field>
              <div className="flex items-end pb-1">
                <Button size="sm" variant="outline" onClick={() => removeDeelname(i)} className="text-red-600"><X size={14} /></Button>
              </div>
            </Row>
          ))}
          <Button size="sm" variant="outline" onClick={addDeelname} className="mt-2"><Plus size={14} className="mr-1" /> Event toevoegen</Button>
        </Section>

        <div className="pt-4 pb-12 flex justify-end gap-3">
          <Button variant="outline" onClick={onCancel}>Annuleren</Button>
          <Button onClick={onSave} disabled={saving} className="bg-[#70C26C] hover:bg-[#5fb35b] text-[#244628] font-semibold">
            {saving ? <><Loader2 size={14} className="animate-spin mr-2" /> Opslaan...</> : <><Save size={14} className="mr-2" /> Opslaan</>}
          </Button>
        </div>
      </div>
    </div>
  );
}

function Section({ title, icon: Icon, children }) {
  return (
    <div className="bg-white rounded-2xl p-6 border border-[#e5e2d9]">
      <h2 className="flex items-center gap-2 text-lg font-bold text-[#244628] mb-4">
        <Icon size={18} className="text-[#70C26C]" />
        {title}
      </h2>
      <div className="space-y-3">{children}</div>
    </div>
  );
}

function Row({ children }) {
  return <div className="grid sm:grid-cols-2 gap-3">{children}</div>;
}

function Field({ label, hint, children }) {
  return (
    <div>
      <Label className="text-xs">{label}</Label>
      {children}
      {hint && <p className="text-[10px] text-[#999] mt-1">{hint}</p>}
    </div>
  );
}
