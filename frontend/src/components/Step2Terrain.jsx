import React, { useRef } from 'react';
import { Upload, Check, Sparkles, X, Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import axios from 'axios';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export function Step2Terrain({ project, setProject, isAnalyzing, setIsAnalyzing, generateAILayout }) {
  const fileInputRef = useRef(null);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      setProject(prev => ({ ...prev, floor_plan_base64: e.target.result }));
      toast.success('Plattegrond geladen');
    };
    reader.readAsDataURL(file);
  };

  const analyzeFloorplan = async () => {
    setIsAnalyzing(true);
    try {
      const res = await axios.post(`${API}/ai/analyze-floorplan-smart`, {
        image_base64: project.floor_plan_base64,
        project_type: project.project_type,
        canvas_width: project.canvas_width,
        canvas_height: project.canvas_height,
      });
      if (res.data.zones?.length > 0) {
        const newZones = res.data.zones.map((z, i) => ({
          ...z,
          id: `ai-zone-${Date.now()}-${i}`,
        }));
        setProject(prev => ({
          ...prev,
          zones: [...prev.zones, ...newZones],
          num_spots: res.data.estimated_spots || prev.num_spots,
        }));
        toast.success(`AI heeft ${newZones.length} zones herkend en ${res.data.estimated_spots} standplaatsen geschat`);
      }
      if (res.data.suggested_scale) {
        setProject(prev => ({ ...prev, scale_meters_per_pixel: res.data.suggested_scale }));
      }
      if (res.data.suggestions?.length > 0) {
        res.data.suggestions.forEach(s => toast.info(s));
      }
    } catch {
      toast.error('Kon plattegrond niet analyseren');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const removeZone = (zoneId) => {
    setProject(prev => ({ ...prev, zones: prev.zones.filter(z => z.id !== zoneId) }));
    toast.success('Zone verwijderd');
  };

  return (
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
        <div className="space-y-3">
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

          <Button
            onClick={analyzeFloorplan}
            disabled={isAnalyzing}
            className="w-full bg-[#244628] hover:bg-[#1a341d] text-white"
            data-testid="analyze-floorplan-btn"
          >
            {isAnalyzing ? (
              <><Loader2 size={16} className="mr-2 animate-spin" /> AI analyseert plattegrond...</>
            ) : (
              <><Sparkles size={16} className="mr-2" /> AI Plattegrond Analyseren</>
            )}
          </Button>
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
            <><Sparkles size={16} className="mr-2 animate-spin" /> AI genereert...</>
          ) : (
            <><Sparkles size={16} className="mr-2" /> Genereer layout voor {project.num_spots + project.num_large_spots} plekken</>
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
  );
}
