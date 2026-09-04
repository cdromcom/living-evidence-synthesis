"use client";

import { useSyncExternalStore } from "react";

type Theme = "light" | "dark";

// A tiny external store rather than useState+useEffect: the initial value
// can only be read in the browser (localStorage/matchMedia), which
// useSyncExternalStore handles without the render-then-immediately-correct
// flash a mount effect would need, and without ever calling setState from
// inside an effect. Module-level since there's one theme per tab; no
// listener is needed for changes originating outside this module (matching
// the previous effect, which never re-read matchMedia after mount either).
let currentTheme: Theme | null = null;
let listeners: Array<() => void> = [];

function readStoredTheme(): Theme {
  const stored = window.localStorage.getItem("theme") as Theme | null;
  return (
    stored ??
    (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light")
  );
}

function getSnapshot(): Theme {
  if (currentTheme === null) currentTheme = readStoredTheme();
  return currentTheme;
}

function getServerSnapshot(): Theme | null {
  return null;
}

function subscribe(callback: () => void) {
  listeners.push(callback);
  return () => {
    listeners = listeners.filter((l) => l !== callback);
  };
}

function setTheme(next: Theme) {
  currentTheme = next;
  document.documentElement.setAttribute("data-theme", next);
  window.localStorage.setItem("theme", next);
  for (const listener of listeners) listener();
}

export default function ThemeToggle() {
  const theme = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);

  function toggle() {
    setTheme(theme === "dark" ? "light" : "dark");
  }

  return (
    <button
      type="button"
      onClick={toggle}
      aria-label={
        theme === null
          ? "Toggle theme"
          : theme === "dark"
            ? "Switch to light mode"
            : "Switch to dark mode"
      }
      className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full border border-border bg-card text-ink transition-colors hover:border-forest hover:text-forest focus:outline-none focus:ring-1 focus:ring-forest"
    >
      {theme === "dark" ? (
        // sun icon (click to go light)
        <svg
          width="15"
          height="15"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <circle cx="12" cy="12" r="4" />
          <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41" />
        </svg>
      ) : (
        // moon icon (click to go dark; also default render before hydration)
        <svg
          width="15"
          height="15"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79Z" />
        </svg>
      )}
    </button>
  );
}
