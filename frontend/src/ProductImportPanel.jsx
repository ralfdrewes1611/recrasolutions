import React, { useState, useRef } from 'react';
import { toast } from 'sonner';
import axios from 'axios';
import { 
  Upload, Globe, FileSpreadsheet, Check, X, Loader2, 
  Package, AlertTriangle, ChevronDown, ChevronUp 
} from 'lucide-react';
import { Button } from './components/ui/button';
import { Input } from './components/ui/input';
import { Label } from './components/ui/label';
import { Badge } from './components/ui/badge';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export function ProductImportPanel({ onProductsAdded }) {
  const [mode, setMode] = useState(null); // 'excel' | 'url' | null
  const [loading, setLoading] = useState(false);
  const [preview, setPreview] = useState(null);
  const [scrapeUrl, setScrapeUrl] = useState('');
  const [editingProducts, setEditingProducts] = useState([]);
  const fileInputRef = useRef(null);

  const handleExcelUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post(`${API}/ai/import-products`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setEditingProducts(res.data.products);
      setPreview({
        mapping: res.data.column_mapping,
        headers: res.data.raw_headers,
        total: res.data.total_rows,
      });
      toast.success(`${res.data.products.length} producten herkend uit ${file.name}`);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Fout bij importeren');
    } finally {
      setLoading(false);
    }
  };

  const handleScrape = async () => {
    if (!scrapeUrl.trim()) return;
    setLoading(true);

    try {
      const res = await axios.post(`${API}/ai/scrape-products`, { url: scrapeUrl });
      setEditingProducts(res.data.products.map(p => ({
        name: p.name,
        category: p.category,
        description: p.description,
        price_purchase: p.price,
        price_lease_monthly: 0,
        installation_cost: 0,
        maintenance_yearly: 0,
        dimensions_width: p.dimensions_width,
        dimensions_height: p.dimensions_height,
        confidence: 0.8,
      })));
      setPreview({ source: res.data.page_title, total: res.data.products.length });
      toast.success(`${res.data.products.length} producten gevonden op ${res.data.page_title}`);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Kon pagina niet scrapen');
    } finally {
      setLoading(false);
    }
  };

  const confirmImport = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API}/ai/import-products/confirm`, {
        products: editingProducts,
      });
      toast.success(`${res.data.saved} producten opgeslagen!`);
      setEditingProducts([]);
      setPreview(null);
      setMode(null);
      if (onProductsAdded) onProductsAdded();
    } catch (err) {
      toast.error('Fout bij opslaan');
    } finally {
      setLoading(false);
    }
  };

  const removeProduct = (index) => {
    setEditingProducts(prev => prev.filter((_, i) => i !== index));
  };

  const updateProduct = (index, field, value) => {
    setEditingProducts(prev => prev.map((p, i) => 
      i === index ? { ...p, [field]: value } : p
    ));
  };

  // Show preview/edit list
  if (editingProducts.length > 0) {
    return (
      <div className="space-y-3" data-testid="import-preview">
        <div className="flex items-center justify-between">
          <h4 className="font-bold text-sm text-[#333333]">
            {editingProducts.length} producten gevonden
          </h4>
          <Button variant="ghost" size="sm" onClick={() => { setEditingProducts([]); setPreview(null); setMode(null); }}>
            <X size={14} className="mr-1" /> Annuleren
          </Button>
        </div>

        <div className="space-y-2 max-h-[400px] overflow-y-auto">
          {editingProducts.map((p, i) => (
            <div key={i} className="p-2.5 bg-white border border-[#e5e2d9] rounded-lg" data-testid={`import-product-${i}`}>
              <div className="flex items-start justify-between gap-2">
                <div className="flex-1 min-w-0">
                  <input
                    className="font-semibold text-sm text-[#333333] bg-transparent border-none p-0 w-full focus:outline-none focus:ring-0"
                    value={p.name}
                    onChange={(e) => updateProduct(i, 'name', e.target.value)}
                  />
                  <div className="flex gap-2 mt-1 flex-wrap">
                    <select
                      className="text-xs bg-[#FDF9ED] border border-[#e5e2d9] rounded px-1.5 py-0.5"
                      value={p.category}
                      onChange={(e) => updateProduct(i, 'category', e.target.value)}
                    >
                      {['sanitair','slagboom','camera','wifi','verlichting','betaalsysteem','toegangscontrole','douchelezer','energie','overig'].map(c => (
                        <option key={c} value={c}>{c}</option>
                      ))}
                    </select>
                    <input
                      className="text-xs w-20 bg-[#FDF9ED] border border-[#e5e2d9] rounded px-1.5 py-0.5"
                      type="number"
                      placeholder="Prijs"
                      value={p.price_purchase || ''}
                      onChange={(e) => updateProduct(i, 'price_purchase', parseFloat(e.target.value) || 0)}
                    />
                    <input
                      className="text-xs w-14 bg-[#FDF9ED] border border-[#e5e2d9] rounded px-1.5 py-0.5"
                      type="number"
                      step="0.5"
                      placeholder="B(m)"
                      value={p.dimensions_width || ''}
                      onChange={(e) => updateProduct(i, 'dimensions_width', parseFloat(e.target.value) || 1)}
                    />
                    <span className="text-xs text-[#777777]">x</span>
                    <input
                      className="text-xs w-14 bg-[#FDF9ED] border border-[#e5e2d9] rounded px-1.5 py-0.5"
                      type="number"
                      step="0.5"
                      placeholder="L(m)"
                      value={p.dimensions_height || ''}
                      onChange={(e) => updateProduct(i, 'dimensions_height', parseFloat(e.target.value) || 1)}
                    />
                  </div>
                </div>
                <Button variant="ghost" size="icon" className="w-6 h-6 text-red-400 hover:text-red-600 flex-shrink-0" onClick={() => removeProduct(i)}>
                  <X size={12} />
                </Button>
              </div>
            </div>
          ))}
        </div>

        <Button 
          onClick={confirmImport} 
          disabled={loading || editingProducts.length === 0}
          className="w-full bg-[#70C26C] hover:bg-[#5fb35b] text-white font-semibold"
          data-testid="confirm-import-btn"
        >
          {loading ? <Loader2 size={16} className="mr-2 animate-spin" /> : <Check size={16} className="mr-2" />}
          {editingProducts.length} producten importeren
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-2" data-testid="import-panel">
      <Label className="text-sm font-medium text-[#333333]">Producten importeren</Label>
      
      <div className="grid grid-cols-2 gap-2">
        <button
          onClick={() => { setMode('excel'); fileInputRef.current?.click(); }}
          disabled={loading}
          className={`p-3 rounded-xl border-2 text-center transition-all bg-white ${
            mode === 'excel' ? 'border-[#70C26C] bg-[#70C26C]/5' : 'border-[#e5e2d9] hover:border-[#70C26C]/50'
          }`}
          data-testid="import-excel-btn"
        >
          <FileSpreadsheet size={20} className="mx-auto text-[#70C26C] mb-1" />
          <span className="text-xs font-medium text-[#333333]">Excel/CSV</span>
        </button>
        <button
          onClick={() => setMode('url')}
          disabled={loading}
          className={`p-3 rounded-xl border-2 text-center transition-all bg-white ${
            mode === 'url' ? 'border-[#70C26C] bg-[#70C26C]/5' : 'border-[#e5e2d9] hover:border-[#70C26C]/50'
          }`}
          data-testid="import-url-btn"
        >
          <Globe size={20} className="mx-auto text-[#2563eb] mb-1" />
          <span className="text-xs font-medium text-[#333333]">Website URL</span>
        </button>
      </div>

      <input ref={fileInputRef} type="file" accept=".xlsx,.xls,.csv" onChange={handleExcelUpload} className="hidden" />
      
      {mode === 'url' && (
        <div className="flex gap-2">
          <Input
            placeholder="https://leverancier.nl/producten"
            value={scrapeUrl}
            onChange={(e) => setScrapeUrl(e.target.value)}
            className="bg-white border-[#e5e2d9] text-sm"
            data-testid="scrape-url-input"
          />
          <Button
            onClick={handleScrape}
            disabled={loading || !scrapeUrl.trim()}
            className="bg-[#70C26C] hover:bg-[#5fb35b] text-white px-3 flex-shrink-0"
            data-testid="scrape-btn"
          >
            {loading ? <Loader2 size={16} className="animate-spin" /> : <Globe size={16} />}
          </Button>
        </div>
      )}

      {loading && (
        <div className="flex items-center gap-2 p-3 bg-[#70C26C]/10 rounded-lg">
          <Loader2 size={16} className="animate-spin text-[#70C26C]" />
          <span className="text-xs text-[#333333]">AI analyseert{mode === 'excel' ? ' bestand' : ' website'}...</span>
        </div>
      )}
    </div>
  );
}
