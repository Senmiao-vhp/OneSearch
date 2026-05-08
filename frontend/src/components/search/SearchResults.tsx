'use client';

import { useSearchStore } from '@/modules/search/store/searchStore';
import { GithubResultCard } from './GithubResultCard';
import { Pagination } from './Pagination';
import { useSearch } from '@/modules/search/hooks/useSearch';

const sourceConfig = {
  github: { title: 'GitHub 代码仓库', icon: '💻', color: 'gray' },
  csdn: { title: 'CSDN 技术博客', icon: '📚', color: 'orange' },
  gitee: { title: 'Gitee 代码仓库', icon: '🐱', color: 'red' },
  cnki: { title: '知网学术论文', icon: '📄', color: 'blue' },
};

type SourceKey = keyof typeof sourceConfig;

export function SearchResults() {
  const { activeTab, results, loading, searchBySource, query } = useSearchStore();

  const handlePageChange = (page: number) => {
    const source = activeTab === 'all' ? 'github' : activeTab;
    searchBySource(source as SourceKey, query, page);
  };

  if (activeTab === 'all') {
    const allResults = [
      ...results.github.items.map(item => ({ ...item, source: 'github' as const })),
      ...results.csdn.items.map(item => ({ ...item, source: 'csdn' as const })),
      ...results.gitee.items.map(item => ({ ...item, source: 'gitee' as const })),
      ...results.cnki.items.map(item => ({ ...item, source: 'cnki' as const })),
    ];

    return (
      <div className="space-y-8">
        {(['github', 'csdn', 'gitee', 'cnki'] as const).map((source) => {
          const config = sourceConfig[source];
          const sourceData = results[source];
          const isLoading = loading[source];

          if (sourceData.items.length === 0 && !isLoading) return null;

          return (
            <div key={source} className="space-y-4">
              <div className="flex items-center gap-2">
                <h2 className="text-lg font-semibold text-gray-800">
                  {config.icon} {config.title}
                </h2>
                <span className="text-sm text-gray-400">
                  共 {sourceData.total.toLocaleString()} 条结果
                </span>
              </div>

              {isLoading ? (
                <div className="space-y-4">
                  {[1, 2, 3].map((i) => (
                    <div key={i} className="p-4 bg-white rounded-xl border border-gray-100 animate-pulse">
                      <div className="h-5 bg-gray-200 rounded w-1/3 mb-3"></div>
                      <div className="h-4 bg-gray-200 rounded w-2/3 mb-2"></div>
                      <div className="h-3 bg-gray-100 rounded w-1/4"></div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="space-y-3">
                  {sourceData.items.slice(0, 5).map((item) => (
                    <GithubResultCard key={item.id} item={item} />
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>
    );
  }

  const config = sourceConfig[activeTab as SourceKey];
  const sourceData = results[activeTab as SourceKey];
  const isLoading = loading[activeTab as SourceKey];
  const totalPages = Math.ceil(sourceData.total / sourceData.per_page);

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <h2 className="text-xl font-semibold text-gray-800">
          {config.icon} {config.title}
        </h2>
        <span className="text-sm text-gray-400">
          共 {sourceData.total.toLocaleString()} 条结果
        </span>
      </div>

      {isLoading ? (
        <div className="space-y-4">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="p-5 bg-white rounded-xl border border-gray-100 animate-pulse">
              <div className="h-6 bg-gray-200 rounded w-1/3 mb-3"></div>
              <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div className="h-3 bg-gray-100 rounded w-1/4"></div>
            </div>
          ))}
        </div>
      ) : sourceData.items.length === 0 ? (
        <div className="text-center py-12 text-gray-400">
          <svg className="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p>未找到相关结果</p>
        </div>
      ) : (
        <>
          <div className="space-y-3">
            {sourceData.items.map((item) => (
              <GithubResultCard key={item.id} item={item} />
            ))}
          </div>
          <Pagination
            currentPage={sourceData.page}
            totalPages={totalPages}
            onPageChange={(page) => handlePageChange(page)}
          />
        </>
      )}
    </div>
  );
}
