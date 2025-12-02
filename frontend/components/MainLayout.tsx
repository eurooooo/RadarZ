"use client";

import LeftSidebar from "./layout/LeftSidebar";
import CenterContent from "./layout/CenterContent";
import RightSidebar from "./layout/RightSidebar";

interface MainLayoutProps {
  children: React.ReactNode;
}

export default function MainLayout({ children }: MainLayoutProps) {
  return (
    <div className="min-h-screen bg-white">
      <div className="flex">
        <LeftSidebar />
        <CenterContent>{children}</CenterContent>
        <RightSidebar />
      </div>
    </div>
  );
}
