/**
 * Manuscript API service.
 */

import { request } from './api-client';
import { Manuscript } from '@/types';

export interface ManuscriptUploadResponse {
  id: string;
  title: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
}

export const manuscriptService = {
  /**
   * List all manuscripts for a world.
   */
  list: async (worldId: string): Promise<Manuscript[]> => {
    return request<Manuscript[]>(`/api/v1/manuscripts/?world_id=${worldId}`);
  },

  /**
   * Get a single manuscript by ID.
   */
  get: async (worldId: string, id: string): Promise<Manuscript> => {
    return request<Manuscript>(`/api/v1/manuscripts/${id}`);
  },

  /**
   * Upload a new manuscript.
   */
  upload: async (worldId: string, file: File): Promise<Manuscript> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', file.name);

    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/manuscripts/?world_id=${worldId}`,
      {
        method: 'POST',
        body: formData,
      }
    );

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ message: 'Upload failed' }));
      throw new Error(errorData.message || 'Failed to upload manuscript');
    }

    return response.json();
  },

  /**
   * Delete a manuscript.
   */
  delete: async (worldId: string, id: string): Promise<void> => {
    await request<void>(`/api/v1/manuscripts/${id}`, {
      method: 'DELETE',
    });
  },

  /**
   * Get manuscript processing status.
   */
  getStatus: async (id: string): Promise<Manuscript> => {
    return request<Manuscript>(`/api/v1/manuscripts/${id}/status`);
  },
};
