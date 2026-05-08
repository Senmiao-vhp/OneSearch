import { apiClient } from './client';
import { MergedRepoSearchResponse } from './types';

export interface SearchParams {
  q: string;
  page?: number;
  per_page?: number;
}

/** 单次请求拉取 GitHub + Gitee 合并结果 */
export const searchApi = {
  searchReposMerged: async (
    params: SearchParams
  ): Promise<MergedRepoSearchResponse> => {
    return apiClient.get('/search/repos', params);
  },
};
