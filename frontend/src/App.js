import React, { useState, useEffect, useRef, useCallback } from 'react';
import axios from 'axios';
import { Toaster, toast } from 'sonner';
import { 
  ChevronRight, ChevronLeft, Upload, Grid3X3, Package, 
  Sparkles, FileText, Download, Plus, Trash2, Bath, Camera, 
  Wifi, Lightbulb, CreditCard, Key, ArrowRight, Zap, Check, 
  AlertTriangle, Info, X, RotateCw, FolderOpen, Save,
  Settings, HelpCircle, Phone, Mail, MapPin,
  Droplets, PenTool, MousePointer, Layers, Eye, EyeOff,
  BatteryCharging, Sun, Plug, ToggleLeft, ToggleRight,
  Car, TreePine, Tent, CircleDot, Grip, Move, Square
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
const CANVAS_SCALE = 10; // 10px per meter, dus 3m = 30px

// Category icons and colors
const categoryIcons = {
  sanitair: Bath,
  slagboom: ArrowRight,
  camera: Camera,
  wifi: Wifi,
  verlichting: Lightbulb,
  betaalsysteem: CreditCard,
  toegangscontrole: Key,
  douchelezer: Droplets,
  energie: BatteryCharging,
};

const categoryColors = {
  sanitair: '#70C26C',
  slagboom: '#d97706',
  camera: '#dc2626',
  wifi: '#2563eb',
  verlichting: '#ca8a04',
  betaalsysteem: '#7c3aed',
  toegangscontrole: '#db2777',
  douchelezer: '#0891b2',
  energie: '#059669',
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
  energie: 'Energie & Off-Grid',
};

const projectTypes = [
  { value: 'camperplaats', label: 'Camperplaats', icon: Car },
  { value: 'camping', label: 'Camping', icon: Tent },
  { value: 'resort', label: 'Resort', icon: TreePine },
  { value: 'jachthaven', label: 'Jachthaven', icon: MapPin },
];

const WIZARD_STEPS = [
  { id: 1, title: 'Project', description: 'Basisgegevens', icon: Package },
  { id: 2, title: 'Terrein', description: 'Plattegrond & AI Layout', icon: MapPin },
  { id: 3, title: 'Producten', description: 'Configureren', icon: Settings },
  { id: 4, title: 'Energie', description: 'Stroomvoorziening', icon: BatteryCharging },
  { id: 5, title: 'Offerte', description: 'Afronden', icon: FileText },
];

const ENERGY_MODES = [
  { id: 'grid', label: 'Netaansluiting', description: 'Volledig op het elektriciteitsnet', icon: Plug },
  { id: 'hybrid', label: 'Hybrid', description: 'Net + zonnepanelen + accu\'s', icon: Sun },
  { id: 'offgrid', label: 'Off-Grid', description: '100% zelfvoorzienend', icon: BatteryCharging },
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
    num_large_spots: 5,
    energy_mode: 'grid',
  });
  
  // UI state
  const [selectedCategory, setSelectedCategory] = useState('all');
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
  const [showRealProducts, setShowRealProducts] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);
  const [sanitairConfigs, setSanitairConfigs] = useState({});
  const [selectedProduct, setSelectedProduct] = useState(null); // click-to-place
  const [pointerDrag, setPointerDrag] = useState(null); // { product, x, y } for custom drag
  const [movingItem, setMovingItem] = useState(null); // { placedId, offsetX, offsetY } for repositioning
  const [viewMode, setViewMode] = useState('2d'); // 'icon' or '2d'

  const canvasRef = useRef(null);
  const fileInputRef = useRef(null);

  // Fetch data on mount
  useEffect(() => {
    fetchProducts();
    fetchProjects();
  }, []);

  // Update recommendations when products change
  useEffect(() => {
    if (project.id && project.placed_products.length > 0) {
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
        newProject();
      }
      toast.success('Project verwijderd');
    } catch (error) {
      console.error('Error deleting project:', error);
      toast.error('Kon project niet verwijderen');
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
      toast.success('Plattegrond geüpload');
    };
    reader.readAsDataURL(file);
  };

  const generateAILayout = async () => {
    setIsAnalyzing(true);
    try {
      toast.success(`Layout wordt gegenereerd voor ${project.num_spots} normale en ${project.num_large_spots} grote plekken...`);
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Schaal: 1px = 0.1m, dus 10px = 1m
      const scale = 10; // px per meter
      // Realistische afmetingen (in meters)
      const normalW = 8, normalH = 10;   // 80m² standplaats
      const largeW = 12, largeH = 15;    // 180m² comfort/XL
      const roadWidth = 5;               // 5m breed
      const gapX = 2, gapY = 2;          // 2m tussenruimte

      const spots = [];
      const cols = Math.min(5, Math.ceil(Math.sqrt(project.num_spots)));
      const startX = 80;  // ruimte voor weg links
      const startY = 80;  // ruimte voor weg boven

      // Rondrit weg (U-vorm rondom de standplaatsen)
      const totalNormalRows = Math.ceil(project.num_spots / cols);
      const blockW = cols * (normalW + gapX) * scale;
      const blockH = totalNormalRows * (normalH + gapY) * scale;
      const roadW = roadWidth * scale;

      const roadZones = [
        {
          id: `zone-road-top-${Date.now()}`,
          name: 'Hoofdweg',
          type: 'toegangsweg',
          points: [
            { x: startX - roadW, y: startY - roadW },
            { x: startX + blockW + roadW, y: startY - roadW },
            { x: startX + blockW + roadW, y: startY },
            { x: startX - roadW, y: startY },
          ],
          color: '#9ca3af',
        },
        {
          id: `zone-road-left-${Date.now()}`,
          name: 'Weg links',
          type: 'toegangsweg',
          points: [
            { x: startX - roadW, y: startY },
            { x: startX, y: startY },
            { x: startX, y: startY + blockH },
            { x: startX - roadW, y: startY + blockH },
          ],
          color: '#9ca3af',
        },
        {
          id: `zone-road-right-${Date.now()}`,
          name: 'Weg rechts',
          type: 'toegangsweg',
          points: [
            { x: startX + blockW, y: startY },
            { x: startX + blockW + roadW, y: startY },
            { x: startX + blockW + roadW, y: startY + blockH },
            { x: startX + blockW, y: startY + blockH },
          ],
          color: '#9ca3af',
        },
        {
          id: `zone-road-bottom-${Date.now()}`,
          name: 'Weg onder',
          type: 'toegangsweg',
          points: [
            { x: startX - roadW, y: startY + blockH },
            { x: startX + blockW + roadW, y: startY + blockH },
            { x: startX + blockW + roadW, y: startY + blockH + roadW },
            { x: startX - roadW, y: startY + blockH + roadW },
          ],
          color: '#9ca3af',
        },
      ];

      // Normale standplaatsen (8x10m = 80m²)
      for (let i = 0; i < project.num_spots; i++) {
        const row = Math.floor(i / cols);
        const col = i % cols;
        const px = startX + col * (normalW + gapX) * scale;
        const py = startY + row * (normalH + gapY) * scale;
        const pw = normalW * scale;
        const ph = normalH * scale;
        spots.push({
          id: `spot-${Date.now()}-${i}`,
          name: `Plek ${i + 1} (${normalW}x${normalH}m)`,
          type: 'standplaats',
          points: [
            { x: px, y: py },
            { x: px + pw, y: py },
            { x: px + pw, y: py + ph },
            { x: px, y: py + ph },
          ],
          color: '#70C26C',
        });
      }

      // Grote standplaatsen (12x15m = 180m²)
      const largeStartY = startY + blockH + roadW + gapY * scale;
      const largeCols = Math.min(3, project.num_large_spots);
      for (let i = 0; i < project.num_large_spots; i++) {
        const col = i % largeCols;
        const row = Math.floor(i / largeCols);
        const px = startX + col * (largeW + gapX) * scale;
        const py = largeStartY + row * (largeH + gapY) * scale;
        const pw = largeW * scale;
        const ph = largeH * scale;
        spots.push({
          id: `spot-large-${Date.now()}-${i}`,
          name: `XL Plek ${i + 1} (${largeW}x${largeH}m)`,
          type: 'grote_standplaats',
          points: [
            { x: px, y: py },
            { x: px + pw, y: py },
            { x: px + pw, y: py + ph },
            { x: px, y: py + ph },
          ],
          color: '#2563eb',
        });
      }

      // Canvas groter maken als nodig
      const maxX = Math.max(...[...roadZones, ...spots].flatMap(z => z.points.map(p => p.x))) + 60;
      const maxY = Math.max(...[...roadZones, ...spots].flatMap(z => z.points.map(p => p.y))) + 60;

      setProject(prev => ({
        ...prev,
        zones: [...roadZones, ...spots],
        canvas_width: Math.max(prev.canvas_width, maxX),
        canvas_height: Math.max(prev.canvas_height, maxY),
      }));

      toast.success(`Layout gegenereerd: ${project.num_spots} standplaatsen (${normalW}x${normalH}m) + ${project.num_large_spots} XL (${largeW}x${largeH}m) met rondrit`);
    } catch (error) {
      console.error('Error generating AI layout:', error);
      toast.error('Kon layout niet genereren');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleCanvasClick = (e) => {
    // Als we een item aan het verplaatsen zijn, negeer klik
    if (movingItem) return;

    // Click-to-place mode: als er een product geselecteerd is, plaats het
    if (selectedProduct && canvasTool === 'select') {
      const canvas = canvasRef.current;
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const snappedX = Math.round(x / 24) * 24;
      const snappedY = Math.round(y / 24) * 24;

      const newPlacedProduct = {
        id: `placed-${Date.now()}`,
        product_id: selectedProduct.id,
        x: snappedX,
        y: snappedY,
        rotation: 0,
        quantity: 1,
      };

      setProject(prev => ({
        ...prev,
        placed_products: [...prev.placed_products, newPlacedProduct],
      }));

      toast.success(`${selectedProduct.name} geplaatst`);
      setSelectedProduct(null); // Wis selectie na plaatsing
      return;
    }

    // Deselect placed item als we op lege canvas klikken
    if (canvasTool === 'select' && selectedItem) {
      setSelectedItem(null);
      return;
    }

    // Zone drawing mode
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
      color: '#70C26C',
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

  // Improved drag handlers
  const handleDragStart = (e, product) => {
    e.dataTransfer.setData('application/json', JSON.stringify(product));
    e.dataTransfer.effectAllowed = 'copy';
    setDraggedProduct(product);
  };

  const handleDragEnd = () => {
    setDraggedProduct(null);
  };

  const handleCanvasDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    let product = draggedProduct;
    if (!product) {
      try {
        const data = e.dataTransfer.getData('application/json');
        product = JSON.parse(data);
      } catch (err) {
        return;
      }
    }
    
    if (!product) return;

    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const snappedX = Math.round(x / 24) * 24;
    const snappedY = Math.round(y / 24) * 24;

    const newPlacedProduct = {
      id: `placed-${Date.now()}`,
      product_id: product.id,
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
    setIsDragOver(false);
    toast.success(`${product.name} geplaatst`);
  };

  const handleCanvasDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    e.dataTransfer.dropEffect = 'copy';
    if (!isDragOver) setIsDragOver(true);
  };

  const handleCanvasDragLeave = (e) => {
    e.preventDefault();
    if (!e.currentTarget.contains(e.relatedTarget)) {
      setIsDragOver(false);
    }
  };

  // Custom pointer-based drag (works in all browsers)
  const handlePointerDragStart = useCallback((e, product) => {
    e.preventDefault();
    setPointerDrag({ product, x: e.clientX, y: e.clientY });
    setSelectedProduct(null);
  }, []);

  useEffect(() => {
    if (!pointerDrag) return;
    
    const handleMove = (e) => {
      setPointerDrag(prev => prev ? { ...prev, x: e.clientX, y: e.clientY } : null);
    };
    const handleUp = (e) => {
      const canvas = canvasRef.current;
      if (canvas) {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        if (x >= 0 && y >= 0 && x <= rect.width && y <= rect.height) {
          const snappedX = Math.round(x / 24) * 24;
          const snappedY = Math.round(y / 24) * 24;
          const newPlaced = {
            id: `placed-${Date.now()}`,
            product_id: pointerDrag.product.id,
            x: snappedX,
            y: snappedY,
            rotation: 0,
            quantity: 1,
          };
          setProject(prev => ({
            ...prev,
            placed_products: [...prev.placed_products, newPlaced],
          }));
          toast.success(`${pointerDrag.product.name} geplaatst`);
        }
      }
      setPointerDrag(null);
    };
    
    document.addEventListener('mousemove', handleMove);
    document.addEventListener('mouseup', handleUp);
    return () => {
      document.removeEventListener('mousemove', handleMove);
      document.removeEventListener('mouseup', handleUp);
    };
  }, [pointerDrag]);

  // Move placed items by dragging them on the canvas
  const handlePlacedItemMouseDown = useCallback((e, placed) => {
    e.stopPropagation();
    e.preventDefault();
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    setMovingItem({
      placedId: placed.id,
      offsetX: e.clientX - rect.left - placed.x,
      offsetY: e.clientY - rect.top - placed.y,
    });
    setSelectedItem(placed);
    setSelectedProduct(null);
  }, []);

  useEffect(() => {
    if (!movingItem) return;
    
    const handleMove = (e) => {
      const canvas = canvasRef.current;
      if (!canvas) return;
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left - movingItem.offsetX;
      const y = e.clientY - rect.top - movingItem.offsetY;
      const snappedX = Math.round(x / 24) * 24;
      const snappedY = Math.round(y / 24) * 24;
      
      setProject(prev => ({
        ...prev,
        placed_products: prev.placed_products.map(p =>
          p.id === movingItem.placedId ? { ...p, x: Math.max(0, snappedX), y: Math.max(0, snappedY) } : p
        ),
      }));
    };
    const handleUp = () => {
      setMovingItem(null);
    };
    
    document.addEventListener('mousemove', handleMove);
    document.addEventListener('mouseup', handleUp);
    return () => {
      document.removeEventListener('mousemove', handleMove);
      document.removeEventListener('mouseup', handleUp);
    };
  }, [movingItem]);

  const handleItemClick = (item) => {
    if (canvasTool !== 'select') return;
    setSelectedItem(selectedItem?.id === item.id ? null : item);
  };

  // Get product dimensions in pixels for canvas rendering
  const getProductPxSize = (product) => {
    const dims = product.dimensions;
    if (!dims) return { w: 32, h: 32 };
    const w = Math.max(dims.width * CANVAS_SCALE, 24);
    const h = Math.max(dims.height * CANVAS_SCALE, 24);
    return { w, h };
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

  // Calculate power consumption
  const powerCalculation = project.placed_products.reduce((acc, pp) => {
    const product = getProductById(pp.product_id);
    if (product) {
      // Estimate power usage based on product type
      const powerUsage = {
        sanitair: 5000, // 5kW for hot water
        douchelezer: 100,
        camera: 15,
        wifi: 20,
        verlichting: 50,
        slagboom: 200,
        betaalsysteem: 50,
        toegangscontrole: 30,
      };
      acc.watts += (powerUsage[product.category] || 100) * pp.quantity;
    }
    return acc;
  }, { watts: 0 });

  // Quick quote calculation (includes sanitair config extras)
  const SANITAIR_EXTRAS = {
    extra_douches: { label: 'Extra douches', price: 2500, lease: 60 },
    familiecabine: { label: 'Familiecabine', price: 3000, lease: 72 },
    warmtepomp: { label: 'Warmtepomp', price: 4500, lease: 108 },
    zonneboiler: { label: 'Zonneboiler', price: 3500, lease: 84 },
  };

  const sanitairExtrasTotal = Object.entries(sanitairConfigs).reduce((acc, [placedId, config]) => {
    (config.extras || []).forEach(extraKey => {
      const extra = SANITAIR_EXTRAS[extraKey];
      if (extra) {
        acc.capex += extra.price;
        acc.lease += extra.lease;
      }
    });
    return acc;
  }, { capex: 0, lease: 0 });

  const quickQuote = project.placed_products.reduce((acc, pp) => {
    const product = getProductById(pp.product_id);
    if (product) {
      acc.capex += product.price_purchase * pp.quantity;
      acc.opex += product.price_lease_monthly * pp.quantity;
      acc.install += product.installation_cost * pp.quantity;
      acc.maintenance += product.maintenance_yearly * pp.quantity;
    }
    return acc;
  }, { capex: sanitairExtrasTotal.capex, opex: sanitairExtrasTotal.lease, install: 0, maintenance: 0 });

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
      num_large_spots: 5,
      energy_mode: 'grid',
    });
    setCurrentStep(1);
    setShowProjectList(false);
  };

  return (
    <TooltipProvider>
      <div className="h-screen w-full flex flex-col overflow-hidden bg-[#FDF9ED]">
        {/* Header */}
        <header className="h-16 bg-[#244628] flex items-center justify-between px-6 flex-shrink-0">
          <div className="flex items-center gap-4">
            <div className="flex flex-col items-center">
              <span className="text-white font-medium text-xl tracking-[0.3em]">RECRA</span>
              <span className="text-white/70 text-[10px] tracking-[0.15em]">— SOLUTIONS —</span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Dialog open={showProjectList} onOpenChange={setShowProjectList}>
              <DialogTrigger asChild>
                <Button variant="ghost" className="text-white/90 hover:text-white hover:bg-white/10" data-testid="open-projects-btn">
                  <FolderOpen size={18} className="mr-2" />
                  Projecten
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl bg-white border-[#e5e2d9]">
                <DialogHeader>
                  <DialogTitle className="text-[#333333]">Mijn Projecten</DialogTitle>
                  <DialogDescription className="text-[#777777]">
                    Selecteer een project om verder te werken of start een nieuw project.
                  </DialogDescription>
                </DialogHeader>
                <div className="py-4">
                  <Button onClick={newProject} className="w-full mb-4 bg-[#70C26C] hover:bg-[#5fb35b] text-white font-semibold" data-testid="new-project-btn">
                    <Plus size={18} className="mr-2" />
                    Nieuw Project
                  </Button>
                  <ScrollArea className="h-[300px]">
                    <div className="space-y-2">
                      {projects.map((p) => (
                        <div key={p.id} className={`flex items-center justify-between p-4 rounded-lg border cursor-pointer transition-all ${project.id === p.id ? 'border-[#70C26C] bg-[#70C26C]/5' : 'border-[#e5e2d9] hover:border-[#70C26C]'}`} data-testid={`project-item-${p.id}`}>
                          <div className="flex-1" onClick={() => loadProject(p.id)}>
                            <h4 className="font-medium text-[#333333]">{p.name}</h4>
                            <p className="text-sm text-[#777777]">{p.project_type} • {p.placed_products?.length || 0} producten</p>
                          </div>
                          <Button variant="ghost" size="icon" className="text-[#777777] hover:text-red-500" onClick={(e) => { e.stopPropagation(); deleteProject(p.id); }}>
                            <Trash2 size={16} />
                          </Button>
                        </div>
                      ))}
                      {projects.length === 0 && (
                        <div className="text-center py-8 text-[#777777]">
                          <FolderOpen size={48} className="mx-auto mb-2 opacity-50" />
                          <p>Nog geen projecten</p>
                        </div>
                      )}
                    </div>
                  </ScrollArea>
                </div>
              </DialogContent>
            </Dialog>

            <Button variant="ghost" className="text-white/90 hover:text-white hover:bg-white/10" onClick={saveProject} disabled={loading} data-testid="save-project-header-btn">
              <Save size={18} className="mr-2" />
              Opslaan
            </Button>

            <Button className="bg-[#70C26C] hover:bg-[#5fb35b] text-white font-medium">
              Contact
            </Button>

            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="text-white/90 hover:text-white hover:bg-white/10">
                  <HelpCircle size={20} />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="bg-white border-[#e5e2d9]">
                <DropdownMenuItem className="text-[#333333]">
                  <Phone size={16} className="mr-2" />
                  +31 634200253
                </DropdownMenuItem>
                <DropdownMenuItem className="text-[#333333]">
                  <Mail size={16} className="mr-2" />
                  info@recrasolutions.com
                </DropdownMenuItem>
                <DropdownMenuSeparator className="bg-[#e5e2d9]" />
                <DropdownMenuItem className="text-[#333333]">
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
          <div className="w-80 flex-shrink-0 border-r border-[#e5e2d9] bg-[#FFFEF8] flex flex-col">
            {/* Wizard Steps */}
            <div className="p-3 border-b border-[#e5e2d9]">
              <div className="space-y-1">
                {WIZARD_STEPS.map((step) => {
                  const Icon = step.icon;
                  const isActive = currentStep === step.id;
                  const isCompleted = currentStep > step.id;
                  
                  return (
                    <button
                      key={step.id}
                      onClick={() => setCurrentStep(step.id)}
                      className={`w-full flex items-center gap-3 p-2.5 rounded-lg transition-all ${
                        isActive ? 'bg-[#70C26C]/10 border border-[#70C26C]/30' : isCompleted ? 'bg-[#70C26C]/5' : 'hover:bg-[#FDF9ED]'
                      }`}
                      data-testid={`wizard-step-${step.id}`}
                    >
                      <div className={`w-7 h-7 rounded-lg flex items-center justify-center text-sm ${
                        isActive || isCompleted ? 'bg-[#70C26C] text-white' : 'bg-[#e5e2d9] text-[#777777]'
                      }`}>
                        {isCompleted ? <Check size={14} /> : <Icon size={14} />}
                      </div>
                      <div className="text-left">
                        <div className={`text-sm font-medium ${isActive || isCompleted ? 'text-[#70C26C]' : 'text-[#333333]'}`}>
                          {step.title}
                        </div>
                        <div className="text-xs text-[#777777]">{step.description}</div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Step Content - No ScrollArea to fix drag issues */}
            <div className="flex-1 overflow-y-auto p-4">
              {/* Step 1: Project Details */}
              {currentStep === 1 && (
                <div className="space-y-4" data-testid="step-1-content">
                  <div>
                    <Label htmlFor="project-name" className="text-sm font-medium text-[#333333]">Projectnaam</Label>
                    <Input
                      id="project-name"
                      value={project.name}
                      onChange={(e) => setProject(prev => ({ ...prev, name: e.target.value }))}
                      className="mt-1.5 bg-white border-[#e5e2d9]"
                      placeholder="Bijv. Camping De Zonnehoek"
                      data-testid="project-name-input"
                    />
                  </div>

                  <div>
                    <Label className="text-sm font-medium text-[#333333]">Type locatie</Label>
                    <div className="mt-2 grid grid-cols-2 gap-2">
                      {projectTypes.map((type) => {
                        const TypeIcon = type.icon;
                        return (
                          <button
                            key={type.value}
                            onClick={() => setProject(prev => ({ ...prev, project_type: type.value }))}
                            className={`p-3 rounded-xl border-2 text-left transition-all bg-white ${
                              project.project_type === type.value ? 'border-[#70C26C] bg-[#70C26C]/5' : 'border-[#e5e2d9] hover:border-[#70C26C]/50'
                            }`}
                            data-testid={`project-type-${type.value}`}
                          >
                            <TypeIcon size={24} className={project.project_type === type.value ? 'text-[#70C26C]' : 'text-[#777777]'} />
                            <div className="font-medium text-sm mt-1 text-[#333333]">{type.label}</div>
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <Label htmlFor="num-spots" className="text-sm font-medium text-[#333333]">Normale plekken</Label>
                      <Input
                        id="num-spots"
                        type="number"
                        value={project.num_spots}
                        onChange={(e) => setProject(prev => ({ ...prev, num_spots: parseInt(e.target.value) || 0 }))}
                        className="mt-1.5 bg-white border-[#e5e2d9]"
                        min="1"
                        data-testid="num-spots-input"
                      />
                    </div>
                    <div>
                      <Label htmlFor="num-large-spots" className="text-sm font-medium text-[#333333]">Grote plekken</Label>
                      <Input
                        id="num-large-spots"
                        type="number"
                        value={project.num_large_spots}
                        onChange={(e) => setProject(prev => ({ ...prev, num_large_spots: parseInt(e.target.value) || 0 }))}
                        className="mt-1.5 bg-white border-[#e5e2d9]"
                        min="0"
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* Step 2: Terrain & AI Layout */}
              {currentStep === 2 && (
                <div className="space-y-4" data-testid="step-2-content">
                  <div>
                    <Label className="text-sm font-medium text-[#333333]">Plattegrond uploaden</Label>
                    <input ref={fileInputRef} type="file" accept="image/*,.pdf" onChange={handleFileUpload} className="hidden" data-testid="floor-plan-input" />
                    <button
                      onClick={() => fileInputRef.current?.click()}
                      className={`mt-2 w-full p-6 rounded-xl border-2 border-dashed transition-all bg-white ${
                        project.floor_plan_base64 ? 'border-[#70C26C] bg-[#70C26C]/5' : 'border-[#e5e2d9] hover:border-[#70C26C]'
                      }`}
                      data-testid="upload-floor-plan-btn"
                    >
                      {project.floor_plan_base64 ? (
                        <div className="flex flex-col items-center gap-2">
                          <Check className="w-8 h-8 text-[#70C26C]" />
                          <span className="text-sm font-medium text-[#70C26C]">Plattegrond geladen</span>
                        </div>
                      ) : (
                        <div className="flex flex-col items-center gap-2">
                          <Upload className="w-8 h-8 text-[#777777]" />
                          <span className="text-sm font-medium text-[#333333]">Upload plattegrond</span>
                        </div>
                      )}
                    </button>
                  </div>


                  {project.floor_plan_base64 && (
                    <div className="p-3 rounded-xl bg-white border border-[#e5e2d9]" data-testid="scale-settings">
                      <Label className="text-sm font-medium text-[#333333] mb-2 block">Schaal instellen</Label>
                      <p className="text-xs text-[#777777] mb-2">Hoeveel meter is 1 blokje (24px) op de tekening?</p>
                      <div className="flex items-center gap-3">
                        <div className="flex items-center gap-1.5 flex-1">
                          <div className="w-6 h-6 border border-[#e5e2d9] bg-[#FDF9ED] rounded" />
                          <span className="text-sm text-[#333333]">=</span>
                          <Input
                            type="number"
                            step="0.5"
                            min="0.5"
                            max="20"
                            value={Math.round(project.scale_meters_per_pixel * 24 * 10) / 10}
                            onChange={(e) => {
                              const metersPerBlock = parseFloat(e.target.value) || 1;
                              setProject(prev => ({ ...prev, scale_meters_per_pixel: metersPerBlock / 24 }));
                            }}
                            className="w-20 bg-white border-[#e5e2d9] h-8 text-sm"
                            data-testid="scale-input"
                          />
                          <span className="text-sm text-[#777777]">meter</span>
                        </div>
                        <div className="text-xs text-[#777777] bg-[#FDF9ED] px-2 py-1 rounded">
                          Canvas: {Math.round(project.canvas_width * project.scale_meters_per_pixel)}x{Math.round(project.canvas_height * project.scale_meters_per_pixel)}m
                        </div>
                      </div>
                    </div>
                  )}
                  <div className="p-4 rounded-xl bg-[#70C26C]/10 border border-[#70C26C]/20">
                    <div className="flex items-center gap-2 mb-3">
                      <Sparkles size={18} className="text-[#70C26C]" />
                      <span className="font-medium text-[#244628]">AI Layout Generator</span>
                    </div>
                    <p className="text-xs text-[#777777] mb-3">
                      Laat AI automatisch standplaatsen suggereren met een rondrit-layout.
                    </p>
                    <Button
                      onClick={generateAILayout}
                      disabled={isAnalyzing}
                      className="w-full bg-[#70C26C] hover:bg-[#5fb35b] text-white"
                    >
                      {isAnalyzing ? (
                        <>
                          <Sparkles size={16} className="mr-2 animate-spin" />
                          AI genereert...
                        </>
                      ) : (
                        <>
                          <Sparkles size={16} className="mr-2" />
                          Genereer layout voor {project.num_spots + project.num_large_spots} plekken
                        </>
                      )}
                    </Button>
                  </div>

                  {project.zones.length > 0 && (
                    <div>
                      <Label className="text-sm font-medium text-[#333333] mb-2 block">Gegenereerde zones ({project.zones.length})</Label>
                      <div className="space-y-1 max-h-40 overflow-y-auto">
                        {project.zones.slice(0, 5).map((zone) => (
                          <div key={zone.id} className="flex items-center justify-between p-2 bg-white rounded-lg border border-[#e5e2d9]">
                            <div className="flex items-center gap-2">
                              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: zone.color }} />
                              <span className="text-xs font-medium text-[#333333]">{zone.name}</span>
                            </div>
                            <Button variant="ghost" size="icon" className="h-6 w-6 text-[#777777] hover:text-red-500" onClick={() => removeZone(zone.id)}>
                              <X size={12} />
                            </Button>
                          </div>
                        ))}
                        {project.zones.length > 5 && (
                          <p className="text-xs text-[#777777] text-center">+ {project.zones.length - 5} meer zones</p>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Step 3: Products */}
              {currentStep === 3 && (
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
                        <Button
                          variant="ghost"
                          size="icon"
                          className="ml-2"
                          onClick={() => setShowRealProducts(!showRealProducts)}
                        >
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
                          className={`bg-white border rounded-xl p-3 cursor-pointer hover:shadow-md transition-all ${
                            isSelected ? 'border-[#70C26C] ring-2 ring-[#70C26C]/30 bg-[#70C26C]/5' : 'border-[#e5e2d9] hover:border-[#70C26C]'
                          }`}
                          data-testid={`product-card-${product.id}`}
                        >
                          <div className="flex items-start gap-3">
                            {/* Drag handle - hold & drag to canvas */}
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
                              </div>
                            </div>
                          </div>
                          {isSelected && (
                            <div className="mt-2 text-xs text-[#70C26C] font-medium text-center bg-[#70C26C]/10 py-1 rounded">
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
                </div>
              )}

              {/* Step 4: Energy */}
              {currentStep === 4 && (
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
                        <label className="flex items-center gap-2">
                          <input type="checkbox" className="rounded border-[#70C26C]" />
                          <span className="text-[#333333]">Zonnepanelen</span>
                        </label>
                        <label className="flex items-center gap-2">
                          <input type="checkbox" className="rounded border-[#70C26C]" />
                          <span className="text-[#333333]">Accu-opslag</span>
                        </label>
                        <label className="flex items-center gap-2">
                          <input type="checkbox" className="rounded border-[#70C26C]" />
                          <span className="text-[#333333]">Wateropvang & hergebruik</span>
                        </label>
                        <label className="flex items-center gap-2">
                          <input type="checkbox" className="rounded border-[#70C26C]" />
                          <span className="text-[#333333]">Zonneboiler</span>
                        </label>
                        <label className="flex items-center gap-2">
                          <input type="checkbox" className="rounded border-[#70C26C]" />
                          <span className="text-[#333333]">Warmtepomp</span>
                        </label>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Step 5: Quote */}
              {currentStep === 5 && (
                <div className="space-y-4" data-testid="step-5-content">
                  {/* Sanitair configuratie sectie */}
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
                      <div className="h-px bg-[#e5e2d9]" />
                      <div className="flex justify-between">
                        <span className="font-semibold text-[#333333]">Totaal investering</span>
                        <span className="text-lg font-bold text-[#70C26C]">€ {(quickQuote.capex + quickQuote.install).toLocaleString()}</span>
                      </div>
                    </div>
                  </div>

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

                  <Button onClick={exportPDF} disabled={loading || project.placed_products.length === 0} className="w-full bg-[#70C26C] hover:bg-[#5fb35b] text-white font-semibold h-12" data-testid="export-pdf-button">
                    <Download size={18} className="mr-2" />
                    Offerte downloaden (PDF)
                  </Button>
                </div>
              )}
            </div>

            {/* Navigation */}
            <div className="p-4 border-t border-[#e5e2d9] flex gap-2">
              <Button
                variant="outline"
                onClick={() => setCurrentStep(prev => Math.max(1, prev - 1))}
                disabled={currentStep === 1}
                className="flex-1 border-[#e5e2d9] bg-white"
                data-testid="wizard-prev-button"
              >
                <ChevronLeft size={16} className="mr-1" />
                Vorige
              </Button>
              <Button
                onClick={async () => {
                  if (currentStep < 5) {
                    setCurrentStep(prev => prev + 1);
                    if (currentStep === 1 && !project.id) await saveProject();
                  }
                }}
                disabled={currentStep === 5}
                className="flex-1 bg-[#70C26C] hover:bg-[#5fb35b] text-white"
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
            <div className="h-12 bg-white border-b border-[#e5e2d9] flex items-center justify-between px-4">
              <div className="flex items-center gap-2">
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      variant={canvasTool === 'select' ? 'default' : 'ghost'}
                      size="sm"
                      onClick={() => setCanvasTool('select')}
                      className={canvasTool === 'select' ? 'bg-[#70C26C] text-white' : ''}
                      data-testid="tool-select"
                    >
                      <MousePointer size={16} />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>Selecteren</TooltipContent>
                </Tooltip>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      variant={canvasTool === 'zone' ? 'default' : 'ghost'}
                      size="sm"
                      onClick={() => setCanvasTool('zone')}
                      className={canvasTool === 'zone' ? 'bg-[#70C26C] text-white' : ''}
                      data-testid="tool-zone"
                    >
                      <PenTool size={16} />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>Zone tekenen</TooltipContent>
                </Tooltip>
                
                {isDrawingZone && (
                  <>
                    <div className="h-6 w-px bg-[#e5e2d9] mx-2" />
                    <Button size="sm" onClick={finishZone} className="bg-[#70C26C] text-white">
                      <Check size={14} className="mr-1" />
                      Voltooien
                    </Button>
                    <Button size="sm" variant="ghost" onClick={cancelZone}>
                      <X size={14} className="mr-1" />
                      Annuleer
                    </Button>
                  </>
                )}
              </div>

              <div className="flex items-center gap-2 text-sm text-[#777777]">
                <div className="flex items-center bg-[#FDF9ED] rounded-lg p-0.5 border border-[#e5e2d9]" data-testid="view-mode-toggle">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setViewMode('icon')}
                    className={`text-xs px-2 h-7 ${viewMode === 'icon' ? 'bg-white shadow-sm text-[#333333]' : 'text-[#777777]'}`}
                  >
                    <Package size={14} className="mr-1" /> Icoon
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setViewMode('2d')}
                    className={`text-xs px-2 h-7 ${viewMode === '2d' ? 'bg-white shadow-sm text-[#333333]' : 'text-[#777777]'}`}
                  >
                    <Square size={14} className="mr-1" /> 2D
                  </Button>
                </div>
                <span>{project.name} • {project.placed_products.length} producten</span>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button variant="ghost" size="sm" onClick={() => setShowCoverage(!showCoverage)} className={showCoverage ? 'text-[#70C26C]' : ''}>
                      {showCoverage ? <Eye size={16} /> : <EyeOff size={16} />}
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>{showCoverage ? 'Verberg bereik' : 'Toon bereik'}</TooltipContent>
                </Tooltip>
              </div>
            </div>

            {/* Canvas */}
            <div className="flex-1 overflow-auto bg-[#FDF9ED] p-4">
              <div
                ref={canvasRef}
                className={`relative bg-white rounded-xl shadow-lg mx-auto border-2 transition-colors ${canvasTool === 'zone' ? 'cursor-crosshair' : selectedProduct ? 'cursor-copy' : movingItem ? 'cursor-grabbing' : ''} ${isDragOver ? 'border-[#70C26C] bg-[#70C26C]/5' : 'border-[#e5e2d9]'}`}
                style={{ 
                  width: project.canvas_width, 
                  height: project.canvas_height,
                  minWidth: project.canvas_width,
                  backgroundImage: 'linear-gradient(to right, rgba(0,0,0,0.02) 1px, transparent 1px), linear-gradient(to bottom, rgba(0,0,0,0.02) 1px, transparent 1px)',
                  backgroundSize: '24px 24px',
                }}
                onClick={handleCanvasClick}
                onDrop={handleCanvasDrop}
                onDragOver={handleCanvasDragOver}
                onDragLeave={handleCanvasDragLeave}
                data-testid="site-canvas"
              >
                {/* Floor plan background */}
                {project.floor_plan_base64 && (
                  <img src={project.floor_plan_base64} alt="Plattegrond" className="absolute inset-0 w-full h-full object-contain opacity-50 pointer-events-none" />
                )}

                {/* Zones SVG */}
                <svg className="absolute inset-0 w-full h-full pointer-events-none">
                  {project.zones.map((zone) => (
                    <polygon
                      key={zone.id}
                      points={zone.points.map(p => `${p.x},${p.y}`).join(' ')}
                      fill={`${zone.color}20`}
                      stroke={zone.color}
                      strokeWidth="2"
                      strokeDasharray={zone.type === 'toegangsweg' ? '0' : '5,5'}
                    />
                  ))}
                  {currentZonePoints.length > 0 && (
                    <>
                      <polyline points={currentZonePoints.map(p => `${p.x},${p.y}`).join(' ')} fill="none" stroke="#70C26C" strokeWidth="2" strokeDasharray="5,5" />
                      {currentZonePoints.map((point, i) => (
                        <circle key={i} cx={point.x} cy={point.y} r="5" fill="#70C26C" />
                      ))}
                    </>
                  )}
                </svg>

                {/* Placed products */}
                {project.placed_products.map((placed) => {
                  const product = getProductById(placed.product_id);
                  if (!product) return null;
                  
                  const Icon = categoryIcons[product.category] || Package;
                  const color = categoryColors[product.category] || '#70C26C';
                  const isSelected = selectedItem?.id === placed.id;
                  const { w, h } = getProductPxSize(product);
                  const dims = product.dimensions;
                  
                  return (
                    <div
                      key={placed.id}
                      className={`absolute transition-all ${movingItem?.placedId === placed.id ? 'cursor-grabbing z-30 opacity-80' : isSelected ? 'cursor-grab ring-2 ring-[#70C26C] ring-offset-2 z-20' : 'cursor-grab z-10 hover:ring-1 hover:ring-[#70C26C]/50'}`}
                      style={{ left: placed.x, top: placed.y, transform: `rotate(${placed.rotation}deg)` }}
                      onMouseDown={(e) => handlePlacedItemMouseDown(e, placed)}
                      onClick={(e) => { e.stopPropagation(); }}
                      data-testid={`placed-item-${placed.id}`}
                    >
                      {showCoverage && product.coverage_radius && (
                        <div
                          className="absolute rounded-full opacity-15 pointer-events-none"
                          style={{
                            width: product.coverage_radius * 4,
                            height: product.coverage_radius * 4,
                            left: -(product.coverage_radius * 2) + w / 2,
                            top: -(product.coverage_radius * 2) + h / 2,
                            backgroundColor: color,
                            border: `2px dashed ${color}`,
                          }}
                        />
                      )}
                      
                      {viewMode === '2d' ? (
                        /* 2D mode: scaled rectangle with real dimensions */
                        <div
                          className="rounded border-2 flex flex-col items-center justify-center overflow-hidden"
                          style={{
                            width: w,
                            height: h,
                            backgroundColor: `${color}20`,
                            borderColor: color,
                          }}
                        >
                          <Icon size={Math.min(w, h) * 0.4} style={{ color }} className="flex-shrink-0" />
                          {w > 28 && h > 36 && (
                            <span className="text-[7px] font-bold mt-0.5 leading-tight text-center" style={{ color }}>
                              {dims ? `${dims.width}x${dims.height}m` : ''}
                            </span>
                          )}
                        </div>
                      ) : (
                        /* Icon mode: compact icon */
                        <div className="w-12 h-12 rounded-xl flex items-center justify-center shadow-lg border-2 border-white" style={{ backgroundColor: color }}>
                          <Icon size={24} className="text-white" />
                        </div>
                      )}
                      
                      <div className={`absolute ${viewMode === '2d' ? `top-[${h + 4}px]` : 'top-14'} left-1/2 -translate-x-1/2 whitespace-nowrap`} style={{ top: viewMode === '2d' ? h + 4 : 56 }}>
                        <span className="text-[9px] bg-white px-1.5 py-0.5 rounded shadow-sm text-[#333333] border border-[#e5e2d9]">
                          {product.name.length > 15 ? product.name.split(' ').slice(0, 2).join(' ') : product.name}
                        </span>
                      </div>
                    </div>
                  );
                })}

                {/* Selected item controls */}
                {selectedItem && !movingItem && (() => {
                  const selProduct = getProductById(selectedItem.product_id);
                  const selSize = selProduct ? getProductPxSize(selProduct) : { w: 48, h: 48 };
                  const panelLeft = selectedItem.x + (viewMode === '2d' ? selSize.w + 8 : 56);
                  return (
                    <div className="absolute bg-white rounded-lg shadow-xl p-1.5 flex gap-1 border border-[#e5e2d9] z-30" style={{ left: panelLeft, top: selectedItem.y - 4 }}>
                      <Button variant="ghost" size="icon" className="w-8 h-8" onClick={() => setProject(prev => ({ ...prev, placed_products: prev.placed_products.map(p => p.id === selectedItem.id ? { ...p, rotation: (p.rotation + 45) % 360 } : p) }))}>
                        <RotateCw size={14} />
                      </Button>
                      <Button variant="ghost" size="icon" className="w-8 h-8 text-red-500" onClick={() => removeItem(selectedItem.id)}>
                        <Trash2 size={14} />
                      </Button>
                    </div>
                  );
                })()}

                {/* Empty state - pointer-events-none to allow drag & drop through */}
                {project.placed_products.length === 0 && project.zones.length === 0 && (
                  <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                    <div className="text-center max-w-sm p-8">
                      {isDragOver ? (
                        <>
                          <div className="w-16 h-16 rounded-2xl bg-[#70C26C]/10 border-2 border-dashed border-[#70C26C] flex items-center justify-center mx-auto mb-4">
                            <Plus size={32} className="text-[#70C26C]" />
                          </div>
                          <h3 className="font-semibold text-[#70C26C] mb-2">Laat hier los</h3>
                        </>
                      ) : (
                        <>
                          <div className="w-16 h-16 rounded-2xl bg-[#FDF9ED] border border-[#e5e2d9] flex items-center justify-center mx-auto mb-4">
                            <Package size={32} className="text-[#e5e2d9]" />
                          </div>
                          <h3 className="font-semibold text-[#333333] mb-2">Start met configureren</h3>
                          <p className="text-sm text-[#777777]">Klik op een product in de lijst en klik hier om te plaatsen. Of sleep het product direct.</p>
                        </>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Right Sidebar */}
          <div className="w-72 flex-shrink-0 border-l border-[#e5e2d9] bg-[#FFFEF8] flex flex-col">
            <Tabs value={sidebarTab} onValueChange={setSidebarTab} className="flex flex-col h-full">
              <TabsList className="w-full p-1 bg-[#FDF9ED] rounded-none border-b border-[#e5e2d9] h-auto">
                <TabsTrigger value="products" className="flex-1 py-2 data-[state=active]:bg-white data-[state=active]:text-[#70C26C]">
                  Offerte
                </TabsTrigger>
                <TabsTrigger value="ai" className="flex-1 py-2 data-[state=active]:bg-white data-[state=active]:text-[#70C26C]">
                  AI Advies
                </TabsTrigger>
              </TabsList>

              <TabsContent value="products" className="flex-1 m-0 overflow-y-auto p-4">
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-2">
                    <div className="p-3 rounded-xl bg-[#70C26C]/10 border border-[#70C26C]/20">
                      <div className="text-xs text-[#777777]">Investering</div>
                      <div className="font-bold text-[#70C26C]" data-testid="quote-investering">€ {quickQuote.capex.toLocaleString()}</div>
                    </div>
                    <div className="p-3 rounded-xl bg-[#244628]/10 border border-[#244628]/20">
                      <div className="text-xs text-[#777777]">Lease/mnd</div>
                      <div className="font-bold text-[#244628]" data-testid="quote-operational-lease">€ {quickQuote.opex.toLocaleString()}</div>
                      <div className="text-[9px] text-[#777777] mt-0.5">60 mnd incl. SLA</div>
                    </div>
                  </div>

                  <div className="space-y-2">
                    {Object.entries(
                      project.placed_products.reduce((acc, pp) => {
                        const product = getProductById(pp.product_id);
                        if (product) {
                          if (!acc[pp.product_id]) acc[pp.product_id] = { product, count: 0 };
                          acc[pp.product_id].count += pp.quantity;
                        }
                        return acc;
                      }, {})
                    ).map(([productId, { product, count }]) => {
                      const Icon = categoryIcons[product.category] || Package;
                      const color = categoryColors[product.category];
                      
                      return (
                        <div key={productId} className="flex items-center justify-between p-2 rounded-lg bg-white border border-[#e5e2d9]">
                          <div className="flex items-center gap-2">
                            <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ backgroundColor: `${color}15` }}>
                              <Icon size={14} style={{ color }} />
                            </div>
                            <div>
                              <div className="text-xs font-medium text-[#333333]">{product.name}</div>
                              <div className="text-[10px] text-[#777777]">{count}x • € {(product.price_purchase * count).toLocaleString()}</div>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                    {project.placed_products.length === 0 && (
                      <div className="text-center py-6 text-[#777777]">
                        <Package size={24} className="mx-auto mb-2 opacity-50" />
                        <p className="text-xs">Nog geen producten</p>
                      </div>
                    )}
                  </div>

                  <div className="p-3 rounded-xl bg-[#244628] text-white">
                    <div className="flex justify-between mb-1">
                      <span className="text-white/80 text-sm">Totaal</span>
                      <span className="font-bold" data-testid="quote-total">€ {(quickQuote.capex + quickQuote.install).toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between text-xs text-white/60">
                      <span>Incl. installatie</span>
                      <span>€ {quickQuote.install.toLocaleString()}</span>
                    </div>
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="ai" className="flex-1 m-0 overflow-y-auto p-4">
                <div className="space-y-3">
                  <div className="flex items-center gap-2 mb-3">
                    <Sparkles size={18} className="text-[#70C26C]" />
                    <span className="font-medium text-[#333333]">AI Aanbevelingen</span>
                  </div>

                  {recommendations.length > 0 ? (
                    recommendations.map((rec, index) => (
                      <div key={index} className={`rounded-lg border p-3 bg-white ${rec.type === 'warning' ? 'border-amber-300' : 'border-[#70C26C]'}`} data-testid={`ai-recommendation-${index}`}>
                        <div className="flex items-start gap-2">
                          {rec.type === 'warning' ? <AlertTriangle size={14} className="text-amber-500 mt-0.5" /> : <Zap size={14} className="text-[#70C26C] mt-0.5" />}
                          <div>
                            <h4 className="font-medium text-xs text-[#333333]">{rec.title}</h4>
                            <p className="text-[10px] text-[#777777] mt-0.5">{rec.description}</p>
                          </div>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-6 text-[#777777]">
                      <Sparkles size={24} className="mx-auto mb-2 opacity-50" />
                      <p className="text-xs">Plaats producten voor advies</p>
                    </div>
                  )}

                  <Button variant="outline" className="w-full text-xs border-[#70C26C] text-[#70C26C]" onClick={fetchRecommendations} disabled={!project.id} data-testid="refresh-ai-button">
                    <Sparkles size={12} className="mr-1" />
                    Vernieuw
                  </Button>
                </div>
              </TabsContent>
            </Tabs>
          </div>
        </div>

        <Toaster theme="light" position="bottom-right" toastOptions={{ style: { background: '#fff', border: '1px solid #e5e2d9', color: '#333333' } }} />

        {/* Drag ghost - follows cursor during pointer drag */}
        {pointerDrag && (
          <div
            className="fixed pointer-events-none z-50"
            style={{ left: pointerDrag.x - 20, top: pointerDrag.y - 20 }}
          >
            <div
              className="rounded border-2 flex items-center justify-center shadow-xl opacity-80"
              style={{
                width: Math.max((pointerDrag.product.dimensions?.width || 2) * CANVAS_SCALE, 24),
                height: Math.max((pointerDrag.product.dimensions?.height || 2) * CANVAS_SCALE, 24),
                backgroundColor: `${categoryColors[pointerDrag.product.category] || '#70C26C'}30`,
                borderColor: categoryColors[pointerDrag.product.category] || '#70C26C',
              }}
            >
              {React.createElement(categoryIcons[pointerDrag.product.category] || Package, {
                size: 18,
                style: { color: categoryColors[pointerDrag.product.category] || '#70C26C' },
              })}
            </div>
            <div className="text-[9px] text-center mt-1 font-medium text-[#333333] bg-white px-1 py-0.5 rounded shadow-sm border border-[#e5e2d9] whitespace-nowrap">
              {pointerDrag.product.name}
            </div>
          </div>
        )}
      </div>
    </TooltipProvider>
  );
}

export default App;
