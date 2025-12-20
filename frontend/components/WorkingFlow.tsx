"use client";

import { Check } from "lucide-react";
import { SearchState } from "@/hooks/useSearch";

interface WorkingFlowProps {
  state: SearchState;
}

export default function WorkingFlow({ state }: WorkingFlowProps) {
  return (
    <>
      {/* Summary Stats */}
      <div className="mb-6 space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-600">总项目数：</span>
          <span className="font-medium">{state.searchProgress}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">已验证项目：</span>
          <span className="font-medium">{state.projects.length}</span>
        </div>
      </div>

      {/* Step 1: Analysing Questions */}
      <div className="mb-4">
        <div className="flex items-center gap-2 mb-2">
          <Check
            className={`w-5 h-5 ${
              state.searchQueries.length > 0
                ? "text-green-500"
                : "text-gray-300"
            }`}
          />
          <span className="font-medium">1 分析问题</span>
        </div>
        {state.searchQueries.length > 0 && (
          <div className="ml-7 space-y-1">
            {state.searchQueries.map((query, index) => (
              <div key={index} className="text-sm text-gray-700">
                # {query}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Step 2: Validating Criteria */}
      <div className="mb-4">
        <div className="flex items-center gap-2 mb-2">
          <Check
            className={`w-5 h-5 ${
              state.validatingCriteria ? "text-green-500" : "text-gray-300"
            }`}
          />
          <span className="font-medium">2 验证标准</span>
        </div>
        {state.validatingCriteria && (
          <div className="ml-7 text-sm text-gray-700">
            # {state.validatingCriteria}
          </div>
        )}
      </div>

      {/* Step 3: Searching & Validating */}
      <div className="mb-4">
        <div className="flex items-center gap-2 mb-2">
          <Check
            className={`w-5 h-5 ${
              state.projects.length > 0 ? "text-green-500" : "text-gray-300"
            }`}
          />
          <span className="font-medium">3 搜索与验证</span>
        </div>
        {state.projects.length > 0 && (
          <div className="ml-7 space-y-2">
            {state.projects.slice(0, 5).map((project) => (
              <div key={project.id} className="flex items-center gap-2">
                <Check className="w-4 h-4 text-green-500" />
                <span className="text-sm text-gray-700 line-clamp-1">
                  {project.title}
                </span>
              </div>
            ))}
            {state.projects.length > 5 && (
              <div className="text-xs text-gray-500">
                +{state.projects.length - 5} 更多
              </div>
            )}
          </div>
        )}
      </div>
    </>
  );
}
