"use client";

import "./notices.css";

export default function NoticesPage() {
  return (
    <div className="notices-page">
      <h1 className="notices-title">공지사항 관리</h1>
      <div className="notice-list">
        <div className="feed-empty">등록된 공지사항이 없습니다</div>
      </div>
    </div>
  );
}
