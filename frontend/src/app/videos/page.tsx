"use client";

import "./videos.css";

export default function VideosPage() {
  return (
    <div className="videos-page">
      <h1 className="videos-title">영상</h1>
      <div className="video-list">
        <div className="feed-empty">크리에이터 영상이 아직 없습니다</div>
      </div>
    </div>
  );
}
