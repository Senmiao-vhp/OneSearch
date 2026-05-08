import { useQuery } from '@tanstack/react-query';
import { searchApi, SearchParams } from '@/lib/api/search';
import { useSearchParams } from 'next/navigation';

export function useSearch() {
  const searchParams = useSearchParams();
  const query = searchParams.get('q') || '';
  const page = parseInt(searchParams.get('page') || '1');

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['search', 'github', query, page],
    queryFn: () => searchApi.searchGithub({ q: query, page, per_page: 10 }),
    enabled: !!query,
  });

  return {
    results: data?.data,
    isLoading,
    error,
    refetch,
  };
}
