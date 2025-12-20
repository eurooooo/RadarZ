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
    <div className="flex h-screen bg-sky-blue">
      {/* Center Content - Search Results */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4">
              <button className="voxel-button px-5 py-2.5 bg-white text-black font-bold hover:bg-gray-light">
                继续搜索
              </button>
              <button className="voxel-button px-5 py-2.5 bg-white text-black font-bold hover:bg-gray-light">
                分享结果
              </button>
              <button className="voxel-button px-5 py-2.5 bg-white text-black font-bold hover:bg-gray-light">
                问题反馈
              </button>
            </div>
          </div>

          <SearchResults state={state} />
        </div>
      </div>

      {/* Right Sidebar - Working Flow */}
      <div className="w-80 bg-white voxel-border border-l-0 border-b-0 border-t-0 p-6 overflow-y-auto" style={{ boxShadow: '-4px 0px 0px 0px #808080, -8px 0px 0px 0px #1A1A1A' }}>
        <h2 className="text-lg font-bold mb-4 text-black" style={{ textShadow: '2px 2px 0px #808080' }}>工作流程</h2>
        <WorkingFlow state={state} />
      </div>
    </div>
  );
}
