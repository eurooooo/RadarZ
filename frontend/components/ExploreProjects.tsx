import ProjectCard from "./ProjectCard";
import { type Project } from "@/data/mockProjects";

const BACKEND_BASE_URL =
  process.env.NEXT_PUBLIC_BACKEND_BASE_URL ?? "http://127.0.0.1:8000";

async function fetchProjects(): Promise<Project[]> {
  const res = await fetch(`${BACKEND_BASE_URL}/projects`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch projects: ${res.status}`);
  }

  return (await res.json()) as Project[];
}

export default async function ExploreProjects() {
  let projects: Project[] = [];

  try {
    projects = await fetchProjects();
  } catch (error) {
    console.error("Error fetching projects", error);
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-primary mb-6">Explore Projects</h1>

      {projects.length > 0 ? (
        <div>
          {projects.map((project) => (
            <ProjectCard key={project.id} {...project} />
          ))}
        </div>
      ) : (
        <p className="text-sm text-gray-500">No projects found.</p>
      )}
    </div>
  );
}
