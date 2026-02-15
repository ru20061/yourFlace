"use client";

import { useState, useEffect } from "react";
import { api } from "../../lib/api";
import type { Notice, PaginatedResponse } from "../data/types";
import "./notices.css";

export default function NoticesPage() {
  const [notices, setNotices] = useState<Notice[]>([]);
  const [loading, setLoading] = useState(true);
  const [openId, setOpenId] = useState<number | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const res = await api.get<PaginatedResponse<Notice>>("/notices?skip=0&limit=100");
        setNotices(res.items.filter((n) => n.is_active));
      } catch {
        // 조회 실패 시 빈 목록
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const formatDate = (dateStr: string) =>
    new Date(dateStr).toLocaleDateString("ko-KR", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });

  const toggle = (id: number) => setOpenId((prev) => (prev === id ? null : id));

  if (loading) {
    return (
      <div className="notices-page">
        <div className="feed-empty">로딩 중...</div>
      </div>
    );
  }

  return (
    <div className="notices-page">
      <div className="notices-header">
        <h1 className="notices-title">공지사항</h1>
        <p className="notices-subtitle">Flace의 새로운 소식을 확인하세요</p>
      </div>

      {notices.length === 0 ? (
        <div className="feed-empty">등록된 공지사항이 없습니다</div>
      ) : (
        <div className="notices-list">
          {notices.map((notice) => (
            <div
              key={notice.id}
              className={`notice-card${openId === notice.id ? " open" : ""}`}
              onClick={() => toggle(notice.id)}
            >
              <div className="notice-card-header">
                <div className="notice-card-left">
                  <div className="notice-card-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
                      <polyline points="14 2 14 8 20 8" />
                    </svg>
                  </div>
                  <span className="notice-card-title">{notice.title}</span>
                </div>
                <span className="notice-card-date">{formatDate(notice.created_at)}</span>
                <svg className="notice-card-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="9 18 15 12 9 6" />
                </svg>
              </div>

              {openId === notice.id && (
                <div className="notice-card-body">
                  <div className="notice-card-message">{notice.message}</div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
