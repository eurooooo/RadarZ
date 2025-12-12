import { Suspense } from "react";
import Summary from "./project/Summary";

export default async function ProjectViewer({ slug }: { slug: string }) {
  return (
    <main className="flex-1 ml-60 mr-[40%] h-screen overflow-y-auto">
      <div className="max-w-4xl mx-auto px-8 py-8">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-primary mb-2">{slug}</h1>
        </div>
        <Suspense fallback={<div>Loading...</div>}>
          <Summary slug={slug} />
        </Suspense>
      </div>
    </main>
  );
}
