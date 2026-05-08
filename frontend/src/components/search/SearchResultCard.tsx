import { RepoSearchItem } from '@/lib/api/types';

interface SearchResultCardProps {
  item: RepoSearchItem;
}

const SOURCE_LABEL: Record<RepoSearchItem['source'], string> = {
  github: 'GitHub',
  gitee: 'Gitee',
};

export function SearchResultCard({ item }: SearchResultCardProps) {
  return (
    <a
      href={item.html_url}
      target="_blank"
      rel="noopener noreferrer"
      className="block p-4 border border-gray-200 rounded-lg hover:shadow-lg transition-shadow bg-white"
    >
      <div className="flex justify-between items-start gap-4">
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-semibold text-blue-600 truncate">
            {item.full_name}
          </h3>
          <p className="mt-2 text-gray-600 line-clamp-2">
            {item.description || '暂无描述'}
          </p>
        </div>
        <div className="flex items-center gap-4 text-sm text-gray-500 shrink-0">
          <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-100 text-slate-700 border border-slate-200">
            {SOURCE_LABEL[item.source]}
          </span>
          <span className="flex items-center gap-1">
            <span>⭐</span>
            <span>{item.stargazers_count.toLocaleString()}</span>
          </span>
          {item.language && (
            <span className="px-2 py-1 bg-gray-100 rounded text-xs">
              {item.language}
            </span>
          )}
        </div>
      </div>
    </a>
  );
}
