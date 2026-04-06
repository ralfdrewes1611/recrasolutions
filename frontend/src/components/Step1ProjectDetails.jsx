import React from 'react';
import { Car, Tent, TreePine, MapPin } from 'lucide-react';
import { Input } from './ui/input';
import { Label } from './ui/label';

const projectTypes = [
  { value: 'camperplaats', label: 'Camperplaats', icon: Car },
  { value: 'camping', label: 'Camping', icon: Tent },
  { value: 'resort', label: 'Resort', icon: TreePine },
  { value: 'jachthaven', label: 'Jachthaven', icon: MapPin },
];

export function Step1ProjectDetails({ project, setProject }) {
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
