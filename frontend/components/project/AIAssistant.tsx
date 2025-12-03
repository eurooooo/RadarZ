"use client";

import { useState } from "react";
import { Send, Sparkles } from "lucide-react";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export default function AIAssistant() {
  const [message, setMessage] = useState("");
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {
      role: "user",
      content: "What does this project do?",
    },
    {
      role: "assistant",
      content:
        "This project is a powerful open-source solution that helps developers build better applications. It provides a comprehensive set of tools and features designed to streamline the development process.",
    },
  ]);

  const handleSendMessage = () => {
    if (!message.trim()) return;

    setChatMessages([
      ...chatMessages,
      { role: "user", content: message },
      {
        role: "assistant",
        content:
          "This is a placeholder response. The AI assistant feature will be implemented in the future.",
      },
    ]);
    setMessage("");
  };

  return (
    <aside className="w-[40%] fixed right-0 top-0 h-screen bg-white border-l border-gray-100 flex flex-col">
      <div className="p-6 border-b border-gray-100">
        <div className="flex items-center gap-2 mb-4">
          <Sparkles className="w-5 h-5 text-[#B92B27]" />
          <h2 className="text-lg font-semibold text-gray-900">AI Assistant</h2>
        </div>
        <div className="flex gap-2">
          <button className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors">
            Explain Code
          </button>
          <button className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors">
            Summary
          </button>
        </div>
      </div>

      {/* Chat Messages - Scrollable */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {chatMessages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[80%] rounded-lg p-3 ${
                msg.role === "user"
                  ? "bg-[#B92B27] text-white"
                  : "bg-gray-100 text-gray-900"
              }`}
            >
              <p className="text-sm">{msg.content}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Input Area */}
      <div className="p-6 border-t border-gray-100">
        <div className="flex gap-2">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === "Enter") {
                handleSendMessage();
              }
            }}
            placeholder="Ask about this project..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#B92B27] focus:border-transparent"
          />
          <button
            onClick={handleSendMessage}
            className="px-6 py-2 bg-[#B92B27] text-white rounded-lg hover:bg-[#A02622] transition-colors flex items-center gap-2"
          >
            <Send className="w-4 h-4" />
            <span>Send</span>
          </button>
        </div>
      </div>
    </aside>
  );
}
