"use client";

import { useState, useEffect } from "react";
import SearchBar from "@/components/SearchBar";
import SearchContainer from "@/components/SearchContainer";
import { useSearch } from "@/hooks/useSearch";

export default function Page() {
  const [showSearchBar, setShowSearchBar] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const { state, performSearch } = useSearch();

  // 处理搜索发送
  const handleSend = (query: string) => {
    if (query.trim()) {
      setSearchQuery(query.trim());
      setShowSearchBar(false);
      performSearch(query.trim());
    }
  };

  return (
    <>
      {showSearchBar ? (
        <SearchBar onSend={handleSend} />
      ) : (
        <SearchContainer query={searchQuery} state={state} />
      )}
    </>
  );
}
