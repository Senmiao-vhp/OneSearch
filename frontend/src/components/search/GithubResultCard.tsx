'use client';

import { SearchResult } from '@/modules/search/store/searchStore';

interface GithubResultCardProps {
  item: SearchResult;
}

export function GithubResultCard({ item }: GithubResultCardProps) {
  return (
    <a
      href={item.url}
      target="_blank"
      rel="noopener noreferrer"
      className="block p-4 bg-white rounded-xl border border-gray-100 
                 hover:border-blue-200 hover:shadow-lg hover:shadow-blue-500/10
                 transition-all duration-300 group"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-2">
            <svg className="w-5 h-5 text-gray-700" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
            </svg>
            <h3 className="text-lg font-semibold text-blue-600 truncate group-hover:text-blue-700">
              {item.title}
            </h3>
          </div>
          {item.description && (
            <p className="text-gray-600 text-sm line-clamp-2 mb-3">
              {item.description}
            </p>
          )}
          <div className="flex items-center gap-4 text-xs text-gray-400">
            {item.extra?.language && (
              <span className="flex items-center gap-1">
                <span className="w-3 h-3 rounded-full bg-blue-500"></span>
                {item.extra.language}
              </span>
            )}
            {item.extra?.stargazers_count && (
              <span className="flex items-center gap-1">
                ⭐ {item.extra.stargazers_count.toLocaleString()}
              </span>
            )}
            {item.extra?.updated_at && (
              <span>Updated {new Date(item.extra.updated_at).toLocaleDateString('zh-CN')}</span>
            )}
          </div>
        </div>
        <div className="shrink-0 text-blue-500 opacity-0 group-hover:opacity-100 transition-opacity">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
        </div>
      </div>
    </a>
  );
}
