import Link from "next/link";
import Image from "next/image";
import { Star, GitFork, Bookmark } from "lucide-react";

interface ProjectCardProps {
  id: string;
  title: string;
  authors: string;
  description: string;
  tags: string[];
  stars: number;
  forks: number;
  language?: string | null;
}

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
    <Link href={`/project/${id}`} className="block">
      <div className="voxel-card cursor-pointer overflow-hidden p-6 flex flex-col h-full hover:translate-x-1 hover:translate-y-1 transition-transform">
        {/* Header */}
        <div className="mb-3">
          <h2
            className="text-xl font-bold text-black mb-2"
            style={{ textShadow: "2px 2px 0px #808080" }}
          >
            {title}
          </h2>
          <div className="flex items-start gap-2 mb-3">
            <div className="voxel-border p-1 bg-white">
              <Image
                src={`https://github.com/${authors}.png`}
                alt={authors}
                width={20}
                height={20}
                className="block"
              />
            </div>
            <p className="text-sm text-black font-bold">{authors}</p>
          </div>
        </div>

        {/* Tags */}
        <div className="flex flex-wrap gap-2 mb-3">
          {tags.map((tag, index) => (
            <span
              key={index}
              className="voxel-button px-3 py-1 text-black text-xs bg-gray-light font-semibold"
            >
              {tag}
            </span>
          ))}
        </div>

        {/* Description */}
        <p className="text-black text-sm mb-4 line-clamp-3 flex-1 font-medium">
          {description}
        </p>

        {/* Action Bar */}
        <div className="flex items-center gap-4 pt-3 border-t-3 border-black">
          {language && (
            <div className="flex items-center gap-1.5 text-sm text-black font-bold">
              <span
                className="w-4 h-4 voxel-border"
                style={{ backgroundColor: getLanguageColor(language) }}
              />
              {language}
            </div>
          )}
          <div className="flex items-center gap-1.5 text-black font-bold">
            <Star className="w-4 h-4" />
            <span className="text-sm">{stars}</span>
          </div>
          <div className="flex items-center gap-1.5 text-black font-bold">
            <GitFork className="w-4 h-4" />
            <span className="text-sm">{forks}</span>
          </div>
          <div className="flex items-center gap-1.5 text-black ml-auto">
            <div className="voxel-button p-1.5 bg-orange">
              <Bookmark className="w-4 h-4 text-white" />
            </div>
          </div>
        </div>
      </div>
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
