import { MobileBestOnPcNotice } from "@/components/MobileBestOnPcNotice";

export default function ExamLayout({
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
