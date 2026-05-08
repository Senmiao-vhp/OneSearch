'use client';

import { LoginForm } from '@/components/auth/LoginForm';
import Link from 'next/link';

export default function LoginPage() {
  return (
    <main className="min-h-screen flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold mb-2">登录 OneSearch</h1>
          <p className="text-gray-600">开发者一站式信息搜索工具</p>
        </div>
        <div className="bg-white shadow-lg rounded-lg p-8">
          <LoginForm />
          <p className="mt-6 text-center text-gray-600">
            还没有账号?{' '}
            <Link href="/auth/register" className="text-blue-600 hover:underline">
              立即注册
            </Link>
          </p>
        </div>
      </div>
    </main>
  );
}
