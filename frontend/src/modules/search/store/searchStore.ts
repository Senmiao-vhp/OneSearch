import { create } from 'zustand';
import { searchApi } from '@/lib/api';

export type TabType = 'all' | 'github' | 'csdn' | 'gitee' | 'cnki';

export interface SearchResult {
  id: number | string;
  title: string;
  description?: string;
  url: string;
  extra?: Record<string, any>;
}

export interface SearchResults {
  github: {
    items: SearchResult[];
    total: number;
    page: number;
    per_page: number;
  };
  csdn: {
    items: SearchResult[];
    total: number;
    page: number;
    per_page: number;
  };
  gitee: {
    items: SearchResult[];
    total: number;
    page: number;
    per_page: number;
  };
  cnki: {
    items: SearchResult[];
    total: number;
    page: number;
    per_page: number;
  };
}

interface SearchState {
  query: string;
  activeTab: TabType;
  results: SearchResults;
  loading: Record<keyof Omit<SearchResults, 'total'>, boolean>;
  hasSearched: boolean;
  
  setQuery: (query: string) => void;
  setActiveTab: (tab: TabType) => void;
  searchAll: (query: string) => Promise<void>;
  searchBySource: (source: keyof Omit<SearchResults, 'total'>, query: string, page?: number) => Promise<void>;
  reset: () => void;
}

const initialResults = {
  github: { items: [], total: 0, page: 1, per_page: 10 },
  csdn: { items: [], total: 0, page: 1, per_page: 10 },
  gitee: { items: [], total: 0, page: 1, per_page: 10 },
  cnki: { items: [], total: 0, page: 1, per_page: 10 },
};

export const useSearchStore = create<SearchState>((set, get) => ({
  query: '',
  activeTab: 'all',
  results: initialResults,
  loading: {
    github: false,
    csdn: false,
    gitee: false,
    cnki: false,
  },
  hasSearched: false,

  setQuery: (query) => set({ query }),

  setActiveTab: (tab) => set({ activeTab: tab }),

  searchBySource: async (source, query, page = 1) => {
    if (!query.trim()) return;

    set((state) => ({
      loading: { ...state.loading, [source]: true },
    }));

    try {
      if (source === 'github') {
        const response = await searchApi.searchGithub({
          q: query,
          page,
          per_page: 10,
        });
        set((state) => ({
          results: {
            ...state.results,
            github: {
              items: response.data?.items || [],
              total: response.data?.total_count || 0,
              page,
              per_page: 10,
            },
          },
        }));
      } else if (source === 'csdn') {
        const response = await searchApi.searchCsdn({
          q: query,
          page,
          per_page: 10,
        });
        set((state) => ({
          results: {
            ...state.results,
            csdn: {
              items: response.data?.items || [],
              total: response.data?.total || 0,
              page,
              per_page: 10,
            },
          },
        }));
      } else if (source === 'gitee') {
        const response = await searchApi.searchGitee({
          q: query,
          page,
          per_page: 10,
        });
        set((state) => ({
          results: {
            ...state.results,
            gitee: {
              items: response.data?.items || [],
              total: response.data?.total || 0,
              page,
              per_page: 10,
            },
          },
        }));
      } else if (source === 'cnki') {
        const response = await searchApi.searchCnki({
          q: query,
          page,
          per_page: 10,
        });
        set((state) => ({
          results: {
            ...state.results,
            cnki: {
              items: response.data?.items || [],
              total: response.data?.total || 0,
              page,
              per_page: 10,
            },
          },
        }));
      }
    } catch (error) {
      console.error(`Search ${source} failed:`, error);
    } finally {
      set((state) => ({
        loading: { ...state.loading, [source]: false },
      }));
    }
  },

  searchAll: async (query) => {
    if (!query.trim()) return;

    set({ hasSearched: true, activeTab: 'all' });
    
    const sources: (keyof Omit<SearchResults, 'total'>)[] = ['github', 'csdn', 'gitee', 'cnki'];
    
    await Promise.all(
      sources.map((source) => get().searchBySource(source, query, 1))
    );
  },

  reset: () =>
    set({
      query: '',
      activeTab: 'all',
      results: initialResults,
      loading: { github: false, csdn: false, gitee: false, cnki: false },
      hasSearched: false,
    }),
}));
