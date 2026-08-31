import { getNodesByType, getParentSource, getEvidencePatternsForEvd } from "@/lib/data";
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
    const eps = getEvidencePatternsForEvd(evd.id).map((ep) => ({ id: ep.id, title: ep.title }));
    return { evdId: evd.id, evdTitle: evd.title, srcId: src?.id ?? null, eps, values };
  });

  return (
    <main className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
      <h1 className="text-2xl font-semibold">Evidence Quality</h1>
      <p className="mt-1 max-w-[70ch] text-sm text-muted-ink">
        One row per Evidence node ({evds.length} total). Transparency and the four
        Validity domains are judged per finding; every other column is a signal about
        the source paper as a whole, inherited from its parent Source. Sort any column
        by clicking its header, filter with the search box, add or remove columns, and
        export the current view. Click any Evidence, Source, or Evidence Pattern cell
        to open its full page.
      </p>

      <EvidenceQualityTable rows={rows} />
    </main>
  );
}
