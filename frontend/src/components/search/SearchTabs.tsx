'use client';

import { useSearchStore, TabType } from '@/modules/search/store/searchStore';

const tabs: { key: TabType; label: string; icon: string }[] = [
  { key: 'all', label: '全部', icon: '🌐' },
  { key: 'github', label: 'GitHub', icon: '💻' },
  { key: 'csdn', label: 'CSDN', icon: '📚' },
  { key: 'gitee', label: 'Gitee', icon: '🐱' },
  { key: 'cnki', label: '知网', icon: '📄' },
];

export function SearchTabs() {
  const { activeTab, setActiveTab, results, hasSearched } = useSearchStore();

  if (!hasSearched) {
    return (
      <div className="flex items-center justify-center gap-2 py-3">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            disabled
            className="px-4 py-2 text-sm font-medium rounded-full
                       bg-gray-100 text-gray-400 cursor-not-allowed"
          >
            {tab.icon} {tab.label}
          </button>
        ))}
      </div>
    );
  }

  const getTotalResults = () => {
    return results.github.total + results.csdn.total + results.gitee.total + results.cnki.total;
  };

  return (
    <div className="flex items-center justify-center gap-2 py-4 border-b border-gray-100 overflow-x-auto">
      {tabs.map((tab) => {
        const isActive = activeTab === tab.key;
        const count = tab.key === 'all' 
          ? getTotalResults() 
          : results[tab.key as keyof typeof results]?.total || 0;

        return (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`
              px-5 py-2 text-sm font-medium rounded-full whitespace-nowrap
              transition-all duration-200 flex items-center gap-2
              ${isActive 
                ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30' 
                : 'bg-white text-gray-600 border border-gray-200 hover:border-blue-300 hover:text-blue-600'
              }
            `}
          >
            <span>{tab.icon}</span>
            <span>{tab.label}</span>
            {count > 0 && (
              <span className={`
                text-xs px-1.5 py-0.5 rounded-full
                ${isActive ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-500'}
              `}>
                {count > 9999 ? '9999+' : count.toLocaleString()}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
}
