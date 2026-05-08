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

export interface CsdnSearchItem {
  id: string;
  title: string;
  description?: string;
  url: string;
  author?: string;
  publish_time?: string;
  views?: number;
}

export interface GiteeSearchItem {
  id: number;
  name: string;
  full_name: string;
  description: string | null;
  html_url: string;
  stargazers_count: number;
  language: string | null;
  updated_at: string;
}

export interface CnkiSearchItem {
  id: string;
  title: string;
  authors?: string[];
  journal?: string;
  year?: number;
  keywords?: string[];
  abstract?: string;
  url?: string;
}

export interface GithubSearchResponse {
  total_count: number;
  page: number;
  per_page: number;
  items: GithubSearchItem[];
}

export interface CsdnSearchResponse {
  total: number;
  page: number;
  per_page: number;
  items: CsdnSearchItem[];
}

export interface GiteeSearchResponse {
  total: number;
  page: number;
  per_page: number;
  items: GiteeSearchItem[];
}

export interface CnkiSearchResponse {
  total: number;
  page: number;
  per_page: number;
  items: CnkiSearchItem[];
}
