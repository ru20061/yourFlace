"use client";

import Link from "next/link";
import "./header.css";

interface HeaderProps {
  isAdmin?: boolean;
  isLoggedIn?: boolean;
  onToggleSidebar: () => void;
  onLogout?: () => void;
}

export default function Header({ isAdmin = false, isLoggedIn = false, onToggleSidebar, onLogout }: HeaderProps) {
  return (
    <header className="header">
      {/* 왼쪽: 햄버거 */}
      <div className="header-left">
        <button className="hamburger-btn" onClick={onToggleSidebar} aria-label="메뉴 열기">
          <span />
          <span />
          <span />
        </button>
      </div>

      {/* 중앙: 로고 또는 관리자 검색바 */}
      <div className="header-center">
        {isAdmin ? (
          <div className="admin-search">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            <input type="text" placeholder="검색..." />
          </div>
        ) : (
          <Link href="/" className="logo">
            yourFlace
          </Link>
        )}
      </div>

      {/* 오른쪽: MY(로그인시) + 로그아웃 또는 로그인 */}
      <div className="header-right">
        {isLoggedIn ? (
          <>
            <Link href="/profile" className="header-link">
              MY
            </Link>
            <button className="header-link" onClick={onLogout}>로그아웃</button>
          </>
        ) : (
          <Link href="/login" className="auth-btn">
            로그인
          </Link>
        )}
      </div>
    </header>
  );
}
