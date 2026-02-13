"use client";

import "./event-detail.css";

export default function EventDetailPage() {
  return (
    <div className="event-detail-page">
      <div className="event-detail-image" />

      <div className="event-detail-info">
        <div className="event-detail-type">이벤트</div>
        <h1 className="event-detail-title">이벤트 제목</h1>

        <div className="event-detail-meta">
          <div className="event-meta-row">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="4" width="18" height="18" rx="2" />
              <line x1="16" y1="2" x2="16" y2="6" />
              <line x1="8" y1="2" x2="8" y2="6" />
              <line x1="3" y1="10" x2="21" y2="10" />
            </svg>
            <span>날짜 미정</span>
          </div>
          <div className="event-meta-row">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z" />
              <circle cx="12" cy="10" r="3" />
            </svg>
            <span>장소 미정</span>
          </div>
        </div>

        <div className="event-detail-desc">
          이벤트 상세 내용이 여기에 표시됩니다.
        </div>
      </div>

      <div className="event-detail-register-bar">
        <button className="event-detail-register-btn">참가 신청</button>
      </div>
    </div>
  );
}
