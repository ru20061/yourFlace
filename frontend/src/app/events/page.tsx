"use client";

import "./events.css";

export default function EventsPage() {
  return (
    <div className="events-page">
      <h1 className="events-title">이벤트</h1>
      <div className="event-list">
        <div className="feed-empty">등록된 이벤트가 없습니다</div>
      </div>
    </div>
  );
}
