import React from 'react';
import { Tent, Home, Gamepad2, ArrowRight, BarChart3, Map, Settings, Beer } from 'lucide-react';

const flows = [
  {
    id: 'recreatie',
    label: 'Recreatie Infra',
    description: 'Campings, camperplaatsen, vakantieparken — sanitair, slagbomen, camera\'s, WiFi',
    icon: Tent,
    color: '#70C26C',
    image: 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=1200&h=800&fit=crop',
  },
  {
    id: 'chalet',
    label: 'Chalet & Stay',
    description: 'Chalets, glamping, tiny houses — units configureren en plaatsen',
    icon: Home,
    color: '#2563eb',
    image: 'https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=1200&h=800&fit=crop',
  },
  {
    id: 'fec',
    label: 'FEC & Experience',
    description: 'Fun & Entertainment Centers — attracties, horeca, beleving',
    icon: Gamepad2,
    color: '#f59e0b',
    image: 'https://images.unsplash.com/photo-1511882150382-421056c89033?w=1200&h=800&fit=crop',
  },
  {
    id: 'horeca',
    label: 'Horeca & Bar',
    description: 'Bar, POS-kassa\'s, bestelzuilen, vending, pub games & terras',
    icon: Beer,
    color: '#b45309',
    image: 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=1200&h=800&fit=crop',
  },
  {
    id: 'dashboard',
    label: 'Platform Dashboard',
    description: 'Trends, benchmarks, lead scoring — marktdata uit de configurator',
    icon: BarChart3,
    color: '#8B6914',
    image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=800&fit=crop',
  },
  {
    id: 'roadmap',
    label: 'Idee naar Realisatie',
    description: 'Stapsgewijs van ontwerp naar vergunning, bouw en exploitatie',
    icon: Map,
    color: '#8b5cf6',
    image: 'https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=1200&h=800&fit=crop',
  },
  {
    id: 'admin-suppliers',
    label: 'Leveranciersbeheer',
    description: 'Leveranciers toevoegen, bewerken en configurator-toewijzing beheren',
    icon: Settings,
    color: '#64748b',
    image: 'https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=1200&h=800&fit=crop',
  },
];

export function FlowSelector({ onSelect }) {
  return (
    <div className="min-h-screen bg-[#FDF9ED] flex flex-col" data-testid="flow-selector">
      {/* Header */}
      <header className="bg-[#244628] text-white px-6 py-4 sticky top-0 z-30">
        <div className="max-w-7xl mx-auto flex items-center justify-between gap-3">
          <img src="/recra-logo-white.png" alt="RECRA Solutions" className="h-8" />
          <div className="text-xs text-white/60 hidden md:block tracking-widest">RECREATION PROJECT CONFIGURATOR</div>
        </div>
      </header>

      {/* Main */}
      <div className="flex-1 px-6 py-12 lg:py-16">
        <div className="max-w-7xl mx-auto">
          {/* Section header */}
          <div className="mb-12 lg:mb-16">
            <div className="flex items-center gap-3 mb-4">
              <div className="h-px w-10 bg-[#70C26C]" />
              <span className="text-xs font-semibold tracking-[0.25em] text-[#70C26C] uppercase">01 · Start</span>
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-[#244628] tracking-tight mb-4">
              Kies je sector
            </h1>
            <p className="text-base text-[#777777] max-w-xl">
              Direct de best passende producten en leveranciers voor jouw recreatie-, hospitality- of entertainment-project.
            </p>
          </div>

          {/* Flow grid */}
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {flows.map((flow, idx) => {
              const Icon = flow.icon;
              const num = String(idx + 1).padStart(2, '0');
              return (
                <button
                  key={flow.id}
                  onClick={() => onSelect(flow.id)}
                  className="group relative text-left rounded-3xl overflow-hidden bg-white border border-[#e5e2d9] hover:shadow-2xl hover:-translate-y-1 transition-all duration-300"
                  data-testid={`flow-${flow.id}`}
                >
                  {/* Hero image */}
                  <div className="relative aspect-[4/3] overflow-hidden bg-[#244628]">
                    <img
                      src={flow.image}
                      alt={flow.label}
                      loading="lazy"
                      className="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                    />
                    {/* Gradient overlay */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />

                    {/* Number badge */}
                    <div className="absolute top-4 left-4 text-xs font-mono tracking-widest text-white/80">
                      {num}
                    </div>

                    {/* Icon chip */}
                    <div
                      className="absolute top-4 right-4 w-11 h-11 rounded-2xl flex items-center justify-center backdrop-blur-md bg-white/15 border border-white/25"
                    >
                      <Icon size={20} className="text-white" />
                    </div>

                    {/* Title on image */}
                    <div className="absolute bottom-0 left-0 right-0 p-5">
                      <h2 className="text-2xl font-bold text-white drop-shadow-lg">{flow.label}</h2>
                    </div>
                  </div>

                  {/* Description block */}
                  <div className="p-5 flex items-start justify-between gap-3">
                    <p className="text-sm text-[#555] leading-relaxed flex-1">
                      {flow.description}
                    </p>
                    <div
                      className="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 transition-all group-hover:translate-x-1"
                      style={{ backgroundColor: `${flow.color}15`, color: flow.color }}
                    >
                      <ArrowRight size={18} />
                    </div>
                  </div>

                  {/* Bottom accent line */}
                  <div
                    className="absolute bottom-0 left-0 right-0 h-1 origin-left scale-x-0 group-hover:scale-x-100 transition-transform duration-500"
                    style={{ backgroundColor: flow.color }}
                  />
                </button>
              );
            })}
          </div>

          <p className="text-center text-xs text-[#999999] mt-12 tracking-wide">
            RECRA Solutions — Powered by Pleisureworld
          </p>
        </div>
      </div>
    </div>
  );
}
