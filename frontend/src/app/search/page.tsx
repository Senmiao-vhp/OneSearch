'use client';

import { useSearch } from '@/modules/search/hooks/useSearch';
import { SearchResultList } from '@/components/search/SearchResultList';
import { SearchBar } from '@/components/search/SearchBar';

export default function SearchPage() {
  const { results, isLoading, error } = useSearch();

  return (
    <main className="min-h-screen py-8 px-4">
      <div className="container mx-auto max-w-4xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold mb-2">OneSearch 一搜</h1>
          <p className="text-gray-600 mb-8">开发者一站式信息搜索工具</p>
          <SearchBar />
        </div>

        {isLoading && (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-500 border-t-transparent"></div>
            <p className="mt-2 text-gray-600">搜索中...</p>
          </div>
        )}
        
        {error && (
          <div className="text-center py-8 text-red-500">
            搜索失败: {error.message}
          </div>
        )}

        {!isLoading && !error && <SearchResultList results={results} />}
      </div>
    </main>
  );
}
