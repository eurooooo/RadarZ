"use client";

import ProjectCard from "./ProjectCard";
import { SearchState } from "@/hooks/useSearch";

interface SearchResultsProps {
  state: SearchState;
}

export default function SearchResults({ state }: SearchResultsProps) {
  return (
    <>
      {/* Loading State */}
      {state.isSearching && state.projects.length === 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div
              key={i}
              className="relative h-64 bg-white/60 backdrop-blur-sm rounded-xl border border-gray-200/50 overflow-hidden shadow-lg animate-pulse"
            >
              <div className="relative h-full flex flex-col p-6 space-y-4">
                <div className="w-1/3 h-4 bg-gray-200/50 rounded-full"></div>
                <div className="w-full h-6 bg-gray-200/50 rounded-full"></div>
                <div className="w-full h-24 bg-gray-100/50 rounded-lg"></div>
                <div className="mt-auto w-1/2 h-4 bg-gray-200/50 rounded-full"></div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Results Grid */}
      {state.projects.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pb-20">
          {state.projects.map((project) => (
            <div key={project.id} className="relative h-full">
              <ProjectCard {...project} />
            </div>
          ))}
        </div>
      )}

      {/* Empty State */}
      {state.isComplete &&
        state.projects.length === 0 &&
        !state.isSearching && (
          <div className="text-center py-12 text-gray-500">
            未找到符合您条件的项目。
          </div>
        )}
    </>
  );
}
