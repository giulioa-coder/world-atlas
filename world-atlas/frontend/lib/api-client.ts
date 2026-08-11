/**
 * API Client for making HTTP requests to the backend.
 */

// Custom error class for API errors
export class ApiClientError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = 'ApiClientError';
    this.status = status;
  }
}

// Generic paginated response type
export type PaginatedResponse<T> = {
  items: T[];
  total: number;
};

/**
 * Handle HTTP response and extract JSON data or throw error.
 */
export async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorMessage = response.statusText;
    
    // Try to parse error details from JSON response
    try {
      const errorData = await response.json();
      if (errorData.message || errorData.detail) {
        errorMessage = errorData.message || errorData.detail;
      } else if (typeof errorData === 'string') {
        errorMessage = errorData;
      }
    } catch {
      // If parsing fails, use statusText
    }
    
    throw new ApiClientError(errorMessage, response.status);
  }
  
  // Handle empty responses (e.g., 204 No Content)
  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/json')) {
    const text = await response.text();
    return text ? JSON.parse(text) : {} as T;
  }
  
  return {} as T;
}

/**
 * Make an HTTP request to the API.
 * 
 * @param endpoint - API endpoint (should include /api/v1/... prefix)
 * @param options - Fetch options
 * @returns Promise resolving to typed response data
 */
export async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const url = `${baseUrl}${endpoint}`;
  
  // Prepare headers
  const headers: HeadersInit = {
    ...options?.headers,
  };
  
  // Set Content-Type header when there's a body and it's not FormData
  if (options?.body && !(options.body instanceof FormData)) {
    if (typeof options.body === 'string' || options.body instanceof Object) {
      (headers as Record<string, string>)['Content-Type'] = 'application/json';
    }
  }
  
  const response = await fetch(url, {
    ...options,
    headers,
  });
  
  return handleResponse<T>(response);
}
