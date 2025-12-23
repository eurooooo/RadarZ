import { Suspense } from "react";
import Summary from "./Summary";
import { Loader2 } from "lucide-react";

export default async function ProjectViewer({ slug }: { slug: string }) {
  return (
    <main className="flex-1 overflow-y-auto">
      <div className="max-w-4xl mx-auto px-8 py-8">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">{slug}</h1>
        </div>
        <Suspense
          fallback={
            <div className="flex items-center justify-center py-20">
              <Loader2 className="w-8 h-8 text-emerald-500 animate-spin" />
            </div>
          }
        >
          <Summary slug={slug} />
        </Suspense>
      </div>
    </main>
  );
}
