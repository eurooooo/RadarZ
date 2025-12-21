"use client";

import { Check } from "lucide-react";
import { SearchState } from "@/hooks/useSearch";

interface WorkingFlowProps {
  state: SearchState;
}

export default function WorkingFlow({ state }: WorkingFlowProps) {
  return (
    <div className="space-y-3">
      {/* Summary Stats */}
      <div className="flex items-center gap-4 text-xs">
        <div className="flex items-center gap-2">
          <span className="text-gray-600">总项目数：</span>
          <span className="font-medium text-gray-900">
            {state.searchProgress}
          </span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-gray-600">已验证：</span>
          <span className="font-medium text-gray-900">
            {state.projects.length}
          </span>
        </div>
      </div>

      {/* Steps */}
      <div className="flex items-center gap-4 flex-wrap">
        {/* Step 1: Analysing Questions */}
        <div className="flex items-center gap-2">
          <Check
            className={`w-4 h-4 ${
              state.searchQueries.length > 0
                ? "text-green-500"
                : "text-gray-300"
            }`}
          />
          <span className="text-xs font-medium text-gray-700">分析问题</span>
          {state.searchQueries.length > 0 && (
            <span className="text-[10px] text-gray-500">
              ({state.searchQueries.length})
            </span>
          )}
        </div>

        {/* Step 2: Validating Criteria */}
        <div className="flex items-center gap-2">
          <Check
            className={`w-4 h-4 ${
              state.validatingCriteria ? "text-green-500" : "text-gray-300"
            }`}
          />
          <span className="text-xs font-medium text-gray-700">验证标准</span>
        </div>

        {/* Step 3: Searching & Validating */}
        <div className="flex items-center gap-2">
          <Check
            className={`w-4 h-4 ${
              state.projects.length > 0 ? "text-green-500" : "text-gray-300"
            }`}
          />
          <span className="text-xs font-medium text-gray-700">搜索验证</span>
          {state.projects.length > 0 && (
            <span className="text-[10px] text-gray-500">
              ({state.projects.length})
            </span>
          )}
        </div>
      </div>

      {/* Search Queries (if any) */}
      {state.searchQueries.length > 0 && (
        <div className="flex flex-wrap gap-2 pt-2 border-t border-gray-200">
          {state.searchQueries.map((query, index) => (
            <span
              key={index}
              className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-[10px]"
            >
              #{query}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
