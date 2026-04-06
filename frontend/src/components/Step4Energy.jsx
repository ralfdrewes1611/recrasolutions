import React, { useMemo } from 'react';
import { BatteryCharging, Plug, Sun, Zap, Droplets, Flame, Wind, Minus, Plus } from 'lucide-react';
import { Label } from './ui/label';
import { Button } from './ui/button';
import { Input } from './ui/input';

const ENERGY_MODES = [
  { id: 'grid', label: 'Netaansluiting', description: 'Volledig op het elektriciteitsnet', icon: Plug },
  { id: 'hybrid', label: 'Hybrid', description: 'Net + zonnepanelen + accu\'s', icon: Sun },
  { id: 'offgrid', label: 'Off-Grid', description: '100% zelfvoorzienend', icon: BatteryCharging },
];

// Realistic specs for energy components
const SOLAR_PANEL_WP = 450;      // Wp per panel (modern mono)
const SOLAR_PANEL_M2 = 2.0;      // m² per panel
const SOLAR_PANEL_PRICE = 320;    // € per panel installed
const SOLAR_HOURS_NL = 3.5;      // peak sun hours average Netherlands

const BATTERY_KWH = 5;           // kWh per battery unit (LiFePO4)
const BATTERY_PRICE = 2800;      // € per 5kWh battery
const BATTERY_AUTONOMY_DAYS = 1; // days of autonomy target

const HEAT_PUMP_COP = 3.5;       // Coefficient of Performance
const HEAT_PUMP_PRICE = 8500;    // € per unit

const SOLAR_BOILER_LITERS = 300; // liter per unit
const SOLAR_BOILER_PRICE = 3200; // € per unit

const WATER_RECYCLE_PRICE = 12000; // € per system
const WIND_TURBINE_KW = 3;       // kW per small wind turbine
const WIND_TURBINE_PRICE = 6500; // €

export function Step4Energy({ project, setProject, powerCalculation }) {
  const energyConfig = project.energy_config || {
    solar_panels: 0,
    batteries: 0,
    heat_pump: false,
    solar_boiler: false,
    water_recycling: false,
    wind_turbine: false,
  };

  const setEnergyConfig = (updates) => {
    setProject(prev => ({
      ...prev,
      energy_config: { ...(prev.energy_config || energyConfig), ...updates },
    }));
  };

  // Calculations
  const calc = useMemo(() => {
    const totalWatts = powerCalculation.watts || 0;
    const dailyKwh = (totalWatts / 1000) * 10; // 10 operating hours/day avg
    const yearlyKwh = dailyKwh * 365;

    // Solar
    const solarDailyKwh = energyConfig.solar_panels * SOLAR_PANEL_WP * SOLAR_HOURS_NL / 1000;
    const solarYearlyKwh = solarDailyKwh * 365;
    const solarCoverage = dailyKwh > 0 ? Math.min(100, Math.round((solarDailyKwh / dailyKwh) * 100)) : 0;
    const solarCost = energyConfig.solar_panels * SOLAR_PANEL_PRICE;
    const solarM2 = energyConfig.solar_panels * SOLAR_PANEL_M2;

    // Recommended panels for full coverage
    const recommendedPanels = dailyKwh > 0 ? Math.ceil((dailyKwh * 1000) / (SOLAR_PANEL_WP * SOLAR_HOURS_NL)) : 0;

    // Batteries
    const batteryKwh = energyConfig.batteries * BATTERY_KWH;
    const batteryAutonomyHours = totalWatts > 0 ? Math.round((batteryKwh * 1000 / totalWatts) * 10) / 10 : 0;
    const batteryCost = energyConfig.batteries * BATTERY_PRICE;

    // Recommended batteries for 1 day autonomy
    const recommendedBatteries = dailyKwh > 0 ? Math.ceil(dailyKwh / BATTERY_KWH) : 0;

    // Heat pump savings
    const heatPumpSaving = energyConfig.heat_pump ? Math.round(yearlyKwh * 0.15 * (1 - 1/HEAT_PUMP_COP)) : 0;

    // Total costs
    const heatPumpCost = energyConfig.heat_pump ? HEAT_PUMP_PRICE : 0;
    const solarBoilerCost = energyConfig.solar_boiler ? SOLAR_BOILER_PRICE : 0;
    const waterCost = energyConfig.water_recycling ? WATER_RECYCLE_PRICE : 0;
    const windCost = energyConfig.wind_turbine ? WIND_TURBINE_PRICE : 0;
    const totalInvestment = solarCost + batteryCost + heatPumpCost + solarBoilerCost + waterCost + windCost;

    // Grid savings
    const electricityRate = 0.35; // €/kWh NL avg
    const yearlySaving = (solarYearlyKwh + heatPumpSaving) * electricityRate;
    const paybackYears = yearlySaving > 0 ? Math.round(totalInvestment / yearlySaving * 10) / 10 : 0;

    // Grid connection needed
    const gridKva = project.energy_mode === 'offgrid' ? 0 : Math.ceil(Math.max(0, totalWatts - (energyConfig.solar_panels * SOLAR_PANEL_WP * 0.8)) / 1000 / 25) * 25;

    return {
      totalWatts, dailyKwh, yearlyKwh, solarDailyKwh, solarYearlyKwh,
      solarCoverage, solarCost, solarM2, recommendedPanels, batteryKwh,
      batteryAutonomyHours, batteryCost, recommendedBatteries, heatPumpSaving,
      totalInvestment, yearlySaving, paybackYears, gridKva,
    };
  }, [powerCalculation.watts, energyConfig, project.energy_mode]);

  return (
    <div className="space-y-4" data-testid="step-4-content">
      {/* Mode Selection */}
      <div>
        <Label className="text-sm font-medium text-[#333333] mb-3 block">Energievoorziening</Label>
        <div className="space-y-2">
          {ENERGY_MODES.map((mode) => {
            const ModeIcon = mode.icon;
            return (
              <button
                key={mode.id}
                onClick={() => setProject(prev => ({ ...prev, energy_mode: mode.id }))}
                className={`w-full p-3 rounded-xl border-2 text-left transition-all bg-white ${
                  project.energy_mode === mode.id ? 'border-[#70C26C] bg-[#70C26C]/5' : 'border-[#e5e2d9] hover:border-[#70C26C]/50'
                }`}
                data-testid={`energy-mode-${mode.id}`}
              >
                <div className="flex items-center gap-3">
                  <ModeIcon size={20} className={project.energy_mode === mode.id ? 'text-[#70C26C]' : 'text-[#777777]'} />
                  <div>
                    <div className="font-medium text-sm text-[#333333]">{mode.label}</div>
                    <div className="text-xs text-[#777777]">{mode.description}</div>
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Power Summary */}
      <div className="p-3 rounded-xl bg-white border border-[#e5e2d9]">
        <div className="flex items-center gap-2 mb-2">
          <Zap size={16} className="text-[#70C26C]" />
          <span className="font-medium text-sm text-[#333333]">Stroomcalculatie</span>
        </div>
        <div className="space-y-1.5 text-sm">
          <div className="flex justify-between">
            <span className="text-[#777777]">Piek verbruik</span>
            <span className="font-bold text-[#333333]">{(calc.totalWatts / 1000).toFixed(1)} kW</span>
          </div>
          <div className="flex justify-between">
            <span className="text-[#777777]">Dagelijks verbruik</span>
            <span className="font-bold text-[#333333]">{calc.dailyKwh.toFixed(1)} kWh</span>
          </div>
          <div className="flex justify-between">
            <span className="text-[#777777]">Jaarlijks verbruik</span>
            <span className="font-bold text-[#333333]">{Math.round(calc.yearlyKwh).toLocaleString()} kWh</span>
          </div>
          {project.energy_mode !== 'offgrid' && calc.gridKva > 0 && (
            <div className="flex justify-between pt-1 border-t border-[#e5e2d9]">
              <span className="text-[#777777]">Netaansluiting nodig</span>
              <span className="font-bold text-[#70C26C]">{calc.gridKva} kVA</span>
            </div>
          )}
        </div>
      </div>

      {/* Solar Panels */}
      {project.energy_mode !== 'grid' && (
        <div className="p-3 rounded-xl bg-white border border-[#e5e2d9]">
          <div className="flex items-center gap-2 mb-2">
            <Sun size={16} className="text-amber-500" />
            <span className="font-medium text-sm text-[#333333]">Zonnepanelen ({SOLAR_PANEL_WP}Wp/stuk)</span>
          </div>
          <div className="flex items-center gap-3 mb-2">
            <Button variant="outline" size="icon" className="h-8 w-8 border-[#e5e2d9]"
              onClick={() => setEnergyConfig({ solar_panels: Math.max(0, energyConfig.solar_panels - 1) })} data-testid="solar-minus">
              <Minus size={14} />
            </Button>
            <Input type="number" min="0" max="500" value={energyConfig.solar_panels}
              onChange={(e) => setEnergyConfig({ solar_panels: Math.max(0, parseInt(e.target.value) || 0) })}
              className="w-20 text-center bg-white border-[#e5e2d9] h-8" data-testid="solar-panels-input" />
            <Button variant="outline" size="icon" className="h-8 w-8 border-[#e5e2d9]"
              onClick={() => setEnergyConfig({ solar_panels: energyConfig.solar_panels + 1 })} data-testid="solar-plus">
              <Plus size={14} />
            </Button>
            <span className="text-xs text-[#777777]">panelen</span>
          </div>
          {calc.recommendedPanels > 0 && (
            <button onClick={() => setEnergyConfig({ solar_panels: calc.recommendedPanels })}
              className="text-xs text-[#70C26C] hover:underline mb-2 block" data-testid="solar-recommend-btn">
              Aanbevolen: {calc.recommendedPanels} panelen voor 100% dekking
            </button>
          )}
          <div className="space-y-1 text-xs">
            <div className="flex justify-between">
              <span className="text-[#777777]">Opbrengst/dag</span>
              <span className="text-[#333333]">{calc.solarDailyKwh.toFixed(1)} kWh</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#777777]">Dekking</span>
              <span className={`font-bold ${calc.solarCoverage >= 100 ? 'text-[#70C26C]' : 'text-amber-500'}`}>{calc.solarCoverage}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#777777]">Dakoppervlak</span>
              <span className="text-[#333333]">{calc.solarM2.toFixed(0)} m²</span>
            </div>
            <div className="w-full h-2 bg-[#e5e2d9] rounded-full mt-1">
              <div className="h-2 rounded-full transition-all" style={{ width: `${Math.min(100, calc.solarCoverage)}%`, backgroundColor: calc.solarCoverage >= 100 ? '#70C26C' : '#f59e0b' }} />
            </div>
          </div>
        </div>
      )}

      {/* Batteries */}
      {project.energy_mode !== 'grid' && (
        <div className="p-3 rounded-xl bg-white border border-[#e5e2d9]">
          <div className="flex items-center gap-2 mb-2">
            <BatteryCharging size={16} className="text-blue-500" />
            <span className="font-medium text-sm text-[#333333]">Accu-opslag (LiFePO4, {BATTERY_KWH}kWh/stuk)</span>
          </div>
          <div className="flex items-center gap-3 mb-2">
            <Button variant="outline" size="icon" className="h-8 w-8 border-[#e5e2d9]"
              onClick={() => setEnergyConfig({ batteries: Math.max(0, energyConfig.batteries - 1) })} data-testid="battery-minus">
              <Minus size={14} />
            </Button>
            <Input type="number" min="0" max="100" value={energyConfig.batteries}
              onChange={(e) => setEnergyConfig({ batteries: Math.max(0, parseInt(e.target.value) || 0) })}
              className="w-20 text-center bg-white border-[#e5e2d9] h-8" data-testid="batteries-input" />
            <Button variant="outline" size="icon" className="h-8 w-8 border-[#e5e2d9]"
              onClick={() => setEnergyConfig({ batteries: energyConfig.batteries + 1 })} data-testid="battery-plus">
              <Plus size={14} />
            </Button>
            <span className="text-xs text-[#777777]">units</span>
          </div>
          {calc.recommendedBatteries > 0 && (
            <button onClick={() => setEnergyConfig({ batteries: calc.recommendedBatteries })}
              className="text-xs text-[#70C26C] hover:underline mb-2 block" data-testid="battery-recommend-btn">
              Aanbevolen: {calc.recommendedBatteries} units voor 1 dag autonomie
            </button>
          )}
          <div className="space-y-1 text-xs">
            <div className="flex justify-between">
              <span className="text-[#777777]">Totale capaciteit</span>
              <span className="text-[#333333]">{calc.batteryKwh} kWh</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#777777]">Autonomie</span>
              <span className={`font-bold ${calc.batteryAutonomyHours >= 10 ? 'text-[#70C26C]' : 'text-amber-500'}`}>
                {calc.batteryAutonomyHours} uur
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Extra Options */}
      {project.energy_mode !== 'grid' && (
        <div className="p-3 rounded-xl bg-white border border-[#e5e2d9]">
          <div className="font-medium text-sm text-[#333333] mb-2">Extra opties</div>
          <div className="space-y-2">
            {[
              { key: 'heat_pump', label: 'Warmtepomp', desc: `COP ${HEAT_PUMP_COP} — bespaart ~${calc.heatPumpSaving} kWh/jaar`, price: HEAT_PUMP_PRICE, icon: Flame },
              { key: 'solar_boiler', label: 'Zonneboiler', desc: `${SOLAR_BOILER_LITERS}L — warm water via zon`, price: SOLAR_BOILER_PRICE, icon: Sun },
              { key: 'water_recycling', label: 'Wateropvang & hergebruik', desc: 'Regenwater opvang en grijswater recycling', price: WATER_RECYCLE_PRICE, icon: Droplets },
              { key: 'wind_turbine', label: 'Windturbine', desc: `${WIND_TURBINE_KW}kW micro wind — extra opwek`, price: WIND_TURBINE_PRICE, icon: Wind },
            ].map((opt) => {
              const OptIcon = opt.icon;
              return (
                <label key={opt.key} className={`flex items-start gap-3 p-2.5 rounded-lg border cursor-pointer transition-all ${energyConfig[opt.key] ? 'border-[#70C26C] bg-[#70C26C]/5' : 'border-[#e5e2d9] hover:border-[#70C26C]/30'}`} data-testid={`energy-option-${opt.key}`}>
                  <input type="checkbox" checked={!!energyConfig[opt.key]}
                    onChange={(e) => setEnergyConfig({ [opt.key]: e.target.checked })}
                    className="rounded border-[#70C26C] text-[#70C26C] mt-0.5" />
                  <div className="flex-1">
                    <div className="flex items-center gap-1.5">
                      <OptIcon size={14} className={energyConfig[opt.key] ? 'text-[#70C26C]' : 'text-[#777777]'} />
                      <span className="text-sm font-medium text-[#333333]">{opt.label}</span>
                    </div>
                    <p className="text-[10px] text-[#777777] mt-0.5">{opt.desc}</p>
                  </div>
                  <span className="text-xs font-bold text-[#70C26C] whitespace-nowrap">€ {opt.price.toLocaleString()}</span>
                </label>
              );
            })}
          </div>
        </div>
      )}

      {/* Investment Summary */}
      {project.energy_mode !== 'grid' && calc.totalInvestment > 0 && (
        <div className="p-3 rounded-xl bg-[#244628] text-white">
          <div className="font-medium text-sm mb-2">Energie Investering</div>
          <div className="space-y-1.5 text-sm">
            {energyConfig.solar_panels > 0 && (
              <div className="flex justify-between text-white/80">
                <span>{energyConfig.solar_panels}x Zonnepaneel</span>
                <span>€ {calc.solarCost.toLocaleString()}</span>
              </div>
            )}
            {energyConfig.batteries > 0 && (
              <div className="flex justify-between text-white/80">
                <span>{energyConfig.batteries}x Accu ({BATTERY_KWH}kWh)</span>
                <span>€ {calc.batteryCost.toLocaleString()}</span>
              </div>
            )}
            {energyConfig.heat_pump && <div className="flex justify-between text-white/80"><span>Warmtepomp</span><span>€ {HEAT_PUMP_PRICE.toLocaleString()}</span></div>}
            {energyConfig.solar_boiler && <div className="flex justify-between text-white/80"><span>Zonneboiler</span><span>€ {SOLAR_BOILER_PRICE.toLocaleString()}</span></div>}
            {energyConfig.water_recycling && <div className="flex justify-between text-white/80"><span>Wateropvang</span><span>€ {WATER_RECYCLE_PRICE.toLocaleString()}</span></div>}
            {energyConfig.wind_turbine && <div className="flex justify-between text-white/80"><span>Windturbine</span><span>€ {WIND_TURBINE_PRICE.toLocaleString()}</span></div>}
            <div className="h-px bg-white/20" />
            <div className="flex justify-between font-bold" data-testid="energy-total-investment">
              <span>Totaal energie</span>
              <span>€ {calc.totalInvestment.toLocaleString()}</span>
            </div>
            {calc.yearlySaving > 0 && (
              <>
                <div className="flex justify-between text-[#70C26C] text-xs">
                  <span>Jaarlijkse besparing</span>
                  <span>€ {Math.round(calc.yearlySaving).toLocaleString()}</span>
                </div>
                <div className="flex justify-between text-[#70C26C] text-xs">
                  <span>Terugverdientijd</span>
                  <span>{calc.paybackYears} jaar</span>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
