import Link from "next/link";
import { Star, GitFork, Bookmark, TrendingUp } from "lucide-react";

interface ProjectCardProps {
  id: string;
  title: string;
  authors: string;
  date: string;
  description: string;
  tags: string[];
  stars: number;
  forks: number;
}

export default function ProjectCard({
  id,
  title,
  authors,
  date,
  description,
  tags,
  stars,
  forks,
}: ProjectCardProps) {
  return (
    <Link href={`/project/${id}`}>
      <div className="border border-gray-200 rounded-lg mb-4 hover:shadow-md transition-all cursor-pointer overflow-hidden flex">
        {/* Left Panel - Image Preview */}
        <div className="w-48 shrink-0 relative  border-r border-gray-200">
          {/* Loading placeholder - skeleton */}
          <div className="h-full w-full flex flex-col items-center justify-center p-4 animate-pulse">
            <div className="w-full h-full bg-gray-200 rounded-lg mb-2"></div>
            {/* Views indicator */}
            <div className="flex items-center gap-1 text-xs text-gray-500 mt-2">
              <TrendingUp className="w-3 h-3" />
              <span>{stars}</span>
            </div>
          </div>
        </div>

        {/* Right Panel - Content */}
        <div className="flex-1 p-6 flex flex-col">
          {/* Header */}
          <div className="mb-3">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs text-gray-500">{date}</span>
            </div>
            <h2 className="text-xl font-bold text-primary mb-2">{title}</h2>
            <p className="text-sm text-gray-600 mb-3">{authors}</p>
          </div>

          {/* Tags */}
          <div className="flex flex-wrap gap-2 mb-3">
            {tags.map((tag, index) => (
              <span
                key={index}
                className="px-2.5 py-1  text-gray-700 text-xs rounded-md"
              >
                {tag}
              </span>
            ))}
          </div>

          {/* Description */}
          <p className="text-gray-700 text-sm mb-4 line-clamp-3 flex-1">
            {description}
          </p>

          {/* Action Bar */}
          <div className="flex items-center gap-4 pt-4 border-t border-gray-100">
            <div className="flex items-center gap-1.5 text-gray-600">
              <Star className="w-4 h-4" />
              <span className="text-sm">{stars}</span>
            </div>
            <div className="flex items-center gap-1.5 text-gray-600">
              <GitFork className="w-4 h-4" />
              <span className="text-sm">{forks}</span>
            </div>
            <div className="flex items-center gap-1.5 text-gray-600 ml-auto">
              <Bookmark className="w-4 h-4" />
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
}
