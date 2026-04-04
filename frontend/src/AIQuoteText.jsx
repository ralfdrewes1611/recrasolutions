import React, { useState } from 'react';
import { toast } from 'sonner';
import axios from 'axios';
import { Sparkles, Loader2, FileText } from 'lucide-react';
import { Button } from './components/ui/button';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export function AIQuoteText({ project, products, quickQuote }) {
  const [quoteText, setQuoteText] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateQuoteText = async () => {
    setLoading(true);
    try {
      const productList = project.placed_products.map(pp => {
        const p = products.find(prod => prod.id === pp.product_id);
        return p ? { name: p.name, quantity: pp.quantity, price: p.price_purchase } : null;
      }).filter(Boolean);

      const res = await axios.post(`${API}/ai/generate-quote-text`, {
        project_name: project.name,
        project_type: project.project_type,
        num_spots: project.num_spots,
        products: productList,
        total_investment: quickQuote.capex + quickQuote.install,
        lease_monthly: quickQuote.opex,
      });

      setQuoteText(res.data);
      toast.success('Offertetekst gegenereerd');
    } catch (err) {
      toast.error('Kon offertetekst niet genereren');
    } finally {
      setLoading(false);
    }
  };

  if (quoteText) {
    return (
      <div className="p-4 rounded-xl bg-white border border-[#e5e2d9] space-y-3" data-testid="quote-text-section">
        <div className="flex items-center gap-2">
          <FileText size={16} className="text-[#70C26C]" />
          <h3 className="font-bold text-sm text-[#333333]">AI Offertetekst</h3>
        </div>
        <div className="text-sm text-[#333333] space-y-2 leading-relaxed">
          <p className="font-medium">{quoteText.intro}</p>
          <div className="whitespace-pre-line">{quoteText.body}</div>
          <p className="italic text-[#777777]">{quoteText.closing}</p>
        </div>
        <Button 
          variant="ghost" 
          size="sm" 
          onClick={generateQuoteText} 
          className="text-[#70C26C] text-xs"
          disabled={loading}
        >
          <Sparkles size={12} className="mr-1" /> Opnieuw genereren
        </Button>
      </div>
    );
  }

  return (
    <Button
      onClick={generateQuoteText}
      disabled={loading || project.placed_products.length === 0}
      variant="outline"
      className="w-full border-[#70C26C] text-[#70C26C] hover:bg-[#70C26C]/10"
      data-testid="generate-quote-text-btn"
    >
      {loading ? (
        <><Loader2 size={16} className="mr-2 animate-spin" /> AI schrijft offerte...</>
      ) : (
        <><Sparkles size={16} className="mr-2" /> AI offertetekst genereren</>
      )}
    </Button>
  );
}
