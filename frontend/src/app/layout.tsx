import type { Metadata } from "next";
import { IBM_Plex_Mono, Montserrat } from "next/font/google";
import "./globals.css";
import { DeferredClientChrome } from "@/components/DeferredClientChrome";

const PAGE_BG = "#0e1412";
const PAGE_FG = "#e7efe9";

const sans = Montserrat({
  variable: "--font-montserrat",
  subsets: ["latin", "latin-ext"],
  weight: ["400", "500", "600", "700"],
  display: "swap",
  preload: false,
});

const mono = IBM_Plex_Mono({
  variable: "--font-ibm-plex-mono",
  subsets: ["latin", "latin-ext"],
  weight: ["700"],
  display: "swap",
  preload: true,
});

export const metadata: Metadata = {
  title: "VizsgaGO",
  description: "Online coding practice for the Hungarian programming érettségi",
  icons: {
    icon: [
      { url: "/favicons/favicon.ico", sizes: "any" },
      {
        url: "/favicons/favicon-16x16.png",
        sizes: "16x16",
        type: "image/png",
      },
      {
        url: "/favicons/favicon-32x32.png",
        sizes: "32x32",
        type: "image/png",
      },
    ],
    apple: {
      url: "/favicons/apple-touch-icon.png",
      sizes: "180x180",
      type: "image/png",
    },
  },
  manifest: "/favicons/site.webmanifest",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="hu" style={{ backgroundColor: PAGE_BG, color: PAGE_FG }}>
      <body
        className={`${sans.variable} ${mono.variable} antialiased`}
        style={{ backgroundColor: PAGE_BG, color: PAGE_FG, margin: 0 }}
      >
        {children}
        <DeferredClientChrome />
      </body>
    </html>
  );
}
