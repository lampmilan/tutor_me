import { MobileBestOnPcNotice } from "@/components/MobileBestOnPcNotice";

export default function AppLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      {children}
      <MobileBestOnPcNotice />
    </>
  );
}
