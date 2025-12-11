const BACKEND_BASE_URL =
  process.env.NEXT_PUBLIC_BACKEND_BASE_URL ?? "http://127.0.0.1:8000";

interface SummaryResponse {
  repo: string | null;
  summary: string;
}

async function Summary({ slug }: { slug: string }) {
  const res = await fetch(
    `${BACKEND_BASE_URL}/summary/readme?repo_name=${encodeURIComponent(slug)}`,
    { cache: "no-store" }
  );

  if (!res.ok) {
    return (
      <div className="h-screen bg-red-50 border border-red-200 rounded-lg flex items-center justify-center px-6 text-red-600">
        加载摘要失败: {res.status}
      </div>
    );
  }

  const data = (await res.json()) as SummaryResponse;
  return (
    <div className="h-screen border border-gray-200 rounded-lg p-6 bg-white">
      <pre className="whitespace-pre-wrap text-sm text-gray-800 leading-6">
        {data.summary}
      </pre>
    </div>
  );
}

export default Summary;
