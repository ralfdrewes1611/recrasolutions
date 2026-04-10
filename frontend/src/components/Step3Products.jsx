import React from 'react';
import { Package, Eye, EyeOff, X, Bath, Camera, Wifi, Lightbulb, CreditCard, Key, ArrowRight, Droplets, BatteryCharging, Monitor, Heart } from 'lucide-react';
import { Button } from './ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Tooltip, TooltipTrigger, TooltipContent } from './ui/tooltip';
import { ProductImportPanel } from '../ProductImportPanel';

const categoryIcons = {
  sanitair: Bath, slagboom: ArrowRight, camera: Camera, wifi: Wifi,
  verlichting: Lightbulb, betaalsysteem: CreditCard, toegangscontrole: Key,
  douchelezer: Droplets, energie: BatteryCharging, informatiezuil: Monitor,
  wellness: Heart,
};

const categoryColors = {
  sanitair: '#70C26C', slagboom: '#d97706', camera: '#dc2626', wifi: '#2563eb',
  verlichting: '#ca8a04', betaalsysteem: '#7c3aed', toegangscontrole: '#db2777',
  douchelezer: '#0891b2', energie: '#059669', informatiezuil: '#0891b2',
  wellness: '#8B5E3C',
};

const categoryLabels = {
  sanitair: 'Sanitair Units', slagboom: 'Slagbomen', camera: "Camera's",
  wifi: 'WiFi Systemen', verlichting: 'Verlichting', betaalsysteem: 'Betaalsystemen',
  toegangscontrole: 'Toegangscontrole', douchelezer: 'Douchelezers', energie: 'Energie & Off-Grid',
  informatiezuil: 'Informatiezuilen & Kiosken', wellness: 'Wellness — Ticra Outdoor',
};

export { categoryIcons, categoryColors, categoryLabels };

export function Step3Products({
  products, selectedCategory, setSelectedCategory, selectedProduct,
  setSelectedProduct, showRealProducts, setShowRealProducts,
  handlePointerDragStart, fetchProducts,
}) {
  const categories = [...new Set(products.map(p => p.category))];
  const filteredProducts = selectedCategory === 'all'
    ? products
    : products.filter(p => p.category === selectedCategory);

  return (
    <div className="space-y-3" data-testid="step-3-content">
      <div className="flex items-center justify-between">
        <Select value={selectedCategory} onValueChange={setSelectedCategory}>
          <SelectTrigger className="flex-1 bg-white border-[#e5e2d9]" data-testid="category-select">
            <SelectValue placeholder="Alle categorieën" />
          </SelectTrigger>
          <SelectContent className="bg-white border-[#e5e2d9]">
            <SelectItem value="all">Alle categorieën</SelectItem>
            {categories.map((cat) => (
              <SelectItem key={cat} value={cat}>{categoryLabels[cat] || cat}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Tooltip>
          <TooltipTrigger asChild>
            <Button variant="ghost" size="icon" className="ml-2" onClick={() => setShowRealProducts(!showRealProducts)}>
              {showRealProducts ? <Eye size={18} /> : <EyeOff size={18} />}
            </Button>
          </TooltipTrigger>
          <TooltipContent>{showRealProducts ? '2D weergave' : 'Icoon weergave'}</TooltipContent>
        </Tooltip>
      </div>

      <div className="space-y-2">
        {filteredProducts.map((product) => {
          const Icon = categoryIcons[product.category] || Package;
          const color = categoryColors[product.category] || '#70C26C';
          const isSanitair = product.category === 'sanitair';
          const isSelected = selectedProduct?.id === product.id;
          const dims = product.dimensions;

          return (
            <div
              key={product.id}
              onClick={() => setSelectedProduct(isSelected ? null : product)}
              className={`bg-white border rounded-xl overflow-hidden cursor-pointer hover:shadow-md transition-all ${
                isSelected ? 'border-[#70C26C] ring-2 ring-[#70C26C]/30 bg-[#70C26C]/5' : 'border-[#e5e2d9] hover:border-[#70C26C]'
              }`}
              data-testid={`product-card-${product.id}`}
            >
              {product.image && (
                <div className="w-full h-28 bg-[#f0ede6] overflow-hidden">
                  <img src={product.image} alt={product.name} className="w-full h-full object-cover" loading="lazy" />
                </div>
              )}
              <div className="p-3">
                <div className="flex items-start gap-3">
                  <div
                    className="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 cursor-grab active:cursor-grabbing hover:ring-2 hover:ring-[#70C26C]/40 select-none"
                    style={{ backgroundColor: `${color}15` }}
                    onMouseDown={(e) => handlePointerDragStart(e, product)}
                    data-testid={`drag-handle-${product.id}`}
                  >
                    <Icon size={20} style={{ color }} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="font-semibold text-sm text-[#333333] truncate">{product.name}</div>
                    <div className="text-xs text-[#777777] mt-0.5 line-clamp-1">{product.description}</div>
                    <div className="flex items-center gap-2 mt-1.5">
                      {isSanitair ? (
                        <span className="text-sm font-bold text-[#70C26C]">vanaf € {product.price_purchase.toLocaleString()}</span>
                      ) : (
                        <span className="text-sm font-bold text-[#70C26C]">€ {product.price_purchase.toLocaleString()}</span>
                      )}
                      {dims && (dims.width >= 1 || dims.height >= 1) && (
                        <span className="text-[10px] text-[#777777] bg-[#FDF9ED] px-1.5 py-0.5 rounded">{dims.width}x{dims.height}m</span>
                      )}
                      {product.supplier && (
                        <span className="text-[10px] text-[#8B5E3C] bg-[#8B5E3C]/10 px-1.5 py-0.5 rounded">{product.supplier}</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
              {isSelected && (
                <div className="mx-3 mb-3 text-xs text-[#70C26C] font-medium text-center bg-[#70C26C]/10 py-1 rounded">
                  Klik op het canvas om te plaatsen
                </div>
              )}
            </div>
          );
        })}
      </div>

      {selectedProduct ? (
        <div className="flex gap-2">
          <div className="flex-1 text-xs text-[#70C26C] font-medium text-center bg-[#70C26C]/10 p-2 rounded-lg">
            Geselecteerd: {selectedProduct.name}
          </div>
          <Button variant="ghost" size="sm" onClick={() => setSelectedProduct(null)} className="text-[#777777]">
            <X size={14} />
          </Button>
        </div>
      ) : (
        <p className="text-xs text-[#777777] text-center bg-[#FDF9ED] p-2 rounded-lg">
          Klik op een product en dan op het canvas om te plaatsen. Of sleep het product direct.
        </p>
      )}

      <div className="pt-3 border-t border-[#e5e2d9]">
        <ProductImportPanel onProductsAdded={fetchProducts} />
      </div>
    </div>
  );
}
