import { Suspense } from "react";
import Summary from "./Summary";

export default async function ProjectViewer({ slug }: { slug: string }) {
  return (
    <main className="flex-1 ml-60 mr-[40%] h-screen overflow-y-auto bg-sky-blue">
      <div className="max-w-4xl mx-auto px-8 py-8">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-black mb-2" style={{ textShadow: '3px 3px 0px #808080' }}>{slug}</h1>
        </div>
        <Suspense fallback={
          <div className="voxel-card p-6 bg-white">
            <div className="text-black font-bold">加载中...</div>
          </div>
        }>
          <Summary slug={slug} />
        </Suspense>
      </div>
    </main>
  );
}
