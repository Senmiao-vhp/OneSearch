'use client';

import { RegisterForm } from '@/components/auth/RegisterForm';
import Link from 'next/link';

export default function RegisterPage() {
  return (
    <main className="min-h-screen flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold mb-2">注册 OneSearch</h1>
          <p className="text-gray-600">开发者一站式信息搜索工具</p>
        </div>
        <div className="bg-white shadow-lg rounded-lg p-8">
          <RegisterForm />
          <p className="mt-6 text-center text-gray-600">
            已有账号?{' '}
            <Link href="/auth/login" className="text-blue-600 hover:underline">
              立即登录
            </Link>
          </p>
        </div>
      </div>
    </main>
  );
}
