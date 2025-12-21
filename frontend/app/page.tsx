"use client";

import { useState, useEffect, useRef } from "react";
import SearchBar from "@/components/SearchBar";
import SearchResults from "@/components/SearchResults";
import WorkingFlow from "@/components/WorkingFlow";
import { useSearch } from "@/hooks/useSearch";
import { RefreshCw } from "lucide-react";

export default function Home() {
  const [hasSearched, setHasSearched] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const { state, performSearch } = useSearch();
  const resultsRef = useRef<HTMLDivElement>(null);

  // 处理搜索发送
  const handleSend = (query: string) => {
    const trimmedQuery = query.trim();
    if (trimmedQuery) {
      setSearchQuery(trimmedQuery);
      setHasSearched(true);
      performSearch(trimmedQuery);

      // 滚动到结果区域
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }, 100);
    }
  };

  // 重新搜索
  const handleRefresh = () => {
    if (searchQuery) {
      performSearch(searchQuery);
    }
  };

  return (
    <div className="flex flex-col items-center justify-start min-h-screen p-8 max-w-6xl mx-auto w-full">
      <div
        className={`w-full flex flex-col items-center transition-all duration-700 ${
          hasSearched ? "mt-4" : "mt-[15vh]"
        }`}
      >
        <SearchBar onSend={handleSend} />
      </div>

      {hasSearched && (
        <div
          ref={resultsRef}
          className="w-full mt-12 animate-in fade-in slide-in-from-bottom-8 duration-700"
        >
          {/* Header with WorkingFlow */}
          <div className="mb-8 border-b border-gray-100 pb-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-gray-900">推荐项目</h3>
              <button
                onClick={handleRefresh}
                disabled={state.isSearching}
                className="flex items-center gap-2 text-xs font-medium text-gray-500 hover:text-primary transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <RefreshCw
                  size={14}
                  className={state.isSearching ? "animate-spin" : ""}
                />
                重新推荐
              </button>
            </div>
            {/* Compact WorkingFlow */}
            <div className="bg-gray-50 rounded-lg p-3 border border-gray-100">
              <WorkingFlow state={state} />
            </div>
          </div>

          {/* Search Results */}
          <SearchResults state={state} />
        </div>
      )}
    </div>
  );
}
