"use client";

import { useState } from "react";
import { Sparkles } from "lucide-react";

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

  const promptSuggestions = [
    { label: "AI 智能体" },
    { label: "Web 开发" },
    { label: "大语言模型" },
    { label: "聊天机器人" },
    { label: "机器学习" },
  ];

  return (
    <div className="flex flex-col items-center justify-center w-full h-full min-h-screen px-6 py-8 relative">
      {/* Gradient Background */}
      <div className="absolute top-0 left-0 right-0 h-80 bg-gradient-to-b from-primary/15 via-primary/8 to-transparent pointer-events-none" />

      {/* Content */}
      <div className="relative z-10 w-full max-w-4xl">
        {/* Greeting */}
        <div className="mb-8 text-center">
          <div className="mb-4 flex items-center justify-center gap-3">
            <Sparkles className="w-10 h-10 text-primary" />
            <h1 className="text-4xl font-serif text-foreground">搜索灵感</h1>
          </div>
          <p className="text-base text-gray-600 max-w-2xl mx-auto">
            基于用户意图验证。适合研究人员根据特定标准进行文献综述，如特定任务或数据集。
          </p>
        </div>

        {/* Main Search Container */}
        <div className="w-full">
          <div className="bg-white rounded-full shadow-sm border border-gray-100 px-4 py-3 mb-6 flex items-center gap-3">
            {/* Input Area */}
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              placeholder="搜索项目..."
              className="flex-1 text-lg text-foreground placeholder:text-gray-400 bg-transparent border-none outline-none focus:outline-none"
            />

            {/* Send Button */}
            <button
              onClick={handleSend}
              disabled={!inputValue.trim()}
              className="w-10 h-10 rounded-full bg-primary flex items-center justify-center hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed shrink-0"
            >
              <svg
                className="w-5 h-5 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 7l5 5m0 0l-5 5m5-5H6"
                />
              </svg>
            </button>
          </div>

          {/* Prompt Suggestions */}
          <div className="flex items-center justify-center gap-3 flex-wrap">
            {promptSuggestions.map((prompt, index) => (
              <button
                key={index}
                className="px-4 py-2 rounded-full bg-white border border-gray-200 text-sm text-gray-700 hover:bg-gray-50 transition-colors flex items-center gap-2"
              >
                <span>{prompt.label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
