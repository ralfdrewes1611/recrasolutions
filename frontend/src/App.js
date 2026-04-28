import React, { useState, useEffect, useRef, useCallback } from 'react';
import axios from 'axios';
import { Toaster, toast } from 'sonner';
import { FlowSelector } from './FlowSelector';
import { FecWizard } from './FecWizard';
import HorecaWizard from './HorecaWizard';
import EijsinkPartnerPage from './EijsinkPartnerPage';
import { ChaletWizard } from './ChaletWizard';
import { PlatformDashboard } from './PlatformDashboard';
import SupplierProfile from './SupplierProfile';
import { RoadmapView } from './RoadmapView';
import { SubsidyModule } from './SubsidyModule';
import { SupplierAdmin } from './SupplierAdmin';
import { LoginScreen } from './LoginScreen';
import { SupplierPanel } from './SupplierPanel';
import { Step1ProjectDetails } from './components/Step1ProjectDetails';
import { Step2Terrain } from './components/Step2Terrain';
import { Step3Products, categoryIcons, categoryColors } from './components/Step3Products';
import { Step4Energy } from './components/Step4Energy';
import { Step5Quote, SANITAIR_EXTRAS } from './components/Step5Quote';
import {
  ChevronRight, ChevronLeft, Package, Sparkles, FileText,
  Plus, Trash2, MapPin, FolderOpen, Save, Settings,
  HelpCircle, Phone, Mail, PenTool, MousePointer, Eye, EyeOff,
  BatteryCharging, Square, Check, X, Loader2, Zap, AlertTriangle, Download, RotateCw, Lock, Crown,
  TrendingUp,
} from 'lucide-react';
import { Button } from './components/ui/button';
import { ScrollArea } from './components/ui/scroll-area';
import { Tabs, TabsList, TabsTrigger, TabsContent } from './components/ui/tabs';
import {
  Tooltip, TooltipContent, TooltipProvider, TooltipTrigger,
} from './components/ui/tooltip';
import {
  Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger,
} from './components/ui/dialog';
import {
  DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuTrigger,
} from './components/ui/dropdown-menu';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const CANVAS_SCALE = 10;

const WIZARD_STEPS = [
  { id: 1, title: 'Project', description: 'Basisgegevens', icon: Package },
  { id: 2, title: 'Terrein', description: 'Plattegrond & AI Layout', icon: MapPin },
  { id: 3, title: 'Producten', description: 'Configureren', icon: Settings },
  { id: 4, title: 'Energie', description: 'Stroomvoorziening', icon: BatteryCharging },
  { id: 5, title: 'Offerte', description: 'Afronden', icon: FileText },
];

// Paywall tiers
const TIER_LABELS = { free: 'Free', pro: 'Pro', enterprise: 'Enterprise' };
const TIER_COLORS = { free: '#777777', pro: '#70C26C', enterprise: '#244628' };

function App() {
  const [user, setUser] = useState(null);
  const [authChecking, setAuthChecking] = useState(true);
  const [activeFlow, setActiveFlow] = useState(null);
  const [currentStep, setCurrentStep] = useState(1);
  const [products, setProducts] = useState([]);
  const [projects, setProjects] = useState([]);
  const [userTier, setUserTier] = useState('free'); // free | pro | enterprise
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [supplierProfileId, setSupplierProfileId] = useState(null);
  const [project, setProject] = useState({
    id: null, name: 'Nieuw Project', project_type: 'camping', project_flow: 'recreatie',
    address: '', lat: 52.0, lng: 5.0, floor_plan_base64: null, scale_meters_per_pixel: 0.1,
    canvas_width: 1000, canvas_height: 700, placed_products: [], zones: [],
    num_spots: 30, num_large_spots: 5, energy_mode: 'grid',
  });

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
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [pointerDrag, setPointerDrag] = useState(null);
  const [movingItem, setMovingItem] = useState(null);
  const [viewMode, setViewMode] = useState('2d');
  const [matchedSuppliers, setMatchedSuppliers] = useState([]);
  const [showSubsidy, setShowSubsidy] = useState(false);

  const canvasRef = useRef(null);

  // Auth check bij opstarten
  useEffect(() => {
    const token = localStorage.getItem('recra_token');
    if (token) {
      axios.get(`${API}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
        withCredentials: true,
      }).then(res => {
        setUser(res.data);
      }).catch(() => {
        localStorage.removeItem('recra_token');
        localStorage.removeItem('recra_user');
      }).finally(() => setAuthChecking(false));
    } else {
      setAuthChecking(false);
    }
  }, []);

  const handleLogout = () => {
    axios.post(`${API}/auth/logout`, {}, { withCredentials: true }).catch(() => {});
    localStorage.removeItem('recra_token');
    localStorage.removeItem('recra_user');
    setUser(null);
  };

  // Fetch products filtered by active flow
  const fetchProducts = useCallback(async () => {
    try {
      const params = activeFlow ? `?flow=${activeFlow}` : '';
      const response = await axios.get(`${API}/products${params}`);
      setProducts(response.data);
    } catch (error) {
      console.error('Error fetching products:', error);
      toast.error('Kon producten niet laden');
    }
  }, [activeFlow]);

  const fetchProjects = async () => {
    try {
      const response = await axios.get(`${API}/projects`);
      setProjects(response.data);
    } catch (error) {
      console.error('Error fetching projects:', error);
    }
  };

  const fetchMatchedSuppliers = useCallback(async () => {
    try {
      const res = await axios.post(`${API}/suppliers/match`, {
        project_lat: project.lat,
        project_lng: project.lng,
      });
      setMatchedSuppliers(res.data);
    } catch {
      setMatchedSuppliers([]);
    }
  }, [project.lat, project.lng]);

  useEffect(() => { fetchProducts(); fetchProjects(); }, [fetchProducts]);
  useEffect(() => {
    if (project.id && project.placed_products.length > 0) fetchRecommendations();
  }, [project.placed_products, project.id]);
  useEffect(() => { fetchMatchedSuppliers(); }, [fetchMatchedSuppliers]);

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
      toast.error('Kon project niet laden');
    }
  };

  const deleteProject = async (projectId) => {
    try {
      await axios.delete(`${API}/projects/${projectId}`);
      fetchProjects();
      if (project.id === projectId) newProject();
      toast.success('Project verwijderd');
    } catch {
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

  const generateAILayout = async () => {
    setIsAnalyzing(true);
    try {
      toast.success(`Layout wordt gegenereerd voor ${project.num_spots} normale en ${project.num_large_spots} grote plekken...`);
      await new Promise(resolve => setTimeout(resolve, 1500));
      const scale = 10;
      const normalW = 8, normalH = 10;
      const largeW = 12, largeH = 15;
      const roadWidth = 5;
      const gapX = 2, gapY = 2;
      const spots = [];
      const cols = Math.min(5, Math.ceil(Math.sqrt(project.num_spots)));
      const startX = 80, startY = 80;
      const totalNormalRows = Math.ceil(project.num_spots / cols);
      const blockW = cols * (normalW + gapX) * scale;
      const blockH = totalNormalRows * (normalH + gapY) * scale;
      const roadW = roadWidth * scale;

      const roadZones = [
        { id: `zone-road-top-${Date.now()}`, name: 'Hoofdweg', type: 'toegangsweg', points: [{ x: startX - roadW, y: startY - roadW }, { x: startX + blockW + roadW, y: startY - roadW }, { x: startX + blockW + roadW, y: startY }, { x: startX - roadW, y: startY }], color: '#9ca3af' },
        { id: `zone-road-left-${Date.now()}`, name: 'Weg links', type: 'toegangsweg', points: [{ x: startX - roadW, y: startY }, { x: startX, y: startY }, { x: startX, y: startY + blockH }, { x: startX - roadW, y: startY + blockH }], color: '#9ca3af' },
        { id: `zone-road-right-${Date.now()}`, name: 'Weg rechts', type: 'toegangsweg', points: [{ x: startX + blockW, y: startY }, { x: startX + blockW + roadW, y: startY }, { x: startX + blockW + roadW, y: startY + blockH }, { x: startX + blockW, y: startY + blockH }], color: '#9ca3af' },
        { id: `zone-road-bottom-${Date.now()}`, name: 'Weg onder', type: 'toegangsweg', points: [{ x: startX - roadW, y: startY + blockH }, { x: startX + blockW + roadW, y: startY + blockH }, { x: startX + blockW + roadW, y: startY + blockH + roadW }, { x: startX - roadW, y: startY + blockH + roadW }], color: '#9ca3af' },
      ];

      for (let i = 0; i < project.num_spots; i++) {
        const row = Math.floor(i / cols), col = i % cols;
        const px = startX + col * (normalW + gapX) * scale;
        const py = startY + row * (normalH + gapY) * scale;
        spots.push({ id: `spot-${Date.now()}-${i}`, name: `Plek ${i + 1} (${normalW}x${normalH}m)`, type: 'standplaats', points: [{ x: px, y: py }, { x: px + normalW * scale, y: py }, { x: px + normalW * scale, y: py + normalH * scale }, { x: px, y: py + normalH * scale }], color: '#70C26C' });
      }

      const largeStartY = startY + blockH + roadW + gapY * scale;
      const largeCols = Math.min(3, project.num_large_spots);
      for (let i = 0; i < project.num_large_spots; i++) {
        const col = i % largeCols, row = Math.floor(i / largeCols);
        const px = startX + col * (largeW + gapX) * scale;
        const py = largeStartY + row * (largeH + gapY) * scale;
        spots.push({ id: `spot-large-${Date.now()}-${i}`, name: `XL Plek ${i + 1} (${largeW}x${largeH}m)`, type: 'grote_standplaats', points: [{ x: px, y: py }, { x: px + largeW * scale, y: py }, { x: px + largeW * scale, y: py + largeH * scale }, { x: px, y: py + largeH * scale }], color: '#2563eb' });
      }

      const allZones = [...roadZones, ...spots];
      const maxX = Math.max(...allZones.flatMap(z => z.points.map(p => p.x))) + 60;
      const maxY = Math.max(...allZones.flatMap(z => z.points.map(p => p.y))) + 60;

      setProject(prev => ({
        ...prev, zones: allZones,
        canvas_width: Math.max(prev.canvas_width, maxX),
        canvas_height: Math.max(prev.canvas_height, maxY),
      }));
      toast.success(`Layout gegenereerd: ${project.num_spots} standplaatsen + ${project.num_large_spots} XL met rondrit`);
    } catch (error) {
      toast.error('Kon layout niet genereren');
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Canvas interactions
  const handleCanvasClick = (e) => {
    if (movingItem) return;
    if (selectedProduct && canvasTool === 'select') {
      const rect = canvasRef.current.getBoundingClientRect();
      const snappedX = Math.round((e.clientX - rect.left) / 24) * 24;
      const snappedY = Math.round((e.clientY - rect.top) / 24) * 24;
      setProject(prev => ({
        ...prev,
        placed_products: [...prev.placed_products, { id: `placed-${Date.now()}`, product_id: selectedProduct.id, x: snappedX, y: snappedY, rotation: 0, quantity: 1 }],
      }));
      toast.success(`${selectedProduct.name} geplaatst`);
      setSelectedProduct(null);
      return;
    }
    if (canvasTool === 'select' && selectedItem) { setSelectedItem(null); return; }
    if (canvasTool !== 'zone') return;
    const rect = canvasRef.current.getBoundingClientRect();
    setCurrentZonePoints(prev => [...prev, { x: e.clientX - rect.left, y: e.clientY - rect.top }]);
    setIsDrawingZone(true);
  };

  const finishZone = () => {
    if (currentZonePoints.length < 3) { toast.error('Een zone moet minimaal 3 punten hebben'); return; }
    setProject(prev => ({ ...prev, zones: [...prev.zones, { id: `zone-${Date.now()}`, name: `Zone ${prev.zones.length + 1}`, type: 'standplaats', points: currentZonePoints, color: '#70C26C' }] }));
    setCurrentZonePoints([]); setIsDrawingZone(false); setCanvasTool('select');
    toast.success('Zone toegevoegd');
  };

  const cancelZone = () => { setCurrentZonePoints([]); setIsDrawingZone(false); };

  const handleCanvasDrop = (e) => {
    e.preventDefault(); e.stopPropagation();
    let product = draggedProduct;
    if (!product) { try { product = JSON.parse(e.dataTransfer.getData('application/json')); } catch { return; } }
    if (!product) return;
    const rect = canvasRef.current.getBoundingClientRect();
    const snappedX = Math.round((e.clientX - rect.left) / 24) * 24;
    const snappedY = Math.round((e.clientY - rect.top) / 24) * 24;
    setProject(prev => ({ ...prev, placed_products: [...prev.placed_products, { id: `placed-${Date.now()}`, product_id: product.id, x: snappedX, y: snappedY, rotation: 0, quantity: 1 }] }));
    setDraggedProduct(null); setIsDragOver(false);
    toast.success(`${product.name} geplaatst`);
  };

  const handleCanvasDragOver = (e) => { e.preventDefault(); e.stopPropagation(); e.dataTransfer.dropEffect = 'copy'; if (!isDragOver) setIsDragOver(true); };
  const handleCanvasDragLeave = (e) => { e.preventDefault(); if (!e.currentTarget.contains(e.relatedTarget)) setIsDragOver(false); };

  const handlePointerDragStart = useCallback((e, product) => {
    e.preventDefault();
    setPointerDrag({ product, x: e.clientX, y: e.clientY });
    setSelectedProduct(null);
  }, []);

  useEffect(() => {
    if (!pointerDrag) return;
    const handleMove = (e) => setPointerDrag(prev => prev ? { ...prev, x: e.clientX, y: e.clientY } : null);
    const handleUp = (e) => {
      const canvas = canvasRef.current;
      if (canvas) {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left, y = e.clientY - rect.top;
        if (x >= 0 && y >= 0 && x <= rect.width && y <= rect.height) {
          setProject(prev => ({ ...prev, placed_products: [...prev.placed_products, { id: `placed-${Date.now()}`, product_id: pointerDrag.product.id, x: Math.round(x / 24) * 24, y: Math.round(y / 24) * 24, rotation: 0, quantity: 1 }] }));
          toast.success(`${pointerDrag.product.name} geplaatst`);
        }
      }
      setPointerDrag(null);
    };
    document.addEventListener('mousemove', handleMove);
    document.addEventListener('mouseup', handleUp);
    return () => { document.removeEventListener('mousemove', handleMove); document.removeEventListener('mouseup', handleUp); };
  }, [pointerDrag]);

  const handlePlacedItemMouseDown = useCallback((e, placed) => {
    e.stopPropagation(); e.preventDefault();
    const rect = canvasRef.current.getBoundingClientRect();
    setMovingItem({ placedId: placed.id, offsetX: e.clientX - rect.left - placed.x, offsetY: e.clientY - rect.top - placed.y });
    setSelectedItem(placed); setSelectedProduct(null);
  }, []);

  useEffect(() => {
    if (!movingItem) return;
    const handleMove = (e) => {
      const rect = canvasRef.current.getBoundingClientRect();
      const x = Math.round((e.clientX - rect.left - movingItem.offsetX) / 24) * 24;
      const y = Math.round((e.clientY - rect.top - movingItem.offsetY) / 24) * 24;
      setProject(prev => ({ ...prev, placed_products: prev.placed_products.map(p => p.id === movingItem.placedId ? { ...p, x: Math.max(0, x), y: Math.max(0, y) } : p) }));
    };
    const handleUp = () => setMovingItem(null);
    document.addEventListener('mousemove', handleMove);
    document.addEventListener('mouseup', handleUp);
    return () => { document.removeEventListener('mousemove', handleMove); document.removeEventListener('mouseup', handleUp); };
  }, [movingItem]);

  const getProductById = (pid) => products.find(p => p.id === pid);

  const getProductPxSize = (product) => {
    const dims = product.dimensions;
    if (!dims) return { w: 32, h: 32 };
    return { w: Math.max(dims.width * CANVAS_SCALE, 24), h: Math.max(dims.height * CANVAS_SCALE, 24) };
  };

  const removeItem = (itemId) => {
    setProject(prev => ({ ...prev, placed_products: prev.placed_products.filter(p => p.id !== itemId) }));
    setSelectedItem(null); toast.success('Product verwijderd');
  };

  const exportPDF = async () => {
    let projectToExport = project;
    if (!project.id) { const saved = await saveProject(); if (!saved) return; projectToExport = saved; }
    try {
      setLoading(true);
      const response = await axios.post(`${API}/quote/pdf?project_id=${projectToExport.id}`);
      const printWindow = window.open('', '_blank');
      printWindow.document.write(response.data.html);
      printWindow.document.close();
      printWindow.focus();
      setTimeout(() => printWindow.print(), 500);
      toast.success('PDF gegenereerd');
    } catch {
      toast.error('Kon PDF niet genereren');
    } finally {
      setLoading(false);
    }
  };

  const powerCalculation = project.placed_products.reduce((acc, pp) => {
    const product = getProductById(pp.product_id);
    if (product) {
      const powerUsage = { sanitair: 5000, douchelezer: 100, camera: 15, wifi: 20, verlichting: 50, slagboom: 200, betaalsysteem: 50, toegangscontrole: 30 };
      acc.watts += (powerUsage[product.category] || 100) * pp.quantity;
    }
    return acc;
  }, { watts: 0 });

  const sanitairExtrasTotal = Object.entries(sanitairConfigs).reduce((acc, [, config]) => {
    (config.extras || []).forEach(extraKey => {
      const extra = SANITAIR_EXTRAS[extraKey];
      if (extra) { acc.capex += extra.price; acc.lease += extra.lease; }
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

  // Energy investment calculation
  const energyInvestment = (() => {
    const ec = project.energy_config || {};
    if (project.energy_mode === 'grid') return 0;
    let total = 0;
    total += (ec.solar_panels || 0) * 320;    // € per panel
    total += (ec.batteries || 0) * 2800;      // € per battery
    if (ec.heat_pump) total += 8500;
    if (ec.solar_boiler) total += 3200;
    if (ec.water_recycling) total += 12000;
    if (ec.wind_turbine) total += 6500;
    return total;
  })();

  const newProject = () => {
    setProject({
      id: null, name: 'Nieuw Project', project_type: 'camping', project_flow: activeFlow || 'recreatie',
      address: '', lat: 52.0, lng: 5.0, floor_plan_base64: null, scale_meters_per_pixel: 0.1,
      canvas_width: 1000, canvas_height: 700, placed_products: [], zones: [],
      num_spots: 30, num_large_spots: 5, energy_mode: 'grid',
    });
    setCurrentStep(1); setShowProjectList(false);
  };

  // Auth gate — voordat iets anders wordt gerenderd
  if (authChecking) {
    return (
      <div className="min-h-screen bg-[#244628] flex items-center justify-center">
        <div className="text-center">
          <div className="text-2xl font-bold text-white tracking-[6px]">RECRA</div>
          <div className="text-[#70C26C] text-xs tracking-[4px] mt-1">SOLUTIONS</div>
          <div className="w-8 h-8 border-2 border-[#70C26C]/30 border-t-[#70C26C] rounded-full animate-spin mx-auto mt-6" />
        </div>
      </div>
    );
  }

  if (!user) {
    return <LoginScreen onLogin={(userData) => setUser(userData)} />;
  }

  if (!activeFlow) {
    return (
      <FlowSelector onSelect={(flow) => {
        setActiveFlow(flow);
        setProject(prev => ({ ...prev, project_flow: flow }));
      }} />
    );
  }

  // FEC gets its own dedicated wizard (revenue-driven, not asset-driven)
  if (activeFlow === 'fec') {
    return (
      <>
        <FecWizard onBack={() => setActiveFlow(null)} userTier={userTier} />
        <Toaster theme="light" position="bottom-right" toastOptions={{ style: { background: '#fff', border: '1px solid #e5e2d9', color: '#333333' } }} />
      </>
    );
  }

  // Horeca & Bar — bar / kassa / bestelzuilen / pub games configurator
  if (activeFlow === 'horeca') {
    return (
      <>
        <HorecaWizard
          onBack={() => setActiveFlow(null)}
          onOpenEijsinkPage={() => setActiveFlow('partner-eijsink')}
        />
        <Toaster theme="light" position="bottom-right" toastOptions={{ style: { background: '#fff', border: '1px solid #e5e2d9', color: '#333333' } }} />
      </>
    );
  }

  // Eijsink Partner Page — full page (not modal)
  if (activeFlow === 'partner-eijsink') {
    return (
      <>
        <EijsinkPartnerPage onBack={() => setActiveFlow('horeca')} />
        <Toaster theme="light" position="bottom-right" toastOptions={{ style: { background: '#fff', border: '1px solid #e5e2d9', color: '#333333' } }} />
      </>
    );
  }

  // Chalet gets its own dedicated configurator
  if (activeFlow === 'chalet') {
    return (
      <>
        <ChaletWizard onBack={() => setActiveFlow(null)} onRoadmap={() => setActiveFlow('roadmap-chalet')} />
        <Toaster theme="light" position="bottom-right" toastOptions={{ style: { background: '#fff', border: '1px solid #e5e2d9', color: '#333333' } }} />
      </>
    );
  }

  // Platform Dashboard
  if (activeFlow === 'dashboard') {
    return (
      <>
        <PlatformDashboard onBack={() => setActiveFlow(null)} />
        <Toaster theme="light" position="bottom-right" toastOptions={{ style: { background: '#fff', border: '1px solid #e5e2d9', color: '#333333' } }} />
      </>
    );
  }

  // Roadmap view — Idee naar Realisatie
  if (activeFlow === 'roadmap') {
    return (
      <>
        <RoadmapView flowType="recreatie" onBack={() => setActiveFlow(null)} />
        <Toaster theme="light" position="bottom-right" toastOptions={{ style: { background: '#fff', border: '1px solid #e5e2d9', color: '#333333' } }} />
      </>
    );
  }

  // Roadmap for specific flows
  if (activeFlow?.startsWith('roadmap-')) {
    const flow = activeFlow.replace('roadmap-', '');
    return (
      <>
        <RoadmapView flowType={flow} onBack={() => setActiveFlow(null)} />
        <Toaster theme="light" position="bottom-right" toastOptions={{ style: { background: '#fff', border: '1px solid #e5e2d9', color: '#333333' } }} />
      </>
    );
  }

  // Supplier Admin
  if (activeFlow === 'admin-suppliers') {
    return (
      <>
        <SupplierAdmin onBack={() => setActiveFlow(null)} />
        <Toaster theme="light" position="bottom-right" toastOptions={{ style: { background: '#fff', border: '1px solid #e5e2d9', color: '#333333' } }} />
      </>
    );
  }



  return (
    <TooltipProvider>
      <div className="h-screen w-full flex flex-col overflow-hidden bg-[#FDF9ED]">
        {/* Header */}
        <header className="h-16 bg-[#244628] flex items-center justify-between px-6 flex-shrink-0">
          <div className="flex items-center gap-4">
            <button onClick={() => setActiveFlow(null)} className="flex items-center gap-2 hover:opacity-80 transition-opacity" data-testid="header-logo">
              <img src="/recra-logo-white.png" alt="RECRA Solutions" className="h-8" />
            </button>
            <span className="text-white/40 text-sm">|</span>
            <span className="text-[#70C26C] text-sm font-medium capitalize" data-testid="active-flow-label">
              {activeFlow === 'fec' ? 'FEC & Experience' : activeFlow === 'chalet' ? 'Chalet & Stay' : 'Recreatie Infra'}
            </span>
            <span className="text-xs px-2 py-0.5 rounded-full font-medium" style={{ backgroundColor: `${TIER_COLORS[userTier]}20`, color: TIER_COLORS[userTier] }} data-testid="user-tier-badge">
              {TIER_LABELS[userTier]}
            </span>
          </div>
          <div className="flex items-center gap-3">
            <Dialog open={showProjectList} onOpenChange={setShowProjectList}>
              <DialogTrigger asChild>
                <Button variant="ghost" className="text-white/90 hover:text-white hover:bg-white/10" data-testid="open-projects-btn">
                  <FolderOpen size={18} className="mr-2" /> Projecten
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl bg-white border-[#e5e2d9]">
                <DialogHeader>
                  <DialogTitle className="text-[#333333]">Mijn Projecten</DialogTitle>
                  <DialogDescription className="text-[#777777]">Selecteer een project om verder te werken of start een nieuw project.</DialogDescription>
                </DialogHeader>
                <div className="py-4">
                  <Button onClick={newProject} className="w-full mb-4 bg-[#70C26C] hover:bg-[#5fb35b] text-white font-semibold" data-testid="new-project-btn">
                    <Plus size={18} className="mr-2" /> Nieuw Project
                  </Button>
                  <ScrollArea className="h-[300px]">
                    <div className="space-y-2">
                      {projects.map((p) => (
                        <div key={p.id} className={`flex items-center justify-between p-4 rounded-lg border cursor-pointer transition-all ${project.id === p.id ? 'border-[#70C26C] bg-[#70C26C]/5' : 'border-[#e5e2d9] hover:border-[#70C26C]'}`} data-testid={`project-item-${p.id}`}>
                          <div className="flex-1" onClick={() => loadProject(p.id)}>
                            <h4 className="font-medium text-[#333333]">{p.name}</h4>
                            <p className="text-sm text-[#777777]">{p.project_type} - {p.placed_products?.length || 0} producten</p>
                          </div>
                          <Button variant="ghost" size="icon" className="text-[#777777] hover:text-red-500" onClick={(e) => { e.stopPropagation(); deleteProject(p.id); }}>
                            <Trash2 size={16} />
                          </Button>
                        </div>
                      ))}
                      {projects.length === 0 && (
                        <div className="text-center py-8 text-[#777777]">
                          <FolderOpen size={48} className="mx-auto mb-2 opacity-50" /><p>Nog geen projecten</p>
                        </div>
                      )}
                    </div>
                  </ScrollArea>
                </div>
              </DialogContent>
            </Dialog>
            <Button variant="ghost" className="text-white/90 hover:text-white hover:bg-white/10" onClick={saveProject} disabled={loading} data-testid="save-project-header-btn">
              <Save size={18} className="mr-2" /> Opslaan
            </Button>
            <Button className="bg-[#70C26C] hover:bg-[#5fb35b] text-white font-medium">Contact</Button>
            <Button
              variant="ghost"
              className={`text-white/90 hover:text-white hover:bg-white/10 ${showSubsidy ? 'bg-white/10 text-white' : ''}`}
              onClick={() => setShowSubsidy(!showSubsidy)}
              data-testid="subsidy-toggle-btn"
            >
              <TrendingUp size={18} className="mr-2" /> Subsidie Check
            </Button>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="text-white/90 hover:text-white hover:bg-white/10"><HelpCircle size={20} /></Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="bg-white border-[#e5e2d9]">
                <DropdownMenuItem className="text-[#333333]"><Phone size={16} className="mr-2" />+31 634200253</DropdownMenuItem>
                <DropdownMenuItem className="text-[#333333]"><Mail size={16} className="mr-2" />info@recrasolutions.com</DropdownMenuItem>
                <DropdownMenuSeparator className="bg-[#e5e2d9]" />
                <DropdownMenuItem className="text-[#333333]"><HelpCircle size={16} className="mr-2" />Handleiding</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
            <Button variant="ghost" size="sm" onClick={handleLogout}
              className="text-white/50 hover:text-white hover:bg-white/10 text-xs ml-1"
              data-testid="logout-btn">
              Uitloggen
            </Button>
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
                    <button key={step.id} onClick={() => setCurrentStep(step.id)}
                      className={`w-full flex items-center gap-3 p-2.5 rounded-lg transition-all ${isActive ? 'bg-[#70C26C]/10 border border-[#70C26C]/30' : isCompleted ? 'bg-[#70C26C]/5' : 'hover:bg-[#FDF9ED]'}`}
                      data-testid={`wizard-step-${step.id}`}
                    >
                      <div className={`w-7 h-7 rounded-lg flex items-center justify-center text-sm ${isActive || isCompleted ? 'bg-[#70C26C] text-white' : 'bg-[#e5e2d9] text-[#777777]'}`}>
                        {isCompleted ? <Check size={14} /> : <Icon size={14} />}
                      </div>
                      <div className="text-left">
                        <div className={`text-sm font-medium ${isActive || isCompleted ? 'text-[#70C26C]' : 'text-[#333333]'}`}>{step.title}</div>
                        <div className="text-xs text-[#777777]">{step.description}</div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Step Content */}
            <div className="flex-1 overflow-y-auto p-4">
              {currentStep === 1 && <Step1ProjectDetails project={project} setProject={setProject} />}
              {currentStep === 2 && <Step2Terrain project={project} setProject={setProject} isAnalyzing={isAnalyzing} setIsAnalyzing={setIsAnalyzing} generateAILayout={generateAILayout} />}
              {currentStep === 3 && (
                <Step3Products
                  products={products} selectedCategory={selectedCategory} setSelectedCategory={setSelectedCategory}
                  selectedProduct={selectedProduct} setSelectedProduct={setSelectedProduct}
                  showRealProducts={showRealProducts} setShowRealProducts={setShowRealProducts}
                  handlePointerDragStart={handlePointerDragStart} fetchProducts={fetchProducts}
                  onSupplierClick={(supplierName) => {
                    const mapping = { 'Ticra Outdoor': 'ticra-outdoor', 'Kunert Group': 'kunert-group', 'Arcabo': 'arcabo', 'Campsolutions': 'campsolutions', 'BBS Systeembouw': 'bbs-systeembouw' };
                    setSupplierProfileId(mapping[supplierName] || null);
                  }}
                />
              )}
              {currentStep === 4 && <Step4Energy project={project} setProject={setProject} powerCalculation={powerCalculation} />}
              {currentStep === 5 && (
                <Step5Quote
                  project={project} products={products} quickQuote={quickQuote}
                  sanitairConfigs={sanitairConfigs} setSanitairConfigs={setSanitairConfigs}
                  matchedSuppliers={matchedSuppliers} exportPDF={exportPDF} loading={loading}
                  userTier={userTier} onUpgrade={() => setShowUpgradeModal(true)}
                  energyInvestment={energyInvestment}
                  onRoadmap={() => setActiveFlow('roadmap-recreatie')}
                />
              )}
            </div>

            {/* Navigation */}
            <div className="p-4 border-t border-[#e5e2d9] flex gap-2">
              <Button variant="outline" onClick={() => setCurrentStep(prev => Math.max(1, prev - 1))} disabled={currentStep === 1} className="flex-1 border-[#e5e2d9] bg-white" data-testid="wizard-prev-button">
                <ChevronLeft size={16} className="mr-1" /> Vorige
              </Button>
              <Button onClick={async () => { if (currentStep < 5) { setCurrentStep(prev => prev + 1); if (currentStep === 1 && !project.id) await saveProject(); } }} disabled={currentStep === 5} className="flex-1 bg-[#70C26C] hover:bg-[#5fb35b] text-white" data-testid="wizard-next-button">
                Volgende <ChevronRight size={16} className="ml-1" />
              </Button>
            </div>
          </div>

          {/* Main Canvas Area */}
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Canvas Toolbar */}
            <div className="h-12 bg-white border-b border-[#e5e2d9] flex items-center justify-between px-4">
              <div className="flex items-center gap-2">
                <Tooltip><TooltipTrigger asChild>
                  <Button variant={canvasTool === 'select' ? 'default' : 'ghost'} size="sm" onClick={() => setCanvasTool('select')} className={canvasTool === 'select' ? 'bg-[#70C26C] text-white' : ''} data-testid="tool-select"><MousePointer size={16} /></Button>
                </TooltipTrigger><TooltipContent>Selecteren</TooltipContent></Tooltip>
                <Tooltip><TooltipTrigger asChild>
                  <Button variant={canvasTool === 'zone' ? 'default' : 'ghost'} size="sm" onClick={() => setCanvasTool('zone')} className={canvasTool === 'zone' ? 'bg-[#70C26C] text-white' : ''} data-testid="tool-zone"><PenTool size={16} /></Button>
                </TooltipTrigger><TooltipContent>Zone tekenen</TooltipContent></Tooltip>
                {isDrawingZone && (
                  <>
                    <div className="h-6 w-px bg-[#e5e2d9] mx-2" />
                    <Button size="sm" onClick={finishZone} className="bg-[#70C26C] text-white"><Check size={14} className="mr-1" />Voltooien</Button>
                    <Button size="sm" variant="ghost" onClick={cancelZone}><X size={14} className="mr-1" />Annuleer</Button>
                  </>
                )}
              </div>
              <div className="flex items-center gap-2 text-sm text-[#777777]">
                <div className="flex items-center bg-[#FDF9ED] rounded-lg p-0.5 border border-[#e5e2d9]" data-testid="view-mode-toggle">
                  <Button variant="ghost" size="sm" onClick={() => setViewMode('icon')} className={`text-xs px-2 h-7 ${viewMode === 'icon' ? 'bg-white shadow-sm text-[#333333]' : 'text-[#777777]'}`}>
                    <Package size={14} className="mr-1" /> Icoon
                  </Button>
                  <Button variant="ghost" size="sm" onClick={() => setViewMode('2d')} className={`text-xs px-2 h-7 ${viewMode === '2d' ? 'bg-white shadow-sm text-[#333333]' : 'text-[#777777]'}`}>
                    <Square size={14} className="mr-1" /> 2D
                  </Button>
                </div>
                <span>{project.name} - {project.placed_products.length} producten</span>
                <Tooltip><TooltipTrigger asChild>
                  <Button variant="ghost" size="sm" onClick={() => setShowCoverage(!showCoverage)} className={showCoverage ? 'text-[#70C26C]' : ''}>
                    {showCoverage ? <Eye size={16} /> : <EyeOff size={16} />}
                  </Button>
                </TooltipTrigger><TooltipContent>{showCoverage ? 'Verberg bereik' : 'Toon bereik'}</TooltipContent></Tooltip>
              </div>
            </div>

            {/* Canvas */}
            <div className="flex-1 overflow-auto bg-[#FDF9ED] p-4">
              <div
                ref={canvasRef}
                className={`relative bg-white rounded-xl shadow-lg mx-auto border-2 transition-colors ${canvasTool === 'zone' ? 'cursor-crosshair' : selectedProduct ? 'cursor-copy' : movingItem ? 'cursor-grabbing' : ''} ${isDragOver ? 'border-[#70C26C] bg-[#70C26C]/5' : 'border-[#e5e2d9]'}`}
                style={{ width: project.canvas_width, height: project.canvas_height, minWidth: project.canvas_width, backgroundImage: 'linear-gradient(to right, rgba(0,0,0,0.02) 1px, transparent 1px), linear-gradient(to bottom, rgba(0,0,0,0.02) 1px, transparent 1px)', backgroundSize: '24px 24px' }}
                onClick={handleCanvasClick} onDrop={handleCanvasDrop} onDragOver={handleCanvasDragOver} onDragLeave={handleCanvasDragLeave}
                data-testid="site-canvas"
              >
                {project.floor_plan_base64 && <img src={project.floor_plan_base64} alt="Plattegrond" className="absolute inset-0 w-full h-full object-contain opacity-50 pointer-events-none" />}

                <svg className="absolute inset-0 w-full h-full pointer-events-none">
                  {project.zones.map((zone) => (
                    <polygon key={zone.id} points={zone.points.map(p => `${p.x},${p.y}`).join(' ')} fill={`${zone.color}20`} stroke={zone.color} strokeWidth="2" strokeDasharray={zone.type === 'toegangsweg' ? '0' : '5,5'} />
                  ))}
                  {currentZonePoints.length > 0 && (
                    <>
                      <polyline points={currentZonePoints.map(p => `${p.x},${p.y}`).join(' ')} fill="none" stroke="#70C26C" strokeWidth="2" strokeDasharray="5,5" />
                      {currentZonePoints.map((point, i) => <circle key={i} cx={point.x} cy={point.y} r="5" fill="#70C26C" />)}
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
                    <div key={placed.id}
                      className={`absolute transition-all ${movingItem?.placedId === placed.id ? 'cursor-grabbing z-30 opacity-80' : isSelected ? 'cursor-grab ring-2 ring-[#70C26C] ring-offset-2 z-20' : 'cursor-grab z-10 hover:ring-1 hover:ring-[#70C26C]/50'}`}
                      style={{ left: placed.x, top: placed.y, transform: `rotate(${placed.rotation}deg)` }}
                      onMouseDown={(e) => handlePlacedItemMouseDown(e, placed)}
                      onClick={(e) => e.stopPropagation()}
                      data-testid={`placed-item-${placed.id}`}
                    >
                      {showCoverage && product.coverage_radius && (
                        <div className="absolute rounded-full opacity-15 pointer-events-none" style={{ width: product.coverage_radius * 4, height: product.coverage_radius * 4, left: -(product.coverage_radius * 2) + w / 2, top: -(product.coverage_radius * 2) + h / 2, backgroundColor: color, border: `2px dashed ${color}` }} />
                      )}
                      {viewMode === '2d' ? (
                        <div className="rounded border-2 flex flex-col items-center justify-center overflow-hidden" style={{ width: w, height: h, backgroundColor: `${color}20`, borderColor: color }}>
                          <Icon size={Math.min(w, h) * 0.4} style={{ color }} className="flex-shrink-0" />
                          {w > 28 && h > 36 && <span className="text-[7px] font-bold mt-0.5 leading-tight text-center" style={{ color }}>{dims ? `${dims.width}x${dims.height}m` : ''}</span>}
                        </div>
                      ) : (
                        <div className="w-12 h-12 rounded-xl flex items-center justify-center shadow-lg border-2 border-white" style={{ backgroundColor: color }}>
                          <Icon size={24} className="text-white" />
                        </div>
                      )}
                      <div className="absolute left-1/2 -translate-x-1/2 whitespace-nowrap" style={{ top: viewMode === '2d' ? h + 4 : 56 }}>
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
                  return (
                    <div className="absolute bg-white rounded-lg shadow-xl p-1.5 flex gap-1 border border-[#e5e2d9] z-30" style={{ left: selectedItem.x + (viewMode === '2d' ? selSize.w + 8 : 56), top: selectedItem.y - 4 }}>
                      <Button variant="ghost" size="icon" className="w-8 h-8" onClick={() => setProject(prev => ({ ...prev, placed_products: prev.placed_products.map(p => p.id === selectedItem.id ? { ...p, rotation: (p.rotation + 45) % 360 } : p) }))}>
                        <RotateCw size={14} />
                      </Button>
                      <Button variant="ghost" size="icon" className="w-8 h-8 text-red-500" onClick={() => removeItem(selectedItem.id)}>
                        <Trash2 size={14} />
                      </Button>
                    </div>
                  );
                })()}

                {/* Empty state */}
                {project.placed_products.length === 0 && project.zones.length === 0 && (
                  <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                    <div className="text-center max-w-sm p-8">
                      {isDragOver ? (
                        <>
                          <div className="w-16 h-16 rounded-2xl bg-[#70C26C]/10 border-2 border-dashed border-[#70C26C] flex items-center justify-center mx-auto mb-4"><Plus size={32} className="text-[#70C26C]" /></div>
                          <h3 className="font-semibold text-[#70C26C] mb-2">Laat hier los</h3>
                        </>
                      ) : (
                        <>
                          <div className="w-16 h-16 rounded-2xl bg-[#FDF9ED] border border-[#e5e2d9] flex items-center justify-center mx-auto mb-4"><Package size={32} className="text-[#e5e2d9]" /></div>
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
                <TabsTrigger value="products" className="flex-1 py-2 data-[state=active]:bg-white data-[state=active]:text-[#70C26C] text-xs">Offerte</TabsTrigger>
                <TabsTrigger value="suppliers" className="flex-1 py-2 data-[state=active]:bg-white data-[state=active]:text-[#70C26C] text-xs" onClick={(e) => { if (userTier !== 'enterprise') { e.preventDefault(); setShowUpgradeModal(true); } }} disabled={userTier !== 'enterprise'}>
                  {userTier !== 'enterprise' && <Lock size={10} className="mr-1 inline" />}Leveranciers
                </TabsTrigger>
                <TabsTrigger value="ai" className="flex-1 py-2 data-[state=active]:bg-white data-[state=active]:text-[#70C26C] text-xs">AI Advies</TabsTrigger>
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
                              <div className="text-[10px] text-[#777777]">{count}x - € {(product.price_purchase * count).toLocaleString()}</div>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                    {project.placed_products.length === 0 && (
                      <div className="text-center py-6 text-[#777777]">
                        <Package size={24} className="mx-auto mb-2 opacity-50" /><p className="text-xs">Nog geen producten</p>
                      </div>
                    )}
                  </div>

                  <div className="p-3 rounded-xl bg-[#244628] text-white">
                    <div className="flex justify-between mb-1">
                      <span className="text-white/80 text-sm">Totaal</span>
                      <span className="font-bold" data-testid="quote-total">€ {(quickQuote.capex + quickQuote.install + energyInvestment).toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between text-xs text-white/60">
                      <span>Incl. installatie</span>
                      <span>€ {quickQuote.install.toLocaleString()}</span>
                    </div>
                    {energyInvestment > 0 && (
                      <div className="flex justify-between text-xs text-[#70C26C] mt-0.5">
                        <span>Incl. energie</span>
                        <span>€ {energyInvestment.toLocaleString()}</span>
                      </div>
                    )}
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="suppliers" className="flex-1 m-0 overflow-y-auto p-4">
                <SupplierPanel projectLat={project.lat} projectLng={project.lng} />
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
                      <Sparkles size={24} className="mx-auto mb-2 opacity-50" /><p className="text-xs">Plaats producten voor advies</p>
                    </div>
                  )}
                  <Button variant="outline" className="w-full text-xs border-[#70C26C] text-[#70C26C]" onClick={fetchRecommendations} disabled={!project.id} data-testid="refresh-ai-button">
                    <Sparkles size={12} className="mr-1" /> Vernieuw
                  </Button>
                </div>
              </TabsContent>
            </Tabs>
          </div>

          {/* Subsidie Module — Right Sticky Panel */}
          {showSubsidy && (
            <div className="w-80 flex-shrink-0 border-l border-[#e5e2d9] bg-[#FFFEF8] flex flex-col" data-testid="subsidy-sidebar">
              <SubsidyModule
                onClose={() => setShowSubsidy(false)}
                projectContext={{
                  sector: 'Recreatie',
                  projectomschrijving: project.name || '',
                }}
              />
            </div>
          )}
        </div>

        <Toaster theme="light" position="bottom-right" toastOptions={{ style: { background: '#fff', border: '1px solid #e5e2d9', color: '#333333' } }} />

        {/* Upgrade Modal */}
        <Dialog open={showUpgradeModal} onOpenChange={setShowUpgradeModal}>
          <DialogContent className="max-w-lg bg-white border-[#e5e2d9]">
            <DialogHeader>
              <DialogTitle className="text-[#244628] flex items-center gap-2"><Crown size={20} className="text-[#70C26C]" /> Upgrade je plan</DialogTitle>
              <DialogDescription className="text-[#777777]">Kies het plan dat bij je past</DialogDescription>
            </DialogHeader>
            <div className="space-y-3 py-4">
              {[
                { tier: 'free', label: 'Free', price: '€0', features: ['Configurator', 'AI aanbevelingen', 'Projecten opslaan'] },
                { tier: 'pro', label: 'Pro', price: '€49/mnd', features: ['Alles van Free', 'Offerte PDF downloaden', 'AI offertetekst'] },
                { tier: 'enterprise', label: 'Enterprise', price: '€149/mnd', features: ['Alles van Pro', 'Partner matching', 'Leveranciers dashboard', 'API toegang'] },
              ].map((plan) => (
                <button
                  key={plan.tier}
                  onClick={() => { setUserTier(plan.tier); setShowUpgradeModal(false); toast.success(`Plan gewijzigd naar ${plan.label}`); }}
                  className={`w-full p-4 rounded-xl border-2 text-left transition-all ${userTier === plan.tier ? 'border-[#70C26C] bg-[#70C26C]/5' : 'border-[#e5e2d9] hover:border-[#70C26C]/50 bg-white'}`}
                  data-testid={`plan-${plan.tier}`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-bold text-[#333333]">{plan.label}</span>
                    <span className="font-bold text-[#70C26C]">{plan.price}</span>
                  </div>
                  <ul className="space-y-1">
                    {plan.features.map((f, i) => (
                      <li key={i} className="text-xs text-[#777777] flex items-center gap-1.5">
                        <Check size={12} className="text-[#70C26C]" /> {f}
                      </li>
                    ))}
                  </ul>
                  {userTier === plan.tier && <div className="mt-2 text-xs text-[#70C26C] font-medium">Huidig plan</div>}
                </button>
              ))}
            </div>
          </DialogContent>
        </Dialog>

        {/* Drag ghost */}
        {pointerDrag && (
          <div className="fixed pointer-events-none z-50" style={{ left: pointerDrag.x - 20, top: pointerDrag.y - 20 }}>
            <div className="rounded border-2 flex items-center justify-center shadow-xl opacity-80"
              style={{ width: Math.max((pointerDrag.product.dimensions?.width || 2) * CANVAS_SCALE, 24), height: Math.max((pointerDrag.product.dimensions?.height || 2) * CANVAS_SCALE, 24), backgroundColor: `${categoryColors[pointerDrag.product.category] || '#70C26C'}30`, borderColor: categoryColors[pointerDrag.product.category] || '#70C26C' }}
            >
              {React.createElement(categoryIcons[pointerDrag.product.category] || Package, { size: 18, style: { color: categoryColors[pointerDrag.product.category] || '#70C26C' } })}
            </div>
            <div className="text-[9px] text-center mt-1 font-medium text-[#333333] bg-white px-1 py-0.5 rounded shadow-sm border border-[#e5e2d9] whitespace-nowrap">
              {pointerDrag.product.name}
            </div>
          </div>
        )}
      </div>
      {supplierProfileId && (
        <SupplierProfile partnerId={supplierProfileId} onClose={() => setSupplierProfileId(null)} />
      )}
    </TooltipProvider>
  );
}

export default App;
