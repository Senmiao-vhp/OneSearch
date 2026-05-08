import axios, { AxiosInstance, AxiosError, isAxiosError } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true,
    });

    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (isAxiosError(error) && error.code === 'ECONNABORTED') {
          return Promise.reject(new Error('请求超时，合并搜索需访问 GitHub 与 Gitee，请稍后重试或检查网络'));
        }
        if (
          isAxiosError(error) &&
          typeof error.message === 'string' &&
          error.message.toLowerCase().includes('timeout')
        ) {
          return Promise.reject(new Error('请求超时，合并搜索需访问 GitHub 与 Gitee，请稍后重试或检查网络'));
        }
        const message = (error.response?.data as any)?.message || error.message;
        return Promise.reject(new Error(message));
      }
    );
  }

  async get<T>(
    url: string,
    params?: Record<string, any>,
    options?: { timeout?: number }
  ): Promise<T> {
    const response = await this.client.get<T>(url, {
      params,
      ...(options?.timeout != null ? { timeout: options.timeout } : {}),
    });
    return response.data;
  }

  async post<T>(url: string, data?: Record<string, any>): Promise<T> {
    const response = await this.client.post<T>(url, data);
    return response.data;
  }

  async put<T>(url: string, data?: Record<string, any>): Promise<T> {
    const response = await this.client.put<T>(url, data);
    return response.data;
  }

  async delete<T>(url: string): Promise<T> {
    const response = await this.client.delete<T>(url);
    return response.data;
  }
}

export const apiClient = new ApiClient();
