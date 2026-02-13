"use client";

import "./chat.css";

export default function ChatPage() {
  return (
    <div className="chat-page">
      <h1 className="chat-page-title">채팅</h1>
      <div className="chat-room-list">
        <div className="feed-empty">참여 중인 채팅방이 없습니다</div>
      </div>
    </div>
  );
}
