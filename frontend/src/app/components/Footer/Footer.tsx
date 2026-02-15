"use client";

import Link from "next/link";
import "./footer.css";

interface FooterProps {
  isLoggedIn?: boolean;
  isAdmin?: boolean;
}

export default function Footer({ isLoggedIn = false, isAdmin = false }: FooterProps) {
  return (
    <footer className="footer">
      <nav className="footer-nav">
        {/* 홈 */}
        <Link href="/" className="footer-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
          </svg>
          <span>홈</span>
        </Link>

        {/* 공지 */}
        <Link href="/notices" className="footer-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
            <polyline points="14 2 14 8 20 8" />
            <line x1="16" y1="13" x2="8" y2="13" />
            <line x1="16" y1="17" x2="8" y2="17" />
            <polyline points="10 9 9 9 8 9" />
          </svg>
          <span>공지</span>
        </Link>

        {/* 알림 */}
        <Link href="/notifications" className="footer-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9" />
            <path d="M13.73 21a2 2 0 01-3.46 0" />
          </svg>
          <span>알림</span>
        </Link>

        {/* Shop - 로그인 시에만 */}
        {isLoggedIn && (
          <Link href="/shop" className="footer-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z" />
              <line x1="3" y1="6" x2="21" y2="6" />
              <path d="M16 10a4 4 0 01-8 0" />
            </svg>
            <span>Shop</span>
          </Link>
        )}
      </nav>
    </footer>
  );
}
