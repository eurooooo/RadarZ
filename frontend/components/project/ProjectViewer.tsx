const BACKEND_BASE_URL =
  process.env.NEXT_PUBLIC_BACKEND_BASE_URL ?? "http://127.0.0.1:8000";

interface SummaryResponse {
  repo: string | null;
  summary: string;
}

interface ProjectViewerProps {
  slug: string;
}

export default async function ProjectViewer({ slug }: ProjectViewerProps) {
  const res = await fetch(
    `${BACKEND_BASE_URL}/summaries/readme?repo_name=${encodeURIComponent(
      slug
    )}`,
    { cache: "no-store" }
  );

  if (!res.ok) {
    return (
      <main className="flex-1 ml-60 mr-[40%] h-screen overflow-y-auto">
        <div className="max-w-4xl mx-auto px-8 py-8">
          <div className="h-screen bg-red-50 border border-red-200 rounded-lg flex items-center justify-center px-6 text-red-600">
            加载摘要失败: {res.status}
          </div>
        </div>
      </main>
    );
  }

  const data = (await res.json()) as SummaryResponse;

  return (
    <main className="flex-1 ml-60 mr-[40%] h-screen overflow-y-auto">
      <div className="max-w-4xl mx-auto px-8 py-8">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-primary mb-2">{slug}</h1>
          <p className="text-gray-600 mb-4">项目 README 摘要（后端实时生成）</p>
        </div>
        <div className="h-screen border border-gray-200 rounded-lg p-6 bg-white">
          <pre className="whitespace-pre-wrap text-sm text-gray-800 leading-6">
            {data.summary}
          </pre>
        </div>
      </div>
    </main>
  );
}
