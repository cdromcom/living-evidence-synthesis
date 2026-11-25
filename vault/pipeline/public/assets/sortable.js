/* ==========================================================================
   Lightweight sort + filter for markdown tables on the Topics page.
   ==========================================================================
   Targets every <table> inside .ls-leaderboard (added by the Topics-page
   hook). For each table:
     • inserts a search input above
     • makes <th> cells clickable to sort the table by that column
     • supports numeric, percent, and emoji-strength sorting
   No external libraries.
   ========================================================================== */

(function () {
  "use strict";

  // Strength + Winner ordering — used when sorting those columns.
  const STRENGTH_RANK = {
    strong: 3,
    moderate: 2,
    limited: 1,
  };
  const WINNER_RANK = {
    ai: 4,
    "human + ai": 3,
    tie: 2,
    human: 1,
    "—": 0,
  };

  function init() {
    document.querySelectorAll(".ls-leaderboard table").forEach(decorate);
  }

  function decorate(table) {
    if (table.dataset.lsDecorated) return;
    table.dataset.lsDecorated = "1";
    table.classList.add("ls-table");

    addFilter(table);
    addSortHandlers(table);
  }

  function addFilter(table) {
    const wrap = document.createElement("div");
    wrap.className = "ls-filter-wrap";

    const input = document.createElement("input");
    input.type = "search";
    input.className = "ls-filter";
    input.placeholder = "Filter rows — model, technique, winner, strength…";
    input.setAttribute("aria-label", "Filter table rows");

    const counter = document.createElement("span");
    counter.className = "ls-filter-count";

    wrap.appendChild(input);
    wrap.appendChild(counter);
    table.parentNode.insertBefore(wrap, table);

    const tbodyRows = table.querySelectorAll("tbody tr");
    const total = tbodyRows.length;
    counter.textContent = `${total} rows`;

    input.addEventListener("input", () => {
      const q = input.value.trim().toLowerCase();
      let visible = 0;
      tbodyRows.forEach((tr) => {
        const match = !q || tr.textContent.toLowerCase().includes(q);
        tr.style.display = match ? "" : "none";
        if (match) visible++;
      });
      counter.textContent = q
        ? `${visible} of ${total} rows`
        : `${total} rows`;
    });
  }

  function addSortHandlers(table) {
    const headers = table.querySelectorAll("thead th");
    headers.forEach((th, idx) => {
      // The Details column is just an arrow link — not meaningful to sort.
      const label = th.textContent.trim().toLowerCase();
      if (label === "details" || label === "") return;

      th.classList.add("ls-sortable-th");
      th.setAttribute("role", "button");
      th.setAttribute("tabindex", "0");

      const handler = () => sortBy(table, idx, th);
      th.addEventListener("click", handler);
      th.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          handler();
        }
      });
    });
  }

  function sortBy(table, colIdx, header) {
    const tbody = table.querySelector("tbody");
    const rows = Array.from(tbody.querySelectorAll("tr"));
    const direction = header.classList.contains("ls-sort-asc")
      ? "desc"
      : "asc";

    // Detect column kind from the column's text values.
    const cells = rows.map((r) => (r.cells[colIdx]?.textContent || "").trim());
    const kind = detectKind(header, cells);

    rows.sort((a, b) => {
      const av = (a.cells[colIdx]?.textContent || "").trim();
      const bv = (b.cells[colIdx]?.textContent || "").trim();
      return cmp(av, bv, kind);
    });

    if (direction === "desc") rows.reverse();
    rows.forEach((r) => tbody.appendChild(r));

    // Update header sort state.
    table.querySelectorAll("thead th").forEach((t) => {
      t.classList.remove("ls-sort-asc", "ls-sort-desc");
    });
    header.classList.add(`ls-sort-${direction}`);
  }

  function detectKind(header, cells) {
    const label = header.textContent.trim().toLowerCase();
    if (label === "evidence strength" || label.includes("strength"))
      return "strength";
    if (label === "winner") return "winner";
    if (label === "effect size") return "effect";
    // Numeric if every non-dash cell parses as a number.
    const nonDash = cells.filter((c) => c && c !== "—" && c !== "-");
    if (
      nonDash.length > 0 &&
      nonDash.every((c) => !isNaN(parseFloat(c.replace(/[^\d.\-]/g, ""))))
    ) {
      return "numeric";
    }
    return "string";
  }

  function cmp(a, b, kind) {
    if (kind === "strength") {
      return rankCmp(a, b, STRENGTH_RANK);
    }
    if (kind === "winner") {
      return rankCmp(a, b, WINNER_RANK);
    }
    if (kind === "effect") {
      // Effect-size cells like "+20 pp", "−0.15 F1", "≈ 0 (parity)".
      // Sort by the leading signed number; pure-text values fall to the bottom.
      const an = parseSignedLead(a);
      const bn = parseSignedLead(b);
      if (isNaN(an) && isNaN(bn)) return a.localeCompare(b);
      if (isNaN(an)) return 1;
      if (isNaN(bn)) return -1;
      return an - bn;
    }
    if (kind === "numeric") {
      const an = parseFloat(a.replace(/[^\d.\-]/g, ""));
      const bn = parseFloat(b.replace(/[^\d.\-]/g, ""));
      if (isNaN(an) && isNaN(bn)) return 0;
      if (isNaN(an)) return 1;
      if (isNaN(bn)) return -1;
      return an - bn;
    }
    return a.localeCompare(b, undefined, { sensitivity: "base" });
  }

  function parseSignedLead(s) {
    // Pull the first signed numeric token from `s`. Treats Unicode minus (−)
    // and hyphen (-) as negative; "+" as positive; bare numbers as positive.
    const m = s.match(/[+\-−]?\s*\d+(?:\.\d+)?/);
    if (!m) return NaN;
    return parseFloat(m[0].replace(/−/g, "-").replace(/\s+/g, ""));
  }

  function rankCmp(a, b, rank) {
    const ar = rank[a.toLowerCase()] ?? -1;
    const br = rank[b.toLowerCase()] ?? -1;
    return ar - br;
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
