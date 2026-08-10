import { create } from 'zustand';
import { MapLayer } from '@/types';

interface MapState {
  // View state
  zoom: number;
  pan: { x: number; y: number };
  center: { x: number; y: number };
  
  // Layers
  layers: MapLayer[];
  activeLayer: string | null;
  
  // Selection
  selectedLocationId: string | null;
  selectedRoadId: string | null;
  
  // Editor mode
  isEditing: boolean;
  editMode: 'select' | 'create' | 'delete' | 'move';
  
  // Map style
  mapStyle: string;
  
  // Actions
  setZoom: (zoom: number) => void;
  setPan: (x: number, y: number) => void;
  setCenter: (x: number, y: number) => void;
  toggleLayer: (layerId: string) => void;
  setActiveLayer: (layerId: string | null) => void;
  setSelectedLocation: (id: string | null) => void;
  setSelectedRoad: (id: string | null) => void;
  setEditMode: (mode: 'select' | 'create' | 'delete' | 'move') => void;
  setMapStyle: (style: string) => void;
  resetView: () => void;
}

const DEFAULT_LAYERS: MapLayer[] = [
  { id: 'base_terrain', name: 'Base Terrain', visible: true, type: 'base_terrain' },
  { id: 'water', name: 'Water', visible: true, type: 'water' },
  { id: 'elevation', name: 'Elevation', visible: true, type: 'elevation' },
  { id: 'forests', name: 'Forests', visible: true, type: 'forests' },
  { id: 'regions', name: 'Regions', visible: true, type: 'regions' },
  { id: 'roads', name: 'Roads', visible: true, type: 'roads' },
  { id: 'settlements', name: 'Settlements', visible: true, type: 'settlements' },
  { id: 'labels', name: 'Labels', visible: true, type: 'labels' },
  { id: 'journeys', name: 'Journeys', visible: false, type: 'journeys' },
];

export const useMapStore = create<MapState>((set) => ({
  // Initial state
  zoom: 1,
  pan: { x: 0, y: 0 },
  center: { x: 500, y: 500 },
  layers: DEFAULT_LAYERS,
  activeLayer: null,
  selectedLocationId: null,
  selectedRoadId: null,
  isEditing: false,
  editMode: 'select',
  mapStyle: 'medieval_parchment',

  // Actions
  setZoom: (zoom: number) => set({ zoom: Math.max(0.1, Math.min(5, zoom)) }),
  
  setPan: (x: number, y: number) => set({ pan: { x, y } }),
  
  setCenter: (x: number, y: number) => set({ center: { x, y } }),
  
  toggleLayer: (layerId: string) => set((state) => ({
    layers: state.layers.map(layer =>
      layer.id === layerId ? { ...layer, visible: !layer.visible } : layer
    )
  })),
  
  setActiveLayer: (layerId: string | null) => set({ activeLayer: layerId }),
  
  setSelectedLocation: (id: string | null) => set({ selectedLocationId: id }),
  
  setSelectedRoad: (id: string | null) => set({ selectedRoadId: id }),
  
  setEditMode: (mode: 'select' | 'create' | 'delete' | 'move') => set({ 
    editMode: mode,
    isEditing: mode !== 'select'
  }),
  
  setMapStyle: (style: string) => set({ mapStyle: style }),
  
  resetView: () => set({
    zoom: 1,
    pan: { x: 0, y: 0 },
    center: { x: 500, y: 500 },
  }),
}));
