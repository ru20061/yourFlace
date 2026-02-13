"use client";

import Link from "next/link";
import "./footer.css";

interface FooterProps {
  isSubscribed?: boolean;
  isAdmin?: boolean;
}

export default function Footer({ isSubscribed = false, isAdmin = false }: FooterProps) {
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

        {/* 검색 */}
        <Link href="/search" className="footer-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8" />
            <line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
          <span>검색</span>
        </Link>

        {/* 알림 */}
        <Link href="/notifications" className="footer-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9" />
            <path d="M13.73 21a2 2 0 01-3.46 0" />
          </svg>
          <span>알림</span>
        </Link>

        {/* 마이페이지 */}
        <Link href="/profile" className="footer-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
          <span>MY</span>
        </Link>

        {/* 아티스트 채팅 - 구독자만 보임, 관리자는 안 보임 */}
        {isSubscribed && !isAdmin && (
          <Link href="/chat" className="footer-chat-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
            </svg>
            <span>채팅</span>
          </Link>
        )}
      </nav>
    </footer>
  );
}
