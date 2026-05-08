import { useSearchStore } from '@/modules/search/store/searchStore';

export function useSearch() {
  const store = useSearchStore();
  return store;
}
