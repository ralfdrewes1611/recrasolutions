import React from 'react';
import { Tent, Home, Gamepad2, ArrowRight, BarChart3, Map } from 'lucide-react';

const flows = [
  {
    id: 'recreatie',
    label: 'Recreatie Infra',
    description: 'Campings, camperplaatsen, vakantieparken — sanitair, slagbomen, camera\'s, WiFi',
    icon: Tent,
    color: '#70C26C',
    bgColor: '#70C26C10',
  },
  {
    id: 'chalet',
    label: 'Chalet & Stay',
    description: 'Chalets, glamping, tiny houses — units configureren en plaatsen',
    icon: Home,
    color: '#2563eb',
    bgColor: '#2563eb10',
  },
  {
    id: 'fec',
    label: 'FEC & Experience',
    description: 'Fun & Entertainment Centers — attracties, horeca, beleving',
    icon: Gamepad2,
    color: '#f59e0b',
    bgColor: '#f59e0b10',
  },
  {
    id: 'dashboard',
    label: 'Platform Dashboard',
    description: 'Trends, benchmarks, lead scoring — marktdata uit de configurator',
    icon: BarChart3,
    color: '#8B6914',
    bgColor: '#8B691410',
  },
  {
    id: 'roadmap',
    label: 'Idee naar Realisatie',
    description: 'Stapsgewijs van ontwerp naar vergunning, bouw en exploitatie',
    icon: Map,
    color: '#8b5cf6',
    bgColor: '#8b5cf610',
  },
];

export function FlowSelector({ onSelect }) {
  return (
    <div className="min-h-screen bg-[#FDF9ED] flex flex-col" data-testid="flow-selector">
      {/* Header */}
      <header className="bg-[#244628] text-white px-6 py-4">
        <div className="max-w-5xl mx-auto flex items-center gap-3">
          <img src="/recra-logo-white.png" alt="RECRA Solutions" className="h-8" />
        </div>
      </header>

      {/* Main */}
      <div className="flex-1 flex items-center justify-center p-6">
        <div className="max-w-3xl w-full">
          <div className="text-center mb-10">
            <h1 className="text-3xl sm:text-4xl font-bold text-[#244628] mb-3">
              Wat wil je ontwikkelen?
            </h1>
            <p className="text-base text-[#777777] max-w-lg mx-auto">
              Kies je projecttype en configureer direct je terrein met echte producten en leveranciers.
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
            {flows.map((flow) => {
              const Icon = flow.icon;
              return (
                <button
                  key={flow.id}
                  onClick={() => onSelect(flow.id)}
                  className="group text-left p-6 rounded-2xl bg-white border-2 border-[#e5e2d9] hover:border-current transition-all hover:shadow-lg"
                  style={{ '--tw-border-opacity': 1 }}
                  data-testid={`flow-${flow.id}`}
                >
                  <div
                    className="w-14 h-14 rounded-xl flex items-center justify-center mb-4"
                    style={{ backgroundColor: flow.bgColor }}
                  >
                    <Icon size={28} style={{ color: flow.color }} />
                  </div>
                  <h2 className="text-lg font-bold text-[#333333] mb-1">{flow.label}</h2>
                  <p className="text-sm text-[#777777] mb-4 leading-relaxed">{flow.description}</p>
                  <div className="flex items-center gap-1 text-sm font-medium" style={{ color: flow.color }}>
                    Start configuratie <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
                  </div>
                </button>
              );
            })}
          </div>

          <p className="text-center text-xs text-[#999999] mt-8">
            RECRA Solutions — Recreation Project Configurator & Partner Matching Platform
          </p>
        </div>
      </div>
    </div>
  );
}
