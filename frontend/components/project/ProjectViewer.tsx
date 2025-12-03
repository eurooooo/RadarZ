"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getProjectById, type Project } from "@/data/mockProjects";
import BottomSearchBar from "@/components/layout/BottomSearchBar";

export default function ProjectViewer() {
  const params = useParams();
  const id = params.id as string;
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading delay for better UX
    const timer = setTimeout(() => {
      const foundProject = getProjectById(id);
      setProject(foundProject || null);
      setLoading(false);
    }, 300);

    return () => clearTimeout(timer);
  }, [id]);

  return (
    <main className="flex-1 ml-60 mr-[40%]">
      <div className="max-w-4xl mx-auto px-8 py-8">
        {loading ? (
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/2 mb-4"></div>
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-8"></div>
            <div className="h-screen bg-gray-100 rounded"></div>
          </div>
        ) : project ? (
          <>
            <div className="mb-6">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                {project.title}
              </h1>
              <p className="text-gray-600 mb-4">{project.description}</p>
              <div className="flex gap-2 flex-wrap">
                {project.tags.map((tag, index) => (
                  <span
                    key={index}
                    className="px-2.5 py-1 bg-gray-100 text-gray-700 text-xs rounded-full"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
            <div className="h-screen bg-gray-50 border border-gray-200 rounded-lg flex items-center justify-center">
              <div className="text-center">
                <p className="text-gray-500 text-lg mb-2">
                  Readme / Code Viewer Placeholder
                </p>
                <p className="text-gray-400 text-sm">
                  This area will display the project README and code files
                </p>
              </div>
            </div>
          </>
        ) : (
          <div className="h-screen bg-gray-50 border border-gray-200 rounded-lg flex items-center justify-center">
            <p className="text-gray-500">Project not found</p>
          </div>
        )}
      </div>
      <BottomSearchBar />
    </main>
  );
}
