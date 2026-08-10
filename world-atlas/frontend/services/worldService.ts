/**
 * World API service.
 */

import { request, handleResponse, PaginatedResponse } from '@/lib/api-client';
import { World } from '@/types';

export interface WorldCreateInput {
  name: string;
  description?: string;
  genre?: string;
  visual_style?: string;
  scale_km_per_unit?: number;
}

export interface WorldUpdateInput {
  name?: string;
  description?: string;
  genre?: string;
  visual_style?: string;
  scale_km_per_unit?: number;
}

export const worldService = {
  /**
   * List all worlds with pagination.
   */
  list: async (skip = 0, limit = 100): Promise<PaginatedResponse<World>> => {
    return request<PaginatedResponse<World>>(`/api/v1/worlds/?skip=${skip}&limit=${limit}`);
  },

  /**
   * Get a single world by ID.
   */
  get: async (id: string): Promise<World> => {
    return request<World>(`/api/v1/worlds/${id}`);
  },

  /**
   * Create a new world.
   */
  create: async (data: WorldCreateInput): Promise<World> => {
    return request<World>('/api/v1/worlds/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Update an existing world.
   */
  update: async (id: string, data: WorldUpdateInput): Promise<World> => {
    return request<World>(`/api/v1/worlds/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete a world.
   */
  delete: async (id: string): Promise<void> => {
    await request<void>(`/api/v1/worlds/${id}`, {
      method: 'DELETE',
    });
  },

  /**
   * Search worlds by name or description.
   */
  search: async (query: string): Promise<World[]> => {
    return request<World[]>(`/api/v1/worlds/search?q=${encodeURIComponent(query)}`);
  },
};
