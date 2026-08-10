import { create } from 'zustand';
import { World, Location, Manuscript, Character } from '@/types';
import { worldService, locationService, manuscriptService, characterService } from '@/services';

interface WorldState {
  worlds: World[];
  currentWorld: World | null;
  locations: Location[];
  manuscripts: Manuscript[];
  characters: Character[];
  isLoading: boolean;
  error: string | null;
  
  // Actions - Worlds
  fetchWorlds: () => Promise<void>;
  fetchWorld: (id: string) => Promise<void>;
  createWorld: (data: { name: string; description?: string; genre?: string }) => Promise<World>;
  updateWorld: (id: string, data: any) => Promise<void>;
  deleteWorld: (id: string) => Promise<void>;
  
  // Actions - Locations
  fetchLocations: (worldId: string) => Promise<void>;
  createLocation: (worldId: string, data: any) => Promise<Location>;
  updateLocation: (worldId: string, id: string, data: any) => Promise<void>;
  deleteLocation: (worldId: string, id: string) => Promise<void>;
  updateLocationPosition: (worldId: string, id: string, lat: number, lng: number) => Promise<void>;
  
  // Actions - Manuscripts
  fetchManuscripts: (worldId: string) => Promise<void>;
  uploadManuscript: (worldId: string, file: File) => Promise<Manuscript>;
  
  // Actions - Characters
  fetchCharacters: (worldId: string) => Promise<void>;
  createCharacter: (worldId: string, data: { name: string; description?: string }) => Promise<Character>;
}

export const useWorldStore = create<WorldState>((set, get) => ({
  worlds: [],
  currentWorld: null,
  locations: [],
  manuscripts: [],
  characters: [],
  isLoading: false,
  error: null,

  fetchWorlds: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await worldService.list();
      set({ worlds: response.items, isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },

  fetchWorld: async (id: string) => {
    set({ isLoading: true, error: null });
    try {
      const world = await worldService.get(id);
      set({ currentWorld: world, isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },

  createWorld: async (data) => {
    set({ isLoading: true, error: null });
    try {
      const world = await worldService.create(data);
      set((state) => ({ 
        worlds: [...state.worlds, world],
        currentWorld: world,
        isLoading: false 
      }));
      return world;
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  updateWorld: async (id, data) => {
    set({ isLoading: true, error: null });
    try {
      await worldService.update(id, data);
      const world = await worldService.get(id);
      set((state) => ({
        currentWorld: world,
        worlds: state.worlds.map(w => w.id === id ? world : w),
        isLoading: false
      }));
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },

  deleteWorld: async (id) => {
    set({ isLoading: true, error: null });
    try {
      await worldService.delete(id);
      set((state) => ({
        worlds: state.worlds.filter(w => w.id !== id),
        currentWorld: state.currentWorld?.id === id ? null : state.currentWorld,
        isLoading: false
      }));
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },

  fetchLocations: async (worldId: string) => {
    set({ isLoading: true, error: null });
    try {
      const locations = await locationService.list(worldId);
      set({ locations, isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },

  createLocation: async (worldId: string, data: any) => {
    try {
      const location = await locationService.create(worldId, data);
      set((state) => ({ locations: [...state.locations, location] }));
      return location;
    } catch (error: any) {
      set({ error: error.message });
      throw error;
    }
  },

  updateLocation: async (worldId: string, id: string, data: any) => {
    try {
      await locationService.update(worldId, id, data);
      set((state) => ({
        locations: state.locations.map(loc => 
          loc.id === id ? { ...loc, ...data, updated_at: new Date().toISOString() } : loc
        )
      }));
    } catch (error: any) {
      set({ error: error.message });
      throw error;
    }
  },

  deleteLocation: async (worldId: string, id: string) => {
    try {
      await locationService.delete(worldId, id);
      set((state) => ({
        locations: state.locations.filter(loc => loc.id !== id)
      }));
    } catch (error: any) {
      set({ error: error.message });
      throw error;
    }
  },

  updateLocationPosition: async (worldId: string, id: string, lat: number, lng: number) => {
    try {
      await locationService.updatePosition(worldId, id, lat, lng);
      set((state) => ({
        locations: state.locations.map(loc =>
          loc.id === id ? { ...loc, latitude: lat, longitude: lng, updated_at: new Date().toISOString() } : loc
        )
      }));
    } catch (error: any) {
      set({ error: error.message });
      throw error;
    }
  },

  fetchManuscripts: async (worldId: string) => {
    try {
      const manuscripts = await manuscriptService.list(worldId);
      set({ manuscripts });
    } catch (error: any) {
      set({ error: error.message });
    }
  },

  uploadManuscript: async (worldId: string, file: File) => {
    set({ isLoading: true, error: null });
    try {
      const manuscript = await manuscriptService.upload(worldId, file);
      set((state) => ({ 
        manuscripts: [...state.manuscripts, manuscript],
        isLoading: false 
      }));
      return manuscript;
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  fetchCharacters: async (worldId: string) => {
    try {
      const characters = await characterService.list(worldId);
      set({ characters });
    } catch (error: any) {
      set({ error: error.message });
    }
  },

  createCharacter: async (worldId: string, data: { name: string; description?: string }) => {
    try {
      const character = await characterService.create(worldId, data);
      set((state) => ({ characters: [...state.characters, character] }));
      return character;
    } catch (error: any) {
      set({ error: error.message });
      throw error;
    }
  },
}));
