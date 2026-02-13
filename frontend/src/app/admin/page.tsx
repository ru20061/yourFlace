"use client";

import Link from "next/link";
import "./admin.css";

export default function AdminPage() {
  return (
    <div className="admin-page">
      <h1 className="admin-title">관리자 대시보드</h1>

      {/* 통계 카드 */}
      <div className="admin-dashboard">
        <div className="admin-stat-card">
          <div className="admin-stat-label">총 사용자</div>
          <div className="admin-stat-value">0</div>
        </div>
        <div className="admin-stat-card">
          <div className="admin-stat-label">총 아티스트</div>
          <div className="admin-stat-value">0</div>
        </div>
        <div className="admin-stat-card">
          <div className="admin-stat-label">총 구독</div>
          <div className="admin-stat-value">0</div>
        </div>
        <div className="admin-stat-card">
          <div className="admin-stat-label">총 매출</div>
          <div className="admin-stat-value">₩0</div>
        </div>
      </div>

      {/* 메뉴 */}
      <div className="admin-menu-list">
        <Link href="/admin/notices" className="admin-menu-item">
          <div className="admin-menu-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" /><polyline points="14 2 14 8 20 8" /></svg>
          </div>
          공지사항 관리
          <span className="admin-menu-arrow">&gt;</span>
        </Link>
        <Link href="/admin/banners" className="admin-menu-item">
          <div className="admin-menu-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="3" width="18" height="18" rx="2" /><line x1="3" y1="9" x2="21" y2="9" /></svg>
          </div>
          배너 관리
          <span className="admin-menu-arrow">&gt;</span>
        </Link>
        <Link href="/admin/faq" className="admin-menu-item">
          <div className="admin-menu-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10" /><path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3" /><line x1="12" y1="17" x2="12.01" y2="17" /></svg>
          </div>
          FAQ 관리
          <span className="admin-menu-arrow">&gt;</span>
        </Link>
      </div>
    </div>
  );
}
