"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useAuth } from "../../../lib/auth-context";
import { api } from "../../../lib/api";
import type { ChatRoom, ChatMessage, PaginatedResponse } from "../../data/types";
import "./chat-room.css";

interface ChatImageRef {
  id: number;
  chat_message_id: number;
  image_id: number;
}

interface ImageInfo {
  id: number;
  url: string;
}

function formatTime(isoStr: string): string {
  const date = new Date(isoStr);
  const h = date.getHours();
  const m = String(date.getMinutes()).padStart(2, "0");
  const ampm = h < 12 ? "오전" : "오후";
  return `${ampm} ${h % 12 || 12}:${m}`;
}

export default function ChatRoomPage() {
  const params = useParams();
  const roomId = Number(params.roomId);
  const { user } = useAuth();

  const [room, setRoom] = useState<ChatRoom | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  // messageId → image URL
  const [imageMap, setImageMap] = useState<Record<number, string>>({});
  const [loading, setLoading] = useState(true);
  const [inputText, setInputText] = useState("");
  const [brokenImgs, setBrokenImgs] = useState<Set<number>>(new Set());
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!roomId) return;

    (async () => {
      try {
        const [roomRes, msgRes] = await Promise.all([
          api.get<ChatRoom>(`/chat-rooms/${roomId}`),
          api.get<PaginatedResponse<ChatMessage>>(
            `/chat-messages?room_id=${roomId}&skip=0&limit=200`
          ),
        ]);
        setRoom(roomRes);

        const msgs = msgRes.items.filter((m) => m.status === "active");
        setMessages(msgs);

        // 이미지 타입 메시지의 실제 이미지 URL 조회
        const imgMsgIds = msgs
          .filter((m) => m.message_type === "image")
          .map((m) => m.id);

        if (imgMsgIds.length > 0) {
          const chatImgRes = await api.get<PaginatedResponse<ChatImageRef>>(
            `/chat-images?skip=0&limit=200`
          );
          // 이 채팅방 메시지에 해당하는 것만 추출
          const relevantChatImgs = chatImgRes.items.filter((ci) =>
            imgMsgIds.includes(ci.chat_message_id)
          );

          // 각 image_id로 실제 URL 조회
          const newImageMap: Record<number, string> = {};
          await Promise.all(
            relevantChatImgs.map(async (ci) => {
              try {
                const imgInfo = await api.get<ImageInfo>(`/images/${ci.image_id}`);
                newImageMap[ci.chat_message_id] = imgInfo.url;
              } catch {
                // 이미지 조회 실패 시 placeholder
                newImageMap[ci.chat_message_id] = "/placeholder-image.png";
              }
            })
          );
          setImageMap(newImageMap);
        }
      } catch {
        // 오류 무시
      } finally {
        setLoading(false);
      }
    })();
  }, [roomId]);

  // 새 메시지 오면 스크롤 아래로
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // 고정 메시지
  const pinnedMsg = messages.find((m) => m.is_pinned);

  const sendMessage = async () => {
    if (!inputText.trim() || !user) return;
    try {
      const newMsg = await api.post<ChatMessage>("/chat-messages", {
        chat_room_id: roomId,
        sender_id: user.id,
        sender_type: "fan",
        message_type: "text",
        content: inputText.trim(),
      });
      setMessages((prev) => [...prev, newMsg]);
      setInputText("");
    } catch {
      // 전송 실패 무시
    }
  };

  if (loading) {
    return (
      <div className="chat-room-page">
        <div style={{ padding: 24, textAlign: "center", color: "var(--text-tertiary)" }}>
          로딩 중...
        </div>
      </div>
    );
  }

  return (
    <div className="chat-room-page">
      {/* 헤더 */}
      <div className="chat-room-header">
        <Link href="/chat" className="chat-room-back">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </Link>
        <div className="chat-room-header-avatar" />
        <div>
          <div className="chat-room-header-name">{room?.room_name ?? `채팅방 ${roomId}`}</div>
          <div className="chat-room-header-status">활성</div>
        </div>
      </div>

      {/* 고정 메시지 */}
      {pinnedMsg && pinnedMsg.content && (
        <div className="chat-pinned">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="12" y1="17" x2="12" y2="22" />
            <path d="M5 17H19V13L17 7H7L5 13V17Z" />
            <line x1="12" y1="7" x2="12" y2="3" />
          </svg>
          {pinnedMsg.content}
        </div>
      )}

      {/* 메시지 영역 */}
      <div className="chat-messages">
        {messages.length === 0 && (
          <div style={{ textAlign: "center", color: "var(--text-tertiary)", fontSize: 14, marginTop: 40 }}>
            메시지가 없습니다
          </div>
        )}
        {messages.map((msg) => {
          const isMine = user && msg.sender_id === user.id;
          return (
            <div key={msg.id} className={`chat-message${isMine ? " mine" : ""}`}>
              {!isMine && <div className="chat-message-avatar" />}
              <div className="chat-message-bubble">
                {msg.message_type === "image" ? (
                  imageMap[msg.id] && !brokenImgs.has(msg.id) ? (
                    <img
                      src={imageMap[msg.id]}
                      alt="이미지"
                      style={{ maxWidth: 200, borderRadius: 8, display: "block" }}
                      onError={() => setBrokenImgs((prev) => new Set(prev).add(msg.id))}
                    />
                  ) : (
                    <span style={{ color: "var(--text-tertiary)", fontStyle: "italic" }}>📷 이미지</span>
                  )
                ) : msg.message_type === "video" ? (
                  <span style={{ color: "var(--text-tertiary)", fontStyle: "italic" }}>🎥 동영상</span>
                ) : (
                  msg.content || <span style={{ color: "var(--text-tertiary)", fontStyle: "italic" }}>내용 없음</span>
                )}
              </div>
              <span className="chat-message-time">{formatTime(msg.created_at)}</span>
            </div>
          );
        })}
        <div ref={messagesEndRef} />
      </div>

      {/* 메시지 입력 */}
      <div className="chat-input-bar">
        <input
          className="chat-input"
          placeholder="메시지를 입력하세요..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              sendMessage();
            }
          }}
        />
        <button className="chat-send-btn" onClick={sendMessage}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="22" y1="2" x2="11" y2="13" />
            <polygon points="22 2 15 22 11 13 2 9 22 2" />
          </svg>
        </button>
      </div>
    </div>
  );
}
