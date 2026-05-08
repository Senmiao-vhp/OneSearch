import { apiClient } from './client';
import {
  GithubSearchResponse,
  CsdnSearchResponse,
  GiteeSearchResponse,
  CnkiSearchResponse,
  GithubSearchItem,
  CsdnSearchItem,
  GiteeSearchItem,
  CnkiSearchItem,
} from './types';

export interface SearchParams {
  q: string;
  page?: number;
  per_page?: number;
}

export const searchApi = {
  searchGithub: async (params: SearchParams): Promise<{ code: number; message: string; data: GithubSearchResponse }> => {
    const response = await apiClient.get<GithubSearchResponse>('/search/github', params);
    return {
      code: 0,
      message: 'success',
      data: response,
    };
  },

  searchCsdn: async (params: SearchParams): Promise<{ code: number; message: string; data: CsdnSearchResponse }> => {
    const response = await apiClient.get<CsdnSearchResponse>('/search/csdn', params);
    return {
      code: 0,
      message: 'success',
      data: response,
    };
  },

  searchGitee: async (params: SearchParams): Promise<{ code: number; message: string; data: GiteeSearchResponse }> => {
    const response = await apiClient.get<GiteeSearchResponse>('/search/gitee', params);
    return {
      code: 0,
      message: 'success',
      data: response,
    };
  },

  searchCnki: async (params: SearchParams): Promise<{ code: number; message: string; data: CnkiSearchResponse }> => {
    const response = await apiClient.get<CnkiSearchResponse>('/search/cnki', params);
    return {
      code: 0,
      message: 'success',
      data: response,
    };
  },
};
