"use client";

import "./artists.css";

export default function ArtistsPage() {
  return (
    <div className="artists-page">
      <h1 className="artists-title">아티스트</h1>
      <div className="artists-grid">
        <div className="feed-empty" style={{ gridColumn: "1 / -1" }}>
          등록된 아티스트가 없습니다
        </div>
      </div>
    </div>
  );
}
