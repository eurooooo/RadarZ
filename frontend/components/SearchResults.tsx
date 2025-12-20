"use client";

import { Check, Loader2 } from "lucide-react";
import ProjectCard from "./ProjectCard";
import { SearchState } from "@/hooks/useSearch";

interface SearchResultsProps {
  state: SearchState;
}

export default function SearchResults({ state }: SearchResultsProps) {
  return (
    <>
      <div className="text-sm text-gray-600 mb-6">
        总计：{state.projects.length}
      </div>

      {/* Results */}
      {state.isSearching && state.projects.length === 0 && (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </div>
      )}

      {state.projects.length > 0 && (
        <div className="space-y-4">
          {state.projects.map((project) => (
            <div key={project.id} className="relative">
              <ProjectCard {...project} />
              {project.validation_reason && (
                <div className="absolute top-2 right-2 bg-green-100 text-green-800 px-2 py-1 rounded text-xs flex items-center gap-1">
                  <Check className="w-3 h-3" />
                  完美匹配
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {state.isComplete && state.projects.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          未找到符合您条件的项目。
        </div>
      )}
    </>
  );
}
