"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import { Compass, Search, Clock, Settings, Radar } from "lucide-react";

export default function LeftSidebar() {
  const pathname = usePathname();

  const menuItems = [
    { id: "/", icon: Search, label: "搜索" },
    { id: "/explore", icon: Compass, label: "探索" },
    { id: "/history", icon: Clock, label: "历史" },
  ];

  return (
    <div className="w-64 bg-white border-r border-gray-100 flex flex-col p-4 z-10">
      <div className="flex items-center gap-3 px-4 py-6 mb-8">
        <div className="w-8 h-8 bg-emerald-600 rounded-lg flex items-center justify-center">
          <Radar className="text-white w-5 h-5" />
        </div>
        <span className="text-xl font-bold text-gray-800 tracking-tight">
          RadarZ
        </span>
      </div>

      <nav className="flex-1 space-y-1">
        {menuItems.map((item) => {
          const isActive = pathname === item.id;
          return (
            <Link
              key={item.id}
              href={item.id}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 relative group cursor-pointer ${
                isActive
                  ? "text-emerald-700 bg-emerald-50/50"
                  : "text-gray-500 hover:bg-gray-50"
              }`}
            >
              {isActive && (
                <motion.div
                  layoutId="active-pill"
                  className="absolute left-0 w-1 h-6 bg-emerald-600 rounded-full"
                  transition={{ type: "spring", stiffness: 300, damping: 30 }}
                />
              )}
              <item.icon
                className={`w-5 h-5 ${
                  isActive ? "text-emerald-600" : "group-hover:text-emerald-600"
                }`}
              />
              <span className="font-medium">{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="pt-4 border-t border-gray-50">
        <Link
          href="/settings"
          className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-gray-500 hover:bg-gray-50 transition-all duration-300 group cursor-pointer"
        >
          <Settings className="w-5 h-5 group-hover:text-emerald-600" />
          <span className="font-medium">设置</span>
        </Link>
      </div>
    </div>
  );
}
