import { apiClient } from './client';
import { ApiResponse, User, RegisterRequest, LoginRequest } from './types';

export const authApi = {
  register: async (data: RegisterRequest): Promise<ApiResponse<User>> => {
    return apiClient.post('/auth/register', data);
  },

  login: async (data: LoginRequest): Promise<ApiResponse<User>> => {
    return apiClient.post('/auth/login', data);
  },

  logout: async (): Promise<ApiResponse<null>> => {
    return apiClient.post('/auth/logout');
  },

  getCurrentUser: async (): Promise<ApiResponse<User>> => {
    return apiClient.get('/auth/me');
  },
};
