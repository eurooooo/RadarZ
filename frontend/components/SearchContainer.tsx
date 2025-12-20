"use client";

import SearchResults from "./SearchResults";
import WorkingFlow from "./WorkingFlow";
import { SearchState } from "@/hooks/useSearch";

interface SearchContainerProps {
  query: string;
  state: SearchState;
}

export default function SearchContainer({
  query,
  state,
}: SearchContainerProps) {
  return (
    <div className="flex h-screen bg-gray-50">
      {/* Center Content - Search Results */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4">
              <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                继续搜索
              </button>
              <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                分享结果
              </button>
              <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                问题反馈
              </button>
            </div>
          </div>

          <SearchResults state={state} />
        </div>
      </div>

      {/* Right Sidebar - Working Flow */}
      <div className="w-80 bg-white border-l border-gray-200 p-6 overflow-y-auto">
        <h2 className="text-lg font-semibold mb-4">工作流程</h2>
        <WorkingFlow state={state} />
      </div>
    </div>
  );
}
