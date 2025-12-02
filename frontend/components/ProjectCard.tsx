import Link from "next/link";
import { Star, GitFork, Bookmark } from "lucide-react";

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
      <div className="bg-white border border-gray-100 rounded-lg p-6 mb-4 hover:shadow-md hover:-translate-y-0.5 transition-all cursor-pointer">
        {/* Header */}
        <div className="mb-3">
          <h2 className="text-lg font-bold text-gray-900 mb-1">{title}</h2>
          <p className="text-sm text-gray-500">
            {authors} • {date}
          </p>
        </div>

        {/* Description */}
        <p className="text-gray-700 text-sm mb-4 line-clamp-2">{description}</p>

        {/* Tags */}
        <div className="flex flex-wrap gap-2 mb-4">
          {tags.map((tag, index) => (
            <span
              key={index}
              className="px-2.5 py-1 bg-gray-100 text-gray-700 text-xs rounded-full"
            >
              {tag}
            </span>
          ))}
        </div>

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
    </Link>
  );
}
