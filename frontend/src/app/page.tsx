import { SearchBar } from '@/components/search/SearchBar';

export default function HomePage() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-4">
      <h1 className="text-4xl font-bold mb-4 text-center">OneSearch 一搜</h1>
      <p className="text-xl text-gray-600 mb-8 text-center">
        开发者一站式信息搜索工具
      </p>
      <SearchBar />
    </main>
  );
}
