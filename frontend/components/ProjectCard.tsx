"use client";

import Link from "next/link";
import Image from "next/image";
import { motion } from "framer-motion";
import { Star, GitFork, Bookmark } from "lucide-react";
import { Project } from "@/hooks/useSearch";

type ProjectCardProps = Project;

export default function ProjectCard({
  id,
  title,
  authors,
  description,
  tags,
  stars,
  forks,
  language,
}: ProjectCardProps) {
  return (
    <Link href={`/project/${id}`} className="block h-full">
      <motion.div
        whileHover={{ scale: 1.02, borderColor: "#10b981", y: -4 }}
        transition={{ duration: 0.15, ease: "easeOut" }}
        className="border border-gray-200 rounded-xl hover:shadow-xl hover:shadow-emerald-500/10 transition-all cursor-pointer overflow-hidden p-6 flex flex-col h-full bg-white/80 backdrop-blur-sm"
        style={{
          boxShadow:
            "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)",
        }}
      >
        {/* Header */}
        <div className="mb-3">
          <h2 className="text-lg font-bold text-emerald-600 mb-2">{title}</h2>
          <div className="flex items-start gap-2 mb-3">
            <Image
              src={`https://github.com/${authors}.png`}
              alt={authors}
              width={20}
              height={20}
              className="rounded-full self-start mt-0.5"
            />
            <p className="text-xs text-gray-600 font-semibold">{authors}</p>
          </div>
        </div>

        {/* Tags */}
        <div className="flex flex-wrap gap-2 mb-3">
          {tags.map((tag, index) => (
            <span
              key={index}
              className="px-2.5 py-1 text-gray-700 text-[10px] rounded-full border border-gray-300 bg-gray-50"
            >
              {tag}
            </span>
          ))}
        </div>

        {/* Description */}
        <p className="text-gray-700 text-xs mb-4 line-clamp-3 flex-1">
          {description}
        </p>

        {/* Action Bar */}
        <div className="flex items-center gap-4 pt-3 border-t border-gray-200">
          {language && (
            <div className="flex items-center gap-1.5 text-xs text-gray-600 font-normal">
              <span
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: getLanguageColor(language) }}
              />
              {language}
            </div>
          )}
          <div className="flex items-center gap-1.5 text-gray-600">
            <Star className="w-4 h-4" />
            <span className="text-xs">{stars}</span>
          </div>
          <div className="flex items-center gap-1.5 text-gray-600">
            <GitFork className="w-4 h-4" />
            <span className="text-xs">{forks}</span>
          </div>
          <div className="flex items-center gap-1.5 text-gray-600 ml-auto">
            <Bookmark className="w-4 h-4" />
          </div>
        </div>
      </motion.div>
    </Link>
  );
}
// GitHub 语言颜色映射
const getLanguageColor = (language: string | null): string => {
  if (!language) return "#586e75";

  const colorMap: Record<string, string> = {
    JavaScript: "#f1e05a",
    TypeScript: "#3178c6",
    Python: "#3572A5",
    Java: "#b07219",
    "C++": "#f34b7d",
    C: "#555555",
    "C#": "#239120",
    PHP: "#4F5D95",
    Ruby: "#701516",
    Go: "#00ADD8",
    Rust: "#dea584",
    Swift: "#FA7343",
    Kotlin: "#A97BFF",
    Dart: "#00B4AB",
    HTML: "#e34c26",
    CSS: "#563d7c",
    Shell: "#89e051",
    PowerShell: "#012456",
    Vue: "#4fc08d",
    React: "#61dafb",
    Angular: "#DD0031",
    Svelte: "#FF3E00",
    R: "#198CE7",
    MATLAB: "#e16737",
    Scala: "#c22d40",
    Clojure: "#db5855",
    Elixir: "#6e4a7e",
    Haskell: "#5e5086",
    Lua: "#000080",
    Perl: "#0298c3",
    "Objective-C": "#438eff",
    "Objective-C++": "#6866fb",
    TeX: "#3D6117",
    Markdown: "#083fa1",
    Dockerfile: "#384d54",
    Makefile: "#427819",
  };

  return colorMap[language] || "#586e75";
};
