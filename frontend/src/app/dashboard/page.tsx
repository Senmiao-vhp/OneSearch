'use client';

import { useAuth } from '@/modules/auth/hooks/useAuth';
import Link from 'next/link';

export default function DashboardPage() {
  const { user, isLoading, logout, isLoggingOut } = useAuth();

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-500 border-t-transparent"></div>
          <p className="mt-2 text-gray-600">加载中...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-center">
          <p className="text-gray-600 mb-4">请先登录</p>
          <Link
            href="/auth/login"
            className="text-blue-600 hover:underline"
          >
            前往登录
          </Link>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen py-8 px-4">
      <div className="container mx-auto max-w-4xl">
        <h1 className="text-2xl font-bold mb-8">用户面板</h1>
        
        <div className="bg-white shadow rounded-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">个人信息</h2>
          <div className="space-y-2">
            <p>
              <span className="text-gray-600">用户名：</span>
              {user.username}
            </p>
            <p>
              <span className="text-gray-600">邮箱：</span>
              {user.email}
            </p>
            {user.created_at && (
              <p>
                <span className="text-gray-600">注册时间：</span>
                {new Date(user.created_at).toLocaleString('zh-CN')}
              </p>
            )}
          </div>
        </div>

        <div className="mb-6">
          <button
            onClick={() => logout()}
            disabled={isLoggingOut}
            className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoggingOut ? '登出中...' : '退出登录'}
          </button>
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">功能预留</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-gray-100 p-4 rounded">
              <h3 className="font-medium">搜索历史</h3>
              <p className="text-gray-500 text-sm mt-1">功能开发中...</p>
            </div>
            <div className="bg-gray-100 p-4 rounded">
              <h3 className="font-medium">收藏夹</h3>
              <p className="text-gray-500 text-sm mt-1">功能开发中...</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
