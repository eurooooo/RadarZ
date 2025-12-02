"use client";

import CenterContent from "@/components/layout/CenterContent";
import RightSidebar from "@/components/layout/RightSidebar";
import LeftSidebar from "@/components/layout/LeftSidebar";

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      <div className="flex">
        <LeftSidebar />
        <CenterContent />
        <RightSidebar />
      </div>
    </div>
  );
}
