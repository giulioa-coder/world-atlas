export interface World {
  id: string;
  name: string;
  description?: string | null;
  genre?: string | null;
  visual_style: string;
  scale_km_per_unit?: number | null;
  created_at: string;
  updated_at: string;
  owner_id: string;
  is_demo: boolean;
}

export interface Location {
  id: string;
  world_id: string;
  name: string;
  location_type: LocationType;
  latitude?: number | null;
  longitude?: number | null;
  elevation?: number | null;
  description?: string | null;
  visual_description?: string | null;
  importance: number;
  confidence: number;
  status: LocationStatus;
  first_appearance_chapter_id?: string | null;
  last_appearance_chapter_id?: string | null;
  metadata: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export type LocationType =
  | 'continent'
  | 'country'
  | 'kingdom'
  | 'region'
  | 'province'
  | 'city'
  | 'town'
  | 'village'
  | 'castle'
  | 'fortress'
  | 'capital'
  | 'harbor'
  | 'port'
  | 'inn'
  | 'temple'
  | 'ruin'
  | 'cave'
  | 'forest'
  | 'mountain'
  | 'mountain_range'
  | 'river'
  | 'lake'
  | 'sea'
  | 'ocean'
  | 'island'
  | 'landmark'
  | 'battlefield'
  | 'magical_area'
  | 'custom';

export type LocationStatus = 'canonical' | 'inferred' | 'suggested' | 'rejected' | 'unknown';

export interface Chapter {
  id: string;
  manuscript_id: string;
  chapter_number: number;
  title?: string | null;
  text: string;
  word_count: number;
  chronological_order?: number | null;
  pov_character?: string | null;
  created_at: string;
}

export interface Manuscript {
  id: string;
  world_id: string;
  title: string;
  file_path: string;
  file_type: string;
  word_count?: number | null;
  status: ManuscriptStatus;
  uploaded_at: string;
  processed_at?: string | null;
}

export type ManuscriptStatus = 'pending' | 'processing' | 'completed' | 'failed';

export interface Character {
  id: string;
  world_id: string;
  name: string;
  description?: string | null;
  role?: string | null;
  created_at: string;
}

export interface CharacterJourney {
  id: string;
  character_id: string;
  chapter_id: string;
  origin_location_id?: string | null;
  destination_location_id?: string | null;
  route_description?: string | null;
  travel_mode?: string | null;
  stated_duration_days?: number | null;
  inferred_duration_days?: number | null;
  distance_km?: number | null;
  confidence: number;
  notes?: string | null;
  created_at: string;
}

export interface Road {
  id: string;
  world_id: string;
  origin_location_id?: string | null;
  destination_location_id?: string | null;
  geometry?: any | null;
  estimated_distance_km?: number | null;
  terrain_type?: string | null;
  travel_modes?: string[] | null;
  created_at: string;
}

export interface Region {
  id: string;
  world_id: string;
  name: string;
  region_type: string;
  geometry?: any | null;
  description?: string | null;
  political_status?: string | null;
  parent_region_id?: string | null;
  created_at: string;
}

export interface LoreEntity {
  id: string;
  world_id: string;
  name: string;
  entity_type: LoreEntityType;
  description?: string | null;
  metadata: Record<string, any>;
  created_at: string;
}

export type LoreEntityType =
  | 'people'
  | 'race'
  | 'species'
  | 'religion'
  | 'deity'
  | 'faction'
  | 'currency'
  | 'language'
  | 'political_entity'
  | 'organization'
  | 'technology'
  | 'magic_system'
  | 'custom';

export interface Inconsistency {
  id: string;
  world_id: string;
  inconsistency_type: string;
  severity: 'low' | 'medium' | 'high';
  description: string;
  related_entities: any[];
  resolution_notes?: string | null;
  status: 'open' | 'dismissed' | 'resolved';
  created_at: string;
}

export interface MapLayer {
  id: string;
  name: string;
  visible: boolean;
  type: MapLayerType;
}

export type MapLayerType =
  | 'base_terrain'
  | 'water'
  | 'elevation'
  | 'forests'
  | 'regions'
  | 'roads'
  | 'settlements'
  | 'labels'
  | 'journeys'
  | 'ui_overlay';

export interface MapStyle {
  id: string;
  name: string;
  description: string;
}

export const MAP_STYLES: MapStyle[] = [
  { id: 'medieval_parchment', name: 'Medieval Parchment', description: 'Classic fantasy map style' },
  { id: 'realistic_atlas', name: 'Realistic Atlas', description: 'Modern cartographic style' },
  { id: 'dark_fantasy', name: 'Dark Fantasy', description: 'Moody and atmospheric' },
  { id: 'high_fantasy', name: 'High Fantasy', description: 'Vibrant and magical' },
  { id: 'minimalist', name: 'Minimalist', description: 'Clean and simple' },
  { id: 'nautical_chart', name: 'Nautical Chart', description: 'Ocean-focused style' },
  { id: 'historical', name: 'Historical', description: 'Old-world map aesthetic' },
  { id: 'sci_fi_holographic', name: 'Sci-Fi Holographic', description: 'Futuristic digital style' },
];
