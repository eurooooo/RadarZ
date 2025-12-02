export default function ProjectCardSkeleton() {
  return (
    <div className="space-y-4">
      {[1, 2, 3].map((i) => (
        <div
          key={i}
          className="bg-white border border-gray-100 rounded-lg p-6 animate-pulse"
        >
          <div className="h-6 bg-gray-200 rounded w-1/3 mb-3"></div>
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-2/3 mb-4"></div>
          <div className="flex gap-2 mb-4">
            <div className="h-6 bg-gray-200 rounded-full w-16"></div>
            <div className="h-6 bg-gray-200 rounded-full w-20"></div>
          </div>
          <div className="h-8 bg-gray-200 rounded w-1/4"></div>
        </div>
      ))}
    </div>
  );
}
