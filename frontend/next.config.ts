import type { NextConfig } from "next";

const backendUrl = process.env.BACKEND_URL || "http://backend:8000";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Browser calls /api/*; Next proxies to the backend service on the Compose network.
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
