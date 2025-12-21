"use client";

import { useState } from "react";
import { ArrowRight } from "lucide-react";

interface ExampleSearchesProps {
  onSearch: (query: string) => void;
}

const domains = [
  "AI",
  "Web",
  "机器学习",
  "前端开发",
  "后端开发",
  "移动开发",
  "数据科学",
  "DevOps",
  "区块链",
  "游戏开发",
];

const exampleQueries: Record<string, string[]> = {
  AI: [
    "使用大语言模型构建智能助手的项目",
    "基于深度学习的图像识别项目",
    "自然语言处理相关的开源项目",
  ],
  Web: [
    "使用 Next.js 构建的全栈应用项目",
    "React 组件库和 UI 框架",
    "现代化的 Web 开发工具和框架",
  ],
  机器学习: [
    "使用 PyTorch 实现的机器学习项目",
    "TensorFlow 深度学习模型和示例",
    "机器学习算法实现和教程项目",
  ],
  前端开发: [
    "Vue.js 3 组件库和模板",
    "TypeScript 前端项目最佳实践",
    "响应式设计的 UI 组件库",
  ],
  后端开发: [
    "使用 FastAPI 构建的 RESTful API 项目",
    "Node.js 微服务架构示例",
    "数据库设计和 ORM 使用示例",
  ],
  移动开发: [
    "React Native 跨平台应用项目",
    "Flutter UI 组件和模板",
    "移动端性能优化实践项目",
  ],
  数据科学: [
    "数据可视化和分析工具",
    "Jupyter Notebook 数据分析项目",
    "数据挖掘和统计学习项目",
  ],
  DevOps: [
    "Docker 容器化部署配置",
    "CI/CD 流水线自动化工具",
    "Kubernetes 编排和监控项目",
  ],
  区块链: [
    "智能合约开发框架",
    "DeFi 协议和 DApp 项目",
    "区块链数据分析和工具",
  ],
  游戏开发: [
    "Unity 游戏开发示例",
    "游戏引擎和工具库",
    "游戏 AI 和物理引擎项目",
  ],
};

export default function ExampleSearches({ onSearch }: ExampleSearchesProps) {
  const [selectedDomain, setSelectedDomain] = useState("AI");

  const handleExampleClick = (query: string) => {
    onSearch(query);
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Title */}
      <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">
        试试这些示例
      </h3>

      {/* Domain Categories - Horizontal Scrollable */}
      <div className="mb-6 overflow-x-auto scrollbar-hide">
        <div className="flex gap-2 pb-2 min-w-max">
          {domains.map((domain) => (
            <button
              key={domain}
              onClick={() => setSelectedDomain(domain)}
              className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all duration-200 ${
                selectedDomain === domain
                  ? "bg-primary text-white shadow-md shadow-primary/20"
                  : "bg-white text-gray-600 border border-gray-100 hover:bg-gray-50 hover:border-gray-200"
              }`}
            >
              {domain}
            </button>
          ))}
        </div>
      </div>

      {/* Example Queries */}
      <div className="space-y-2">
        {exampleQueries[selectedDomain]?.map((query, index) => (
          <button
            key={index}
            onClick={() => handleExampleClick(query)}
            className="w-full flex items-center justify-between p-4 bg-white border border-gray-100 rounded-lg text-left hover:border-primary/30 hover:shadow-md hover:shadow-primary/5 transition-all duration-200 group"
          >
            <span className="text-sm text-gray-700 group-hover:text-primary transition-colors">
              {query}
            </span>
            <ArrowRight
              size={16}
              className="text-gray-400 group-hover:text-primary group-hover:translate-x-1 transition-all flex-shrink-0 ml-2"
            />
          </button>
        ))}
      </div>
    </div>
  );
}

