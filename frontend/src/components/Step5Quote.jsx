import React from 'react';
import { Bath, Download, Truck, Lock, Map } from 'lucide-react';
import { Button } from './ui/button';
import { AIQuoteText } from '../AIQuoteText';
import { ScenarioCompare } from '../ScenarioCompare';

const SANITAIR_EXTRAS = {
  extra_douches: { label: 'Extra douches', price: 2500, lease: 60 },
  familiecabine: { label: 'Familiecabine', price: 3000, lease: 72 },
  warmtepomp: { label: 'Warmtepomp', price: 4500, lease: 108 },
  zonneboiler: { label: 'Zonneboiler', price: 3500, lease: 84 },
};

export { SANITAIR_EXTRAS };

export function Step5Quote({
  project, products, quickQuote, sanitairConfigs, setSanitairConfigs,
  matchedSuppliers, exportPDF, loading, userTier = 'free', onUpgrade, energyInvestment = 0,
  onRoadmap,
}) {
  const getProductById = (pid) => products.find(p => p.id === pid);

  // Only count travel costs for categories that have placed products
  const categoriesUsed = new Set();
  project.placed_products.forEach(pp => {
    const p = getProductById(pp.product_id);
    if (p) categoriesUsed.add(p.category);
  });

  // Filter suppliers to only those matching used categories
  const relevantSuppliers = (matchedSuppliers || []).filter(ms => {
    const cats = ms.supplier?.categories || [];
    return cats.some(c => categoriesUsed.has(c));
  });

  // Deduplicate: only show the best supplier per category
  const seenCats = new Set();
  const bestSuppliers = [];
  for (const ms of relevantSuppliers) {
    const cats = ms.supplier?.categories || [];
    const matchedCat = cats.find(c => categoriesUsed.has(c) && !seenCats.has(c));
    if (matchedCat) {
      seenCats.add(matchedCat);
      bestSuppliers.push({ ...ms, matchedCategory: matchedCat });
    }
  }

  const travelTotal = bestSuppliers.reduce((sum, ms) => sum + (ms.travel?.total_travel_cost || 0), 0);

  return (
    <div className="space-y-4" data-testid="step-5-content">
      {/* Sanitair configuratie */}
      {project.placed_products.some(pp => {
        const p = getProductById(pp.product_id);
        return p && p.category === 'sanitair';
      }) && (
        <div className="p-4 rounded-xl bg-white border border-[#e5e2d9]">
          <div className="flex items-center gap-2 mb-3">
            <Bath size={18} className="text-[#70C26C]" />
            <h3 className="font-bold text-[#333333]">Sanitair Samenstellen</h3>
          </div>
          <p className="text-xs text-[#777777] mb-3">Configureer modules en betaalmethode per sanitair unit.</p>
          {project.placed_products.filter(pp => {
            const p = getProductById(pp.product_id);
            return p && p.category === 'sanitair';
          }).map((pp) => {
            const product = getProductById(pp.product_id);
            const config = sanitairConfigs[pp.id] || { payment: 'adyen_contactless', extras: [] };

            const toggleExtra = (extraKey) => {
              setSanitairConfigs(prev => {
                const current = prev[pp.id] || { payment: 'adyen_contactless', extras: [] };
                const extras = current.extras.includes(extraKey)
                  ? current.extras.filter(e => e !== extraKey)
                  : [...current.extras, extraKey];
                return { ...prev, [pp.id]: { ...current, extras } };
              });
            };

            return (
              <div key={pp.id} className="mb-3 p-3 rounded-lg border border-[#e5e2d9] bg-[#FFFEF8]" data-testid={`sanitair-config-${pp.id}`}>
                <div className="font-medium text-sm text-[#333333] mb-2">{product.name}</div>
                <div className="text-xs text-[#777777] mb-2">Betaling: Adyen (Contactloos PIN/Apple Pay/Google Pay)</div>
                <div className="space-y-1.5">
                  {Object.entries(SANITAIR_EXTRAS).map(([key, extra]) => (
                    <label key={key} className="flex items-center gap-2 cursor-pointer" data-testid={`sanitair-extra-${key}-${pp.id}`}>
                      <input
                        type="checkbox"
                        checked={config.extras.includes(key)}
                        onChange={() => toggleExtra(key)}
                        className="rounded border-[#70C26C] text-[#70C26C]"
                      />
                      <span className="text-sm text-[#333333] flex-1">{extra.label}</span>
                      <span className="text-xs font-medium text-[#70C26C]">+€{extra.price.toLocaleString()}</span>
                    </label>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Investering */}
      <div className="p-4 rounded-xl bg-white border border-[#e5e2d9]">
        <h3 className="font-bold text-[#333333] mb-3">Investering</h3>
        <div className="space-y-2">
          <div className="flex justify-between">
            <span className="text-[#777777]">Aankoopkosten</span>
            <span className="font-bold text-[#70C26C]">€ {quickQuote.capex.toLocaleString()}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-[#777777]">Installatiekosten</span>
            <span className="text-[#333333]">€ {quickQuote.install.toLocaleString()}</span>
          </div>
          {travelTotal > 0 && (
            <div className="flex justify-between">
              <span className="text-[#777777] flex items-center gap-1"><Truck size={12} /> Reiskosten</span>
              <span className="text-[#333333]">€ {Math.round(travelTotal).toLocaleString()}</span>
            </div>
          )}
          {energyInvestment > 0 && (
            <div className="flex justify-between">
              <span className="text-[#777777] flex items-center gap-1">Energie-installatie</span>
              <span className="text-[#333333]">€ {energyInvestment.toLocaleString()}</span>
            </div>
          )}
          <div className="h-px bg-[#e5e2d9]" />
          <div className="flex justify-between">
            <span className="font-semibold text-[#333333]">Totaal investering</span>
            <span className="text-lg font-bold text-[#70C26C]">€ {(quickQuote.capex + quickQuote.install + Math.round(travelTotal) + energyInvestment).toLocaleString()}</span>
          </div>
        </div>
      </div>

      {/* Reiskosten detail */}
      {bestSuppliers.length > 0 && (
        <div className="p-4 rounded-xl bg-white border border-[#e5e2d9]">
          <div className="flex items-center gap-2 mb-3">
            <Truck size={18} className="text-[#70C26C]" />
            <h3 className="font-bold text-[#333333]">Reiskosten Leveranciers</h3>
          </div>
          <div className="space-y-2">
            {bestSuppliers.map((ms, i) => (
              <div key={i} className="flex justify-between items-center p-2 rounded-lg bg-[#FDF9ED]">
                <div>
                  <div className="text-sm font-medium text-[#333333]">{ms.supplier?.name}</div>
                  <div className="text-[10px] text-[#777777]">{ms.matchedCategory} - {ms.travel?.distance_km} km - {Math.round((ms.travel?.travel_time_hours || 0) * 60)} min</div>
                </div>
                <span className="text-sm font-bold text-[#70C26C]">€ {ms.travel?.total_travel_cost?.toLocaleString()}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Operational Lease */}
      <div className="p-4 rounded-xl bg-white border border-[#e5e2d9]">
        <h3 className="font-bold text-[#333333] mb-1">Operational Lease</h3>
        <p className="text-xs text-[#777777] mb-3">Uitgaande van 60 maanden incl. SLA onderhoudscontract</p>
        <div className="space-y-2">
          <div className="flex justify-between">
            <span className="text-[#777777]">Per maand</span>
            <span className="font-bold text-[#70C26C]">€ {quickQuote.opex.toLocaleString()}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-[#777777]">Per jaar</span>
            <span className="text-[#333333]">€ {(quickQuote.opex * 12).toLocaleString()}</span>
          </div>
        </div>
      </div>

      <AIQuoteText project={project} products={products} quickQuote={quickQuote} />

      {userTier === 'free' ? (
        <Button
          onClick={onUpgrade}
          className="w-full bg-[#244628] hover:bg-[#1a341d] text-white font-semibold h-12"
          data-testid="export-pdf-locked"
        >
          <Lock size={18} className="mr-2" />
          Upgrade naar Pro voor PDF export
        </Button>
      ) : (
        <Button
          onClick={exportPDF}
          disabled={loading || project.placed_products.length === 0}
          className="w-full bg-[#70C26C] hover:bg-[#5fb35b] text-white font-semibold h-12"
          data-testid="export-pdf-button"
        >
          <Download size={18} className="mr-2" />
          Offerte downloaden (PDF)
        </Button>
      )}

      {onRoadmap && (
        <Button
          onClick={onRoadmap}
          variant="outline"
          className="w-full border-[#244628] text-[#244628] hover:bg-[#244628] hover:text-white font-medium h-10 mt-2"
          data-testid="roadmap-button"
        >
          <Map size={16} className="mr-2" />
          Idee naar Realisatie — Roadmap bekijken
        </Button>
      )}

      {/* 3 Offerte Scenario's */}
      <div className="mt-4" data-testid="scenario-section">
        <ScenarioCompare
          flowType="recreatie"
          projectDescription={project?.name || 'Recreatiepark'}
          investmentRange={quickQuote ? (quickQuote.capex_total > 100000 ? '> €100K' : quickQuote.capex_total > 25000 ? '€25K - €100K' : '€10K - €25K') : '€25K - €100K'}
        />
      </div>
    </div>
  );
}
