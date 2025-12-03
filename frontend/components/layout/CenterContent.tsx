import ExploreProjects from "../ExploreProjects";
import BottomSearchBar from "./BottomSearchBar";

export default function CenterContent() {
  return (
    <main className="flex-1 ml-60 min-h-screen relative">
      <div className="max-w-4xl mx-auto px-6 py-8 pb-24">
        <ExploreProjects />
        <BottomSearchBar />
      </div>
    </main>
  );
}
