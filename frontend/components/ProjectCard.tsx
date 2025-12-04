import Link from "next/link";
import Image from "next/image";
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
    <Link href={`/project/${id}`}>
      <div className="border border-gray-200 rounded-lg mb-4 hover:shadow-md transition-all cursor-pointer overflow-hidden flex">
        {/* Left Panel - Image Preview */}
        <div className="w-48 shrink-0 relative border-r border-gray-200 bg-gray-100">
          {image_url ? (
            <>
              <Image
                src={image_url}
                alt={`${title} preview`}
                fill
                className="object-cover"
                unoptimized
              />
              {/* Stars indicator overlay */}
              <div className="absolute bottom-2 left-2 right-2 flex items-center gap-1 text-xs text-white bg-black/50 backdrop-blur-sm px-2 py-1 rounded">
                <TrendingUp className="w-3 h-3" />
                <span>{stars}</span>
              </div>
            </>
          ) : (
            /* Fallback placeholder */
            <div className="h-full w-full flex flex-col items-center justify-center p-4 bg-gradient-to-br from-gray-100 to-gray-200">
              <div className="w-full h-full flex items-center justify-center">
                <div className="text-center">
                  <div className="w-16 h-16 mx-auto mb-2 bg-gray-300 rounded-lg flex items-center justify-center">
                    <Star className="w-8 h-8 text-gray-400" />
                  </div>
                  <p className="text-xs text-gray-500 mt-2">No Preview</p>
                </div>
              </div>
              {/* Stars indicator */}
              <div className="absolute bottom-2 left-2 right-2 flex items-center gap-1 text-xs text-gray-600">
                <TrendingUp className="w-3 h-3" />
                <span>{stars}</span>
              </div>
            </div>
          )}
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
