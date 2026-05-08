import { apiClient } from './client';
import { GithubSearchResponse } from './types';

export interface SearchParams {
  q: string;
  page?: number;
  per_page?: number;
}

/** 与 FastAPI GithubSearchResponse 一致，直连 JSON，无外层 { code, data } */
export const searchApi = {
  searchGithub: async (params: SearchParams): Promise<GithubSearchResponse> => {
    return apiClient.get('/search/github', params);
  },
};
