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
    <div className="flex flex-col items-center justify-center w-full h-full min-h-screen px-6 py-8 relative bg-sky-blue">
      {/* 体素风格云朵装饰 */}
      <div className="absolute top-20 left-10 w-24 h-16 bg-gray-light voxel-cloud opacity-80" />
      <div className="absolute top-32 right-20 w-32 h-20 bg-gray-light voxel-cloud opacity-70" />
      <div className="absolute top-16 right-1/3 w-20 h-14 bg-gray-light voxel-cloud opacity-75" />

      {/* Content */}
      <div className="relative z-10 w-full max-w-4xl">
        {/* Greeting */}
        <div className="mb-8 text-center">
          <div className="mb-4 flex items-center justify-center gap-3">
            <div className="voxel-border bg-orange p-2">
              <Sparkles className="w-10 h-10 text-white" />
            </div>
            <h1
              className="text-5xl font-bold text-black"
              style={{ textShadow: "3px 3px 0px #808080" }}
            >
              搜索灵感
            </h1>
          </div>
          <p className="text-base text-black/80 max-w-2xl mx-auto font-medium">
            智能分析您的搜索需求，精准推荐符合标准的 GitHub
            项目，如特定技术栈或功能特性。
          </p>
        </div>

        {/* Main Search Container */}
        <div className="w-full">
          <div className="voxel-input bg-white px-6 py-4 mb-6 flex items-center gap-3">
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
              className="flex-1 text-lg text-black placeholder:text-gray-dark bg-transparent border-none outline-none focus:outline-none font-medium"
            />

            {/* Send Button */}
            <button
              onClick={handleSend}
              disabled={!inputValue.trim()}
              className="voxel-button w-12 h-12 bg-red flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed shrink-0"
            >
              <svg
                className="w-6 h-6 text-white"
                fill="none"
                stroke="currentColor"
                strokeWidth={3}
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
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
                className="voxel-button px-5 py-2.5 bg-white text-sm text-black hover:bg-gray-light font-semibold"
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
