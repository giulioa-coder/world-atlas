/**
 * API object for thin wrapper access to services.
 * Used by components like ManuscriptUploader.
 */

import { manuscriptService } from '@/services';

export const api = {
  manuscripts: {
    upload: manuscriptService.upload.bind(manuscriptService),
  },
};
