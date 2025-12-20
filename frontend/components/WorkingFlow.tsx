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
        <div className="voxel-card p-3 mb-2">
          <div className="flex justify-between">
            <span className="text-black font-bold">总项目数：</span>
            <span className="font-bold text-orange">{state.searchProgress}</span>
          </div>
        </div>
        <div className="voxel-card p-3">
          <div className="flex justify-between">
            <span className="text-black font-bold">已验证项目：</span>
            <span className="font-bold text-red">{state.projects.length}</span>
          </div>
        </div>
      </div>

      {/* Step 1: Analysing Questions */}
      <div className="mb-4">
        <div className="flex items-center gap-2 mb-2">
          <div className={`voxel-border p-1 ${state.searchQueries.length > 0 ? "bg-orange" : "bg-gray-medium"}`}>
            <Check
              className={`w-5 h-5 ${
                state.searchQueries.length > 0
                  ? "text-white"
                  : "text-gray-dark"
              }`}
            />
          </div>
          <span className="font-bold text-black">1 分析问题</span>
        </div>
        {state.searchQueries.length > 0 && (
          <div className="ml-7 space-y-1">
            {state.searchQueries.map((query, index) => (
              <div key={index} className="voxel-button px-2 py-1 bg-white text-sm text-black font-semibold">
                # {query}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Step 2: Validating Criteria */}
      <div className="mb-4">
        <div className="flex items-center gap-2 mb-2">
          <div className={`voxel-border p-1 ${state.validatingCriteria ? "bg-orange" : "bg-gray-medium"}`}>
            <Check
              className={`w-5 h-5 ${
                state.validatingCriteria ? "text-white" : "text-gray-dark"
              }`}
            />
          </div>
          <span className="font-bold text-black">2 验证标准</span>
        </div>
        {state.validatingCriteria && (
          <div className="ml-7">
            <div className="voxel-button px-2 py-1 bg-white text-sm text-black font-semibold">
              # {state.validatingCriteria}
            </div>
          </div>
        )}
      </div>

      {/* Step 3: Searching & Validating */}
      <div className="mb-4">
        <div className="flex items-center gap-2 mb-2">
          <div className={`voxel-border p-1 ${state.projects.length > 0 ? "bg-orange" : "bg-gray-medium"}`}>
            <Check
              className={`w-5 h-5 ${
                state.projects.length > 0 ? "text-white" : "text-gray-dark"
              }`}
            />
          </div>
          <span className="font-bold text-black">3 搜索与验证</span>
        </div>
        {state.projects.length > 0 && (
          <div className="ml-7 space-y-2">
            {state.projects.slice(0, 5).map((project) => (
              <div key={project.id} className="flex items-center gap-2">
                <div className="voxel-border p-1 bg-orange">
                  <Check className="w-4 h-4 text-white" />
                </div>
                <span className="text-sm text-black line-clamp-1 font-semibold">
                  {project.title}
                </span>
              </div>
            ))}
            {state.projects.length > 5 && (
              <div className="text-xs text-black font-bold">
                +{state.projects.length - 5} 更多
              </div>
            )}
          </div>
        )}
      </div>
    </>
  );
}
