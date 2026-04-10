import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { X, ExternalLink, Award, Mic, BookOpen, Star, Users, Clock, Package, ChevronRight, Trophy, Heart } from 'lucide-react';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

function trackClick(partnerId, partnerName, interactionType) {
  axios.post(`${API}/platform/partners/track`, {
    supplier_id: partnerId,
    supplier_name: partnerName,
    interaction_type: interactionType,
    flow_type: 'partner_profile',
  }).catch(() => {});
}

export default function SupplierProfile({ partnerId, onClose }) {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [dynamicTop3, setDynamicTop3] = useState(null);

  useEffect(() => {
    if (!partnerId) return;
    setLoading(true);
    Promise.all([
      axios.get(`${API}/partners/profiles/${partnerId}`),
      axios.get(`${API}/partners/profiles/${partnerId}/dynamic-top3`).catch(() => ({ data: null })),
    ]).then(([profileRes, top3Res]) => {
      setProfile(profileRes.data);
      setDynamicTop3(top3Res.data);
      trackClick(partnerId, profileRes.data.name, 'profile_view');
    }).catch(() => {}).finally(() => setLoading(false));
  }, [partnerId]);

  if (!partnerId) return null;

  const handleWebsiteClick = () => {
    trackClick(partnerId, profile?.name, 'website_click');
    window.open(profile?.website, '_blank');
  };

  const handleBlogClick = () => {
    trackClick(partnerId, profile?.name, 'blog_click');
    window.open(profile?.blog_url, '_blank');
  };

  const handlePodcastClick = () => {
    trackClick(partnerId, profile?.name, 'podcast_click');
    window.open(profile?.podcast?.url, '_blank');
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm" onClick={onClose} data-testid="supplier-profile-overlay">
      <div className="bg-[#FDF9ED] w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-2xl shadow-2xl" onClick={e => e.stopPropagation()} data-testid="supplier-profile-modal">
        {loading ? (
          <div className="p-12 text-center text-[#777]">Laden...</div>
        ) : !profile || profile.error ? (
          <div className="p-12 text-center text-[#777]">Partner niet gevonden</div>
        ) : (
          <>
            {/* Hero */}
            <div className="relative h-48 overflow-hidden rounded-t-2xl">
              <img src={profile.hero_image} alt={profile.name} className="w-full h-full object-cover" />
              <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />
              <button onClick={onClose} className="absolute top-3 right-3 w-8 h-8 rounded-full bg-white/20 backdrop-blur flex items-center justify-center text-white hover:bg-white/40 transition" data-testid="close-profile">
                <X size={16} />
              </button>
              {/* Pleisureworld Badge */}
              {profile.pleisureworld_partner && (
                <div className="absolute top-3 left-3 flex items-center gap-1.5 bg-[#244628]/90 backdrop-blur text-white px-3 py-1.5 rounded-full text-xs font-semibold" data-testid="pleisureworld-badge">
                  <Award size={14} className="text-[#70C26C]" />
                  Pleisureworld {profile.pleisureworld_badge}
                </div>
              )}
              <div className="absolute bottom-3 left-4 right-4">
                <h2 className="text-2xl font-bold text-white">{profile.name}</h2>
                <p className="text-white/80 text-sm mt-0.5">{profile.tagline}</p>
              </div>
            </div>

            <div className="p-5 space-y-5">
              {/* Stats */}
              <div className="grid grid-cols-4 gap-2" data-testid="partner-stats">
                {[
                  { icon: Users, label: 'Parken', value: profile.stats.parken_actief },
                  { icon: Clock, label: 'Ervaring', value: profile.stats.jaren_ervaring },
                  { icon: Package, label: 'Geplaatst', value: profile.stats.producten_geinstalleerd },
                  { icon: Star, label: 'Score', value: profile.stats.klanttevredenheid },
                ].map(s => (
                  <div key={s.label} className="bg-white rounded-xl p-3 text-center border border-[#e5e2d9]">
                    <s.icon size={18} className="mx-auto text-[#70C26C] mb-1" />
                    <div className="text-sm font-bold text-[#333]">{s.value}</div>
                    <div className="text-[10px] text-[#999]">{s.label}</div>
                  </div>
                ))}
              </div>

              {/* Description */}
              <p className="text-sm text-[#555] leading-relaxed">{profile.description}</p>

              {/* Action buttons */}
              <div className="flex gap-2">
                <button onClick={handleWebsiteClick} className="flex-1 flex items-center justify-center gap-2 bg-[#244628] text-white py-2.5 rounded-xl text-sm font-semibold hover:bg-[#1a351e] transition" data-testid="website-link">
                  <ExternalLink size={14} />
                  Bezoek Website
                </button>
                {profile.blog_url && (
                  <button onClick={handleBlogClick} className="flex-1 flex items-center justify-center gap-2 bg-white border border-[#244628] text-[#244628] py-2.5 rounded-xl text-sm font-semibold hover:bg-[#244628]/5 transition" data-testid="blog-link">
                    <BookOpen size={14} />
                    Lees Blog
                  </button>
                )}
              </div>

              {/* Podcast */}
              {profile.podcast && (
                <div className="bg-gradient-to-r from-[#244628] to-[#1a351e] rounded-2xl p-4 text-white" data-testid="podcast-section">
                  <div className="flex items-start gap-3">
                    <div className="w-12 h-12 rounded-xl bg-[#70C26C]/20 flex items-center justify-center flex-shrink-0">
                      <Mic size={24} className="text-[#70C26C]" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="text-[10px] font-semibold text-[#70C26C] uppercase tracking-wider">Leisure Talk Podcast</div>
                      <div className="text-sm font-bold mt-0.5">{profile.podcast.titel}</div>
                      <div className="text-white/70 text-xs mt-1">{profile.podcast.beschrijving}</div>
                      <div className="flex items-center gap-3 mt-2">
                        <span className="text-[10px] text-white/50">{profile.podcast.duur}</span>
                        <span className="text-[10px] text-[#70C26C]">{profile.podcast.gast}</span>
                      </div>
                    </div>
                  </div>
                  <button onClick={handlePodcastClick} className="mt-3 w-full bg-[#70C26C] text-[#244628] py-2.5 rounded-xl text-sm font-bold hover:bg-[#5ba855] transition flex items-center justify-center gap-2" data-testid="podcast-play">
                    <Mic size={14} />
                    Beluister Podcast
                    <ChevronRight size={14} />
                  </button>
                </div>
              )}

              {/* Trendwatcher Quote */}
              {profile.trendwatcher_quote && (
                <div className="bg-white border border-[#e5e2d9] rounded-2xl p-4" data-testid="trendwatcher-quote">
                  <div className="flex gap-3">
                    <div className="text-3xl text-[#70C26C] font-serif leading-none">"</div>
                    <div>
                      <p className="text-sm text-[#333] italic leading-relaxed">{profile.trendwatcher_quote.tekst}</p>
                      <div className="mt-2 flex items-center gap-2">
                        <div className="w-8 h-8 rounded-full bg-[#244628] flex items-center justify-center text-white text-xs font-bold">RO</div>
                        <div>
                          <div className="text-xs font-bold text-[#333]">{profile.trendwatcher_quote.auteur}</div>
                          <div className="text-[10px] text-[#999]">{profile.trendwatcher_quote.functie}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Top 3 Products */}
              {profile.top_producten?.length > 0 && (
                <div data-testid="top-products">
                  <h3 className="text-sm font-bold text-[#333] flex items-center gap-1.5 mb-3">
                    <Trophy size={14} className="text-[#d97706]" />
                    Top 3 Meest Gekozen via Configuratie
                    {dynamicTop3?.source === 'dynamisch' && (
                      <span className="text-[9px] bg-[#10b981]/15 text-[#10b981] px-1.5 py-0.5 rounded-full font-medium ml-1">Live Data</span>
                    )}
                  </h3>
                  <div className="space-y-2">
                    {(dynamicTop3?.top_producten || profile.top_producten).map((prod, i) => (
                      <div key={prod.id || prod.naam || i} className="flex items-center gap-3 bg-white border border-[#e5e2d9] rounded-xl p-3" data-testid={`top-product-${i}`}>
                        {prod.image && (
                          <div className="relative w-16 h-16 rounded-lg overflow-hidden flex-shrink-0 bg-[#f0ede6]">
                            <img src={prod.image} alt={prod.name || prod.naam} className="w-full h-full object-cover" />
                            <div className="absolute top-0 left-0 w-5 h-5 bg-[#d97706] text-white text-[10px] font-bold flex items-center justify-center rounded-br-lg">
                              {i + 1}
                            </div>
                          </div>
                        )}
                        {!prod.image && (
                          <div className="relative w-16 h-16 rounded-lg overflow-hidden flex-shrink-0 bg-[#f0ede6] flex items-center justify-center">
                            <Package size={20} className="text-[#ccc]" />
                            <div className="absolute top-0 left-0 w-5 h-5 bg-[#d97706] text-white text-[10px] font-bold flex items-center justify-center rounded-br-lg">
                              {i + 1}
                            </div>
                          </div>
                        )}
                        <div className="flex-1 min-w-0">
                          <div className="text-xs font-bold text-[#333]">{prod.name || prod.naam}</div>
                          {prod.reden && <div className="text-[10px] text-[#999] mt-0.5">{prod.reden}</div>}
                          <div className="flex items-center gap-2 mt-1">
                            {prod.prijs && <span className="text-xs font-bold text-[#70C26C]">€ {prod.prijs.toLocaleString('nl-NL')}</span>}
                            <span className="text-[10px] text-[#777] bg-[#FDF9ED] px-1.5 py-0.5 rounded">{(prod.configuraties || 0).toLocaleString('nl-NL')}x gekozen</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Events */}
              {profile.deelname?.length > 0 && (
                <div data-testid="events-section">
                  <h3 className="text-sm font-bold text-[#333] mb-2">Evenementen & Deelname</h3>
                  <div className="flex flex-wrap gap-1.5">
                    {profile.deelname.map(d => (
                      <span key={d.event} className="text-[10px] bg-white border border-[#e5e2d9] px-2.5 py-1 rounded-full text-[#555]">
                        {d.event} <span className="text-[#70C26C] font-semibold">· {d.type}</span>
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* USPs */}
              {profile.usps?.length > 0 && (
                <div className="flex flex-wrap gap-1.5" data-testid="usps">
                  {profile.usps.map(u => (
                    <span key={u} className="text-[10px] flex items-center gap-1 bg-[#70C26C]/10 text-[#244628] px-2.5 py-1 rounded-full">
                      <Heart size={10} className="text-[#70C26C]" />
                      {u}
                    </span>
                  ))}
                </div>
              )}

              {/* Pleisureworld CTA */}
              {profile.pleisureworld_partner && (
                <div className="bg-[#FDF9ED] border-2 border-dashed border-[#70C26C] rounded-2xl p-4 text-center" data-testid="pleisureworld-cta">
                  <Award size={20} className="mx-auto text-[#70C26C] mb-1" />
                  <div className="text-xs font-bold text-[#244628]">Pleisureworld Preferred Partner sinds {profile.pleisureworld_sinds}</div>
                  <div className="text-[10px] text-[#777] mt-1">
                    Deze leverancier is geselecteerd als preferred partner door Pleisureworld op basis van kwaliteit, service en klanttevredenheid.
                  </div>
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
