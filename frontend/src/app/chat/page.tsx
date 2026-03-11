"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { api } from "../../lib/api";
import type { ChatRoom, PaginatedResponse } from "../data/types";
import "./chat.css";

function formatTime(isoStr: string | null): string {
  if (!isoStr) return "";
  const date = new Date(isoStr);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMin = Math.floor(diffMs / 60000);
  if (diffMin < 1) return "방금";
  if (diffMin < 60) return `${diffMin}분 전`;
  const diffHr = Math.floor(diffMin / 60);
  if (diffHr < 24) return `${diffHr}시간 전`;
  return `${date.getMonth() + 1}/${date.getDate()}`;
}

export default function ChatPage() {
  const [rooms, setRooms] = useState<ChatRoom[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get<PaginatedResponse<ChatRoom>>("/chat-rooms?skip=0&limit=100")
      .then((res) => setRooms(res.items.filter((r) => r.status === "active")))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="chat-page">
      <h1 className="chat-page-title">채팅</h1>
      <div className="chat-room-list">
        {loading && <div className="feed-empty">로딩 중...</div>}
        {!loading && rooms.length === 0 && (
          <div className="feed-empty">참여 중인 채팅방이 없습니다</div>
        )}
        {rooms.map((room) => (
          <Link key={room.id} href={`/chat/${room.id}`} className="chat-room-item">
            <div className="chat-room-avatar">
              <span style={{ fontSize: 18, fontWeight: 700, color: "var(--color-main)" }}>
                {(room.room_name ?? "채팅")[0]}
              </span>
            </div>
            <div className="chat-room-info">
              <div className="chat-room-name">{room.room_name ?? `채팅방 ${room.id}`}</div>
              <div className="chat-room-last-message">
                {room.last_message_at ? "최근 메시지 있음" : "메시지 없음"}
              </div>
            </div>
            <div className="chat-room-meta">
              <span className="chat-room-time">{formatTime(room.last_message_at)}</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
