"use client";

import { useEffect, useRef, useState } from "react";
import { ArrowUp, ChevronDown } from "lucide-react";

export default function BottomSearchBar() {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Alt+/ to focus search
      if (e.altKey && e.key === "/") {
        e.preventDefault();
        textareaRef.current?.focus();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const handleSend = () => {
    if (message.trim()) {
      // Handle send logic here
      console.log("Sending:", message);
      setMessage("");
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      const scrollHeight = textareaRef.current.scrollHeight;
      const minHeight = 120;
      const maxHeight = 300;
      const newHeight = Math.min(Math.max(scrollHeight, minHeight), maxHeight);
      textareaRef.current.style.height = `${newHeight}px`;
    }
  }, [message]);

  return (
    <div className="fixed bottom-0 left-60 right-0 z-50 bg-cream">
      <div className="mx-auto py-4 max-w-4xl px-6">
        <div className="relative bg-white rounded-2xl border border-gray-200 shadow-sm">
          {/* Textarea */}
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="How can I help you today?"
            className="w-full px-6 pt-6 pb-20 rounded-2xl bg-transparent focus:outline-none text-sm resize-none"
            rows={1}
            style={{
              minHeight: "120px",
              maxHeight: "300px",
            }}
          />

          {/* Bottom controls */}
          <div className="absolute bottom-4 left-6 right-6 flex items-center justify-between">
            {/* Left side - empty (no icons) */}
            <div></div>

            {/* Right side - Model selector and Send button */}
            <div className="flex items-center gap-3">
              {/* Model selector */}
              <div className="flex items-center gap-1 text-sm text-gray-600 cursor-pointer hover:text-gray-900">
                <span>Sonnet 4.5</span>
                <ChevronDown className="w-4 h-4" />
              </div>

              {/* Send button */}
              <button
                onClick={handleSend}
                disabled={!message.trim()}
                className="flex items-center justify-center w-10 h-10 rounded-lg bg-cream hover:bg-[#e8e6e0] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                aria-label="Send message"
              >
                <ArrowUp className="w-5 h-5 text-gray-700" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
