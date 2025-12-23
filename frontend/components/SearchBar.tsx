"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
  Sparkles,
  Search as SearchIcon,
  ArrowRight,
  FileText,
  Zap,
  LayoutGrid,
} from "lucide-react";
import ExampleSearches from "./ExampleSearches";

interface SearchBarProps {
  onSend: (query: string) => void;
}

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

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
    <motion.div
      className="max-w-4xl mx-auto pt-24 pb-12 px-6 flex flex-col items-center"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <motion.div variants={itemVariants} className="mb-6">
        <div className="w-12 h-12 bg-emerald-50 rounded-2xl flex items-center justify-center mb-4 mx-auto">
          <Sparkles className="text-emerald-600 w-6 h-6" />
        </div>
        <h1 className="text-3xl font-bold text-gray-800 text-center mb-2">
          搜索项目
        </h1>
        <p className="text-gray-500 text-center font-medium">
          输入你的创意，RadarZ 为你匹配最合适的开源项目。
        </p>
      </motion.div>

      <motion.div variants={itemVariants} className="w-full mb-12">
        <div className="flex items-center justify-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-700 font-bold text-sm">
              1
            </div>
            <div className="flex items-center gap-1.5 text-gray-500 text-sm font-medium">
              <FileText className="w-4 h-4" />
              <span>描述需求</span>
            </div>
          </div>
          <div className="w-12 h-px bg-gray-200" />
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-700 font-bold text-sm">
              2
            </div>
            <div className="flex items-center gap-1.5 text-gray-500 text-sm font-medium">
              <Zap className="w-4 h-4" />
              <span>AI 深度检索</span>
            </div>
          </div>
          <div className="w-12 h-px bg-gray-200" />
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-700 font-bold text-sm">
              3
            </div>
            <div className="flex items-center gap-1.5 text-gray-500 text-sm font-medium">
              <LayoutGrid className="w-4 h-4" />
              <span>生成对比报告</span>
            </div>
          </div>
        </div>
      </motion.div>

      <motion.div variants={itemVariants} className="w-full max-w-2xl relative mb-12">
        <div className="absolute inset-y-0 left-5 flex items-center pointer-events-none">
          <SearchIcon className="text-gray-400 w-5 h-5" />
        </div>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="一个性能极高且带权限管理的 Golang 后端框架"
          className="w-full pl-14 pr-16 py-4 bg-white border border-gray-100 rounded-full shadow-sm focus:shadow-md focus:border-emerald-200 focus:ring-4 focus:ring-emerald-50 outline-none transition-all duration-300 text-lg placeholder:text-gray-300"
        />
        <button
          onClick={handleSend}
          disabled={!inputValue.trim()}
          className="absolute right-2 top-2 bottom-2 px-5 bg-emerald-600 text-white rounded-full flex items-center justify-center hover:bg-emerald-700 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 cursor-pointer"
        >
          <ArrowRight className="w-5 h-5" />
        </button>
      </motion.div>

      <motion.div variants={itemVariants} className="w-full">
        <h3 className="text-center text-gray-800 font-semibold mb-6">
          试试这些示例
        </h3>
        <ExampleSearches onSearch={handleExampleSearch} />
      </motion.div>
    </motion.div>
  );
}
