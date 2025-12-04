import { Star, TrendingUp } from "lucide-react";

export default function ProjectCardSkeleton() {
  return (
    <div className="border border-gray-200 rounded-lg mb-4 overflow-hidden flex animate-pulse">
      {/* Left Panel - Image Preview Skeleton */}
      <div className="w-48 shrink-0 relative border-r border-gray-200 bg-gray-200">
        <div className="h-full w-full flex flex-col items-center justify-center p-4">
          <div className="w-full h-full bg-gray-300 rounded-lg"></div>
          {/* Stars indicator skeleton */}
          <div className="absolute bottom-2 left-2 right-2 flex items-center gap-1 text-xs text-gray-500">
            <TrendingUp className="w-3 h-3" />
            <div className="h-3 w-8 bg-gray-300 rounded"></div>
          </div>
        </div>
      </div>

      {/* Right Panel - Content Skeleton */}
      <div className="flex-1 p-6 flex flex-col">
        {/* Header Skeleton */}
        <div className="mb-3">
          <div className="flex items-center justify-between mb-2">
            <div className="h-3 w-16 bg-gray-200 rounded"></div>
          </div>
          <div className="h-6 w-48 bg-gray-200 rounded mb-2"></div>
          <div className="h-4 w-24 bg-gray-200 rounded mb-3"></div>
        </div>

        {/* Tags Skeleton */}
        <div className="flex flex-wrap gap-2 mb-3">
          <div className="h-6 w-16 bg-gray-200 rounded"></div>
          <div className="h-6 w-20 bg-gray-200 rounded"></div>
          <div className="h-6 w-14 bg-gray-200 rounded"></div>
        </div>

        {/* Description Skeleton */}
        <div className="mb-4 flex-1 space-y-2">
          <div className="h-4 w-full bg-gray-200 rounded"></div>
          <div className="h-4 w-full bg-gray-200 rounded"></div>
          <div className="h-4 w-3/4 bg-gray-200 rounded"></div>
        </div>

        {/* Action Bar Skeleton */}
        <div className="flex items-center gap-4 pt-4 border-t border-gray-100">
          <div className="h-4 w-12 bg-gray-200 rounded"></div>
          <div className="h-4 w-12 bg-gray-200 rounded"></div>
        </div>
      </div>
    </div>
  );
}
