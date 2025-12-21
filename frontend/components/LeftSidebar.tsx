"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Compass, Search, Clock, Settings, Zap } from "lucide-react";

export default function LeftSidebar() {
  const pathname = usePathname();

  const menuItems = [
    { id: "/", icon: Search, label: "搜索" },
    { id: "/explore", icon: Compass, label: "探索" },
    { id: "/history", icon: Clock, label: "历史" },
  ];

  return (
    <aside className="w-64 border-r border-gray-100 h-screen flex flex-col bg-white sticky top-0 overflow-y-auto shrink-0">
      {/* Logo */}
      <div className="p-6 mb-8 flex items-center gap-2">
        <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center text-white">
          <Zap size={18} fill="currentColor" />
        </div>
        <Link
          href="/"
          className="text-xl font-bold text-primary tracking-tight"
        >
          RadarZ
        </Link>
      </div>

      {/* Navigation Menu */}
      <nav className="flex-1 px-4 space-y-2">
        {menuItems.map((item) => {
          const isActive = pathname === item.id;
          return (
            <Link
              key={item.id}
              href={item.id}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group ${
                isActive
                  ? "bg-primary/10 text-primary font-semibold shadow-sm shadow-primary/5"
                  : "text-gray-500 hover:bg-gray-50 hover:text-gray-900"
              }`}
            >
              <item.icon
                size={20}
                className={
                  isActive
                    ? "text-primary"
                    : "text-gray-400 group-hover:text-gray-600"
                }
              />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Settings */}
      <div className="p-4 mt-auto border-t border-gray-50">
        <Link
          href="/settings"
          className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
            pathname === "/settings"
              ? "bg-gray-100 text-gray-900 font-semibold"
              : "text-gray-500 hover:bg-gray-50"
          }`}
        >
          <Settings size={20} />
          <span>设置</span>
        </Link>
      </div>
    </aside>
  );
}
