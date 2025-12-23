export default function ProjectCardSkeleton() {
  return (
    <div className="border border-gray-200 rounded-lg hover:shadow-md transition-all overflow-hidden p-6 flex flex-col h-full animate-pulse">
      {/* Header Skeleton */}
      <div className="mb-3">
        <div className="h-6 w-3/4 bg-gray-200 rounded mb-2"></div>
        <div className="flex items-start gap-2 mb-3">
          <div className="w-5 h-5 rounded-full bg-gray-200"></div>
          <div className="h-4 w-24 bg-gray-200 rounded"></div>
        </div>
      </div>

      {/* Tags Skeleton */}
      <div className="flex flex-wrap gap-2 mb-3">
        <div className="h-6 w-16 bg-gray-200 rounded-full"></div>
        <div className="h-6 w-20 bg-gray-200 rounded-full"></div>
        <div className="h-6 w-14 bg-gray-200 rounded-full"></div>
      </div>

      {/* Description Skeleton */}
      <div className="mb-4 flex-1 space-y-2">
        <div className="h-4 w-full bg-gray-200 rounded"></div>
        <div className="h-4 w-full bg-gray-200 rounded"></div>
        <div className="h-4 w-3/4 bg-gray-200 rounded"></div>
      </div>

      {/* Action Bar Skeleton */}
      <div className="flex items-center gap-4 pt-3 border-t border-gray-200">
        <div className="h-4 w-12 bg-gray-200 rounded"></div>
        <div className="h-4 w-12 bg-gray-200 rounded"></div>
        <div className="h-4 w-12 bg-gray-200 rounded ml-auto"></div>
      </div>
    </div>
  );
}
