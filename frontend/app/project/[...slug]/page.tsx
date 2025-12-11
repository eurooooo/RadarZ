import ProjectViewer from "@/components/project/ProjectViewer";
import AIAssistant from "@/components/project/AIAssistant";

interface PageProps {
  params: Promise<{
    slug?: string[];
  }>;
}

export default async function ProjectDetailPage({ params }: PageProps) {
  const resolved = await params;
  const slug = (resolved.slug ?? []).join("/") || "";

  return (
    <>
      <ProjectViewer slug={slug} />
      <AIAssistant />
    </>
  );
}
