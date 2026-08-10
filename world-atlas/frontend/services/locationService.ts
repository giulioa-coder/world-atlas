/**
 * Location API service.
 */

import { request, PaginatedResponse } from './api-client';
import { Location, LocationType, LocationStatus } from '@/types';

export interface LocationCreateInput {
  name: string;
  location_type: LocationType;
  latitude?: number;
  longitude?: number;
  elevation?: number;
  description?: string;
  visual_description?: string;
  importance?: number;
  extra_data?: Record<string, any>;
}

export interface LocationUpdateInput {
  name?: string;
  location_type?: LocationType;
  latitude?: number;
  longitude?: number;
  elevation?: number;
  description?: string;
  visual_description?: string;
  importance?: number;
  status?: LocationStatus;
  confidence?: number;
  extra_data?: Record<string, any>;
}

export const locationService = {
  /**
   * List all locations for a world.
   */
  list: async (worldId: string): Promise<Location[]> => {
    return request<Location[]>(`/api/v1/locations/?world_id=${worldId}`);
  },

  /**
   * Get a single location by ID.
   */
  get: async (worldId: string, id: string): Promise<Location> => {
    return request<Location>(`/api/v1/locations/${id}`);
  },

  /**
   * Create a new location.
   */
  create: async (worldId: string, data: LocationCreateInput): Promise<Location> => {
    return request<Location>(`/api/v1/locations/?world_id=${worldId}`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Update an existing location.
   */
  update: async (worldId: string, id: string, data: LocationUpdateInput): Promise<Location> => {
    return request<Location>(`/api/v1/locations/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete a location.
   */
  delete: async (worldId: string, id: string): Promise<void> => {
    await request<void>(`/api/v1/locations/${id}`, {
      method: 'DELETE',
    });
  },

  /**
   * Update location coordinates.
   */
  updatePosition: async (
    worldId: string,
    id: string,
    latitude: number,
    longitude: number
  ): Promise<Location> => {
    return request<Location>(`/api/v1/locations/${id}/position`, {
      method: 'PATCH',
      body: JSON.stringify({ latitude, longitude }),
    });
  },

  /**
   * Get locations by type.
   */
  getByType: async (worldId: string, type: LocationType): Promise<Location[]> => {
    return request<Location[]>(`/api/v1/locations/?world_id=${worldId}&type=${type}`);
  },

  /**
   * Search locations by name.
   */
  search: async (worldId: string, query: string): Promise<Location[]> => {
    return request<Location[]>(`/api/v1/locations/search?world_id=${worldId}&q=${encodeURIComponent(query)}`);
  },
};
