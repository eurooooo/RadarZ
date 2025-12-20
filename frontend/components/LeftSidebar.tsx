"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Compass, Search } from "lucide-react";

export default function LeftSidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 h-screen w-60 bg-gray-light flex flex-col voxel-border border-r-0 border-b-0 border-t-0" style={{ boxShadow: '4px 0px 0px 0px #808080, 8px 0px 0px 0px #1A1A1A' }}>
      {/* Logo */}
      <div className="p-6">
        <Link
          href="/"
          className="flex items-center gap-3 text-2xl font-bold text-black"
        >
          <div className="voxel-border bg-orange p-2">
            <img src="/logo.svg" alt="RadarZ Logo" className="w-8 h-8 shrink-0" />
          </div>
          <span style={{ textShadow: '2px 2px 0px #808080' }}>RadarZ</span>
        </Link>
      </div>

      {/* Navigation Menu */}
      <nav className="flex-1 px-4">
        <ul className="space-y-3">
          <li>
            <Link
              href="/"
              className={`voxel-button flex items-center gap-3 px-4 py-3 font-bold ${
                pathname === "/"
                  ? "bg-orange text-white"
                  : "bg-white text-black"
              }`}
            >
              <Search className="w-5 h-5" />
              <span>搜索</span>
            </Link>
          </li>
          <li>
            <Link
              href="/explore"
              className={`voxel-button flex items-center gap-3 px-4 py-3 font-bold ${
                pathname === "/explore"
                  ? "bg-orange text-white"
                  : "bg-white text-black"
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
        <div className="voxel-border w-12 h-12 bg-red flex items-center justify-center">
          <span className="text-white font-bold text-lg">N</span>
        </div>
      </div>
    </aside>
  );
}
