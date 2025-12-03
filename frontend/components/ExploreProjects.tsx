import ProjectCard from "./ProjectCard";
import ProjectCardSkeleton from "./ProjectCardSkeleton";
import { type Project } from "@/data/mockProjects";

interface ExploreProjectsProps {
  projects: Project[];
  loading: boolean;
}

export default function ExploreProjects({
  projects,
  loading,
}: ExploreProjectsProps) {
  return (
    <div>
      <h1 className="text-2xl font-bold text-primary mb-6">Explore Projects</h1>

      {loading && <ProjectCardSkeleton />}

      {!loading && projects.length > 0 && (
        <div>
          {projects.map((project) => (
            <ProjectCard key={project.id} {...project} />
          ))}
        </div>
      )}
    </div>
  );
}
