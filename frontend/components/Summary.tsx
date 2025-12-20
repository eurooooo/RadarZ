const BACKEND_BASE_URL =
  process.env.NEXT_PUBLIC_BACKEND_BASE_URL ?? "http://127.0.0.1:8000";

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
      <div className="voxel-card p-6 bg-red flex items-center justify-center text-white font-bold">
        加载摘要失败: {res.status}
      </div>
    );
  }

  const data = (await res.json()) as SummaryResponse;
  return (
    <div className="voxel-card p-6 bg-white">
      <pre className="whitespace-pre-wrap text-sm text-black leading-6 font-medium">
        {data.summary}
      </pre>
    </div>
  );
}

export default Summary;
