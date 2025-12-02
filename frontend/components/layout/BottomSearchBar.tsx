"use client";

import { useEffect, useRef } from "react";
import { Search, ArrowUp } from "lucide-react";

export default function BottomSearchBar() {
  const searchInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Alt+/ to focus search
      if (e.altKey && e.key === "/") {
        e.preventDefault();
        searchInputRef.current?.focus();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <div className="fixed bottom-0 left-60 right-0 lg:right-[300px] z-50 bg-white border-t border-gray-100 shadow-lg">
      <div className="max-w-3xl mx-auto px-6 py-4">
        <div className="flex items-center gap-3">
          {/* Search Input */}
          <div className="flex-1 relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              ref={searchInputRef}
              type="text"
              placeholder="Ask anything about projects... (Alt+/ to search)"
              className="w-full pl-12 pr-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#B92B27] focus:border-transparent text-sm"
            />
          </div>

          {/* Scroll to Top Button */}
          <button
            onClick={scrollToTop}
            className="flex items-center justify-center w-10 h-10 rounded-full bg-white border border-gray-200 hover:bg-gray-50 hover:border-gray-300 transition-colors shrink-0"
            aria-label="Scroll to top"
          >
            <ArrowUp className="w-5 h-5 text-gray-600" />
          </button>
        </div>
      </div>
    </div>
  );
}

