import { apiClient } from './client';
import { ApiResponse, GithubSearchResponse } from './types';

export interface SearchParams {
  q: string;
  page?: number;
  per_page?: number;
}

export const searchApi = {
  searchGithub: async (params: SearchParams): Promise<ApiResponse<GithubSearchResponse>> => {
    return apiClient.get('/search/github', params);
  },
};
