"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export function Header() {
  const pathname = usePathname();
  
  return (
    <header className="site-header">
      <div className="brand">
        <Link href="/" style={{ display: "flex", alignItems: "center", gap: "0.85rem", textDecoration: "none", color: "inherit" }}>
          <div className="brand-mark" aria-hidden>
            <svg viewBox="0 0 32 32" fill="none">
              <path
                d="M8 14c0-4 2.5-7 6-7s5 2 6 4c1-2 3-4 6-4 3.5 0 6 3 6 7v6c0 2-1 4-3 4-2.5 0-4-2-5-3.5-.5 1-2 3.5-4.5 3.5S10 27 9 25.5C8 27 6 29 3.5 29 1.5 29 0 27 0 25V14z"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
              />
            </svg>
          </div>
          <div>
            <span className="brand-name">DantShaant</span>
            <span className="brand-tag">Autonomous dental AI</span>
          </div>
        </Link>
      </div>
      
      <nav style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
        <Link 
          href="/" 
          style={{ 
            padding: "0.5rem 1rem",
            fontSize: "0.85rem",
            fontWeight: pathname === "/" ? "600" : "500",
            color: pathname === "/" ? "var(--accent)" : "var(--text-muted)",
            textDecoration: "none",
            transition: "color 0.2s ease"
          }}
        >
          Analyzer
        </Link>
        <Link 
          href="/chat" 
          style={{ 
            padding: "0.5rem 1rem",
            fontSize: "0.85rem",
            fontWeight: pathname === "/chat" ? "600" : "500",
            color: pathname === "/chat" ? "var(--accent)" : "var(--text-muted)",
            textDecoration: "none",
            transition: "color 0.2s ease"
          }}
        >
          Chat
        </Link>
        <div className="header-badge">
          <span className="pulse-dot" />
          Demo ready
        </div>
      </nav>
    </header>
  );
}
