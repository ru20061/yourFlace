"use client";

import "./banners.css";

export default function BannersPage() {
  return (
    <div className="banners-page">
      <h1 className="banners-title">배너 관리</h1>
      <div className="banner-list">
        <div className="feed-empty">등록된 배너가 없습니다</div>
      </div>
    </div>
  );
}
