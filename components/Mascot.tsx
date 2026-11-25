/**
 * The site mascot: a small cherub with a halo riding the green tortoise.
 * Drawn inline so it follows the theme (shell uses the forest color) and needs
 * no image request. Decorative: the link next to it carries the name.
 */
export default function Mascot({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 44 34" className={className} aria-hidden="true" focusable="false">
      {/* tortoise */}
      <g className="text-forest">
        <path d="M5 26 C5 15 13 11 22 11 C31 11 37 16 37 26 Z" fill="currentColor" />
        <ellipse cx="38.6" cy="23.2" rx="4.2" ry="3.3" fill="currentColor" />
        <rect x="9" y="25" width="6" height="5.4" rx="2.2" fill="currentColor" />
        <rect x="27.5" y="25" width="6" height="5.4" rx="2.2" fill="currentColor" />
        <path d="M5.2 25.5 L1.6 27.4 L5.6 28.2 Z" fill="currentColor" />
      </g>
      <path d="M13 25 C13 18 17 14.5 22 14.5 M22 14.5 C27 14.5 31 18 31 25 M22 14.5 V25" fill="none" stroke="var(--color-paper)" strokeOpacity="0.55" strokeWidth="1" />
      <circle cx="40.2" cy="22.2" r="0.8" fill="var(--color-paper)" />
      {/* cherub */}
      <ellipse cx="16.4" cy="9.6" rx="3.6" ry="2" transform="rotate(-28 16.4 9.6)" fill="#fff" stroke="#b7b2a5" strokeWidth="0.6" />
      <ellipse cx="27.6" cy="9.6" rx="3.6" ry="2" transform="rotate(28 27.6 9.6)" fill="#fff" stroke="#b7b2a5" strokeWidth="0.6" />
      <path d="M18.8 13.2 C18.8 10 25.2 10 25.2 13.2 L26 15 H18 Z" fill="#fff" stroke="#b7b2a5" strokeWidth="0.6" />
      <circle cx="22" cy="6.8" r="2.9" fill="#f2c7a3" />
      <ellipse cx="22" cy="2.5" rx="3.1" ry="0.95" fill="none" stroke="#e0a91c" strokeWidth="1" />
      <circle cx="21" cy="6.8" r="0.35" fill="#6b4a33" />
      <circle cx="23" cy="6.8" r="0.35" fill="#6b4a33" />
      <path d="M19.2 14.6 L18 17 M24.8 14.6 L26 17" stroke="#f2c7a3" strokeWidth="1.3" strokeLinecap="round" />
    </svg>
  );
}
