import type { NextConfig } from "next";

const backendUrl = (
  process.env.BACKEND_URL ||
  process.env.API_URL ||
  "http://localhost:8000"
).replace(/\/$/, "");

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Inline the small Tailwind bundle so first paint is not blocked on a CSS chunk.
  experimental: {
    inlineCss: true,
  },
  // Browser calls /api/*; Next rewrites to Cloud Run (prod) or Compose/local backend.
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${backendUrl}/:path*`,
      },
    ];
  },
};

export default nextConfig;
