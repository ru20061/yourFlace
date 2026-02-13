"use client";

import Link from "next/link";
import "./chat-room.css";

export default function ChatRoomPage() {
  return (
    <div className="chat-room-page">
      {/* 채팅방 헤더 */}
      <div className="chat-room-header">
        <Link href="/chat" className="chat-room-back">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </Link>
        <div className="chat-room-header-avatar" />
        <div>
          <div className="chat-room-header-name">아티스트명</div>
          <div className="chat-room-header-status">온라인</div>
        </div>
      </div>

      {/* 메시지 영역 */}
      <div className="chat-messages">
        <div className="chat-message">
          <div className="chat-message-avatar" />
          <div className="chat-message-bubble">안녕하세요!</div>
          <span className="chat-message-time">오후 2:30</span>
        </div>
        <div className="chat-message mine">
          <div className="chat-message-bubble">안녕하세요! 반갑습니다!</div>
          <span className="chat-message-time">오후 2:31</span>
        </div>
      </div>

      {/* 메시지 입력 */}
      <div className="chat-input-bar">
        <button className="chat-attach-btn">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48" />
          </svg>
        </button>
        <input className="chat-input" placeholder="메시지를 입력하세요..." />
        <button className="chat-send-btn">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="22" y1="2" x2="11" y2="13" />
            <polygon points="22 2 15 22 11 13 2 9 22 2" />
          </svg>
        </button>
      </div>
    </div>
  );
}
