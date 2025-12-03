"use client";

import Link from "next/link";
import { Compass, TrendingUp, LogIn } from "lucide-react";

export default function LeftSidebar() {
  return (
    <aside className="fixed left-0 top-0 h-screen w-60 bg-[#F9FAFB] border-r border-gray-100 flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-gray-100">
        <Link href="/" className="text-2xl font-bold text-[#B92B27]">
          RadarZ
        </Link>
      </div>

      {/* Navigation Menu */}
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          <li>
            <Link
              href="/"
              className="flex items-center gap-3 px-4 py-2 rounded-lg bg-white text-gray-900 font-medium hover:bg-gray-50 transition-colors"
            >
              <Compass className="w-5 h-5" />
              <span>Explore</span>
            </Link>
          </li>
          <li>
            <Link
              href="/trending"
              className="flex items-center gap-3 px-4 py-2 rounded-lg text-gray-700 hover:bg-white transition-colors"
            >
              <TrendingUp className="w-5 h-5" />
              <span>Trending Repos</span>
            </Link>
          </li>
          <li>
            <Link
              href="/signin"
              className="flex items-center gap-3 px-4 py-2 rounded-lg text-gray-700 hover:bg-white transition-colors"
            >
              <LogIn className="w-5 h-5" />
              <span>Sign In</span>
            </Link>
          </li>
        </ul>
      </nav>
    </aside>
  );
}
