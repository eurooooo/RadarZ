"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Check, Loader2 } from "lucide-react";
import { SearchState } from "@/hooks/useSearch";

interface WorkingFlowProps {
  state: SearchState;
}

// 动态日志消息
const logMessages = [
  "正在解析语义...",
  "正在生成搜索查询...",
  "正在筛选活跃仓库...",
  "正在验证开源协议...",
  "正在分析项目质量...",
  "正在匹配相关项目...",
  "正在验证项目信息...",
  "正在整理搜索结果...",
];

export default function WorkingFlow({ state }: WorkingFlowProps) {
  const [currentLog, setCurrentLog] = useState("");
  const [logIndex, setLogIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);

  // 打字机效果
  useEffect(() => {
    if (!state.isSearching) {
      const timer = setTimeout(() => {
        setCurrentLog("");
        setLogIndex(0);
        setCharIndex(0);
      }, 0);
      return () => clearTimeout(timer);
    }

    const message = logMessages[logIndex % logMessages.length];

    if (charIndex < message.length) {
      const timer = setTimeout(() => {
        setCurrentLog(message.slice(0, charIndex + 1));
        setCharIndex(charIndex + 1);
      }, 50);
      return () => clearTimeout(timer);
    } else {
      // 当前消息打完，等待后切换到下一条
      const timer = setTimeout(() => {
        setLogIndex((prev) => (prev + 1) % logMessages.length);
        setCharIndex(0);
        setCurrentLog("");
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, [state.isSearching, logIndex, charIndex]);

  // 步骤状态
  const steps = [
    {
      id: 1,
      label: "分析问题",
      isActive: state.searchQueries.length > 0,
      isCompleted: state.searchQueries.length > 0,
      count: state.searchQueries.length,
      isProcessing: state.isSearching && state.searchQueries.length === 0,
    },
    {
      id: 2,
      label: "验证标准",
      isActive: state.validateCriteria.length > 0,
      isCompleted: state.validateCriteria.length > 0,
      count: state.validateCriteria.length,
      isProcessing:
        state.isSearching &&
        state.searchQueries.length > 0 &&
        state.validateCriteria.length === 0,
    },
    {
      id: 3,
      label: "搜索验证",
      isActive: state.projects.length > 0,
      isCompleted: state.projects.length > 0,
      count: state.projects.length,
      isProcessing:
        state.isSearching &&
        state.validateCriteria.length > 0 &&
        state.projects.length === 0,
    },
  ];

  return (
    <div className="space-y-4">
      {/* 水平步进器 */}
      <div className="relative">
        <div className="flex items-start justify-between">
          {steps.map((step, index) => (
            <div key={step.id} className="flex items-start flex-1">
              {/* 步骤圆圈和内容 */}
              <div className="relative z-10 flex flex-col items-center w-full">
                {/* 步骤圆圈 */}
                <motion.div
                  className={`relative w-8 h-8 rounded-full flex items-center justify-center transition-all duration-300 ${
                    step.isCompleted
                      ? "bg-gradient-to-br from-emerald-500 to-emerald-600 shadow-lg shadow-emerald-500/30"
                      : step.isProcessing
                      ? "bg-gradient-to-br from-emerald-400 to-emerald-500 shadow-lg shadow-emerald-400/40"
                      : "bg-gray-200"
                  }`}
                  animate={
                    step.isProcessing
                      ? {
                          scale: [1, 1.1, 1],
                          boxShadow: [
                            "0 0 0 0 rgba(16, 185, 129, 0.4)",
                            "0 0 0 6px rgba(16, 185, 129, 0)",
                            "0 0 0 0 rgba(16, 185, 129, 0)",
                          ],
                        }
                      : {}
                  }
                  transition={{
                    duration: 2,
                    repeat: step.isProcessing ? Infinity : 0,
                    ease: "easeInOut",
                  }}
                >
                  <AnimatePresence mode="wait">
                    {step.isCompleted ? (
                      <motion.div
                        initial={{ scale: 0, rotate: -180 }}
                        animate={{ scale: 1, rotate: 0 }}
                        exit={{ scale: 0, rotate: 180 }}
                        transition={{
                          type: "spring",
                          stiffness: 500,
                          damping: 25,
                        }}
                      >
                        <Check className="w-4 h-4 text-white" strokeWidth={3} />
                      </motion.div>
                    ) : step.isProcessing ? (
                      <Loader2 className="w-4 h-4 text-white animate-spin" />
                    ) : (
                      <div className="w-4 h-4 rounded-full bg-white/30" />
                    )}
                  </AnimatePresence>

                  {/* 呼吸灯效果 */}
                  {step.isProcessing && (
                    <motion.div
                      className="absolute inset-0 rounded-full bg-emerald-400"
                      animate={{
                        opacity: [0.5, 1, 0.5],
                        scale: [1, 1.2, 1],
                      }}
                      transition={{
                        duration: 2,
                        repeat: Infinity,
                        ease: "easeInOut",
                      }}
                      style={{ filter: "blur(8px)" }}
                    />
                  )}
                </motion.div>

                {/* 步骤标签 */}
                <div className="mt-2 text-center w-full">
                  <div
                    className={`text-xs font-semibold transition-colors ${
                      step.isCompleted || step.isProcessing
                        ? "text-emerald-600"
                        : "text-gray-400"
                    }`}
                  >
                    {step.label}
                  </div>
                  {step.count !== undefined && step.count > 0 && (
                    <motion.div
                      initial={{ opacity: 0, y: -5 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="text-[10px] text-emerald-500 font-medium mt-0.5"
                    >
                      ({step.count})
                    </motion.div>
                  )}
                </div>

                {/* 步骤1下方：搜索查询标签 */}
                {step.id === 1 && state.searchQueries.length > 0 && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    className="mt-3 w-full flex flex-wrap gap-2 justify-center"
                  >
                    {state.searchQueries.map((query, queryIndex) => (
                      <motion.span
                        key={queryIndex}
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: queryIndex * 0.1 }}
                        className="px-2.5 py-1 bg-gradient-to-r from-emerald-50 to-emerald-100/50 text-emerald-700 rounded-full text-[10px] font-medium border border-emerald-200/50 shadow-sm backdrop-blur-sm"
                      >
                        #{query}
                      </motion.span>
                    ))}
                  </motion.div>
                )}

                {/* 步骤2下方：验证标准标签 */}
                {step.id === 2 && state.validateCriteria.length > 0 && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    className="mt-3 w-full flex flex-wrap gap-2 justify-center"
                  >
                    {state.validateCriteria.map((criterion, criterionIndex) => (
                      <motion.span
                        key={criterionIndex}
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: criterionIndex * 0.1 }}
                        className="px-2.5 py-1 bg-gradient-to-r from-blue-50 to-blue-100/50 text-blue-700 rounded-full text-[10px] font-medium border border-blue-200/50 shadow-sm backdrop-blur-sm"
                      >
                        ✓ {criterion}
                      </motion.span>
                    ))}
                  </motion.div>
                )}

                {/* 步骤3下方：统计信息 */}
                {step.id === 3 && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-3 w-full flex flex-col items-center gap-2"
                  >
                    <div className="flex items-center gap-4 text-xs">
                      <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/60 backdrop-blur-sm border border-gray-200/50 shadow-sm">
                        <span className="text-gray-600">总项目数：</span>
                        <motion.span
                          key={state.searchProgress}
                          initial={{ scale: 1.2, color: "#10b981" }}
                          animate={{ scale: 1, color: "#111827" }}
                          className="font-bold text-gray-900"
                        >
                          {state.searchProgress}
                        </motion.span>
                      </div>
                      <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/60 backdrop-blur-sm border border-gray-200/50 shadow-sm">
                        <span className="text-gray-600">已验证：</span>
                        <motion.span
                          key={state.projects.length}
                          initial={{ scale: 1.2, color: "#10b981" }}
                          animate={{ scale: 1, color: "#111827" }}
                          className="font-bold text-gray-900"
                        >
                          {state.projects.length}
                        </motion.span>
                      </div>
                    </div>
                  </motion.div>
                )}
              </div>

              {/* 连接线 */}
              {index < steps.length - 1 && (
                <div className="flex-1 h-0.5 mx-2 mt-4 relative overflow-visible">
                  {/* 基础线 */}
                  <div
                    className={`absolute inset-0 transition-all duration-500 ${
                      step.isCompleted
                        ? "bg-gradient-to-r from-emerald-500 to-emerald-400"
                        : "bg-gray-200"
                    }`}
                  />

                  {/* 流光效果 */}
                  {step.isCompleted && (
                    <motion.div
                      className="absolute inset-0 bg-gradient-to-r from-transparent via-white/60 to-transparent"
                      initial={{ x: "-100%" }}
                      animate={{ x: "200%" }}
                      transition={{
                        duration: 2,
                        repeat: Infinity,
                        ease: "linear",
                      }}
                    />
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* 动态日志区域 */}
      <AnimatePresence>
        {state.isSearching && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="relative overflow-hidden rounded-lg bg-gradient-to-r from-emerald-50/50 via-emerald-50/30 to-emerald-50/50 backdrop-blur-sm border border-emerald-100/50 p-3 shadow-sm"
          >
            <div className="flex items-center gap-2">
              <motion.div
                className="w-2 h-2 rounded-full bg-emerald-500"
                animate={{ opacity: [1, 0.3, 1] }}
                transition={{ duration: 1.5, repeat: Infinity }}
              />
              <span className="text-xs font-medium text-emerald-700">
                {currentLog}
                <motion.span
                  animate={{ opacity: [1, 0] }}
                  transition={{ duration: 0.8, repeat: Infinity }}
                  className="ml-1"
                >
                  |
                </motion.span>
              </span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
