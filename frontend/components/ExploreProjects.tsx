import { Suspense } from "react";
import ProjectCard from "./ProjectCard";
import ProjectCardSkeleton from "./ProjectCardSkeleton";

const BACKEND_BASE_URL =
  process.env.NEXT_PUBLIC_BACKEND_BASE_URL ?? "http://127.0.0.1:8000";

export interface Project {
  id: string;
  title: string;
  authors: string;
  description: string;
  tags: string[];
  stars: number;
  forks: number;
  language?: string | null;
}

async function fetchProjects(): Promise<Project[]> {
  const res = await fetch(`${BACKEND_BASE_URL}/projects`, {
    next: { revalidate: 3600 },
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch projects: ${res.status}`);
  }

  return (await res.json()) as Project[];
}

async function ProjectsList() {
  const projects = await fetchProjects();

  if (projects.length === 0) {
    return <p className="text-xs text-gray-500">未找到项目。</p>;
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {projects.map((project) => (
        <ProjectCard key={project.id} {...project} />
      ))}
    </div>
  );
}

export default function ExploreProjects() {
  return (
    <div>
      <h1 className="text-xl font-bold text-primary mb-6">探索项目</h1>

      <Suspense
        fallback={
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {Array.from({ length: 5 }).map((_, index) => (
              <ProjectCardSkeleton key={index} />
            ))}
          </div>
        }
      >
        <ProjectsList />
      </Suspense>
    </div>
  );
}
