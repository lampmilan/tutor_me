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
