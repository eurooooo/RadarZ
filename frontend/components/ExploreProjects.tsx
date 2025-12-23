import { Suspense } from "react";
import ProjectCard from "./ProjectCard";
import ProjectCardSkeleton from "./ProjectCardSkeleton";
import { Project } from "@/hooks/useSearch";
import { BACKEND_BASE_URL } from "@/lib/config";

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
      <h1 className="text-xl font-bold text-gray-800 mb-6">探索项目</h1>

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
