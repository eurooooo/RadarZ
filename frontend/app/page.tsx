"use client";

import { useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import SearchBar from "@/components/SearchBar";
import SearchResults from "@/components/SearchResults";
import WorkingFlow from "@/components/WorkingFlow";
import { useSearch } from "@/hooks/useSearch";
import { ChevronLeft } from "lucide-react";

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

  // 返回搜索
  const handleBack = () => {
    setHasSearched(false);
    setSearchQuery("");
  };

  return (
    <div className="flex-1 flex flex-col relative overflow-y-auto">
      <AnimatePresence mode="wait">
        {!hasSearched ? (
          <motion.div
            key="search-home"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="flex-1"
          >
            <SearchBar onSend={handleSend} />
          </motion.div>
        ) : (
          <motion.div
            key="results-view"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            ref={resultsRef}
            className="flex-1 p-8"
          >
            <div className="max-w-5xl mx-auto">
              {/* Back Button */}
              <div className="mb-8 flex items-center justify-between">
                <button
                  onClick={handleBack}
                  className="flex items-center gap-2 text-gray-500 hover:text-emerald-600 transition-colors font-medium group cursor-pointer"
                >
                  <ChevronLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
                  返回搜索
                </button>
              </div>

              {/* Header with Search Query */}
              <header className="mb-10">
                <h2 className="text-gray-400 text-sm font-bold uppercase tracking-widest mb-2">
                  搜索关键词
                </h2>
                <h1 className="text-3xl font-bold text-gray-800">
                  "{searchQuery}"
                </h1>
              </header>

              {/* Header with WorkingFlow */}
              <div className="mb-8 border-b border-gray-100/50 pb-6">
                {/* Enhanced WorkingFlow with glassmorphism */}
                <div className="relative rounded-2xl bg-gradient-to-br from-white/80 via-emerald-50/30 to-white/80 backdrop-blur-md p-6 border border-emerald-100/50 shadow-xl shadow-emerald-500/5">
                  <WorkingFlow state={state} />
                </div>
              </div>

              {/* Search Results */}
              <SearchResults state={state} />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
