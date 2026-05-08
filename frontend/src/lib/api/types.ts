export interface ApiResponse<T = any> {
  code: number;
  message: string;
  data: T;
}

export interface User {
  id: number;
  email: string;
  username: string;
  created_at?: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
}

export interface LoginRequest {
  login: string;
  password: string;
}

export interface GithubSearchItem {
  id: number;
  name: string;
  full_name: string;
  description: string | null;
  html_url: string;
  stargazers_count: number;
  language: string | null;
  updated_at: string;
}

/** 合并搜索的单条记录（GitHub + Gitee） */
export type RepoSearchItem = GithubSearchItem & {
  source: 'github' | 'gitee';
};

export interface GithubSearchResponse {
  total_count: number;
  page: number;
  per_page: number;
  items: GithubSearchItem[];
}

/** GET /search/repos 单次请求两源合并 */
export interface MergedRepoSearchResponse {
  page: number;
  per_page: number;
  github_total_count: number;
  items: RepoSearchItem[];
  github_error?: string | null;
  gitee_error?: string | null;
}
