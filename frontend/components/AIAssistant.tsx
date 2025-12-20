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
    <aside className="w-[40%] fixed right-0 top-0 h-screen voxel-border border-l-0 border-b-0 border-t-0 flex flex-col bg-white" style={{ boxShadow: '-4px 0px 0px 0px #808080, -8px 0px 0px 0px #1A1A1A' }}>
      <div className="p-6 border-b-3 border-black">
        <div className="flex items-center gap-2 mb-4">
          <div className="voxel-border bg-orange p-1.5">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-lg font-bold text-black" style={{ textShadow: '2px 2px 0px #808080' }}>AI Assistant</h2>
        </div>
        <div className="flex gap-2">
          <button className="voxel-button flex-1 px-4 py-2 bg-white text-black text-sm font-bold hover:bg-gray-light">
            Explain Code
          </button>
          <button className="voxel-button flex-1 px-4 py-2 bg-white text-black text-sm font-bold hover:bg-gray-light">
            Summary
          </button>
        </div>
      </div>

      {/* Chat Messages - Scrollable */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-sky-blue">
        {chatMessages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[80%] voxel-card p-3 ${
                msg.role === "user"
                  ? "bg-orange text-white"
                  : "bg-white text-black"
              }`}
            >
              <p className="text-sm font-medium">{msg.content}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Input Area */}
      <div className="p-6 border-t-3 border-black bg-white">
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
            className="voxel-input flex-1 px-4 py-2 bg-white text-black font-medium placeholder:text-gray-dark"
          />
          <button
            onClick={handleSendMessage}
            className="voxel-button px-6 py-2 bg-red text-white font-bold flex items-center gap-2"
          >
            <Send className="w-4 h-4" />
            <span>Send</span>
          </button>
        </div>
      </div>
    </aside>
  );
}
