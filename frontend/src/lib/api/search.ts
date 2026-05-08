import { apiClient } from './client';
import { MergedRepoSearchResponse } from './types';

export interface SearchParams {
  q: string;
  page?: number;
  per_page?: number;
}

/** 单次请求拉取 GitHub + Gitee 合并结果；需等双上游，单独放宽超时（毫秒） */
const SEARCH_MERGED_TIMEOUT_MS = 90_000;

export const searchApi = {
  searchReposMerged: async (
    params: SearchParams
  ): Promise<MergedRepoSearchResponse> => {
    return apiClient.get('/search/repos', params, {
      timeout: SEARCH_MERGED_TIMEOUT_MS,
    });
  },
};
