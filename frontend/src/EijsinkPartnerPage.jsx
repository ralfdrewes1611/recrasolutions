import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import {
  ArrowLeft, ExternalLink, Award, Mic, BookOpen, Users, Clock, Package, Star,
  Trophy, ChevronRight, CheckCircle2, MapPin, Calendar, Quote,
} from 'lucide-react';
import { Button } from './components/ui/button';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;
const PARTNER_ID = 'eijsink';

function track(interaction_type) {
  axios.post(`${API}/platform/partners/track`, {
    supplier_id: PARTNER_ID,
    supplier_name: 'Eijsink',
    interaction_type,
    flow_type: 'partner_page',
  }).catch(() => {});
}

export default function EijsinkPartnerPage({ onBack }) {
  const [profile, setProfile] = useState(null);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      axios.get(`${API}/partners/profiles/${PARTNER_ID}`),
      axios.get(`${API}/horeca/products`),
    ]).then(([profileRes, productsRes]) => {
      setProfile(profileRes.data);
      // Filter products belonging to this partner
      const eijsinkProducts = (productsRes.data || []).filter(p => p.supplier === 'Eijsink');
      setProducts(eijsinkProducts);
      track('page_view');
    }).catch(() => {}).finally(() => setLoading(false));
  }, []);

  const productsByCategory = useMemo(() => {
    const map = {};
    products.forEach(p => {
      if (!map[p.category]) map[p.category] = [];
      map[p.category].push(p);
    });
    return map;
  }, [products]);

  const categoryLabels = {
    kassa: 'Kassa & POS-systemen',
    bestelzuil: 'Bestelzuilen (zelfbestel)',
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#FDF9ED] flex items-center justify-center" data-testid="eijsink-loading">
        <div className="text-[#777]">Laden...</div>
      </div>
    );
  }
  if (!profile || profile.error) {
    return (
      <div className="min-h-screen bg-[#FDF9ED] flex flex-col items-center justify-center gap-4">
        <div className="text-[#777]">Partner niet gevonden</div>
        <Button onClick={onBack} variant="outline">Terug</Button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#FDF9ED]" data-testid="eijsink-partner-page">
      {/* Top nav */}
      <header className="bg-[#244628] text-white px-6 py-4 sticky top-0 z-30 shadow-md">
        <div className="max-w-6xl mx-auto flex items-center justify-between gap-4">
          <button
            onClick={onBack}
            className="flex items-center gap-2 text-sm hover:bg-white/10 px-3 py-1.5 rounded-lg transition-colors"
            data-testid="eijsink-back-btn"
          >
            <ArrowLeft size={16} /> Terug
          </button>
          <div className="text-xs text-white/60 tracking-widest hidden md:block">PARTNER PROFIEL</div>
        </div>
      </header>

      {/* Hero */}
      <section className="relative h-[420px] md:h-[480px] overflow-hidden">
        <img
          src={profile.hero_image}
          alt={profile.name}
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-[#244628] via-[#244628]/60 to-[#244628]/10" />
        <div className="absolute inset-0 flex items-end">
          <div className="max-w-6xl mx-auto w-full px-6 pb-10">
            {profile.pleisureworld_partner && (
              <div className="inline-flex items-center gap-2 bg-[#70C26C]/95 text-[#244628] px-3 py-1.5 rounded-full text-xs font-bold mb-4">
                <Award size={14} /> Pleisureworld {profile.pleisureworld_badge}
              </div>
            )}
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-3 tracking-tight">{profile.name}</h1>
            <p className="text-base md:text-lg text-white/85 max-w-2xl">{profile.tagline}</p>
          </div>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-6 py-10 space-y-12">
        {/* Stats */}
        <section className="grid grid-cols-2 md:grid-cols-4 gap-3" data-testid="eijsink-stats">
          <StatCard icon={Users} label="Locaties actief" value={profile.stats?.parken_actief} color="#70C26C" />
          <StatCard icon={Clock} label="Jaren ervaring" value={profile.stats?.jaren_ervaring} color="#2563eb" />
          <StatCard icon={Package} label="Geïnstalleerd" value={profile.stats?.producten_geinstalleerd} color="#b45309" />
          <StatCard icon={Star} label="Score" value={profile.stats?.klanttevredenheid} color="#f59e0b" />
        </section>

        {/* About */}
        <section data-testid="eijsink-about">
          <SectionHeader number="01" title="Over deze partner" />
          <p className="text-[#555] leading-relaxed text-[15px] max-w-3xl">{profile.description}</p>

          <div className="grid sm:grid-cols-2 gap-3 mt-6 max-w-3xl">
            {(profile.usps || []).map((usp, i) => (
              <div key={i} className="flex items-start gap-2.5 bg-white p-3 rounded-xl border border-[#e5e2d9]">
                <CheckCircle2 size={18} className="text-[#70C26C] flex-shrink-0 mt-0.5" />
                <span className="text-sm text-[#244628]">{usp}</span>
              </div>
            ))}
          </div>

          <div className="flex flex-wrap gap-3 mt-6">
            <Button
              onClick={() => { track('website_click'); window.open(profile.website, '_blank'); }}
              data-testid="eijsink-website-btn"
              className="bg-[#244628] hover:bg-[#244628]/90 text-white"
            >
              <ExternalLink size={16} className="mr-2" /> Bezoek Website
            </Button>
            {profile.blog_url && (
              <Button
                onClick={() => { track('blog_click'); window.open(profile.blog_url, '_blank'); }}
                variant="outline"
                data-testid="eijsink-blog-btn"
              >
                <BookOpen size={16} className="mr-2" /> Lees Blog
              </Button>
            )}
          </div>
        </section>

        {/* Products */}
        {products.length > 0 && (
          <section data-testid="eijsink-products">
            <SectionHeader number="02" title="Producten in de configurator" />
            <p className="text-sm text-[#777] mb-6">
              {products.length} producten direct te configureren in de Horeca-flow.
            </p>

            {Object.entries(productsByCategory).map(([cat, items]) => (
              <div key={cat} className="mb-8">
                <h3 className="text-sm font-bold text-[#244628] uppercase tracking-wide mb-3">
                  {categoryLabels[cat] || cat}
                </h3>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {items.map(p => (
                    <div
                      key={p.id}
                      className="bg-white rounded-2xl p-5 border border-[#e5e2d9] hover:shadow-md transition-shadow"
                      data-testid={`eijsink-product-${p.id}`}
                    >
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <span className="text-[10px] uppercase tracking-wide text-[#777] bg-[#f5f5f0] px-2 py-0.5 rounded-full">
                          {p.tier}
                        </span>
                        <span className="text-xs font-medium text-[#10b981]">€ {p.revenue_per_hour}/u omzet</span>
                      </div>
                      <h4 className="font-bold text-[#244628] mb-1">{p.name}</h4>
                      <p className="text-xs text-[#777] mb-4 line-clamp-3">{p.description}</p>
                      <div className="flex items-end justify-between pt-3 border-t border-[#e5e2d9]">
                        <div>
                          <div className="text-[10px] text-[#777] uppercase tracking-wide">Investering</div>
                          <div className="font-bold text-[#244628]">€ {p.price_purchase.toLocaleString('nl-NL')}</div>
                        </div>
                        <div className="text-right">
                          <div className="text-[10px] text-[#777] uppercase tracking-wide">Lease</div>
                          <div className="font-bold text-[#b45309]">vanaf € {Math.round(p.price_lease_monthly)}/mnd</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </section>
        )}

        {/* Trendwatcher quote */}
        {profile.trendwatcher_quote && (
          <section className="bg-white rounded-3xl p-8 border border-[#e5e2d9] relative overflow-hidden" data-testid="eijsink-quote">
            <Quote size={64} className="absolute top-4 right-4 text-[#70C26C]/10" />
            <SectionHeader number="03" title="Trendwatcher in gesprek" />
            <p className="text-lg text-[#244628] italic leading-relaxed mb-4 max-w-3xl">
              &ldquo;{profile.trendwatcher_quote.tekst}&rdquo;
            </p>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-[#70C26C] flex items-center justify-center text-white font-bold text-sm">
                RO
              </div>
              <div>
                <div className="font-semibold text-[#244628]">{profile.trendwatcher_quote.auteur}</div>
                <div className="text-xs text-[#777]">{profile.trendwatcher_quote.functie}</div>
              </div>
            </div>
          </section>
        )}

        {/* Podcast */}
        {profile.podcast && (
          <section className="bg-[#244628] rounded-3xl p-8 text-white relative overflow-hidden" data-testid="eijsink-podcast">
            <div className="flex items-start gap-4 mb-4">
              <div className="w-12 h-12 rounded-2xl bg-[#70C26C]/20 flex items-center justify-center">
                <Mic size={20} className="text-[#70C26C]" />
              </div>
              <div className="flex-1">
                <div className="text-xs tracking-widest text-[#70C26C] uppercase mb-1">Leisure Talk Podcast</div>
                <h3 className="text-xl font-bold mb-2">{profile.podcast.titel}</h3>
                <p className="text-sm text-white/75 mb-3 max-w-3xl leading-relaxed">{profile.podcast.beschrijving}</p>
                <div className="flex items-center gap-4 text-xs text-white/60">
                  <span className="flex items-center gap-1"><Clock size={12} /> {profile.podcast.duur}</span>
                  <span>{profile.podcast.gast}</span>
                </div>
              </div>
            </div>
            <Button
              onClick={() => { track('podcast_click'); window.open(profile.podcast.url, '_blank'); }}
              className="w-full bg-[#70C26C] hover:bg-[#70C26C]/90 text-[#244628] font-semibold"
              data-testid="eijsink-podcast-btn"
            >
              <Mic size={16} className="mr-2" /> Beluister Podcast
            </Button>
          </section>
        )}

        {/* Events */}
        {profile.deelname && profile.deelname.length > 0 && (
          <section data-testid="eijsink-events">
            <SectionHeader number="04" title="Aanwezig op events" />
            <div className="grid sm:grid-cols-2 gap-3">
              {profile.deelname.map((d, i) => (
                <div key={i} className="flex items-center justify-between p-4 bg-white rounded-xl border border-[#e5e2d9]">
                  <div className="flex items-center gap-3">
                    <Calendar size={16} className="text-[#70C26C]" />
                    <span className="text-sm text-[#244628] font-medium">{d.event}</span>
                  </div>
                  <span className="text-xs text-[#777] bg-[#fafaf7] px-2 py-1 rounded-full">{d.type}</span>
                </div>
              ))}
            </div>
          </section>
        )}

        <div className="pt-6 pb-12 text-center">
          <Button
            onClick={onBack}
            variant="outline"
            data-testid="eijsink-back-bottom-btn"
          >
            <ArrowLeft size={16} className="mr-2" /> Terug naar configurator
          </Button>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon: Icon, label, value, color }) {
  return (
    <div className="bg-white rounded-2xl p-4 border border-[#e5e2d9] text-center">
      <div
        className="w-10 h-10 mx-auto rounded-xl flex items-center justify-center mb-2"
        style={{ backgroundColor: `${color}15`, color }}
      >
        <Icon size={18} />
      </div>
      <div className="text-2xl font-bold text-[#244628]">{value || '—'}</div>
      <div className="text-xs text-[#777] mt-0.5">{label}</div>
    </div>
  );
}

function SectionHeader({ number, title }) {
  return (
    <div className="mb-5">
      <div className="flex items-center gap-3 mb-2">
        <div className="h-px w-8 bg-[#70C26C]" />
        <span className="text-xs font-mono tracking-widest text-[#70C26C]">{number}</span>
      </div>
      <h2 className="text-2xl md:text-3xl font-bold text-[#244628] tracking-tight">{title}</h2>
    </div>
  );
}
