"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, X } from "lucide-react";

/**
 * Compact navigation for widths below 1100px. A disclosure button
 * (aria-expanded / aria-controls) reveals the same links as the desktop nav.
 * Escape closes it and returns focus to the button; following a link closes it.
 */
export default function MobileNav({ items }: { items: { href: string; label: string }[] }) {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();
  const buttonRef = useRef<HTMLButtonElement>(null);
  const [lastPath, setLastPath] = useState(pathname);
  if (pathname !== lastPath) {
    setLastPath(pathname);
    setOpen(false);
  }

  useEffect(() => {
    if (!open) return;
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") {
        setOpen(false);
        buttonRef.current?.focus();
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  return (
    <div className="min-[1180px]:hidden">
      <button
        ref={buttonRef}
        type="button"
        aria-expanded={open}
        aria-controls="mobile-nav-menu"
        aria-label={open ? "Close menu" : "Open menu"}
        onClick={() => setOpen((v) => !v)}
        className="flex h-11 w-11 items-center justify-center rounded-md border border-border bg-card text-ink transition-colors hover:border-forest hover:text-forest"
      >
        {open ? <X className="h-5 w-5" aria-hidden /> : <Menu className="h-5 w-5" aria-hidden />}
      </button>
      {open && (
        <nav
          id="mobile-nav-menu"
          aria-label="Main"
          className="absolute inset-x-0 top-14 z-40 border-b border-border bg-paper px-4 py-2 shadow-md sm:px-6"
        >
          <ul className="mx-auto grid max-w-6xl grid-cols-1 sm:grid-cols-2">
            {items.map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  aria-current={pathname === item.href || pathname.startsWith(item.href + "/") ? "page" : undefined}
                  className="flex min-h-11 items-center text-sm text-muted-ink transition-colors hover:text-ink aria-[current=page]:font-semibold aria-[current=page]:text-ink"
                >
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      )}
    </div>
  );
}
