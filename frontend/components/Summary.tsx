import { BACKEND_BASE_URL } from "@/lib/config";

interface SummaryResponse {
  repo: string | null;
  summary: string;
}

async function Summary({ slug }: { slug: string }) {
  const res = await fetch(
    `${BACKEND_BASE_URL}/summary?repo_name=${encodeURIComponent(slug)}`,
    { cache: "no-store" }
  );

  if (!res.ok) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-2xl flex items-center justify-center px-6 py-12 text-red-600">
        加载摘要失败: {res.status}
      </div>
    );
  }

  const data = (await res.json()) as SummaryResponse;
  return (
    <div className="border border-gray-100 rounded-2xl p-6 bg-white shadow-sm">
      <pre className="whitespace-pre-wrap text-sm text-gray-700 leading-relaxed">
        {data.summary}
      </pre>
    </div>
  );
}

export default Summary;
