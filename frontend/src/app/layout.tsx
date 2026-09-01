import type { Metadata } from "next";
import { IBM_Plex_Mono, Montserrat } from "next/font/google";
import "./globals.css";
import { CookieConsentBanner } from "@/components/CookieConsentBanner";
import { MobileBestOnPcNotice } from "@/components/MobileBestOnPcNotice";
import { PostHogProvider } from "@/components/PostHogProvider";

const sans = Montserrat({
  variable: "--font-montserrat",
  subsets: ["latin", "latin-ext"],
  weight: ["400", "500", "600", "700"],
});

const mono = IBM_Plex_Mono({
  variable: "--font-ibm-plex-mono",
  subsets: ["latin", "latin-ext"],
  weight: ["400", "500", "700"],
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
    <html lang="hu">
      <body className={`${sans.variable} ${mono.variable} antialiased`}>
        <PostHogProvider>
          {children}
          <MobileBestOnPcNotice />
          <CookieConsentBanner />
        </PostHogProvider>
      </body>
    </html>
  );
}
