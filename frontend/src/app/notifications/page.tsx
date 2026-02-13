"use client";

import "./notifications.css";

export default function NotificationsPage() {
  return (
    <div className="notifications-page">
      <h1 className="notifications-title">알림</h1>
      <div className="notification-list">
        <div className="feed-empty">알림이 없습니다</div>
      </div>
    </div>
  );
}
