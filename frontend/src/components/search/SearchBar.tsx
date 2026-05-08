'use client';

import { useState, FormEvent } from 'react';
import { useSearchStore } from '@/modules/search/store/searchStore';

export function SearchBar() {
  const [inputValue, setInputValue] = useState('');
  const { query, setQuery, searchAll, hasSearched, loading } = useSearchStore();

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      setQuery(inputValue.trim());
      searchAll(inputValue.trim());
    }
  };

  const isLoading = loading.github || loading.csdn || loading.gitee || loading.cnki;

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <div className="relative flex items-center">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="搜索代码仓库、技术博客、学术论文..."
          className="w-full px-5 py-4 pr-24 text-lg border-2 border-gray-200 rounded-full 
                     focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 
                     outline-none transition-all duration-300
                     placeholder:text-gray-400"
        />
        <button
          type="submit"
          disabled={isLoading || !inputValue.trim()}
          className="absolute right-2 px-6 py-2 bg-blue-600 text-white font-medium rounded-full
                     hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed
                     transition-colors duration-200 flex items-center gap-2"
        >
          {isLoading ? (
            <>
              <svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              搜索中
            </>
          ) : (
            <>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              搜索
            </>
          )}
        </button>
      </div>
    </form>
  );
}
