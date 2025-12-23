import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import LeftSidebar from "@/components/LeftSidebar";

const inter = Inter({
  variable: "--font-sans",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "RadarZ - GitHub 项目发现",
  description: "发现和探索 GitHub 项目",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className={`${inter.variable} antialiased`}>
        <div className="min-h-screen flex">
          <LeftSidebar />
          <main className="flex-1 min-h-screen bg-content bg-content-gradient">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
