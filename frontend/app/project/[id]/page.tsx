"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { ArrowLeft, Send, Sparkles } from "lucide-react";
import { getProjectById, type Project } from "@/data/mockProjects";

export default function ProjectDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [chatMessages, setChatMessages] = useState([
    {
      role: "user" as const,
      content: "What does this project do?",
    },
    {
      role: "assistant" as const,
      content:
        "This project is a powerful open-source solution that helps developers build better applications. It provides a comprehensive set of tools and features designed to streamline the development process.",
    },
  ]);

  useEffect(() => {
    // Simulate loading delay for better UX
    const timer = setTimeout(() => {
      const foundProject = getProjectById(id);
      setProject(foundProject || null);
      setLoading(false);
    }, 300);

    return () => clearTimeout(timer);
  }, [id]);

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
    <div className="min-h-screen bg-white">
      <div className="flex">
        {/* Left Navigation - Minimal */}
        <aside className="w-20 fixed left-0 top-0 h-screen bg-[#F9FAFB] border-r border-gray-100 flex flex-col items-center pt-6">
          <button
            onClick={() => router.back()}
            className="p-3 rounded-lg hover:bg-white transition-colors"
            aria-label="Go back"
          >
            <ArrowLeft className="w-6 h-6 text-gray-700" />
          </button>
        </aside>

        {/* Center - Readme Viewer (60%) */}
        <main className="flex-1 ml-20 mr-[40%]">
          <div className="max-w-4xl mx-auto px-8 py-8">
            {loading ? (
              <div className="animate-pulse">
                <div className="h-8 bg-gray-200 rounded w-1/2 mb-4"></div>
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-8"></div>
                <div className="h-screen bg-gray-100 rounded"></div>
              </div>
            ) : project ? (
              <>
                <div className="mb-6">
                  <h1 className="text-3xl font-bold text-gray-900 mb-2">
                    {project.title}
                  </h1>
                  <p className="text-gray-600 mb-4">{project.description}</p>
                  <div className="flex gap-2 flex-wrap">
                    {project.tags.map((tag, index) => (
                      <span
                        key={index}
                        className="px-2.5 py-1 bg-gray-100 text-gray-700 text-xs rounded-full"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
                <div className="h-screen bg-gray-50 border border-gray-200 rounded-lg flex items-center justify-center">
                  <div className="text-center">
                    <p className="text-gray-500 text-lg mb-2">
                      Readme / Code Viewer Placeholder
                    </p>
                    <p className="text-gray-400 text-sm">
                      This area will display the project README and code files
                    </p>
                  </div>
                </div>
              </>
            ) : (
              <div className="h-screen bg-gray-50 border border-gray-200 rounded-lg flex items-center justify-center">
                <p className="text-gray-500">Project not found</p>
              </div>
            )}
          </div>
        </main>

        {/* Right - AI Assistant (40%, Fixed) */}
        <aside className="w-[40%] fixed right-0 top-0 h-screen bg-white border-l border-gray-100 flex flex-col">
          <div className="p-6 border-b border-gray-100">
            <div className="flex items-center gap-2 mb-4">
              <Sparkles className="w-5 h-5 text-[#B92B27]" />
              <h2 className="text-lg font-semibold text-gray-900">
                AI Assistant
              </h2>
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
      </div>
    </div>
  );
}
