"use client";

import "./gallery.css";

export default function GalleryPage() {
  return (
    <div className="gallery-page">
      <div className="gallery-header">
        <h1 className="gallery-title">갤러리</h1>
      </div>
      <div className="gallery-grid">
        <div className="feed-empty" style={{ gridColumn: "1 / -1" }}>
          아티스트 이미지가 아직 없습니다
        </div>
      </div>
    </div>
  );
}
