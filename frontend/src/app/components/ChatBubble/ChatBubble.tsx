"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { api } from "../../../lib/api";
import { useAuth } from "../../../lib/auth-context";
import type { SidebarCreator, ChatRoom, ChatMessage, PaginatedResponse } from "../../data/types";
import "./chatbubble.css";

interface ChatBubbleProps {
  subscribedCreators: SidebarCreator[];
}

interface ChatCreatorItem {
  creator: SidebarCreator;
  chatRoom: ChatRoom | null;
  lastMessage: string | null;
  lastMessageAt: string | null;
}

type View = "list" | "chat";

export default function ChatBubble({ subscribedCreators }: ChatBubbleProps) {
  const { user } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [view, setView] = useState<View>("list");
  const [chatList, setChatList] = useState<ChatCreatorItem[]>([]);
  const [loading, setLoading] = useState(false);
  const panelRef = useRef<HTMLDivElement>(null);

  // 채팅방 상태
  const [activeItem, setActiveItem] = useState<ChatCreatorItem | null>(null);
  const [activeRoom, setActiveRoom] = useState<ChatRoom | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [msgLoading, setMsgLoading] = useState(false);
  const [msgInput, setMsgInput] = useState("");
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 패널 외부 클릭 시 닫기
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (panelRef.current && !panelRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    }
    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [isOpen]);

  // 패널 닫힐 때 뷰 리셋
  useEffect(() => {
    if (!isOpen) {
      setView("list");
      setActiveItem(null);
      setActiveRoom(null);
      setMessages([]);
      setMsgInput("");
    }
  }, [isOpen]);

  // 패널 열 때 채팅방 목록 조회
  useEffect(() => {
    if (!isOpen || subscribedCreators.length === 0) return;

    (async () => {
      setLoading(true);
      try {
        const roomsRes = await api.get<PaginatedResponse<ChatRoom>>(
          "/chat-rooms/?skip=0&limit=100"
        );

        const roomByCreator = new Map<number, ChatRoom>();
        for (const room of roomsRes.items) {
          if (room.creator_id && room.status === "active") {
            roomByCreator.set(room.creator_id, room);
          }
        }

        const items: ChatCreatorItem[] = [];
        for (const creator of subscribedCreators) {
          const room = roomByCreator.get(creator.id) || null;
          let lastMessage: string | null = null;
          let lastMessageAt: string | null = null;

          if (room) {
            try {
              const msgsRes = await api.get<PaginatedResponse<ChatMessage>>(
                `/chat-messages/?skip=0&limit=1`
              );
              const roomMsgs = msgsRes.items.filter(
                (m) => m.chat_room_id === room.id && m.status === "active"
              );
              if (roomMsgs.length > 0) {
                lastMessage = roomMsgs[0].content;
                lastMessageAt = roomMsgs[0].created_at;
              }
            } catch {
              // ignore
            }
            lastMessageAt = lastMessageAt || room.last_message_at;
          }

          items.push({ creator, chatRoom: room, lastMessage, lastMessageAt });
        }

        setChatList(items);
      } catch {
        setChatList(
          subscribedCreators.map((creator) => ({
            creator,
            chatRoom: null,
            lastMessage: null,
            lastMessageAt: null,
          }))
        );
      } finally {
        setLoading(false);
      }
    })();
  }, [isOpen, subscribedCreators]);

  // 메시지 목록 불러오기
  const loadMessages = useCallback(async (roomId: number) => {
    setMsgLoading(true);
    try {
      const res = await api.get<PaginatedResponse<ChatMessage>>(
        `/chat-messages/?skip=0&limit=100`
      );
      const roomMsgs = res.items
        .filter((m) => m.chat_room_id === roomId && m.status === "active")
        .sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
      setMessages(roomMsgs);
    } catch {
      setMessages([]);
    } finally {
      setMsgLoading(false);
    }
  }, []);

  // 스크롤 하단으로
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // 크리에이터 클릭 → 채팅방 진입
  const handleChatClick = async (item: ChatCreatorItem) => {
    setActiveItem(item);

    if (item.chatRoom) {
      setActiveRoom(item.chatRoom);
      setView("chat");
      await loadMessages(item.chatRoom.id);
    } else {
      // 채팅방 없으면 새로 생성
      try {
        const newRoom = await api.post<ChatRoom>("/chat-rooms", {
          room_type: "subscription",
          creator_id: item.creator.id,
          room_name: item.creator.name,
          status: "active",
        });
        setActiveRoom(newRoom);
        setView("chat");
        setMessages([]);
      } catch {
        // 생성 실패 시 빈 채팅방 표시
        setActiveRoom(null);
        setView("chat");
        setMessages([]);
      }
    }
  };

  // 메시지 전송
  const handleSend = async () => {
    if (!msgInput.trim() || !activeRoom || sending) return;
    setSending(true);
    try {
      const newMsg = await api.post<ChatMessage>("/chat-messages", {
        chat_room_id: activeRoom.id,
        sender_type: "fan",
        message_type: "text",
        content: msgInput.trim(),
        status: "active",
      });
      setMessages((prev) => [...prev, newMsg]);
      setMsgInput("");
    } catch {
      alert("메시지 전송에 실패했습니다");
    } finally {
      setSending(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // 뒤로가기 (채팅 → 목록)
  const handleBack = () => {
    setView("list");
    setActiveItem(null);
    setActiveRoom(null);
    setMessages([]);
    setMsgInput("");
  };

  const formatTime = (dateStr: string | null) => {
    if (!dateStr) return "";
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    if (minutes < 1) return "방금";
    if (minutes < 60) return `${minutes}분 전`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}시간 전`;
    const days = Math.floor(hours / 24);
    if (days < 7) return `${days}일 전`;
    return date.toLocaleDateString("ko-KR", { month: "short", day: "numeric" });
  };

  const formatMsgTime = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleTimeString("ko-KR", { hour: "numeric", minute: "2-digit" });
  };

  if (subscribedCreators.length === 0) return null;

  return (
    <div className="chat-bubble-container" ref={panelRef}>
      {isOpen && (
        <div className="chat-bubble-panel">
          {view === "list" ? (
            <>
              {/* 목록 헤더 */}
              <div className="chat-bubble-panel-header">
                <span className="chat-bubble-panel-title">채팅</span>
                <button
                  className="chat-bubble-panel-close"
                  onClick={() => setIsOpen(false)}
                >
                  ✕
                </button>
              </div>

              {/* 크리에이터 목록 */}
              <div className="chat-bubble-panel-list">
                {loading ? (
                  <div className="chat-bubble-empty">불러오는 중...</div>
                ) : chatList.length === 0 ? (
                  <div className="chat-bubble-empty">구독한 크리에이터가 없습니다</div>
                ) : (
                  chatList.map((item) => (
                    <button
                      key={item.creator.id}
                      className="chat-bubble-item"
                      onClick={() => handleChatClick(item)}
                    >
                      <div className="chat-bubble-avatar">
                        {item.creator.profileImage ? (
                          <img
                            src={item.creator.profileImage}
                            alt={item.creator.name}
                          />
                        ) : (
                          <span className="chat-bubble-avatar-text">
                            {item.creator.name[0]}
                          </span>
                        )}
                      </div>
                      <div className="chat-bubble-info">
                        <div className="chat-bubble-name">{item.creator.name}</div>
                        <div className="chat-bubble-last-msg">
                          {item.lastMessage || "대화를 시작해보세요"}
                        </div>
                      </div>
                      {item.lastMessageAt && (
                        <div className="chat-bubble-time">
                          {formatTime(item.lastMessageAt)}
                        </div>
                      )}
                    </button>
                  ))
                )}
              </div>
            </>
          ) : (
            <>
              {/* 채팅방 헤더 */}
              <div className="chat-bubble-panel-header">
                <button className="chat-bubble-back" onClick={handleBack}>
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="15 18 9 12 15 6" />
                  </svg>
                </button>
                <div className="chat-bubble-room-avatar">
                  {activeItem?.creator.profileImage ? (
                    <img src={activeItem.creator.profileImage} alt="" />
                  ) : (
                    <span>{activeItem?.creator.name[0]}</span>
                  )}
                </div>
                <span className="chat-bubble-panel-title">
                  {activeItem?.creator.name}
                </span>
                <button
                  className="chat-bubble-panel-close"
                  onClick={() => setIsOpen(false)}
                  style={{ marginLeft: "auto" }}
                >
                  ✕
                </button>
              </div>

              {/* 메시지 영역 */}
              <div className="chat-bubble-messages">
                {msgLoading ? (
                  <div className="chat-bubble-empty">불러오는 중...</div>
                ) : messages.length === 0 ? (
                  <div className="chat-bubble-empty">
                    대화를 시작해보세요
                  </div>
                ) : (
                  messages.map((msg) => {
                    const isMine = msg.sender_id === user?.id;
                    return (
                      <div
                        key={msg.id}
                        className={`chat-bubble-msg ${isMine ? "mine" : ""}`}
                      >
                        {!isMine && (
                          <div className="chat-bubble-msg-avatar">
                            {activeItem?.creator.profileImage ? (
                              <img src={activeItem.creator.profileImage} alt="" />
                            ) : (
                              <span>{activeItem?.creator.name[0]}</span>
                            )}
                          </div>
                        )}
                        <div className="chat-bubble-msg-bubble">
                          {msg.content}
                        </div>
                        <span className="chat-bubble-msg-time">
                          {formatMsgTime(msg.created_at)}
                        </span>
                      </div>
                    );
                  })
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* 메시지 입력 */}
              <div className="chat-bubble-input-bar">
                <input
                  className="chat-bubble-input"
                  placeholder="메시지를 입력하세요..."
                  value={msgInput}
                  onChange={(e) => setMsgInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  disabled={!activeRoom}
                />
                <button
                  className="chat-bubble-send"
                  onClick={handleSend}
                  disabled={!msgInput.trim() || sending || !activeRoom}
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <line x1="22" y1="2" x2="11" y2="13" />
                    <polygon points="22 2 15 22 11 13 2 9 22 2" />
                  </svg>
                </button>
              </div>
            </>
          )}
        </div>
      )}

      {/* 플로팅 버튼 */}
      <button
        className="chat-bubble-btn"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="채팅"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
        </svg>
      </button>
    </div>
  );
}
