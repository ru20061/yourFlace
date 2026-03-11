"use client";

import "./celebs.css";

export default function ArtistsPage() {
  return (
    <div className="artists-page">
      <h1 className="artists-title">크리에이터</h1>
      <div className="artists-grid">
        <div className="feed-empty" style={{ gridColumn: "1 / -1" }}>
          등록된 크리에이터가 없습니다
        </div>
      </div>
    </div>
  );
}
