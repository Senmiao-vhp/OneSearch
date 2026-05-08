'use client';

import { Header } from '@/components/layout/Header';
import { SearchBar } from '@/components/search/SearchBar';
import { SearchTabs } from '@/components/search/SearchTabs';
import { SearchResults } from '@/components/search/SearchResults';
import { useSearchStore } from '@/modules/search/store/searchStore';

export default function HomePage() {
  const { hasSearched } = useSearchStore();

  return (
    <div className="min-h-screen bg-slate-50">
      <Header />
      
      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-3 bg-gradient-to-r from-blue-600 to-blue-500 bg-clip-text text-transparent">
            OneSearch 一搜
          </h1>
          <p className="text-lg text-gray-500 mb-8">
            开发者一站式信息搜索工具
          </p>
          <SearchBar />
        </div>

        <SearchTabs />

        <div className="mt-6">
          {hasSearched ? (
            <SearchResults />
          ) : (
            <div className="text-center py-16">
              <div className="w-24 h-24 mx-auto mb-6 bg-gradient-to-br from-blue-100 to-blue-50 rounded-full flex items-center justify-center">
                <svg className="w-12 h-12 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <h2 className="text-xl font-semibold text-gray-700 mb-2">
                开始搜索
              </h2>
              <p className="text-gray-400 max-w-md mx-auto">
                输入关键词，同时搜索 GitHub、CSDN、Gitee、知网 四大平台
              </p>
            </div>
          )}
        </div>
      </main>

      <footer className="border-t border-gray-200 py-6 mt-auto">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-gray-400">
          <p>OneSearch 一搜 · 让搜索更简单</p>
        </div>
      </footer>
    </div>
  );
}
