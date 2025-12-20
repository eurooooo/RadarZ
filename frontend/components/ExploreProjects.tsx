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
    return <p className="text-sm text-black font-bold">未找到项目。</p>;
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
    <div className="p-6 bg-sky-blue min-h-screen">
      <h1 className="text-3xl font-bold text-black mb-6" style={{ textShadow: '3px 3px 0px #808080' }}>探索项目</h1>

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
