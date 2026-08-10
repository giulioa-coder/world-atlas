'use client';

import { useEffect, useRef, useState } from 'react';
import { useWorldStore } from '@/stores/worldStore';
import { useMapStore } from '@/stores/mapStore';
import { Location } from '@/types';
import { Plus, Minus, Move, MousePointer2 } from 'lucide-react';

interface MapCanvasProps {
  worldId: string;
}

export function MapCanvas({ worldId }: MapCanvasProps) {
  const svgRef = useRef<SVGSVGElement>(null);
  const { locations, fetchLocations, updateLocationPosition } = useWorldStore();
  const { zoom, pan, setPan, setZoom, selectedLocationId, setSelectedLocation, editMode } = useMapStore();
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [isMovingLocation, setIsMovingLocation] = useState(false);

  useEffect(() => {
    fetchLocations(worldId);
  }, [worldId]);

  const handleWheel = (e: React.WheelEvent) => {
    e.preventDefault();
    const delta = e.deltaY > 0 ? -0.1 : 0.1;
    setZoom(zoom + delta);
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    if (editMode === 'move' && selectedLocationId) {
      setIsMovingLocation(true);
      return;
    }
    setIsDragging(true);
    setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (isDragging) {
      setPan(e.clientX - dragStart.x, e.clientY - dragStart.y);
    }
    if (isMovingLocation && selectedLocationId) {
      const svg = svgRef.current;
      if (svg) {
        const rect = svg.getBoundingClientRect();
        const x = (e.clientX - rect.left - pan.x) / zoom;
        const y = (e.clientY - rect.top - pan.y) / zoom;
        // Convert to lat/lng approximation (simplified)
        const lng = (x / 1000) * 360 - 180;
        const lat = 90 - (y / 1000) * 180;
        updateLocationPosition(worldId, selectedLocationId, lat, lng);
      }
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
    setIsMovingLocation(false);
  };

  const getLocationColor = (type: string) => {
    const colors: Record<string, string> = {
      city: '#ef4444',
      town: '#f97316',
      village: '#eab308',
      castle: '#8b5cf6',
      forest: '#22c55e',
      mountain: '#6b7280',
      river: '#3b82f6',
      lake: '#3b82f6',
      ocean: '#0ea5e9',
      default: '#64748b',
    };
    return colors[type] || colors.default;
  };

  const getLocationIcon = (type: string) => {
    const icons: Record<string, string> = {
      city: '●',
      town: '◉',
      village: '○',
      castle: '♔',
      forest: '♣',
      mountain: '▲',
      default: '•',
    };
    return icons[type] || icons.default;
  };

  return (
    <div className="h-full w-full bg-background relative overflow-hidden">
      {/* Toolbar */}
      <div className="absolute top-4 left-4 z-10 flex flex-col gap-2">
        <button
          onClick={() => setZoom(zoom + 0.2)}
          className="p-2 bg-card border rounded-md hover:bg-accent"
          title="Zoom In"
        >
          <Plus className="h-5 w-5" />
        </button>
        <button
          onClick={() => setZoom(zoom - 0.2)}
          className="p-2 bg-card border rounded-md hover:bg-accent"
          title="Zoom Out"
        >
          <Minus className="h-5 w-5" />
        </button>
        <div className="p-2 bg-card border rounded-md">
          {editMode === 'move' ? (
            <Move className="h-5 w-5 text-primary" />
          ) : (
            <MousePointer2 className="h-5 w-5" />
          )}
        </div>
      </div>

      {/* Zoom indicator */}
      <div className="absolute top-4 right-4 z-10 px-3 py-1 bg-card border rounded-md text-sm">
        {Math.round(zoom * 100)}%
      </div>

      {/* Map SVG */}
      <svg
        ref={svgRef}
        className="w-full h-full cursor-grab active:cursor-grabbing"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onWheel={handleWheel}
      >
        <g transform={`translate(${pan.x}, ${pan.y}) scale(${zoom})`}>
          {/* Grid background */}
          <defs>
            <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse">
              <path d="M 50 0 L 0 0 0 50" fill="none" stroke="hsl(var(--border))" strokeWidth="0.5"/>
            </pattern>
          </defs>
          <rect width="1000" height="1000" fill="url(#grid)" />
          
          {/* Locations */}
          {locations.map((location) => (
            <g
              key={location.id}
              onClick={(e) => {
                e.stopPropagation();
                setSelectedLocation(location.id);
              }}
              className="cursor-pointer hover:opacity-80"
              style={{
                transform: `translate(${((location.longitude || 0) + 180) / 360 * 1000}px, ${(90 - (location.latitude || 0)) / 180 * 1000}px)`,
              }}
            >
              <circle
                r={selectedLocationId === location.id ? 12 : 8}
                fill={getLocationColor(location.location_type)}
                stroke="white"
                strokeWidth="2"
                className="transition-all"
              />
              <text
                y="-12"
                textAnchor="middle"
                className="text-xs fill-foreground pointer-events-none"
                style={{ fontSize: '12px', fontWeight: '-semibold' }}
              >
                {location.name}
              </text>
            </g>
          ))}
        </g>
      </svg>

      {/* Help text */}
      {locations.length === 0 && (
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="text-center text-muted-foreground">
            <p className="text-lg font-medium mb-2">No locations yet</p>
            <p className="text-sm">Locations will appear here once created</p>
          </div>
        </div>
      )}
    </div>
  );
}
