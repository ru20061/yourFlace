"use client";

import "./search.css";

const WEEKDAYS = ["일", "월", "화", "수", "목", "금", "토"];

export default function SearchPage() {
  return (
    <div className="search-page">
      <h1 className="search-title">검색</h1>

      {/* 검색바 */}
      <div className="search-bar">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
        <input type="text" placeholder="아티스트, 이벤트, 게시글 검색..." />
      </div>

      {/* 캘린더 검색 UI */}
      <div className="search-calendar">
        <div className="search-calendar-header">
          <span className="search-calendar-month">2026년 2월</span>
          <div className="search-calendar-nav">
            <button>&lt;</button>
            <button>&gt;</button>
          </div>
        </div>
        <div className="search-calendar-weekdays">
          {WEEKDAYS.map((day) => (
            <div key={day} className="search-calendar-weekday">{day}</div>
          ))}
        </div>
        <div className="search-calendar-days">
          {Array.from({ length: 28 }, (_, i) => (
            <div
              key={i}
              className={`search-calendar-day ${i + 1 === 13 ? "today" : ""}`}
            >
              {i + 1}
            </div>
          ))}
        </div>
      </div>

      {/* 검색 필터 */}
      <div className="search-filters">
        <button className="search-filter-chip active">전체</button>
        <button className="search-filter-chip">아티스트</button>
        <button className="search-filter-chip">게시글</button>
        <button className="search-filter-chip">이벤트</button>
        <button className="search-filter-chip">상품</button>
      </div>

      {/* 검색 결과 */}
      <div className="search-results">
        <div className="feed-empty">검색어를 입력하세요</div>
      </div>
    </div>
  );
}
