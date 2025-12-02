export interface Project {
  id: string;
  title: string;
  authors: string;
  date: string;
  description: string;
  tags: string[];
  stars: number;
  forks: number;
}

export const mockProjects: Project[] = [
  {
    id: "1",
    title: "facebook/react",
    authors: "Facebook",
    date: "2 days ago",
    description:
      "A declarative, efficient, and flexible JavaScript library for building user interfaces. React makes it painless to create interactive UIs.",
    tags: ["javascript", "react", "ui", "frontend"],
    stars: 234000,
    forks: 46000,
  },
  {
    id: "2",
    title: "vercel/next.js",
    authors: "Vercel",
    date: "1 day ago",
    description:
      "The React Framework for Production. Next.js gives you the best developer experience with all the features you need for production.",
    tags: ["javascript", "react", "nextjs", "framework"],
    stars: 125000,
    forks: 25000,
  },
  {
    id: "3",
    title: "microsoft/typescript",
    authors: "Microsoft",
    date: "3 days ago",
    description:
      "TypeScript is a superset of JavaScript that compiles to clean JavaScript output. It adds static type definitions to JavaScript.",
    tags: ["typescript", "language", "compiler"],
    stars: 98000,
    forks: 12800,
  },
  {
    id: "4",
    title: "tailwindlabs/tailwindcss",
    authors: "Tailwind Labs",
    date: "5 hours ago",
    description:
      "A utility-first CSS framework for rapidly building custom user interfaces. Build modern websites without ever leaving your HTML.",
    tags: ["css", "tailwind", "utility-first", "design"],
    stars: 75000,
    forks: 3900,
  },
  {
    id: "5",
    title: "openai/gpt-4",
    authors: "OpenAI",
    date: "1 week ago",
    description:
      "GPT-4 is a large multimodal model that can accept image and text inputs and produce text outputs. It exhibits human-level performance on various professional and academic benchmarks.",
    tags: ["ai", "machine-learning", "nlp", "gpt"],
    stars: 45000,
    forks: 5600,
  },
  {
    id: "6",
    title: "tensorflow/tensorflow",
    authors: "Google",
    date: "4 days ago",
    description:
      "An end-to-end open source platform for machine learning. TensorFlow makes it easy for beginners and experts to create machine learning models.",
    tags: ["python", "machine-learning", "tensorflow", "deep-learning"],
    stars: 180000,
    forks: 88000,
  },
  {
    id: "7",
    title: "nodejs/node",
    authors: "Node.js Foundation",
    date: "6 hours ago",
    description:
      "Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine. It uses an event-driven, non-blocking I/O model.",
    tags: ["javascript", "nodejs", "runtime", "backend"],
    stars: 102000,
    forks: 28000,
  },
  {
    id: "8",
    title: "vuejs/vue",
    authors: "Evan You",
    date: "1 day ago",
    description:
      "Vue.js is a progressive, incrementally-adoptable JavaScript framework for building UI on the web. It's designed from the ground up to be incrementally adoptable.",
    tags: ["javascript", "vue", "framework", "frontend"],
    stars: 210000,
    forks: 35000,
  },
];

export function getProjectById(id: string): Project | undefined {
  return mockProjects.find((project) => project.id === id);
}

