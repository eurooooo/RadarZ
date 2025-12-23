"use client";

import { useState } from "react";
import { Sparkles, Search as SearchIcon, ArrowRight } from "lucide-react";
import ExampleSearches from "./ExampleSearches";

interface SearchBarProps {
  onSend: (query: string) => void;
}

export default function SearchBar({ onSend }: SearchBarProps) {
  const [inputValue, setInputValue] = useState("");

  const handleSend = () => {
    if (inputValue.trim()) {
      onSend(inputValue.trim());
    }
  };

  const handleExampleSearch = (query: string) => {
    setInputValue(query);
    onSend(query);
  };

  return (
    <div className="flex flex-col items-center justify-start w-full p-8 max-w-6xl mx-auto">
      <div className="w-full flex flex-col items-center">
        {/* Title Section */}
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-primary/5 rounded-xl text-primary">
            <Sparkles size={28} className="animate-pulse" />
          </div>
          <h2 className="text-3xl font-bold text-gray-900 tracking-tight">
            搜索项目
          </h2>
        </div>

        {/* Description */}
        <p className="text-gray-500 text-base text-center max-w-xl mb-12 leading-relaxed">
          智能分析您的搜索需求，精准推荐符合技术栈、功能特性或质量标准的 GitHub
          项目。
        </p>

        {/* Search Form */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="w-full max-w-2xl relative mb-8 group"
        >
          <div className="absolute left-6 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-primary transition-colors">
            <SearchIcon size={20} />
          </div>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="搜索项目，如 'Next.js 仪表盘模板'..."
            className="w-full pl-14 pr-16 py-5 bg-white border border-gray-100 rounded-full text-base shadow-sm focus:outline-none focus:ring-4 focus:ring-primary/10 focus:border-primary/30 transition-all placeholder:text-gray-300"
          />
          <button
            type="submit"
            disabled={!inputValue.trim()}
            className="absolute right-3 top-1/2 -translate-y-1/2 p-3 bg-primary text-white rounded-full hover:bg-primary-dark hover:scale-105 active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-primary/20"
          >
            <ArrowRight size={22} />
          </button>
        </form>

        {/* Example Searches */}
        <div className="w-full mt-8">
          <ExampleSearches onSearch={handleExampleSearch} />
        </div>
      </div>
    </div>
  );
}
