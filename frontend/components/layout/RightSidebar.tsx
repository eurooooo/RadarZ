"use client";

import { Flame } from "lucide-react";

export default function RightSidebar() {
  return (
    <aside className="hidden lg:block w-[300px] sticky top-0 h-screen overflow-y-auto bg-white border-l border-gray-100 p-6">
      <div className="space-y-6">
        {/* Hot Topics Card */}
        <div className="bg-white border border-gray-100 rounded-lg p-4 hover:shadow-md transition-shadow">
          <div className="flex items-center gap-2 mb-4">
            <Flame className="w-5 h-5 text-[#B92B27]" />
            <h3 className="font-semibold text-gray-900">Hot Topics</h3>
          </div>
          <ul className="space-y-2">
            <li className="text-sm text-gray-600 hover:text-[#B92B27] cursor-pointer">
              #react
            </li>
            <li className="text-sm text-gray-600 hover:text-[#B92B27] cursor-pointer">
              #nextjs
            </li>
            <li className="text-sm text-gray-600 hover:text-[#B92B27] cursor-pointer">
              #typescript
            </li>
            <li className="text-sm text-gray-600 hover:text-[#B92B27] cursor-pointer">
              #ai
            </li>
          </ul>
        </div>

        {/* Events Card */}
        <div className="bg-white border border-gray-100 rounded-lg p-4 hover:shadow-md transition-shadow">
          <h3 className="font-semibold text-gray-900 mb-4">Events</h3>
          <p className="text-sm text-gray-500">No events at the moment</p>
        </div>
      </div>
    </aside>
  );
}

