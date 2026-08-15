"use client";

import { useEffect, useMemo, useState } from "react";
import Fuse from "fuse.js";
import { ALL_NODES, type NodeType } from "@/lib/data";
import NodeTypeBadge from "./NodeTypeBadge";
import NodePicker from "./NodePicker";

const TYPE_OPTIONS: { value: NodeType; label: string; hint: string }[] = [
  { value: "QUE", label: "Question", hint: "an unknown the work addresses" },
  { value: "CLM", label: "Claim", hint: "a generalization across evidence" },
  { value: "EVD", label: "Evidence", hint: "one observation from one source" },
  { value: "CVT", label: "Caveat", hint: "a limitation qualifying evidence" },
  { value: "SRC", label: "Source", hint: "a paper this corpus cites" },
  { value: "EP", label: "Evidence Pattern", hint: "a finding recurring across papers" },
];

const MIN_WORDS = 50;
const MAX_WORDS = 250;

function countWords(s: string) {
  return s.trim() ? s.trim().split(/\s+/).length : 0;
}

export default function ContributeForm() {
  const [auth, setAuth] = useState<{ signedIn: boolean; login?: string } | null>(null);
  const [type, setType] = useState<NodeType>("CLM");
  const [title, setTitle] = useState("");
  const [citekey, setCitekey] = useState("");
  const [body, setBody] = useState("");
  const [addresses, setAddresses] = useState<string[]>([]);
  const [supports, setSupports] = useState<string[]>([]);
  const [derivedFrom, setDerivedFrom] = useState<string[]>([]);
  const [qualifies, setQualifies] = useState<string[]>([]);
  const [instantiates, setInstantiates] = useState<string[]>([]);
  const [relatesTo, setRelatesTo] = useState<string[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<{ compareUrl: string } | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/github/me")
      .then((r) => r.json())
      .then(setAuth)
      .catch(() => setAuth({ signedIn: false }));
  }, []);

  const dupFuse = useMemo(() => new Fuse(ALL_NODES, { keys: ["title"], threshold: 0.3 }), []);
  const duplicates = useMemo(() => {
    if (title.trim().length < 6) return [];
    return dupFuse.search(title).slice(0, 3);
  }, [dupFuse, title]);

  const words = countWords(body);
  const wordsOk = words >= MIN_WORDS && words <= MAX_WORDS;

  function resetEdges() {
    setAddresses([]);
    setSupports([]);
    setDerivedFrom([]);
    setQualifies([]);
    setInstantiates([]);
    setRelatesTo([]);
  }

  function requiredEdgesOk() {
    if (type === "CLM") return addresses.length > 0;
    if (type === "EVD") return derivedFrom.length > 0;
    if (type === "CVT") return qualifies.length > 0;
    if (type === "EP") return instantiates.length > 0;
    return true;
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const res = await fetch("/api/contribute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type,
          title,
          body,
          citekey: type === "SRC" ? citekey : undefined,
          edges: { addresses, supports, derivedFrom, qualifies, instantiates, relatesTo },
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Submission failed");
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Submission failed");
    } finally {
      setSubmitting(false);
    }
  }

  if (auth === null) return null;

  if (!auth.signedIn) {
    return (
      <div className="rounded-lg border border-border bg-card p-5">
        <h2 className="text-base font-semibold">Sign in to contribute</h2>
        <p className="mt-1.5 max-w-[60ch] text-sm text-muted-ink">
          Signing in with GitHub lets you submit a draft node directly. We
          fork this repo into your account, commit your draft on a branch,
          and hand you a link to open the pull request yourself. Nothing is
          published without your final click on GitHub.
        </p>
        <a
          href="/api/github/login?next=/contribute"
          className="mt-4 inline-flex items-center gap-2 rounded-lg bg-forest px-4 py-2 text-sm font-medium text-paper"
        >
          Sign in with GitHub
        </a>
      </div>
    );
  }

  if (result) {
    return (
      <div className="rounded-lg border border-border bg-card p-5">
        <h2 className="text-base font-semibold">Draft committed</h2>
        <p className="mt-1.5 max-w-[60ch] text-sm text-muted-ink">
          Your draft is on a branch in your fork. Open the pull request to
          finish: review the diff, add a description if you like, and click
          &quot;Create pull request&quot; on GitHub.
        </p>
        <a
          href={result.compareUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-4 inline-flex items-center gap-2 rounded-lg bg-forest px-4 py-2 text-sm font-medium text-paper"
        >
          Open pull request on GitHub ↗
        </a>
        <button
          type="button"
          onClick={() => {
            setResult(null);
            setTitle("");
            setBody("");
            resetEdges();
          }}
          className="ml-3 text-sm text-muted-ink hover:text-ink"
        >
          Submit another
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={submit} className="rounded-lg border border-border bg-card p-5">
      <div className="flex items-center justify-between">
        <h2 className="text-base font-semibold">Draft a node</h2>
        <span className="text-xs text-muted-ink">
          Signed in as <span className="font-medium text-ink">{auth.login}</span>
        </span>
      </div>

      <div className="mt-4">
        <label className="block text-xs font-semibold uppercase tracking-wide text-muted-ink">
          Type
        </label>
        <div className="mt-1.5 flex flex-wrap gap-1.5">
          {TYPE_OPTIONS.map((opt) => (
            <button
              key={opt.value}
              type="button"
              title={opt.hint}
              onClick={() => {
                setType(opt.value);
                resetEdges();
              }}
              className="rounded-full border px-1"
              style={{ borderColor: type === opt.value ? "transparent" : undefined }}
            >
              <span
                className={type === opt.value ? "opacity-100" : "opacity-50 hover:opacity-80"}
              >
                <NodeTypeBadge type={opt.value} />
              </span>
            </button>
          ))}
        </div>
      </div>

      <div className="mt-4">
        <label className="block text-xs font-semibold uppercase tracking-wide text-muted-ink" htmlFor="title">
          Title
        </label>
        <input
          id="title"
          required
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder={
            type === "SRC" ? "Full citation or paper title" : "A short, specific, readable title"
          }
          className="mt-1.5 w-full rounded-md border border-border bg-paper px-3 py-2 text-sm text-ink placeholder:text-muted-ink focus:border-forest focus:outline-none focus:ring-1 focus:ring-forest"
        />
        {duplicates.length > 0 && (
          <div className="mt-1.5 rounded-md border border-verdict-edit/40 bg-accent-wash p-2 text-xs">
            <p className="font-medium">Possibly already covered:</p>
            <ul className="mt-1 space-y-0.5">
              {duplicates.map((d) => (
                <li key={d.item.id} className="flex items-center gap-1.5">
                  <NodeTypeBadge type={d.item.type} />
                  <span className="mono text-muted-ink">{d.item.id}</span>
                  <span className="truncate">{d.item.title}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {type === "SRC" && (
        <div className="mt-4">
          <label className="block text-xs font-semibold uppercase tracking-wide text-muted-ink" htmlFor="citekey">
            Citekey
          </label>
          <input
            id="citekey"
            required
            value={citekey}
            onChange={(e) => setCitekey(e.target.value)}
            placeholder="e.g. smithExampleFinding2026"
            className="mono mt-1.5 w-full rounded-md border border-border bg-paper px-3 py-2 text-sm text-ink placeholder:text-muted-ink focus:border-forest focus:outline-none focus:ring-1 focus:ring-forest"
          />
        </div>
      )}

      <div className="mt-4">
        <label className="flex items-center justify-between text-xs font-semibold uppercase tracking-wide text-muted-ink" htmlFor="body">
          <span>Body (50-250 words)</span>
          <span className={wordsOk ? "text-forest" : "text-muted-ink"}>{words} words</span>
        </label>
        <textarea
          id="body"
          required
          rows={6}
          value={body}
          onChange={(e) => setBody(e.target.value)}
          placeholder="Self-contained prose. For Evidence: the finding plus a verbatim quote and page locator. For Claims: the generalization, present tense."
          className="mt-1.5 w-full rounded-md border border-border bg-paper px-3 py-2 text-sm text-ink placeholder:text-muted-ink focus:border-forest focus:outline-none focus:ring-1 focus:ring-forest"
        />
      </div>

      <div className="mt-4 space-y-4">
        {type === "CLM" && (
          <>
            <NodePicker
              label="Addresses (required)"
              hint="Which existing Question(s) does this claim respond to?"
              targetType="QUE"
              value={addresses}
              onChange={setAddresses}
            />
            <NodePicker
              label="Supporting evidence (optional)"
              hint="Existing Evidence nodes that already support this claim."
              targetType="EVD"
              value={supports}
              onChange={setSupports}
            />
          </>
        )}
        {type === "EVD" && (
          <>
            <NodePicker
              label="Derived from (required)"
              hint="Which Source is this observation drawn from?"
              targetType="SRC"
              value={derivedFrom}
              onChange={setDerivedFrom}
            />
            <NodePicker
              label="Supports claim(s) (optional)"
              hint="Existing Claims this evidence bears on."
              targetType="CLM"
              value={supports}
              onChange={setSupports}
            />
            <NodePicker
              label="Instantiates pattern (optional)"
              hint="An Evidence Pattern this observation is an instance of."
              targetType="EP"
              value={instantiates}
              onChange={setInstantiates}
            />
          </>
        )}
        {type === "CVT" && (
          <NodePicker
            label="Applies to (required)"
            hint="Which Evidence node(s) does this caveat qualify?"
            targetType="EVD"
            value={qualifies}
            onChange={setQualifies}
          />
        )}
        {type === "EP" && (
          <>
            <NodePicker
              label="Instantiating evidence (required)"
              hint="Evidence nodes from independent papers that instantiate this pattern."
              targetType="EVD"
              value={instantiates}
              onChange={setInstantiates}
            />
            <NodePicker
              label="Related claims (optional)"
              hint="Claims this pattern generalizes or connects to."
              targetType="CLM"
              value={relatesTo}
              onChange={setRelatesTo}
            />
          </>
        )}
      </div>

      <div className="mt-5">
        <div className="flex items-center gap-3">
          <button
            type="submit"
            disabled={submitting || !wordsOk || !title.trim() || !requiredEdgesOk()}
            className="rounded-lg bg-forest px-4 py-2 text-sm font-medium text-paper disabled:opacity-50"
          >
            {submitting ? "Committing draft…" : "Submit as draft PR"}
          </button>
        </div>
        {!submitting && (!wordsOk || !title.trim() || !requiredEdgesOk()) && (
          <ul className="mt-2 space-y-0.5 text-xs text-muted-ink">
            {!title.trim() && <li>• Title is required.</li>}
            {!wordsOk && (
              <li>
                • Body must be {MIN_WORDS}-{MAX_WORDS} words (currently {words}).
              </li>
            )}
            {!requiredEdgesOk() && <li>• Fill in the required link(s) above for this node type.</li>}
          </ul>
        )}
      </div>
      {error && <p className="mt-2 text-xs text-destructive">{error}</p>}
    </form>
  );
}
