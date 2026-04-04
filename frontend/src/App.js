import React, { useState, useEffect, useRef, useCallback } from 'react';
import axios from 'axios';
import { Toaster, toast } from 'sonner';
import { 
  ChevronRight, ChevronLeft, Upload, Grid3X3, Package, 
  Sparkles, FileText, Download, Plus, Trash2, Bath, Camera, 
  Wifi, Lightbulb, CreditCard, Key, ArrowRight, Zap, Check, 
  AlertTriangle, Info, X, RotateCw, FolderOpen, Save, Menu,
  Settings, HelpCircle, Phone, Mail, MapPin, Clock, Users,
  Shield, Droplets, PenTool, MousePointer, Undo, Redo,
  ZoomIn, ZoomOut, Maximize2, Layers, Eye, EyeOff
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
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from './components/ui/dialog';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from './components/ui/dropdown-menu';

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
  douchelezer: Droplets,
};

const categoryColors = {
  sanitair: '#4a9b7f',
  slagboom: '#f59e0b',
  camera: '#ef4444',
  wifi: '#3b82f6',
  verlichting: '#eab308',
  betaalsysteem: '#8b5cf6',
  toegangscontrole: '#ec4899',
  douchelezer: '#06b6d4',
};

const categoryLabels = {
  sanitair: 'Sanitair Units',
  slagboom: 'Slagbomen',
  camera: "Camera's",
  wifi: 'WiFi Systemen',
  verlichting: 'Verlichting',
  betaalsysteem: 'Betaalsystemen',
  toegangscontrole: 'Toegangscontrole',
  douchelezer: 'Douchelezers',
};

const projectTypes = [
  { value: 'camperplaats', label: 'Camperplaats', icon: '🚐', description: 'Specifiek voor campers en motorhomes' },
  { value: 'camping', label: 'Camping', icon: '⛺', description: 'Traditionele camping met diverse accommodaties' },
  { value: 'resort', label: 'Resort', icon: '🏨', description: 'Premium verblijfsaccommodatie' },
  { value: 'jachthaven', label: 'Jachthaven', icon: '⛵', description: 'Havens en watersportfaciliteiten' },
];

const WIZARD_STEPS = [
  { id: 1, title: 'Project', description: 'Basisgegevens', icon: Package },
  { id: 2, title: 'Terrein', description: 'Plattegrond & Zones', icon: MapPin },
  { id: 3, title: 'Producten', description: 'Configureren', icon: Settings },
  { id: 4, title: 'Offerte', description: 'Afronden', icon: FileText },
];

const CANVAS_TOOLS = [
  { id: 'select', icon: MousePointer, label: 'Selecteren' },
  { id: 'zone', icon: PenTool, label: 'Zone tekenen' },
];

function App() {
  // Core state
  const [currentStep, setCurrentStep] = useState(1);
  const [products, setProducts] = useState([]);
  const [projects, setProjects] = useState([]);
  const [project, setProject] = useState({
    id: null,
    name: 'Nieuw Project',
    project_type: 'camping',
    floor_plan_base64: null,
    scale_meters_per_pixel: 0.1,
    canvas_width: 1000,
    canvas_height: 700,
    placed_products: [],
    zones: [],
    num_spots: 30,
  });
  
  // UI state
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [quote, setQuote] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [draggedProduct, setDraggedProduct] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showProjectList, setShowProjectList] = useState(false);
  const [canvasTool, setCanvasTool] = useState('select');
  const [isDrawingZone, setIsDrawingZone] = useState(false);
  const [currentZonePoints, setCurrentZonePoints] = useState([]);
  const [showCoverage, setShowCoverage] = useState(true);
  const [sidebarTab, setSidebarTab] = useState('products');

  const canvasRef = useRef(null);
  const fileInputRef = useRef(null);

  // Fetch data on mount
  useEffect(() => {
    fetchProducts();
    fetchProjects();
  }, []);

  // Update quote and recommendations when products change
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

  const fetchProjects = async () => {
    try {
      const response = await axios.get(`${API}/projects`);
      setProjects(response.data);
    } catch (error) {
      console.error('Error fetching projects:', error);
    }
  };

  const saveProject = async () => {
    try {
      setLoading(true);
      let savedProject;
      if (project.id) {
        const response = await axios.put(`${API}/projects/${project.id}`, project);
        savedProject = response.data;
      } else {
        const response = await axios.post(`${API}/projects`, project);
        savedProject = response.data;
      }
      setProject(savedProject);
      fetchProjects();
      toast.success('Project opgeslagen');
      return savedProject;
    } catch (error) {
      console.error('Error saving project:', error);
      toast.error('Kon project niet opslaan');
      return null;
    } finally {
      setLoading(false);
    }
  };

  const loadProject = async (projectId) => {
    try {
      const response = await axios.get(`${API}/projects/${projectId}`);
      setProject(response.data);
      setShowProjectList(false);
      setCurrentStep(3);
      toast.success('Project geladen');
    } catch (error) {
      console.error('Error loading project:', error);
      toast.error('Kon project niet laden');
    }
  };

  const deleteProject = async (projectId) => {
    try {
      await axios.delete(`${API}/projects/${projectId}`);
      fetchProjects();
      if (project.id === projectId) {
        setProject({
          id: null,
          name: 'Nieuw Project',
          project_type: 'camping',
          floor_plan_base64: null,
          scale_meters_per_pixel: 0.1,
          canvas_width: 1000,
          canvas_height: 700,
          placed_products: [],
          zones: [],
          num_spots: 30,
        });
      }
      toast.success('Project verwijderd');
    } catch (error) {
      console.error('Error deleting project:', error);
      toast.error('Kon project niet verwijderen');
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
      
      setIsAnalyzing(true);
      try {
        const response = await axios.post(`${API}/ai/analyze-floorplan`, {
          image_base64: base64,
          project_type: project.project_type
        });
        
        if (response.data.estimated_spots) {
          setProject(prev => ({ ...prev, num_spots: response.data.estimated_spots }));
          toast.success(`AI heeft ${response.data.estimated_spots} standplaatsen gedetecteerd`);
        }
      } catch (error) {
        console.error('Error analyzing floor plan:', error);
      } finally {
        setIsAnalyzing(false);
      }
    };
    reader.readAsDataURL(file);
  };

  const handleCanvasClick = (e) => {
    if (canvasTool !== 'zone') return;
    
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    setCurrentZonePoints(prev => [...prev, { x, y }]);
    setIsDrawingZone(true);
  };

  const finishZone = () => {
    if (currentZonePoints.length < 3) {
      toast.error('Een zone moet minimaal 3 punten hebben');
      return;
    }
    
    const newZone = {
      id: `zone-${Date.now()}`,
      name: `Zone ${project.zones.length + 1}`,
      type: 'standplaats',
      points: currentZonePoints,
      color: '#4a9b7f',
    };
    
    setProject(prev => ({
      ...prev,
      zones: [...prev.zones, newZone],
    }));
    
    setCurrentZonePoints([]);
    setIsDrawingZone(false);
    setCanvasTool('select');
    toast.success('Zone toegevoegd');
  };

  const cancelZone = () => {
    setCurrentZonePoints([]);
    setIsDrawingZone(false);
  };

  const handleCanvasDrop = (e) => {
    e.preventDefault();
    if (!draggedProduct || canvasTool !== 'select') return;

    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

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
    toast.success(`${draggedProduct.name} geplaatst`);
  };

  const handleCanvasDragOver = (e) => {
    e.preventDefault();
  };

  const handleItemClick = (item) => {
    if (canvasTool !== 'select') return;
    setSelectedItem(selectedItem?.id === item.id ? null : item);
  };

  const removeItem = (itemId) => {
    setProject(prev => ({
      ...prev,
      placed_products: prev.placed_products.filter(p => p.id !== itemId),
    }));
    setSelectedItem(null);
    toast.success('Product verwijderd');
  };

  const removeZone = (zoneId) => {
    setProject(prev => ({
      ...prev,
      zones: prev.zones.filter(z => z.id !== zoneId),
    }));
    toast.success('Zone verwijderd');
  };

  const exportPDF = async () => {
    let projectToExport = project;
    
    if (!project.id) {
      const saved = await saveProject();
      if (!saved) return;
      projectToExport = saved;
    }

    try {
      setLoading(true);
      const response = await axios.post(`${API}/quote/pdf?project_id=${projectToExport.id}`);
      
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

  const getProductById = (productId) => products.find(p => p.id === productId);

  const filteredProducts = selectedCategory === 'all' 
    ? products 
    : products.filter(p => p.category === selectedCategory);

  const categories = [...new Set(products.map(p => p.category))];

  // Quick quote calculation
  const quickQuote = project.placed_products.reduce((acc, pp) => {
    const product = getProductById(pp.product_id);
    if (product) {
      acc.capex += product.price_purchase * pp.quantity;
      acc.opex += product.price_lease_monthly * pp.quantity;
      acc.install += product.installation_cost * pp.quantity;
      acc.maintenance += product.maintenance_yearly * pp.quantity;
    }
    return acc;
  }, { capex: 0, opex: 0, install: 0, maintenance: 0 });

  const newProject = () => {
    setProject({
      id: null,
      name: 'Nieuw Project',
      project_type: 'camping',
      floor_plan_base64: null,
      scale_meters_per_pixel: 0.1,
      canvas_width: 1000,
      canvas_height: 700,
      placed_products: [],
      zones: [],
      num_spots: 30,
    });
    setCurrentStep(1);
    setShowProjectList(false);
  };

  return (
    <TooltipProvider>
      <div className="h-screen w-full flex flex-col overflow-hidden bg-[#f8faf9]">
        {/* Header */}
        <header className="h-16 header-gradient flex items-center justify-between px-6 flex-shrink-0">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
                <Package className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-white font-bold text-lg tracking-tight">RECRA Solutions</h1>
                <p className="text-white/70 text-xs">Configurator Platform</p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Dialog open={showProjectList} onOpenChange={setShowProjectList}>
              <DialogTrigger asChild>
                <Button 
                  variant="ghost" 
                  className="text-white hover:bg-white/10"
                  data-testid="open-projects-btn"
                >
                  <FolderOpen size={18} className="mr-2" />
                  Projecten
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl bg-white">
                <DialogHeader>
                  <DialogTitle className="text-[#1e3a5f]">Mijn Projecten</DialogTitle>
                  <DialogDescription>
                    Selecteer een project om verder te werken of start een nieuw project.
                  </DialogDescription>
                </DialogHeader>
                <div className="py-4">
                  <Button 
                    onClick={newProject} 
                    className="w-full mb-4 btn-recra-primary"
                    data-testid="new-project-btn"
                  >
                    <Plus size={18} className="mr-2" />
                    Nieuw Project
                  </Button>
                  <ScrollArea className="h-[300px]">
                    <div className="space-y-2">
                      {projects.map((p) => (
                        <div
                          key={p.id}
                          className={`project-card flex items-center justify-between ${
                            project.id === p.id ? 'active' : ''
                          }`}
                          data-testid={`project-item-${p.id}`}
                        >
                          <div 
                            className="flex-1 cursor-pointer"
                            onClick={() => loadProject(p.id)}
                          >
                            <h4 className="font-medium text-[#1e3a5f]">{p.name}</h4>
                            <p className="text-sm text-gray-500">
                              {p.project_type} • {p.placed_products?.length || 0} producten
                            </p>
                          </div>
                          <Button
                            variant="ghost"
                            size="icon"
                            className="text-gray-400 hover:text-red-500"
                            onClick={(e) => {
                              e.stopPropagation();
                              deleteProject(p.id);
                            }}
                          >
                            <Trash2 size={16} />
                          </Button>
                        </div>
                      ))}
                      {projects.length === 0 && (
                        <div className="text-center py-8 text-gray-400">
                          <FolderOpen size={48} className="mx-auto mb-2 opacity-50" />
                          <p>Nog geen projecten</p>
                        </div>
                      )}
                    </div>
                  </ScrollArea>
                </div>
              </DialogContent>
            </Dialog>

            <Button 
              variant="ghost" 
              className="text-white hover:bg-white/10"
              onClick={saveProject}
              disabled={loading}
              data-testid="save-project-header-btn"
            >
              <Save size={18} className="mr-2" />
              Opslaan
            </Button>

            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="text-white hover:bg-white/10">
                  <HelpCircle size={20} />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="bg-white">
                <DropdownMenuItem>
                  <Phone size={16} className="mr-2" />
                  +31 634200253
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <Mail size={16} className="mr-2" />
                  info@recrasolutions.com
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem>
                  <HelpCircle size={16} className="mr-2" />
                  Handleiding
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </header>

        {/* Main Content */}
        <div className="flex-1 flex overflow-hidden">
          {/* Left Sidebar */}
          <div className="w-80 flex-shrink-0 border-r border-gray-200 bg-white flex flex-col">
            {/* Wizard Steps */}
            <div className="p-4 border-b border-gray-100">
              <div className="space-y-1">
                {WIZARD_STEPS.map((step) => {
                  const Icon = step.icon;
                  const isActive = currentStep === step.id;
                  const isCompleted = currentStep > step.id;
                  
                  return (
                    <button
                      key={step.id}
                      onClick={() => setCurrentStep(step.id)}
                      className={`w-full flex items-center gap-3 p-3 rounded-lg transition-all ${
                        isActive 
                          ? 'bg-[#4a9b7f]/10 border border-[#4a9b7f]/30' 
                          : isCompleted
                            ? 'bg-green-50'
                            : 'hover:bg-gray-50'
                      }`}
                      data-testid={`wizard-step-${step.id}`}
                    >
                      <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                        isActive 
                          ? 'bg-[#4a9b7f] text-white' 
                          : isCompleted
                            ? 'bg-green-500 text-white'
                            : 'bg-gray-100 text-gray-400'
                      }`}>
                        {isCompleted ? <Check size={16} /> : <Icon size={16} />}
                      </div>
                      <div className="text-left">
                        <div className={`text-sm font-medium ${
                          isActive ? 'text-[#4a9b7f]' : isCompleted ? 'text-green-600' : 'text-gray-600'
                        }`}>
                          {step.title}
                        </div>
                        <div className="text-xs text-gray-400">{step.description}</div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Step Content */}
            <ScrollArea className="flex-1">
              <div className="p-4">
                {/* Step 1: Project Details */}
                {currentStep === 1 && (
                  <div className="space-y-5 animate-fade-in-up" data-testid="step-1-content">
                    <div>
                      <Label htmlFor="project-name" className="text-sm font-medium text-gray-700">
                        Projectnaam
                      </Label>
                      <Input
                        id="project-name"
                        value={project.name}
                        onChange={(e) => setProject(prev => ({ ...prev, name: e.target.value }))}
                        className="mt-1.5"
                        placeholder="Bijv. Camping De Zonnehoek"
                        data-testid="project-name-input"
                      />
                    </div>

                    <div>
                      <Label className="text-sm font-medium text-gray-700">Type locatie</Label>
                      <div className="mt-2 grid grid-cols-2 gap-2">
                        {projectTypes.map((type) => (
                          <button
                            key={type.value}
                            onClick={() => setProject(prev => ({ ...prev, project_type: type.value }))}
                            className={`p-3 rounded-xl border-2 text-left transition-all ${
                              project.project_type === type.value
                                ? 'border-[#4a9b7f] bg-[#4a9b7f]/5'
                                : 'border-gray-200 hover:border-[#4a9b7f]/50'
                            }`}
                            data-testid={`project-type-${type.value}`}
                          >
                            <span className="text-2xl">{type.icon}</span>
                            <div className="font-medium text-sm mt-1 text-gray-800">{type.label}</div>
                          </button>
                        ))}
                      </div>
                    </div>

                    <div>
                      <Label htmlFor="num-spots" className="text-sm font-medium text-gray-700">
                        Aantal standplaatsen
                      </Label>
                      <Input
                        id="num-spots"
                        type="number"
                        value={project.num_spots}
                        onChange={(e) => setProject(prev => ({ ...prev, num_spots: parseInt(e.target.value) || 0 }))}
                        className="mt-1.5"
                        min="1"
                        data-testid="num-spots-input"
                      />
                    </div>

                    <div className="p-4 rounded-xl bg-gradient-to-br from-[#4a9b7f]/10 to-[#4a9b7f]/5 border border-[#4a9b7f]/20">
                      <div className="flex items-start gap-3">
                        <div className="w-8 h-8 rounded-lg bg-[#4a9b7f]/20 flex items-center justify-center flex-shrink-0">
                          <Sparkles size={16} className="text-[#4a9b7f]" />
                        </div>
                        <div>
                          <h4 className="font-medium text-sm text-[#2d5a3d]">Slimme configuratie</h4>
                          <p className="text-xs text-gray-600 mt-1">
                            Onze AI helpt u met optimale productplaatsing en geeft advies op basis van uw terreininrichting.
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Step 2: Terrain */}
                {currentStep === 2 && (
                  <div className="space-y-5 animate-fade-in-up" data-testid="step-2-content">
                    <div>
                      <Label className="text-sm font-medium text-gray-700">Plattegrond uploaden</Label>
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
                            ? 'border-[#4a9b7f] bg-[#4a9b7f]/5'
                            : 'border-gray-300 hover:border-[#4a9b7f] bg-gray-50'
                        }`}
                        data-testid="upload-floor-plan-btn"
                      >
                        {isAnalyzing ? (
                          <div className="flex flex-col items-center gap-2">
                            <Sparkles className="w-10 h-10 text-[#4a9b7f] animate-pulse-soft" />
                            <span className="text-sm font-medium text-[#4a9b7f]">AI analyseert plattegrond...</span>
                          </div>
                        ) : project.floor_plan_base64 ? (
                          <div className="flex flex-col items-center gap-2">
                            <Check className="w-10 h-10 text-[#4a9b7f]" />
                            <span className="text-sm font-medium text-[#4a9b7f]">Plattegrond geladen</span>
                            <span className="text-xs text-gray-500">Klik om te wijzigen</span>
                          </div>
                        ) : (
                          <div className="flex flex-col items-center gap-2">
                            <Upload className="w-10 h-10 text-gray-400" />
                            <span className="text-sm font-medium text-gray-600">Upload uw plattegrond</span>
                            <span className="text-xs text-gray-400">PDF of afbeelding (max. 10MB)</span>
                          </div>
                        )}
                      </button>
                    </div>

                    <div>
                      <Label className="text-sm font-medium text-gray-700 mb-2 block">Zones</Label>
                      <p className="text-xs text-gray-500 mb-3">
                        Definieer zones op uw terrein voor betere AI-aanbevelingen.
                      </p>
                      
                      {project.zones.length > 0 ? (
                        <div className="space-y-2">
                          {project.zones.map((zone, index) => (
                            <div 
                              key={zone.id}
                              className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                            >
                              <div className="flex items-center gap-2">
                                <div 
                                  className="w-3 h-3 rounded-full"
                                  style={{ backgroundColor: zone.color }}
                                />
                                <span className="text-sm font-medium">{zone.name}</span>
                                <Badge variant="secondary" className="text-xs">
                                  {zone.type}
                                </Badge>
                              </div>
                              <Button
                                variant="ghost"
                                size="icon"
                                className="h-7 w-7 text-gray-400 hover:text-red-500"
                                onClick={() => removeZone(zone.id)}
                              >
                                <X size={14} />
                              </Button>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="text-center py-6 bg-gray-50 rounded-xl">
                          <Layers className="w-8 h-8 text-gray-300 mx-auto mb-2" />
                          <p className="text-sm text-gray-400">Nog geen zones gedefinieerd</p>
                          <p className="text-xs text-gray-400 mt-1">
                            Gebruik het zone-gereedschap op het canvas
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Step 3: Products */}
                {currentStep === 3 && (
                  <div className="space-y-4 animate-fade-in-up" data-testid="step-3-content">
                    <div>
                      <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                        <SelectTrigger className="w-full" data-testid="category-select">
                          <SelectValue placeholder="Alle categorieën" />
                        </SelectTrigger>
                        <SelectContent className="bg-white">
                          <SelectItem value="all">Alle categorieën</SelectItem>
                          {categories.map((cat) => (
                            <SelectItem key={cat} value={cat}>
                              {categoryLabels[cat] || cat}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-2">
                      {filteredProducts.map((product) => {
                        const Icon = categoryIcons[product.category] || Package;
                        const color = categoryColors[product.category] || '#4a9b7f';
                        
                        return (
                          <div
                            key={product.id}
                            draggable
                            onDragStart={() => setDraggedProduct(product)}
                            onDragEnd={() => setDraggedProduct(null)}
                            className="product-card bg-white border border-gray-200 rounded-xl p-3 cursor-grab active:cursor-grabbing"
                            data-testid={`product-card-${product.id}`}
                          >
                            <div className="flex items-start gap-3">
                              <div 
                                className="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0"
                                style={{ backgroundColor: `${color}15` }}
                              >
                                <Icon size={24} style={{ color }} />
                              </div>
                              <div className="flex-1 min-w-0">
                                <div className="font-semibold text-sm text-gray-800 truncate">
                                  {product.name}
                                </div>
                                <div className="text-xs text-gray-500 mt-0.5 line-clamp-2">
                                  {product.description}
                                </div>
                                <div className="flex items-center gap-2 mt-2">
                                  <span className="text-sm font-bold text-[#4a9b7f]">
                                    € {product.price_purchase.toLocaleString()}
                                  </span>
                                  <span className="text-xs text-gray-400">
                                    of € {product.price_lease_monthly}/mnd
                                  </span>
                                </div>
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>

                    <p className="text-xs text-gray-400 text-center pt-2">
                      Sleep producten naar het canvas om te plaatsen
                    </p>
                  </div>
                )}

                {/* Step 4: Quote */}
                {currentStep === 4 && (
                  <div className="space-y-5 animate-fade-in-up" data-testid="step-4-content">
                    <div className="card-recra p-5">
                      <h3 className="font-bold text-lg text-[#1e3a5f] mb-4">Investering</h3>
                      
                      <div className="space-y-3">
                        <div className="flex justify-between items-center">
                          <span className="text-gray-600">Aankoopkosten (CAPEX)</span>
                          <span className="font-bold text-[#4a9b7f]">
                            € {quickQuote.capex.toLocaleString()}
                          </span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-gray-600">Installatiekosten</span>
                          <span className="font-medium">€ {quickQuote.install.toLocaleString()}</span>
                        </div>
                        <div className="h-px bg-gray-200" />
                        <div className="flex justify-between items-center">
                          <span className="font-semibold text-[#1e3a5f]">Totaal investering</span>
                          <span className="text-xl font-bold text-[#4a9b7f]">
                            € {(quickQuote.capex + quickQuote.install).toLocaleString()}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="card-recra p-5">
                      <h3 className="font-bold text-lg text-[#1e3a5f] mb-4">Lease optie (OPEX)</h3>
                      <div className="space-y-3">
                        <div className="flex justify-between items-center">
                          <span className="text-gray-600">Per maand</span>
                          <span className="font-bold text-[#4a9b7f]">
                            € {quickQuote.opex.toLocaleString()}
                          </span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-gray-600">Per jaar</span>
                          <span className="font-medium">€ {(quickQuote.opex * 12).toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-gray-600">Onderhoud per jaar</span>
                          <span className="font-medium">€ {quickQuote.maintenance.toLocaleString()}</span>
                        </div>
                      </div>
                    </div>

                    <Button
                      onClick={exportPDF}
                      disabled={loading || project.placed_products.length === 0}
                      className="w-full btn-recra-primary h-12"
                      data-testid="export-pdf-button"
                    >
                      <Download size={18} className="mr-2" />
                      Offerte downloaden (PDF)
                    </Button>

                    <div className="text-center">
                      <p className="text-xs text-gray-500">
                        Of neem direct contact op voor persoonlijk advies
                      </p>
                      <a 
                        href="tel:+31634200253" 
                        className="text-sm font-medium text-[#4a9b7f] hover:underline"
                      >
                        +31 634200253
                      </a>
                    </div>
                  </div>
                )}
              </div>
            </ScrollArea>

            {/* Navigation */}
            <div className="p-4 border-t border-gray-100 flex gap-2">
              <Button
                variant="outline"
                onClick={() => setCurrentStep(prev => Math.max(1, prev - 1))}
                disabled={currentStep === 1}
                className="flex-1"
                data-testid="wizard-prev-button"
              >
                <ChevronLeft size={16} className="mr-1" />
                Vorige
              </Button>
              <Button
                onClick={async () => {
                  if (currentStep < 4) {
                    setCurrentStep(prev => prev + 1);
                    if (currentStep === 1 && !project.id) {
                      await saveProject();
                    }
                  }
                }}
                disabled={currentStep === 4}
                className="flex-1 btn-recra-primary"
                data-testid="wizard-next-button"
              >
                Volgende
                <ChevronRight size={16} className="ml-1" />
              </Button>
            </div>
          </div>

          {/* Main Canvas Area */}
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Canvas Toolbar */}
            <div className="h-12 bg-white border-b border-gray-200 flex items-center justify-between px-4">
              <div className="flex items-center gap-2">
                {CANVAS_TOOLS.map((tool) => {
                  const Icon = tool.icon;
                  return (
                    <Tooltip key={tool.id}>
                      <TooltipTrigger asChild>
                        <Button
                          variant={canvasTool === tool.id ? 'default' : 'ghost'}
                          size="sm"
                          onClick={() => setCanvasTool(tool.id)}
                          className={canvasTool === tool.id ? 'bg-[#4a9b7f] text-white' : ''}
                          data-testid={`tool-${tool.id}`}
                        >
                          <Icon size={16} />
                        </Button>
                      </TooltipTrigger>
                      <TooltipContent>{tool.label}</TooltipContent>
                    </Tooltip>
                  );
                })}
                
                {isDrawingZone && (
                  <>
                    <div className="h-6 w-px bg-gray-200 mx-2" />
                    <Button
                      size="sm"
                      onClick={finishZone}
                      className="bg-green-500 hover:bg-green-600 text-white"
                    >
                      <Check size={14} className="mr-1" />
                      Zone voltooien
                    </Button>
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={cancelZone}
                    >
                      <X size={14} className="mr-1" />
                      Annuleren
                    </Button>
                  </>
                )}
              </div>

              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-500">
                  {project.name} • {project.placed_products.length} producten
                </span>
                <div className="h-6 w-px bg-gray-200 mx-2" />
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setShowCoverage(!showCoverage)}
                      className={showCoverage ? 'text-[#4a9b7f]' : 'text-gray-400'}
                    >
                      {showCoverage ? <Eye size={16} /> : <EyeOff size={16} />}
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>
                    {showCoverage ? 'Verberg bereik' : 'Toon bereik'}
                  </TooltipContent>
                </Tooltip>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button variant="ghost" size="sm">
                      <Grid3X3 size={16} />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>Snap to grid (24px)</TooltipContent>
                </Tooltip>
              </div>
            </div>

            {/* Canvas */}
            <div className="flex-1 overflow-auto bg-gray-100 p-4">
              <div
                ref={canvasRef}
                className={`relative bg-white rounded-xl shadow-lg canvas-grid-pattern mx-auto ${
                  canvasTool === 'zone' ? 'cursor-crosshair' : ''
                }`}
                style={{ 
                  width: project.canvas_width, 
                  height: project.canvas_height,
                  minWidth: project.canvas_width,
                }}
                onClick={handleCanvasClick}
                onDrop={handleCanvasDrop}
                onDragOver={handleCanvasDragOver}
                data-testid="site-canvas"
              >
                {/* Floor plan background */}
                {project.floor_plan_base64 && (
                  <img
                    src={project.floor_plan_base64}
                    alt="Plattegrond"
                    className="absolute inset-0 w-full h-full object-contain opacity-50 pointer-events-none"
                  />
                )}

                {/* Zones SVG */}
                <svg className="absolute inset-0 w-full h-full pointer-events-none">
                  {project.zones.map((zone) => (
                    <polygon
                      key={zone.id}
                      className="zone-polygon"
                      points={zone.points.map(p => `${p.x},${p.y}`).join(' ')}
                      style={{ stroke: zone.color }}
                    />
                  ))}
                  {/* Current drawing zone */}
                  {currentZonePoints.length > 0 && (
                    <>
                      <polyline
                        points={currentZonePoints.map(p => `${p.x},${p.y}`).join(' ')}
                        fill="none"
                        stroke="#4a9b7f"
                        strokeWidth="2"
                        strokeDasharray="5,5"
                      />
                      {currentZonePoints.map((point, i) => (
                        <circle
                          key={i}
                          cx={point.x}
                          cy={point.y}
                          r="5"
                          fill="#4a9b7f"
                        />
                      ))}
                    </>
                  )}
                </svg>

                {/* Placed products */}
                {project.placed_products.map((placed) => {
                  const product = getProductById(placed.product_id);
                  if (!product) return null;
                  
                  const Icon = categoryIcons[product.category] || Package;
                  const color = categoryColors[product.category] || '#4a9b7f';
                  const isSelected = selectedItem?.id === placed.id;
                  
                  return (
                    <div
                      key={placed.id}
                      className={`canvas-item absolute ${isSelected ? 'selected' : ''}`}
                      style={{
                        left: placed.x,
                        top: placed.y,
                        transform: `rotate(${placed.rotation}deg)`,
                      }}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleItemClick(placed);
                      }}
                      data-testid={`placed-item-${placed.id}`}
                    >
                      {/* Coverage radius */}
                      {showCoverage && product.coverage_radius && (
                        <div
                          className="coverage-circle absolute rounded-full"
                          style={{
                            width: product.coverage_radius * 4,
                            height: product.coverage_radius * 4,
                            left: -(product.coverage_radius * 2) + 24,
                            top: -(product.coverage_radius * 2) + 24,
                            backgroundColor: color,
                            border: `2px dashed ${color}`,
                          }}
                        />
                      )}
                      
                      {/* Product icon */}
                      <div
                        className="w-12 h-12 rounded-xl flex items-center justify-center shadow-lg border-2 border-white"
                        style={{ 
                          backgroundColor: color,
                          boxShadow: isSelected ? `0 0 0 3px ${color}40` : undefined,
                        }}
                      >
                        <Icon size={24} className="text-white" />
                      </div>
                      
                      {/* Label */}
                      <div className="absolute top-14 left-1/2 -translate-x-1/2 whitespace-nowrap">
                        <span className="text-[11px] bg-white px-2 py-1 rounded shadow-sm text-gray-700 font-medium">
                          {product.name.split(' ')[0]}
                        </span>
                      </div>
                    </div>
                  );
                })}

                {/* Selected item controls */}
                {selectedItem && (
                  <div
                    className="absolute bg-white rounded-lg shadow-xl p-1 flex gap-1 border border-gray-200"
                    style={{
                      left: selectedItem.x + 60,
                      top: selectedItem.y - 8,
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
                          className="w-8 h-8 text-red-500 hover:text-red-600 hover:bg-red-50"
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
                {project.placed_products.length === 0 && !project.floor_plan_base64 && (
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="text-center max-w-sm p-8">
                      <div className="w-20 h-20 rounded-2xl bg-gray-100 flex items-center justify-center mx-auto mb-4">
                        <Package size={40} className="text-gray-300" />
                      </div>
                      <h3 className="font-semibold text-lg text-gray-700 mb-2">
                        Start met configureren
                      </h3>
                      <p className="text-sm text-gray-500">
                        Upload een plattegrond of sleep producten vanuit het linkerpaneel naar dit canvas om uw terrein in te richten.
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Right Sidebar */}
          <div className="w-80 flex-shrink-0 border-l border-gray-200 bg-white flex flex-col">
            <Tabs value={sidebarTab} onValueChange={setSidebarTab} className="flex flex-col h-full">
              <TabsList className="w-full p-1 bg-gray-50 rounded-none border-b border-gray-200 h-auto">
                <TabsTrigger 
                  value="quote" 
                  className="flex-1 py-2.5 data-[state=active]:bg-white data-[state=active]:shadow-sm"
                  data-testid="tab-quote"
                >
                  <FileText size={14} className="mr-1.5" />
                  Offerte
                </TabsTrigger>
                <TabsTrigger 
                  value="ai" 
                  className="flex-1 py-2.5 data-[state=active]:bg-white data-[state=active]:shadow-sm"
                  data-testid="tab-ai"
                >
                  <Sparkles size={14} className="mr-1.5" />
                  AI Advies
                </TabsTrigger>
              </TabsList>

              <TabsContent value="quote" className="flex-1 m-0 overflow-hidden">
                <ScrollArea className="h-full">
                  <div className="p-5 space-y-5">
                    <div>
                      <h2 className="font-bold text-lg text-[#1e3a5f]">Real-time Offerte</h2>
                      <p className="text-sm text-gray-500 mt-1">
                        Automatisch berekend op basis van uw configuratie
                      </p>
                    </div>
                    
                    {/* Summary cards */}
                    <div className="grid grid-cols-2 gap-3">
                      <div className="p-4 rounded-xl bg-gradient-to-br from-[#4a9b7f]/10 to-[#4a9b7f]/5 border border-[#4a9b7f]/20">
                        <div className="text-xs text-gray-500 mb-1">CAPEX</div>
                        <div className="text-xl font-bold text-[#4a9b7f]" data-testid="quote-capex">
                          € {quickQuote.capex.toLocaleString()}
                        </div>
                      </div>
                      <div className="p-4 rounded-xl bg-gradient-to-br from-[#1e3a5f]/10 to-[#1e3a5f]/5 border border-[#1e3a5f]/20">
                        <div className="text-xs text-gray-500 mb-1">OPEX/mnd</div>
                        <div className="text-xl font-bold text-[#1e3a5f]" data-testid="quote-opex">
                          € {quickQuote.opex.toLocaleString()}
                        </div>
                      </div>
                    </div>

                    {/* Product list */}
                    <div>
                      <h3 className="text-sm font-semibold text-gray-700 mb-3">Geplaatste producten</h3>
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
                              className="flex items-center justify-between p-3 rounded-xl bg-gray-50 border border-gray-100"
                            >
                              <div className="flex items-center gap-3">
                                <div
                                  className="w-10 h-10 rounded-lg flex items-center justify-center"
                                  style={{ backgroundColor: `${color}15` }}
                                >
                                  <Icon size={18} style={{ color }} />
                                </div>
                                <div>
                                  <div className="text-sm font-medium text-gray-800">{product.name}</div>
                                  <div className="text-xs text-gray-500">
                                    {count}x • € {(product.price_purchase * count).toLocaleString()}
                                  </div>
                                </div>
                              </div>
                            </div>
                          );
                        })}

                        {project.placed_products.length === 0 && (
                          <div className="text-center py-8 text-gray-400">
                            <Package size={32} className="mx-auto mb-2 opacity-50" />
                            <p className="text-sm">Nog geen producten geplaatst</p>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Total */}
                    <div className="p-4 rounded-xl bg-[#1e3a5f] text-white">
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-white/80">Totaal investering</span>
                        <span className="text-2xl font-bold" data-testid="quote-total">
                          € {(quickQuote.capex + quickQuote.install).toLocaleString()}
                        </span>
                      </div>
                      <div className="flex justify-between items-center text-sm text-white/60">
                        <span>Inclusief installatie</span>
                        <span>€ {quickQuote.install.toLocaleString()}</span>
                      </div>
                    </div>
                  </div>
                </ScrollArea>
              </TabsContent>

              <TabsContent value="ai" className="flex-1 m-0 overflow-hidden">
                <ScrollArea className="h-full">
                  <div className="p-5 space-y-4">
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#4a9b7f] to-[#2d5a3d] flex items-center justify-center">
                        <Sparkles className="text-white" size={16} />
                      </div>
                      <div>
                        <h2 className="font-bold text-lg text-[#1e3a5f]">AI Aanbevelingen</h2>
                        <p className="text-xs text-gray-500">Gebaseerd op uw configuratie</p>
                      </div>
                    </div>

                    <div className="space-y-3">
                      {recommendations.length > 0 ? (
                        recommendations.map((rec, index) => (
                          <div
                            key={index}
                            className={`rounded-xl border p-4 ${
                              rec.type === 'warning'
                                ? 'border-amber-200 bg-amber-50'
                                : rec.type === 'suggestion'
                                  ? 'border-blue-200 bg-blue-50'
                                  : 'border-green-200 bg-green-50'
                            }`}
                            data-testid={`ai-recommendation-${index}`}
                          >
                            <div className="flex items-start gap-3">
                              <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
                                rec.type === 'warning'
                                  ? 'bg-amber-100 text-amber-600'
                                  : rec.type === 'suggestion'
                                    ? 'bg-blue-100 text-blue-600'
                                    : 'bg-green-100 text-green-600'
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
                                <h4 className="font-semibold text-sm text-gray-800">{rec.title}</h4>
                                <p className="text-xs text-gray-600 mt-1">{rec.description}</p>
                                {rec.action && (
                                  <Button
                                    size="sm"
                                    variant="ghost"
                                    className="mt-2 h-7 text-xs text-[#4a9b7f] hover:text-[#4a9b7f] hover:bg-[#4a9b7f]/10 p-0"
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
                          <div className="w-16 h-16 rounded-2xl bg-gray-100 flex items-center justify-center mx-auto mb-3">
                            <Sparkles size={28} className="text-gray-300" />
                          </div>
                          <p className="text-sm text-gray-500">
                            Plaats producten om AI-aanbevelingen te ontvangen
                          </p>
                        </div>
                      )}
                    </div>

                    <Button
                      variant="outline"
                      className="w-full border-[#4a9b7f] text-[#4a9b7f] hover:bg-[#4a9b7f]/10"
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
        </div>

        <Toaster 
          theme="light" 
          position="bottom-right"
          toastOptions={{
            style: {
              background: '#fff',
              border: '1px solid #e5e7eb',
              color: '#1e3a5f',
            },
          }}
        />
      </div>
    </TooltipProvider>
  );
}

export default App;
