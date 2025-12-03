"use client";

import { useEffect, useState } from "react";
import ExploreProjects from "../ExploreProjects";
import { mockProjects, type Project } from "@/data/mockProjects";
import BottomSearchBar from "./BottomSearchBar";

export default function CenterContent() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading delay for better UX
    const timer = setTimeout(() => {
      setProjects(mockProjects);
      setLoading(false);
    }, 500);

    return () => clearTimeout(timer);
  }, []);

  return (
    <main className="flex-1 ml-60 min-h-screen relative">
      <div className="max-w-4xl mx-auto px-6 py-8 pb-24">
        <ExploreProjects projects={projects} loading={loading} />
        <BottomSearchBar />
      </div>
    </main>
  );
}
