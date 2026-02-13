"use client";

import { useState } from "react";
import "./artist-detail.css";

const TABS = ["포스트", "이미지", "영상"] as const;

export default function ArtistDetailPage() {
  const [activeTab, setActiveTab] = useState<(typeof TABS)[number]>(TABS[0]);

  return (
    <div className="artist-detail-page">
      {/* 커버 이미지 */}
      <div className="artist-profile-header">
        <div className="artist-cover" />
        <div className="artist-profile-info">
          <div className="artist-avatar-large" />
          <h1 className="artist-name">아티스트명</h1>
          <p className="artist-bio">아티스트 소개가 여기에 표시됩니다.</p>
          <div className="artist-social-links">
            <span className="artist-social-link">Instagram</span>
            <span className="artist-social-link">Twitter</span>
          </div>
          <button className="artist-subscribe-btn">구독하기</button>
        </div>
      </div>

      {/* 통계 */}
      <div className="artist-stats">
        <div className="artist-stat-item">
          <div className="artist-stat-value">0</div>
          <div className="artist-stat-label">구독자</div>
        </div>
        <div className="artist-stat-item">
          <div className="artist-stat-value">0</div>
          <div className="artist-stat-label">게시글</div>
        </div>
        <div className="artist-stat-item">
          <div className="artist-stat-value">0</div>
          <div className="artist-stat-label">이미지</div>
        </div>
      </div>

      {/* 콘텐츠 탭 */}
      <nav className="artist-content-tabs">
        {TABS.map((tab) => (
          <button
            key={tab}
            className={`artist-content-tab ${activeTab === tab ? "active" : ""}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </button>
        ))}
      </nav>

      <div style={{ padding: 16 }}>
        <div className="feed-empty">콘텐츠가 아직 없습니다</div>
      </div>
    </div>
  );
}
