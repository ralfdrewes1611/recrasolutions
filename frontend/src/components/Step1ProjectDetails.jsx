import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Car, Tent, TreePine, MapPin, TrendingUp, Scale, Info } from 'lucide-react';
import { Input } from './ui/input';
import { Label } from './ui/label';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const projectTypes = [
  { value: 'camperplaats', label: 'Camperplaats', icon: Car },
  { value: 'camping', label: 'Camping', icon: Tent },
  { value: 'resort', label: 'Resort', icon: TreePine },
  { value: 'jachthaven', label: 'Jachthaven', icon: MapPin },
];

const potentieColors = {
  'zeer hoog': '#244628',
  'hoog': '#70C26C',
  'medium': '#d97706',
  'laag': '#dc2626',
};

export function Step1ProjectDetails({ project, setProject }) {
  const [provinces, setProvinces] = useState([]);
  const [selectedProvince, setSelectedProvince] = useState(null);

  useEffect(() => {
    axios.get(`${API}/location/provinces`).then(res => setProvinces(res.data)).catch(() => {});
  }, []);

  const handleProvinceClick = (province) => {
    setSelectedProvince(selectedProvince?.id === province.id ? null : province);
    setProject(prev => ({ ...prev, province: province.id, province_name: province.name }));
  };

  return (
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
        <Label className="text-sm font-medium text-[#333333]">Projectlocatie</Label>
        <Input
          value={project.address}
          onChange={(e) => setProject(prev => ({ ...prev, address: e.target.value }))}
          className="mt-1.5 bg-white border-[#e5e2d9]"
          placeholder="Adres of plaatsnaam"
          data-testid="project-address-input"
        />
        <div className="grid grid-cols-2 gap-2 mt-1.5">
          <Input
            type="number"
            step="0.001"
            value={project.lat}
            onChange={(e) => setProject(prev => ({ ...prev, lat: parseFloat(e.target.value) || 52 }))}
            className="bg-white border-[#e5e2d9] text-sm"
            placeholder="Latitude"
            data-testid="project-lat-input"
          />
          <Input
            type="number"
            step="0.001"
            value={project.lng}
            onChange={(e) => setProject(prev => ({ ...prev, lng: parseFloat(e.target.value) || 5 }))}
            className="bg-white border-[#e5e2d9] text-sm"
            placeholder="Longitude"
            data-testid="project-lng-input"
          />
        </div>
      </div>

      {/* Locatie-intelligentie: Provincie selectie */}
      {provinces.length > 0 && (
        <div data-testid="location-intelligence">
          <Label className="text-sm font-medium text-[#333333] flex items-center gap-1.5">
            <TrendingUp size={14} className="text-[#70C26C]" />
            Locatie-intelligentie
          </Label>
          <p className="text-xs text-[#777] mt-0.5 mb-2">Selecteer een provincie voor grondprijzen en regelgeving.</p>
          <div className="grid grid-cols-3 gap-1.5">
            {provinces.map(p => {
              const isActive = selectedProvince?.id === p.id || project.province === p.id;
              const potColor = potentieColors[p.recreatie_potentie] || '#777';
              return (
                <button key={p.id} onClick={() => handleProvinceClick(p)}
                  className={`text-left px-2 py-1.5 rounded-lg border text-[11px] transition-all ${isActive ? 'bg-[#244628] text-white border-[#244628]' : 'bg-white text-[#555] border-[#e5e2d9] hover:border-[#70C26C]'}`}
                  data-testid={`province-${p.id}`}
                >
                  <div className="font-semibold truncate">{p.name}</div>
                  <div className={`flex items-center gap-1 mt-0.5 ${isActive ? 'text-white/70' : 'text-[#999]'}`}>
                    <span>€{p.grondprijs_m2.indicatief}/m²</span>
                    <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: isActive ? '#70C26C' : potColor }} />
                  </div>
                </button>
              );
            })}
          </div>
          {(selectedProvince || provinces.find(p => p.id === project.province)) && (
            <div className="mt-2 bg-white border border-[#e5e2d9] rounded-xl p-3 space-y-2" data-testid="province-detail">
              {(() => {
                const prov = selectedProvince || provinces.find(p => p.id === project.province);
                if (!prov) return null;
                return (
                  <>
                    <div className="flex items-center justify-between">
                      <div className="font-bold text-sm text-[#333]">{prov.name}</div>
                      <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full" style={{ backgroundColor: `${potentieColors[prov.recreatie_potentie]}15`, color: potentieColors[prov.recreatie_potentie] }}>
                        {prov.recreatie_potentie}
                      </span>
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div className="bg-[#FDF9ED] rounded-lg p-2">
                        <div className="text-[#999] text-[10px]">Grondprijs/m²</div>
                        <div className="font-bold text-[#333]">€{prov.grondprijs_m2.min} — €{prov.grondprijs_m2.max}</div>
                      </div>
                      <div className="bg-[#FDF9ED] rounded-lg p-2">
                        <div className="text-[#999] text-[10px]">Toerisme Score</div>
                        <div className="font-bold text-[#333]">{prov.toerisme_score} / 10</div>
                      </div>
                    </div>
                    <div className="flex flex-wrap gap-1">
                      {prov.kenmerken.map(k => (
                        <span key={k} className="text-[10px] bg-[#244628]/10 text-[#244628] px-2 py-0.5 rounded-full">{k}</span>
                      ))}
                    </div>
                  </>
                );
              })()}
            </div>
          )}
        </div>
      )}

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
  );
}
