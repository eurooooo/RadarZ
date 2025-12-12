"use client";

import { useState } from "react";

export default function SearchBar() {
  const [inputValue, setInputValue] = useState("");
  const [selectedModel, setSelectedModel] = useState("GPT-5");

  const handleSend = () => {
    if (inputValue.trim()) {
      // Handle send action
      console.log("Sending:", inputValue);
    }
  };

  const promptSuggestions = [
    { label: "AI Agent" },
    { label: "Web Dev" },
    { label: "LLM" },
    { label: "Chatbot" },
    { label: "AI Agent" },
  ];

  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-6 py-12">
      {/* Greeting */}
      <div className="mb-8 flex items-center gap-3">
        <img src="/logo.svg" alt="Logo" className="w-10 h-10" />
        <h1 className="text-4xl font-serif text-foreground">RadarZ</h1>
      </div>

      {/* Main Search Container */}
      <div className="w-full max-w-4xl">
        <div className="bg-white rounded-3xl shadow-sm border border-gray-100 p-4 mb-6">
          {/* Input Area */}
          <div className="mb-3">
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
              placeholder="Search for projects ..."
              className="w-full text-lg text-foreground placeholder:text-gray-400 bg-transparent border-none outline-none focus:outline-none"
            />
          </div>

          {/* Bottom Controls */}
          <div className="flex items-center justify-between">
            {/* Left Controls */}
            <div className="flex items-center gap-2">
              <button className="w-7 h-7 rounded-lg bg-gray-50 border border-gray-200 flex items-center justify-center hover:bg-gray-100 transition-colors">
                <svg
                  className="w-3.5 h-3.5 text-gray-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  />
                </svg>
              </button>
              <button className="w-7 h-7 rounded-lg bg-gray-50 border border-gray-200 flex items-center justify-center hover:bg-gray-100 transition-colors">
                <svg
                  className="w-3.5 h-3.5 text-gray-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </button>
            </div>

            {/* Right Controls */}
            <div className="flex items-center gap-3">
              {/* Model Selector */}
              <div className="flex items-center gap-1 cursor-pointer hover:opacity-80 transition-opacity">
                <span className="text-sm text-gray-600">{selectedModel}</span>
                <svg
                  className="w-3.5 h-3.5 text-gray-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </div>

              {/* Send Button */}
              <button
                onClick={handleSend}
                disabled={!inputValue.trim()}
                className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
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
          </div>
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
  );
}
