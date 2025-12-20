import { useState, useCallback } from "react";

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

export interface SearchState {
  searchQueries: string[];
  validatingCriteria: string;
  searchProgress: number;
  projects: Project[];
  isSearching: boolean;
  isComplete: boolean;
}

export function useSearch() {
  const [state, setState] = useState<SearchState>({
    searchQueries: [],
    validatingCriteria: "",
    searchProgress: 0,
    projects: [],
    isSearching: false,
    isComplete: false,
  });

  const performSearch = useCallback(async (query: string) => {
    if (!query.trim()) return;

    // 重置状态
    setState({
      searchQueries: [],
      validatingCriteria: "",
      searchProgress: 0,
      projects: [],
      isSearching: true,
      isComplete: false,
    });

    try {
      const response = await fetch(
        `http://localhost:8000/search?user_input=${encodeURIComponent(query)}`
      );

      if (!response.ok) {
        throw new Error("Search failed");
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) return;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const data = JSON.parse(line.slice(6));

              if (data.type === "search_queries") {
                setState((prev) => ({
                  ...prev,
                  searchQueries: data.data,
                }));
              } else if (data.type === "validating_criteria") {
                setState((prev) => ({
                  ...prev,
                  validatingCriteria: data.data,
                }));
              } else if (data.type === "search_progress") {
                setState((prev) => ({
                  ...prev,
                  searchProgress: data.data.total,
                }));
              } else if (data.type === "project") {
                setState((prev) => ({
                  ...prev,
                  projects: [...prev.projects, data.data],
                }));
              } else if (data.type === "complete") {
                setState((prev) => ({
                  ...prev,
                  isComplete: true,
                  isSearching: false,
                }));
              } else if (data.type === "error") {
                console.error("Search error:", data.data);
                setState((prev) => ({
                  ...prev,
                  isSearching: false,
                }));
              }
            } catch (e) {
              console.error("Failed to parse SSE data:", e);
            }
          }
        }
      }
    } catch (error) {
      console.error("Search error:", error);
      setState((prev) => ({
        ...prev,
        isSearching: false,
      }));
    }
  }, []);

  return {
    state,
    performSearch,
  };
}
