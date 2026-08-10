/**
 * Character API service.
 */

import { request } from './api-client';
import { Character } from '@/types';

export interface CharacterCreateInput {
  name: string;
  description?: string;
  role?: string;
}

export const characterService = {
  /**
   * List all characters for a world.
   */
  list: async (worldId: string): Promise<Character[]> => {
    return request<Character[]>(`/api/v1/characters/?world_id=${worldId}`);
  },

  /**
   * Get a single character by ID.
   */
  get: async (worldId: string, id: string): Promise<Character> => {
    return request<Character>(`/api/v1/characters/${id}`);
  },

  /**
   * Create a new character.
   */
  create: async (worldId: string, data: CharacterCreateInput): Promise<Character> => {
    return request<Character>(`/api/v1/characters/?world_id=${worldId}`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Update an existing character.
   */
  update: async (worldId: string, id: string, data: Partial<CharacterCreateInput>): Promise<Character> => {
    return request<Character>(`/api/v1/characters/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete a character.
   */
  delete: async (worldId: string, id: string): Promise<void> => {
    await request<void>(`/api/v1/characters/${id}`, {
      method: 'DELETE',
    });
  },

  /**
   * Search characters by name.
   */
  search: async (worldId: string, query: string): Promise<Character[]> => {
    return request<Character[]>(`/api/v1/characters/search?world_id=${worldId}&q=${encodeURIComponent(query)}`);
  },
};
