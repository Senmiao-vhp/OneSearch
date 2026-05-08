import { SearchResultCard } from './SearchResultCard';
import { GithubSearchResponse } from '@/lib/api/types';

interface SearchResultListProps {
  results: GithubSearchResponse | undefined;
}

export function SearchResultList({ results }: SearchResultListProps) {
  if (!results) return null;

  if (results.items.length === 0) {
    return <div className="text-center py-8 text-gray-500">未找到相关结果</div>;
  }

  return (
    <div className="space-y-4">
      <div className="text-gray-500">
        找到 {results.total_count.toLocaleString()} 个结果
      </div>
      {results.items.map((item) => (
        <SearchResultCard key={item.id} item={item} />
      ))}
    </div>
  );
}
