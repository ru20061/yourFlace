"use client";

import { useState, useEffect } from "react";
import { useAuth } from "../../lib/auth-context";
import { api } from "../../lib/api";
import { getRelativeTime } from "../../lib/utils";
import type { Notification, PaginatedResponse } from "../data/types";
import "./notifications.css";

const NOTI_TYPE_ICON: Record<string, JSX.Element> = {
  content: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
      <polyline points="14 2 14 8 20 8" />
    </svg>
  ),
  post: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
      <polyline points="14 2 14 8 20 8" />
    </svg>
  ),
  comment: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
    </svg>
  ),
  payment: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <rect x="1" y="4" width="22" height="16" rx="2" ry="2" />
      <line x1="1" y1="10" x2="23" y2="10" />
    </svg>
  ),
  event: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
      <line x1="16" y1="2" x2="16" y2="6" />
      <line x1="8" y1="2" x2="8" y2="6" />
      <line x1="3" y1="10" x2="21" y2="10" />
    </svg>
  ),
};

const DEFAULT_ICON = (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9" />
    <path d="M13.73 21a2 2 0 01-3.46 0" />
  </svg>
);

export default function NotificationsPage() {
  const { user, isLoading: authLoading } = useAuth();
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) return;
    (async () => {
      try {
        const res = await api.get<PaginatedResponse<Notification>>("/notifications/?skip=0&limit=100");
        const sorted = [...res.items].sort(
          (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        );
        setNotifications(sorted);
      } catch {
        // 조회 실패 시 빈 목록 유지
      } finally {
        setLoading(false);
      }
    })();
  }, [user]);

  const handleMarkRead = async (id: number) => {
    try {
      await api.patch(`/notifications/${id}`, { is_read: true });
      setNotifications((prev) =>
        prev.map((n) => (n.id === id ? { ...n, is_read: true } : n))
      );
    } catch {
      // 무시
    }
  };

  if (authLoading || loading) {
    return (
      <div className="notifications-page">
        <h1 className="notifications-title">알림</h1>
        <div className="feed-empty">로딩 중...</div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="notifications-page">
        <h1 className="notifications-title">알림</h1>
        <div className="feed-empty">로그인 후 이용해주세요</div>
      </div>
    );
  }

  return (
    <div className="notifications-page">
      <h1 className="notifications-title">알림</h1>
      <div className="notification-list">
        {notifications.length === 0 ? (
          <div className="feed-empty">알림이 없습니다</div>
        ) : (
          notifications.map((noti) => (
            <div
              key={noti.id}
              className={`notification-item${!noti.is_read ? " unread" : ""}`}
              onClick={() => { if (!noti.is_read) handleMarkRead(noti.id); }}
              style={{ cursor: !noti.is_read ? "pointer" : "default" }}
            >
              <div className="notification-icon">
                {NOTI_TYPE_ICON[noti.noti_type] ?? DEFAULT_ICON}
              </div>
              <div className="notification-content">
                {noti.title && (
                  <div className="notification-text">
                    <strong>{noti.title}</strong>
                  </div>
                )}
                {noti.message && (
                  <div className="notification-text">{noti.message}</div>
                )}
                <div className="notification-time">{getRelativeTime(noti.created_at)}</div>
              </div>
              {!noti.is_read && <div className="notification-unread-dot" />}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
