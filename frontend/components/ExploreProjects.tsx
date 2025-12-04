import { Suspense } from "react";
import ProjectCard from "./ProjectCard";
import ProjectCardSkeleton from "./ProjectCardSkeleton";
import { type Project } from "@/data/mockProjects";

const BACKEND_BASE_URL =
  process.env.NEXT_PUBLIC_BACKEND_BASE_URL ?? "http://127.0.0.1:8000";

async function fetchProjects(): Promise<Project[]> {
  const res = await fetch(`${BACKEND_BASE_URL}/projects`, {
    next: { revalidate: 10 }, // 每10秒重新验证
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch projects: ${res.status}`);
  }

  return (await res.json()) as Project[];
}

async function ProjectsList() {
  const projects = await fetchProjects();

  if (projects.length === 0) {
    return <p className="text-sm text-gray-500">No projects found.</p>;
  }

  return (
    <div>
      {projects.map((project) => (
        <ProjectCard key={project.id} {...project} />
      ))}
    </div>
  );
}

export default function ExploreProjects() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-primary mb-6">Explore Projects</h1>

      <Suspense
        fallback={
          <div>
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
