import Link from "next/link";
import Image from "next/image";
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
  image_url?: string | null;
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
  image_url,
}: ProjectCardProps) {
  return (
    <Link href={`/project/${id}`} className="block max-w-2xl">
      <div className="border border-gray-200 rounded-lg mb-4 hover:shadow-md transition-all cursor-pointer overflow-hidden flex">
        {/* Left Panel - Image Preview */}

        {/* Right Panel - Content */}
        <div className="flex-1 p-6 flex flex-col">
          {/* Header */}
          <div className="mb-3">
            <h2 className="text-xl font-bold text-primary mb-2">{title}</h2>
            <div className="flex items-start gap-2 mb-3">
              <Image
                src={`https://github.com/${authors}.png`}
                alt={authors}
                width={20}
                height={20}
                className="rounded-full self-start mt-0.5"
              />
              <p className="text-sm text-gray-600">{authors}</p>
            </div>
          </div>

          {/* Tags */}
          <div className="flex flex-wrap gap-2 mb-3">
            {tags.map((tag, index) => (
              <span
                key={index}
                className="px-2.5 py-1 text-gray-700 text-xs rounded-full border border-gray-300 bg-gray-50"
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
          <div className="flex items-center gap-4 pt-4 border-t border-gray-200">
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
