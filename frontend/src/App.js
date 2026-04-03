import React, { useState, useEffect, useCallback, useRef } from 'react';
import axios from 'axios';
import { Toaster, toast } from 'sonner';
import { 
  ChevronRight, ChevronLeft, Upload, Grid3X3, Package, 
  Sparkles, FileText, Download, Plus, Minus, Trash2,
  Bath, Camera, Wifi, Lightbulb, CreditCard, Key, 
  ArrowRight, Zap, Check, AlertTriangle, Info, X,
  Move, RotateCw, Maximize2
} from 'lucide-react';
import { Button } from './components/ui/button';
import { ScrollArea } from './components/ui/scroll-area';
import { Badge } from './components/ui/badge';
import { Tabs, TabsList, TabsTrigger, TabsContent } from './components/ui/tabs';
import { Input } from './components/ui/input';
import { Label } from './components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from './components/ui/select';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from './components/ui/tooltip';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Icon mapping for product categories
const categoryIcons = {
  sanitair: Bath,
  slagboom: ArrowRight,
  camera: Camera,
  wifi: Wifi,
  verlichting: Lightbulb,
  betaalsysteem: CreditCard,
  toegangscontrole: Key,
};

const categoryColors = {
  sanitair: '#0ea5e9',
  slagboom: '#f59e0b',
  camera: '#ef4444',
  wifi: '#10b981',
  verlichting: '#fbbf24',
  betaalsysteem: '#8b5cf6',
  toegangscontrole: '#ec4899',
};

const projectTypes = [
  { value: 'camperplaats', label: 'Camperplaats', description: 'Specifiek voor campers en motorhomes' },
  { value: 'camping', label: 'Camping', description: 'Traditionele camping met diverse accommodaties' },
  { value: 'resort', label: 'Resort', description: 'Premium verblijfsaccommodatie' },
  { value: 'tijdelijke_housing', label: 'Tijdelijke Housing', description: 'Re-Nest en flexibele huisvesting' },
];

const WIZARD_STEPS = [
  { id: 1, title: 'Project', icon: Package },
  { id: 2, title: 'Terrein', icon: Grid3X3 },
  { id: 3, title: 'Producten', icon: Zap },
  { id: 4, title: 'Offerte', icon: FileText },
];

function App() {
  // State
  const [currentStep, setCurrentStep] = useState(1);
  const [products, setProducts] = useState([]);
  const [project, setProject] = useState({
    id: null,
    name: 'Nieuw Project',
    project_type: 'camping',
    floor_plan_base64: null,
    scale_meters_per_pixel: 0.1,
    canvas_width: 800,
    canvas_height: 600,
    placed_products: [],
    zones: [],
    num_spots: 30,
  });
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [quote, setQuote] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [draggedProduct, setDraggedProduct] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const canvasRef = useRef(null);
  const fileInputRef = useRef(null);

  // Fetch products on mount
  useEffect(() => {
    fetchProducts();
  }, []);

  // Calculate quote when products change
  useEffect(() => {
    if (project.id && project.placed_products.length > 0) {
      calculateQuote();
      fetchRecommendations();
    }
  }, [project.placed_products, project.id]);

  const fetchProducts = async () => {
    try {
      const response = await axios.get(`${API}/products`);
      setProducts(response.data);
    } catch (error) {
      console.error('Error fetching products:', error);
      toast.error('Kon producten niet laden');
    }
  };

  const saveProject = async () => {
    try {
      setLoading(true);
      if (project.id) {
        const response = await axios.put(`${API}/projects/${project.id}`, project);
        setProject(response.data);
      } else {
        const response = await axios.post(`${API}/projects`, project);
        setProject(response.data);
      }
      toast.success('Project opgeslagen');
    } catch (error) {
      console.error('Error saving project:', error);
      toast.error('Kon project niet opslaan');
    } finally {
      setLoading(false);
    }
  };

  const calculateQuote = async () => {
    if (!project.id) return;
    try {
      const response = await axios.post(`${API}/quote/calculate?project_id=${project.id}`);
      setQuote(response.data);
    } catch (error) {
      console.error('Error calculating quote:', error);
    }
  };

  const fetchRecommendations = async () => {
    if (!project.id) return;
    try {
      const response = await axios.post(`${API}/ai/recommendations?project_id=${project.id}`);
      setRecommendations(response.data.recommendations || []);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (e) => {
      const base64 = e.target.result;
      setProject(prev => ({ ...prev, floor_plan_base64: base64 }));
      
      // Analyze with AI
      setIsAnalyzing(true);
      try {
        const response = await axios.post(`${API}/ai/analyze-floorplan`, {
          image_base64: base64,
          project_type: project.project_type
        });
        
        if (response.data.estimated_spots) {
          setProject(prev => ({ 
            ...prev, 
            num_spots: response.data.estimated_spots 
          }));
        }
        
        if (response.data.suggestions?.length > 0) {
          toast.success(response.data.suggestions[0]);
        }
      } catch (error) {
        console.error('Error analyzing floor plan:', error);
      } finally {
        setIsAnalyzing(false);
      }
    };
    reader.readAsDataURL(file);
  };

  const handleCanvasDrop = (e) => {
    e.preventDefault();
    if (!draggedProduct) return;

    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Snap to grid (24px)
    const snappedX = Math.round(x / 24) * 24;
    const snappedY = Math.round(y / 24) * 24;

    const newPlacedProduct = {
      id: `placed-${Date.now()}`,
      product_id: draggedProduct.id,
      x: snappedX,
      y: snappedY,
      rotation: 0,
      quantity: 1,
    };

    setProject(prev => ({
      ...prev,
      placed_products: [...prev.placed_products, newPlacedProduct],
    }));

    setDraggedProduct(null);
  };

  const handleCanvasDragOver = (e) => {
    e.preventDefault();
  };

  const handleItemClick = (item) => {
    setSelectedItem(selectedItem?.id === item.id ? null : item);
  };

  const removeItem = (itemId) => {
    setProject(prev => ({
      ...prev,
      placed_products: prev.placed_products.filter(p => p.id !== itemId),
    }));
    setSelectedItem(null);
  };

  const exportPDF = async () => {
    if (!project.id) {
      toast.error('Sla eerst het project op');
      return;
    }

    try {
      setLoading(true);
      const response = await axios.post(`${API}/quote/pdf?project_id=${project.id}`);
      
      // Open HTML in new window for printing
      const printWindow = window.open('', '_blank');
      printWindow.document.write(response.data.html);
      printWindow.document.close();
      printWindow.focus();
      setTimeout(() => printWindow.print(), 500);
      
      toast.success('PDF gegenereerd');
    } catch (error) {
      console.error('Error generating PDF:', error);
      toast.error('Kon PDF niet genereren');
    } finally {
      setLoading(false);
    }
  };

  const getProductById = (productId) => {
    return products.find(p => p.id === productId);
  };

  const filteredProducts = selectedCategory === 'all' 
    ? products 
    : products.filter(p => p.category === selectedCategory);

  const categories = [...new Set(products.map(p => p.category))];

  // Quick quote calculation from placed products
  const quickQuote = project.placed_products.reduce((acc, pp) => {
    const product = getProductById(pp.product_id);
    if (product) {
      acc.capex += product.price_purchase * pp.quantity;
      acc.opex += product.price_lease_monthly * pp.quantity;
      acc.install += product.installation_cost * pp.quantity;
    }
    return acc;
  }, { capex: 0, opex: 0, install: 0 });

  return (
    <TooltipProvider>
      <div className="h-screen w-full flex overflow-hidden bg-[#09090b] text-white font-['Manrope']">
        {/* Left Sidebar - Wizard & Products */}
        <div className="w-80 flex-shrink-0 border-r border-[#27272a] bg-[#09090b] flex flex-col z-20">
          {/* Logo */}
          <div className="p-6 border-b border-[#27272a]">
            <h1 className="font-['Outfit'] text-2xl font-semibold tracking-tight">
              <span className="text-[#0ea5e9]">RECRA</span>
              <span className="text-[#10b981]"> Solutions</span>
            </h1>
            <p className="text-sm text-[#71717a] mt-1">Configurator Platform</p>
          </div>

          {/* Wizard Steps */}
          <div className="p-4 border-b border-[#27272a]">
            <div className="flex items-center justify-between">
              {WIZARD_STEPS.map((step, index) => {
                const Icon = step.icon;
                const isActive = currentStep === step.id;
                const isCompleted = currentStep > step.id;
                
                return (
                  <React.Fragment key={step.id}>
                    <button
                      onClick={() => setCurrentStep(step.id)}
                      className={`flex flex-col items-center gap-1 transition-all ${
                        isActive 
                          ? 'text-[#0ea5e9]' 
                          : isCompleted 
                            ? 'text-[#10b981]' 
                            : 'text-[#71717a]'
                      }`}
                      data-testid={`wizard-step-${step.id}`}
                    >
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center transition-all ${
                        isActive 
                          ? 'bg-[#0ea5e9]/20 border border-[#0ea5e9]' 
                          : isCompleted
                            ? 'bg-[#10b981]/20 border border-[#10b981]'
                            : 'bg-[#18181b] border border-[#27272a]'
                      }`}>
                        {isCompleted ? <Check size={14} /> : <Icon size={14} />}
                      </div>
                      <span className="text-[10px] font-medium">{step.title}</span>
                    </button>
                    {index < WIZARD_STEPS.length - 1 && (
                      <div className={`flex-1 h-px mx-2 ${
                        currentStep > step.id ? 'bg-[#10b981]' : 'bg-[#27272a]'
                      }`} />
                    )}
                  </React.Fragment>
                );
              })}
            </div>
          </div>

          {/* Step Content */}
          <ScrollArea className="flex-1">
            <div className="p-4">
              {/* Step 1: Project Details */}
              {currentStep === 1 && (
                <div className="space-y-4 animate-slide-in" data-testid="step-1-content">
                  <div>
                    <Label htmlFor="project-name" className="text-[#a1a1aa] text-sm">
                      Projectnaam
                    </Label>
                    <Input
                      id="project-name"
                      value={project.name}
                      onChange={(e) => setProject(prev => ({ ...prev, name: e.target.value }))}
                      className="mt-1 bg-[#18181b] border-[#27272a] text-white"
                      placeholder="Bijv. Camping De Zonnehoek"
                      data-testid="project-name-input"
                    />
                  </div>

                  <div>
                    <Label className="text-[#a1a1aa] text-sm">Projecttype</Label>
                    <div className="mt-2 space-y-2">
                      {projectTypes.map((type) => (
                        <button
                          key={type.value}
                          onClick={() => setProject(prev => ({ ...prev, project_type: type.value }))}
                          className={`w-full p-3 rounded-lg border text-left transition-all ${
                            project.project_type === type.value
                              ? 'border-[#0ea5e9] bg-[#0ea5e9]/10'
                              : 'border-[#27272a] bg-[#18181b] hover:border-[#0ea5e9]/50'
                          }`}
                          data-testid={`project-type-${type.value}`}
                        >
                          <div className="font-medium text-sm">{type.label}</div>
                          <div className="text-xs text-[#71717a] mt-0.5">{type.description}</div>
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="num-spots" className="text-[#a1a1aa] text-sm">
                      Aantal standplaatsen
                    </Label>
                    <Input
                      id="num-spots"
                      type="number"
                      value={project.num_spots}
                      onChange={(e) => setProject(prev => ({ ...prev, num_spots: parseInt(e.target.value) || 0 }))}
                      className="mt-1 bg-[#18181b] border-[#27272a] text-white font-mono"
                      min="1"
                      data-testid="num-spots-input"
                    />
                  </div>
                </div>
              )}

              {/* Step 2: Terrain Upload */}
              {currentStep === 2 && (
                <div className="space-y-4 animate-slide-in" data-testid="step-2-content">
                  <div>
                    <Label className="text-[#a1a1aa] text-sm">Plattegrond uploaden</Label>
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept="image/*,.pdf"
                      onChange={handleFileUpload}
                      className="hidden"
                      data-testid="floor-plan-input"
                    />
                    <button
                      onClick={() => fileInputRef.current?.click()}
                      className={`mt-2 w-full p-8 rounded-xl border-2 border-dashed transition-all ${
                        project.floor_plan_base64
                          ? 'border-[#10b981] bg-[#10b981]/5'
                          : 'border-[#27272a] hover:border-[#0ea5e9] bg-[#18181b]'
                      }`}
                      data-testid="upload-floor-plan-btn"
                    >
                      {isAnalyzing ? (
                        <div className="flex flex-col items-center gap-2">
                          <Sparkles className="w-8 h-8 text-[#10b981] animate-pulse" />
                          <span className="text-sm text-[#10b981]">AI analyseert...</span>
                        </div>
                      ) : project.floor_plan_base64 ? (
                        <div className="flex flex-col items-center gap-2">
                          <Check className="w-8 h-8 text-[#10b981]" />
                          <span className="text-sm text-[#10b981]">Plattegrond geladen</span>
                          <span className="text-xs text-[#71717a]">Klik om te wijzigen</span>
                        </div>
                      ) : (
                        <div className="flex flex-col items-center gap-2">
                          <Upload className="w-8 h-8 text-[#71717a]" />
                          <span className="text-sm text-[#a1a1aa]">Upload plattegrond</span>
                          <span className="text-xs text-[#71717a]">PDF of afbeelding</span>
                        </div>
                      )}
                    </button>
                  </div>

                  <div>
                    <Label htmlFor="scale" className="text-[#a1a1aa] text-sm">
                      Schaal (meters per pixel)
                    </Label>
                    <Input
                      id="scale"
                      type="number"
                      step="0.01"
                      value={project.scale_meters_per_pixel}
                      onChange={(e) => setProject(prev => ({ 
                        ...prev, 
                        scale_meters_per_pixel: parseFloat(e.target.value) || 0.1 
                      }))}
                      className="mt-1 bg-[#18181b] border-[#27272a] text-white font-mono"
                      data-testid="scale-input"
                    />
                  </div>

                  <div className="p-4 rounded-lg bg-[#18181b] border border-[#27272a]">
                    <div className="flex items-center gap-2 text-[#10b981] mb-2">
                      <Sparkles size={16} />
                      <span className="text-sm font-medium">AI Tip</span>
                    </div>
                    <p className="text-xs text-[#a1a1aa]">
                      Upload een plattegrond en onze AI herkent automatisch zones en schat het aantal standplaatsen.
                    </p>
                  </div>
                </div>
              )}

              {/* Step 3: Product Selection */}
              {currentStep === 3 && (
                <div className="space-y-4 animate-slide-in" data-testid="step-3-content">
                  <div>
                    <Label className="text-[#a1a1aa] text-sm">Categorie</Label>
                    <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                      <SelectTrigger className="mt-1 bg-[#18181b] border-[#27272a]" data-testid="category-select">
                        <SelectValue placeholder="Alle categorieën" />
                      </SelectTrigger>
                      <SelectContent className="bg-[#18181b] border-[#27272a]">
                        <SelectItem value="all">Alle categorieën</SelectItem>
                        {categories.map((cat) => (
                          <SelectItem key={cat} value={cat}>
                            {cat.charAt(0).toUpperCase() + cat.slice(1)}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    {filteredProducts.map((product) => {
                      const Icon = categoryIcons[product.category] || Package;
                      const color = categoryColors[product.category] || '#0ea5e9';
                      
                      return (
                        <div
                          key={product.id}
                          draggable
                          onDragStart={() => setDraggedProduct(product)}
                          onDragEnd={() => setDraggedProduct(null)}
                          className="product-card bg-[#18181b] border border-[#27272a] rounded-lg p-3 cursor-grab active:cursor-grabbing"
                          data-testid={`product-card-${product.id}`}
                        >
                          <div className="flex items-start gap-3">
                            <div 
                              className="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0"
                              style={{ backgroundColor: `${color}20` }}
                            >
                              <Icon size={20} style={{ color }} />
                            </div>
                            <div className="flex-1 min-w-0">
                              <div className="font-medium text-sm truncate">{product.name}</div>
                              <div className="text-xs text-[#71717a] mt-0.5 line-clamp-2">{product.description}</div>
                              <div className="flex items-center gap-2 mt-2">
                                <Badge variant="secondary" className="text-xs bg-[#27272a] text-[#a1a1aa]">
                                  {product.category}
                                </Badge>
                                <span className="text-xs font-mono text-[#0ea5e9]">
                                  € {product.price_purchase.toLocaleString()}
                                </span>
                              </div>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  <p className="text-xs text-[#71717a] text-center">
                    Sleep producten naar de plattegrond
                  </p>
                </div>
              )}

              {/* Step 4: Quote */}
              {currentStep === 4 && (
                <div className="space-y-4 animate-slide-in" data-testid="step-4-content">
                  <div className="p-4 rounded-lg bg-[#18181b] border border-[#27272a]">
                    <h3 className="font-['Outfit'] font-semibold text-lg mb-4">Kostenoverzicht</h3>
                    
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-[#a1a1aa]">CAPEX (Aankoop)</span>
                        <span className="font-mono text-[#0ea5e9]">
                          € {quickQuote.capex.toLocaleString()}
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-[#a1a1aa]">Installatie</span>
                        <span className="font-mono">€ {quickQuote.install.toLocaleString()}</span>
                      </div>
                      <div className="h-px bg-[#27272a]" />
                      <div className="flex justify-between items-center">
                        <span className="font-medium">Totaal investering</span>
                        <span className="font-mono text-lg text-[#0ea5e9]">
                          € {(quickQuote.capex + quickQuote.install).toLocaleString()}
                        </span>
                      </div>
                    </div>

                    <div className="mt-4 pt-4 border-t border-[#27272a]">
                      <h4 className="text-sm text-[#a1a1aa] mb-2">OPEX (Lease)</h4>
                      <div className="flex justify-between items-center">
                        <span className="text-sm">Per maand</span>
                        <span className="font-mono text-[#10b981]">
                          € {quickQuote.opex.toLocaleString()}
                        </span>
                      </div>
                    </div>
                  </div>

                  <Button
                    onClick={exportPDF}
                    disabled={loading || project.placed_products.length === 0}
                    className="w-full bg-white text-[#09090b] hover:bg-gray-200 font-semibold"
                    data-testid="export-pdf-button"
                  >
                    <Download size={16} className="mr-2" />
                    Offerte downloaden (PDF)
                  </Button>

                  <Button
                    onClick={saveProject}
                    disabled={loading}
                    variant="outline"
                    className="w-full border-[#0ea5e9] text-[#0ea5e9] hover:bg-[#0ea5e9]/10"
                    data-testid="save-project-button"
                  >
                    Project opslaan
                  </Button>
                </div>
              )}
            </div>
          </ScrollArea>

          {/* Navigation */}
          <div className="p-4 border-t border-[#27272a] flex gap-2">
            <Button
              variant="outline"
              onClick={() => setCurrentStep(prev => Math.max(1, prev - 1))}
              disabled={currentStep === 1}
              className="flex-1 border-[#27272a]"
              data-testid="wizard-prev-button"
            >
              <ChevronLeft size={16} />
              Vorige
            </Button>
            <Button
              onClick={() => {
                if (currentStep < 4) {
                  setCurrentStep(prev => prev + 1);
                  if (!project.id) saveProject();
                }
              }}
              disabled={currentStep === 4}
              className="flex-1 bg-gradient-to-r from-[#0ea5e9] to-[#10b981] hover:shadow-[0_0_20px_rgba(14,165,233,0.4)]"
              data-testid="wizard-next-button"
            >
              Volgende
              <ChevronRight size={16} />
            </Button>
          </div>
        </div>

        {/* Main Canvas Area */}
        <div className="flex-1 relative overflow-hidden bg-[#09090b]">
          {/* Canvas Header */}
          <div className="absolute top-0 left-0 right-0 z-10 p-4 flex justify-between items-center">
            <div className="glass rounded-lg px-4 py-2 border border-white/5">
              <span className="text-sm text-[#a1a1aa]">
                {project.name} • {project.placed_products.length} items geplaatst
              </span>
            </div>
            <div className="flex gap-2">
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button variant="outline" size="icon" className="border-[#27272a] bg-[#18181b]">
                    <Grid3X3 size={16} />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>Snap to grid: 24px</TooltipContent>
              </Tooltip>
            </div>
          </div>

          {/* Canvas */}
          <div
            ref={canvasRef}
            className="w-full h-full canvas-dot-pattern relative"
            onDrop={handleCanvasDrop}
            onDragOver={handleCanvasDragOver}
            data-testid="site-canvas"
          >
            {/* Floor plan background */}
            {project.floor_plan_base64 && (
              <img
                src={project.floor_plan_base64}
                alt="Plattegrond"
                className="absolute inset-0 w-full h-full object-contain opacity-40"
              />
            )}

            {/* Placed products */}
            {project.placed_products.map((placed) => {
              const product = getProductById(placed.product_id);
              if (!product) return null;
              
              const Icon = categoryIcons[product.category] || Package;
              const color = categoryColors[product.category] || '#0ea5e9';
              const isSelected = selectedItem?.id === placed.id;
              
              return (
                <div
                  key={placed.id}
                  className={`canvas-item absolute cursor-pointer transition-all ${
                    isSelected ? 'selected' : ''
                  }`}
                  style={{
                    left: placed.x,
                    top: placed.y,
                    transform: `rotate(${placed.rotation}deg)`,
                  }}
                  onClick={() => handleItemClick(placed)}
                  data-testid={`placed-item-${placed.id}`}
                >
                  {/* Coverage radius */}
                  {product.coverage_radius && (
                    <div
                      className="coverage-circle absolute rounded-full"
                      style={{
                        width: product.coverage_radius * 4,
                        height: product.coverage_radius * 4,
                        left: -(product.coverage_radius * 2) + 20,
                        top: -(product.coverage_radius * 2) + 20,
                        backgroundColor: `${color}30`,
                        border: `1px dashed ${color}50`,
                      }}
                    />
                  )}
                  
                  {/* Product icon */}
                  <div
                    className="w-10 h-10 rounded-lg flex items-center justify-center shadow-lg"
                    style={{ 
                      backgroundColor: color,
                      boxShadow: isSelected ? `0 0 20px ${color}` : undefined,
                    }}
                  >
                    <Icon size={20} className="text-white" />
                  </div>
                  
                  {/* Label */}
                  <div className="absolute top-12 left-1/2 -translate-x-1/2 whitespace-nowrap">
                    <span className="text-[10px] bg-[#18181b]/90 px-2 py-0.5 rounded text-[#a1a1aa]">
                      {product.name.split(' ')[0]}
                    </span>
                  </div>
                </div>
              );
            })}

            {/* Selected item controls */}
            {selectedItem && (
              <div
                className="absolute glass rounded-lg p-2 flex gap-1 border border-white/10"
                style={{
                  left: selectedItem.x + 50,
                  top: selectedItem.y - 10,
                }}
              >
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="w-8 h-8"
                      onClick={() => {
                        setProject(prev => ({
                          ...prev,
                          placed_products: prev.placed_products.map(p =>
                            p.id === selectedItem.id
                              ? { ...p, rotation: (p.rotation + 45) % 360 }
                              : p
                          ),
                        }));
                      }}
                    >
                      <RotateCw size={14} />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>Roteren</TooltipContent>
                </Tooltip>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="w-8 h-8 text-red-400 hover:text-red-300 hover:bg-red-400/10"
                      onClick={() => removeItem(selectedItem.id)}
                    >
                      <Trash2 size={14} />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>Verwijderen</TooltipContent>
                </Tooltip>
              </div>
            )}

            {/* Empty state */}
            {project.placed_products.length === 0 && (
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center max-w-sm">
                  <div className="w-16 h-16 rounded-2xl bg-[#18181b] border border-[#27272a] flex items-center justify-center mx-auto mb-4">
                    <Package size={32} className="text-[#71717a]" />
                  </div>
                  <h3 className="font-['Outfit'] font-medium text-lg mb-2">Start met configureren</h3>
                  <p className="text-sm text-[#71717a]">
                    Sleep producten vanuit het linkerpaneel naar deze plattegrond om uw terrein in te richten.
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Right Sidebar - Quote & AI */}
        <div className="w-96 flex-shrink-0 border-l border-[#27272a] bg-[#09090b]/80 backdrop-blur-2xl flex flex-col z-20 shadow-2xl">
          <Tabs defaultValue="quote" className="flex flex-col h-full">
            <TabsList className="w-full p-1 bg-[#18181b] rounded-none border-b border-[#27272a]">
              <TabsTrigger 
                value="quote" 
                className="flex-1 data-[state=active]:bg-[#0ea5e9]/20 data-[state=active]:text-[#0ea5e9]"
                data-testid="tab-quote"
              >
                <FileText size={14} className="mr-2" />
                Offerte
              </TabsTrigger>
              <TabsTrigger 
                value="ai" 
                className="flex-1 data-[state=active]:bg-[#10b981]/20 data-[state=active]:text-[#10b981]"
                data-testid="tab-ai"
              >
                <Sparkles size={14} className="mr-2" />
                AI Advies
              </TabsTrigger>
            </TabsList>

            <TabsContent value="quote" className="flex-1 m-0 overflow-hidden">
              <ScrollArea className="h-full">
                <div className="p-6 space-y-4">
                  <h2 className="font-['Outfit'] font-semibold text-xl">Real-time Offerte</h2>
                  
                  {/* Summary cards */}
                  <div className="grid grid-cols-2 gap-3">
                    <div className="p-4 rounded-xl bg-[#18181b] border border-[#27272a]">
                      <div className="text-xs text-[#71717a] mb-1">CAPEX</div>
                      <div className="font-mono text-lg text-[#0ea5e9]" data-testid="quote-capex">
                        € {quickQuote.capex.toLocaleString()}
                      </div>
                    </div>
                    <div className="p-4 rounded-xl bg-[#18181b] border border-[#27272a]">
                      <div className="text-xs text-[#71717a] mb-1">OPEX/mnd</div>
                      <div className="font-mono text-lg text-[#10b981]" data-testid="quote-opex">
                        € {quickQuote.opex.toLocaleString()}
                      </div>
                    </div>
                  </div>

                  {/* Product list */}
                  <div>
                    <h3 className="text-sm font-medium text-[#a1a1aa] mb-3">Geplaatste producten</h3>
                    <div className="space-y-2">
                      {Object.entries(
                        project.placed_products.reduce((acc, pp) => {
                          const product = getProductById(pp.product_id);
                          if (product) {
                            if (!acc[pp.product_id]) {
                              acc[pp.product_id] = { product, count: 0 };
                            }
                            acc[pp.product_id].count += pp.quantity;
                          }
                          return acc;
                        }, {})
                      ).map(([productId, { product, count }]) => {
                        const Icon = categoryIcons[product.category] || Package;
                        const color = categoryColors[product.category];
                        
                        return (
                          <div
                            key={productId}
                            className="flex items-center justify-between p-3 rounded-lg bg-[#18181b] border border-[#27272a]"
                          >
                            <div className="flex items-center gap-3">
                              <div
                                className="w-8 h-8 rounded-md flex items-center justify-center"
                                style={{ backgroundColor: `${color}20` }}
                              >
                                <Icon size={16} style={{ color }} />
                              </div>
                              <div>
                                <div className="text-sm font-medium">{product.name}</div>
                                <div className="text-xs text-[#71717a]">
                                  {count}x • € {(product.price_purchase * count).toLocaleString()}
                                </div>
                              </div>
                            </div>
                          </div>
                        );
                      })}

                      {project.placed_products.length === 0 && (
                        <div className="text-center py-8 text-[#71717a] text-sm">
                          Nog geen producten geplaatst
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Total */}
                  <div className="p-4 rounded-xl bg-gradient-to-br from-[#0ea5e9]/10 to-[#10b981]/10 border border-[#0ea5e9]/20">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-[#a1a1aa]">Totaal investering</span>
                      <span className="font-mono text-xl text-[#0ea5e9]" data-testid="quote-total">
                        € {(quickQuote.capex + quickQuote.install).toLocaleString()}
                      </span>
                    </div>
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-[#71717a]">Incl. installatie</span>
                      <span className="font-mono text-[#71717a]">
                        € {quickQuote.install.toLocaleString()}
                      </span>
                    </div>
                  </div>
                </div>
              </ScrollArea>
            </TabsContent>

            <TabsContent value="ai" className="flex-1 m-0 overflow-hidden">
              <ScrollArea className="h-full">
                <div className="p-6 space-y-4">
                  <div className="flex items-center gap-2">
                    <Sparkles className="text-[#10b981]" size={20} />
                    <h2 className="font-['Outfit'] font-semibold text-xl">AI Aanbevelingen</h2>
                  </div>

                  <div className="space-y-3">
                    {recommendations.length > 0 ? (
                      recommendations.map((rec, index) => (
                        <div
                          key={index}
                          className={`relative overflow-hidden rounded-xl border p-4 ${
                            rec.type === 'warning'
                              ? 'border-[#f59e0b]/40 bg-gradient-to-b from-[#18181b] to-[#09090b]'
                              : rec.type === 'suggestion'
                                ? 'border-[#0ea5e9]/40 bg-gradient-to-b from-[#18181b] to-[#09090b]'
                                : 'border-[#10b981]/40 bg-gradient-to-b from-[#18181b] to-[#09090b]'
                          }`}
                          data-testid={`ai-recommendation-${index}`}
                        >
                          <div className="flex items-start gap-3">
                            <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
                              rec.type === 'warning'
                                ? 'bg-[#f59e0b]/20 text-[#f59e0b]'
                                : rec.type === 'suggestion'
                                  ? 'bg-[#0ea5e9]/20 text-[#0ea5e9]'
                                  : 'bg-[#10b981]/20 text-[#10b981]'
                            }`}>
                              {rec.type === 'warning' ? (
                                <AlertTriangle size={16} />
                              ) : rec.type === 'suggestion' ? (
                                <Info size={16} />
                              ) : (
                                <Zap size={16} />
                              )}
                            </div>
                            <div className="flex-1">
                              <h4 className="font-medium text-sm">{rec.title}</h4>
                              <p className="text-xs text-[#a1a1aa] mt-1">{rec.description}</p>
                              {rec.action && (
                                <Button
                                  size="sm"
                                  variant="ghost"
                                  className="mt-2 h-7 text-xs text-[#0ea5e9] hover:text-[#0ea5e9] hover:bg-[#0ea5e9]/10 p-0"
                                >
                                  {rec.action}
                                  <ChevronRight size={12} className="ml-1" />
                                </Button>
                              )}
                            </div>
                          </div>
                        </div>
                      ))
                    ) : (
                      <div className="text-center py-8">
                        <div className="w-12 h-12 rounded-xl bg-[#18181b] border border-[#27272a] flex items-center justify-center mx-auto mb-3">
                          <Sparkles size={24} className="text-[#71717a]" />
                        </div>
                        <p className="text-sm text-[#71717a]">
                          Plaats producten om AI-aanbevelingen te ontvangen
                        </p>
                      </div>
                    )}
                  </div>

                  <Button
                    variant="outline"
                    className="w-full border-[#10b981] text-[#10b981] hover:bg-[#10b981]/10"
                    onClick={fetchRecommendations}
                    disabled={!project.id}
                    data-testid="refresh-ai-button"
                  >
                    <Sparkles size={14} className="mr-2" />
                    Vernieuw aanbevelingen
                  </Button>
                </div>
              </ScrollArea>
            </TabsContent>
          </Tabs>
        </div>

        <Toaster 
          theme="dark" 
          position="bottom-right"
          toastOptions={{
            style: {
              background: '#18181b',
              border: '1px solid #27272a',
              color: '#fff',
            },
          }}
        />
      </div>
    </TooltipProvider>
  );
}

export default App;
