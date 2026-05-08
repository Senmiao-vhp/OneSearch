import { SearchResultCard } from './SearchResultCard';
import { MergedRepoSearchResponse } from '@/lib/api/types';

interface SearchResultListProps {
  results: MergedRepoSearchResponse | undefined;
}

export function SearchResultList({ results }: SearchResultListProps) {
  if (!results) return null;

  const { items, github_total_count, github_error, gitee_error } = results;

  if (items.length === 0) {
    return <div className="text-center py-8 text-gray-500">未找到相关结果</div>;
  }

  return (
    <div className="space-y-4">
      {(github_error || gitee_error) && (
        <div className="rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-900">
          {github_error && <p>GitHub：{github_error}</p>}
          {gitee_error && <p>Gitee：{gitee_error}</p>}
        </div>
      )}
      <div className="text-gray-500">
        GitHub 索引约 {github_total_count.toLocaleString()} 条；本页合并展示 {items.length} 条（按 Star 排序）
      </div>
      {items.map((item) => (
        <SearchResultCard key={`${item.source}-${item.id}`} item={item} />
      ))}
    </div>
  );
}
