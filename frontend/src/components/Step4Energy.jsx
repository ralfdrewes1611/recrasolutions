import React from 'react';
import { BatteryCharging, Plug, Sun } from 'lucide-react';
import { Label } from './ui/label';

const ENERGY_MODES = [
  { id: 'grid', label: 'Netaansluiting', description: 'Volledig op het elektriciteitsnet', icon: Plug },
  { id: 'hybrid', label: 'Hybrid', description: 'Net + zonnepanelen + accu\'s', icon: Sun },
  { id: 'offgrid', label: 'Off-Grid', description: '100% zelfvoorzienend', icon: BatteryCharging },
];

export function Step4Energy({ project, setProject, powerCalculation }) {
  return (
    <div className="space-y-4" data-testid="step-4-content">
      <div>
        <Label className="text-sm font-medium text-[#333333] mb-3 block">Energievoorziening</Label>
        <div className="space-y-2">
          {ENERGY_MODES.map((mode) => {
            const ModeIcon = mode.icon;
            return (
              <button
                key={mode.id}
                onClick={() => setProject(prev => ({ ...prev, energy_mode: mode.id }))}
                className={`w-full p-4 rounded-xl border-2 text-left transition-all bg-white ${
                  project.energy_mode === mode.id ? 'border-[#70C26C] bg-[#70C26C]/5' : 'border-[#e5e2d9] hover:border-[#70C26C]/50'
                }`}
                data-testid={`energy-mode-${mode.id}`}
              >
                <div className="flex items-center gap-3">
                  <ModeIcon size={24} className={project.energy_mode === mode.id ? 'text-[#70C26C]' : 'text-[#777777]'} />
                  <div>
                    <div className="font-medium text-[#333333]">{mode.label}</div>
                    <div className="text-xs text-[#777777]">{mode.description}</div>
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      <div className="p-4 rounded-xl bg-white border border-[#e5e2d9]">
        <div className="flex items-center gap-2 mb-3">
          <BatteryCharging size={18} className="text-[#70C26C]" />
          <span className="font-medium text-[#333333]">Stroomcalculatie</span>
        </div>
        <div className="space-y-2">
          <div className="flex justify-between">
            <span className="text-sm text-[#777777]">Geschat verbruik</span>
            <span className="font-bold text-[#333333]">{(powerCalculation.watts / 1000).toFixed(1)} kW</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm text-[#777777]">Aanbevolen aansluiting</span>
            <span className="font-bold text-[#70C26C]">{Math.ceil(powerCalculation.watts / 1000 / 25) * 25} kVA</span>
          </div>
        </div>
      </div>

      {project.energy_mode !== 'grid' && (
        <div className="p-4 rounded-xl bg-[#70C26C]/10 border border-[#70C26C]/20">
          <h4 className="font-medium text-[#244628] mb-2">Off-Grid Opties</h4>
          <div className="space-y-2 text-sm">
            {['Zonnepanelen', 'Accu-opslag', 'Wateropvang & hergebruik', 'Zonneboiler', 'Warmtepomp'].map(opt => (
              <label key={opt} className="flex items-center gap-2">
                <input type="checkbox" className="rounded border-[#70C26C]" />
                <span className="text-[#333333]">{opt}</span>
              </label>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
