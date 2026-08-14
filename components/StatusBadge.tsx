import { curationStatusTone } from "@/lib/ui";

const TONE_CLASS: Record<string, string> = {
  draft: "bg-muted-surface text-muted-ink border-border",
  reviewed: "bg-accent-wash text-forest border-forest/30",
  other: "bg-muted-surface text-muted-ink border-border",
};

export default function StatusBadge({ status }: { status: string }) {
  const tone = curationStatusTone(status);
  return (
    <span
      className={`inline-block rounded-full border px-2 py-0.5 text-[0.6875rem] font-semibold uppercase tracking-wide ${TONE_CLASS[tone]}`}
    >
      {status}
    </span>
  );
}
