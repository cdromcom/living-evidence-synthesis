import { getNodesByType, getParentSource } from "@/lib/data";
import { QUALITY_COLUMNS } from "@/lib/qualityColumns";
import EvidenceQualityTable, { type QualityRow } from "@/components/EvidenceQualityTable";

export const metadata = { title: "Evidence Quality — Living Evidence Synthesis" };

export default function EvidenceQualityPage() {
  const evds = getNodesByType("EVD");

  const rows: QualityRow[] = evds.map((evd) => {
    const src = getParentSource(evd.id);
    const signalSource = src ?? evd;
    const values = Object.fromEntries(
      QUALITY_COLUMNS.map((c) => [c.id, c.value(evd, signalSource)])
    );
    return { evdId: evd.id, evdTitle: evd.title, srcId: src?.id ?? null, values };
  });

  return (
    <main className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
      <h1 className="text-2xl font-semibold">Evidence Quality</h1>
      <p className="mt-1 max-w-[70ch] text-sm text-muted-ink">
        One row per Evidence node ({evds.length} total). Transparency and the four
        Validity domains are judged per finding; every other column is a signal about
        the source paper as a whole, inherited from its parent Source. Add or remove
        columns below, or export the current view. Click any Evidence or Source cell
        to open its full page.
      </p>

      <EvidenceQualityTable rows={rows} />
    </main>
  );
}
