"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Compass, Search } from "lucide-react";

export default function LeftSidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 h-screen w-60 bg-sidebar flex flex-col">
      {/* Logo */}
      <div className="p-6">
        <Link
          href="/"
          className="flex items-center gap-3 text-2xl font-bold text-primary"
        >
          <img src="/logo.svg" alt="RadarZ Logo" className="w-8 h-8 shrink-0" />
          <span>RadarZ</span>
        </Link>
      </div>

      {/* Navigation Menu */}
      <nav className="flex-1 px-4">
        <ul className="space-y-2">
          <li>
            <Link
              href="/"
              className={`flex items-center gap-3 px-4 py-2 rounded-lg font-medium transition-colors ${
                pathname === "/"
                  ? "bg-gray-100 text-foreground"
                  : "text-gray-600 hover:text-foreground"
              }`}
            >
              <Search className="w-5 h-5" />
              <span>搜索</span>
            </Link>
          </li>
          <li>
            <Link
              href="/explore"
              className={`flex items-center gap-3 px-4 py-2 rounded-lg font-medium transition-colors ${
                pathname === "/explore"
                  ? "bg-gray-100 text-foreground"
                  : "text-gray-600 hover:text-foreground"
              }`}
            >
              <Compass className="w-5 h-5" />
              <span>探索</span>
            </Link>
          </li>
        </ul>
      </nav>

      {/* User Profile */}
      <div className="p-4">
        <div className="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center">
          <span className="text-white font-semibold">N</span>
        </div>
      </div>
    </aside>
  );
}
