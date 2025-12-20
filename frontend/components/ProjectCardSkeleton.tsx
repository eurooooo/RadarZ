import { Star, TrendingUp } from "lucide-react";

export default function ProjectCardSkeleton() {
  return (
    <div className="voxel-card mb-4 overflow-hidden flex animate-pulse">
      {/* Left Panel - Image Preview Skeleton */}
      <div className="w-48 shrink-0 relative border-r-3 border-black bg-gray-medium">
        <div className="h-full w-full flex flex-col items-center justify-center p-4">
          <div className="w-full h-full bg-gray-light"></div>
          {/* Stars indicator skeleton */}
          <div className="absolute bottom-2 left-2 right-2 flex items-center gap-1 text-xs text-black">
            <TrendingUp className="w-3 h-3" />
            <div className="h-3 w-8 bg-gray-light"></div>
          </div>
        </div>
      </div>

      {/* Right Panel - Content Skeleton */}
      <div className="flex-1 p-6 flex flex-col bg-white">
        {/* Header Skeleton */}
        <div className="mb-3">
          <div className="flex items-center justify-between mb-2">
            <div className="h-3 w-16 bg-gray-medium"></div>
          </div>
          <div className="h-6 w-48 bg-gray-medium mb-2"></div>
          <div className="h-4 w-24 bg-gray-medium mb-3"></div>
        </div>

        {/* Tags Skeleton */}
        <div className="flex flex-wrap gap-2 mb-3">
          <div className="h-6 w-16 bg-gray-medium"></div>
          <div className="h-6 w-20 bg-gray-medium"></div>
          <div className="h-6 w-14 bg-gray-medium"></div>
        </div>

        {/* Description Skeleton */}
        <div className="mb-4 flex-1 space-y-2">
          <div className="h-4 w-full bg-gray-medium"></div>
          <div className="h-4 w-full bg-gray-medium"></div>
          <div className="h-4 w-3/4 bg-gray-medium"></div>
        </div>

        {/* Action Bar Skeleton */}
        <div className="flex items-center gap-4 pt-4 border-t-3 border-black">
          <div className="h-4 w-12 bg-gray-medium"></div>
          <div className="h-4 w-12 bg-gray-medium"></div>
        </div>
      </div>
    </div>
  );
}
