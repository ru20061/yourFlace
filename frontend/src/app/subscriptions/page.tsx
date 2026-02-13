"use client";

import "./subscriptions.css";

export default function SubscriptionsPage() {
  return (
    <div className="subscriptions-page">
      <h1 className="subscriptions-title">내 구독</h1>
      <div className="subscription-list">
        <div className="feed-empty">구독 중인 아티스트가 없습니다</div>
      </div>
    </div>
  );
}
