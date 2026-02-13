"use client";

import { useState } from "react";
import "./home.css";

const TABS = ["유저 포스트", "아티스트 포스트", "아티스트 이미지", "아티스트 동영상"] as const;

export default function HomePage() {
  const [activeTab, setActiveTab] = useState<(typeof TABS)[number]>(TABS[0]);

  return (
    <div className="home-page">
      {/* 카테고리 탭 - HEADER 바로 아래 */}
      <nav className="category-tabs">
        {TABS.map((tab) => (
          <button
            key={tab}
            className={`category-tab ${activeTab === tab ? "active" : ""}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </button>
        ))}
      </nav>

      {/* 피드 콘텐츠 영역 */}
      <div className="feed-container">
        {activeTab === "유저 포스트" && (
          <div className="feed-list">
            <div className="feed-empty">유저 포스트가 아직 없습니다</div>
          </div>
        )}
        {activeTab === "아티스트 포스트" && (
          <div className="feed-list">
            <div className="feed-empty">아티스트 포스트가 아직 없습니다</div>
          </div>
        )}
        {activeTab === "아티스트 이미지" && (
          <div className="gallery-grid">
            <div className="feed-empty">아티스트 이미지가 아직 없습니다</div>
          </div>
        )}
        {activeTab === "아티스트 동영상" && (
          <div className="video-list">
            <div className="feed-empty">아티스트 동영상이 아직 없습니다</div>
          </div>
        )}
      </div>
    </div>
  );
}
