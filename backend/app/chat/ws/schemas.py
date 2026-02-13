from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


# --- 클라이언트 → 서버 (수신) ---

class WSChatSend(BaseModel):
    """채팅 메시지 전송"""
    type: Literal["chat.send"]
    content: str
    message_type: Literal["text", "image", "video", "file"] = "text"


class WSTyping(BaseModel):
    """타이핑 표시"""
    type: Literal["typing.start", "typing.stop"]


class WSReadReceipt(BaseModel):
    """메시지 읽음 처리"""
    type: Literal["read"]
    message_id: int


# --- 서버 → 클라이언트 (발신) ---

class WSChatMessage(BaseModel):
    """채팅 메시지 브로드캐스트"""
    type: Literal["chat.message"] = "chat.message"
    id: int
    chat_room_id: int
    sender_id: int
    sender_type: str
    content: Optional[str] = None
    message_type: str = "text"
    created_at: str


class WSTypingBroadcast(BaseModel):
    """타이핑 상태 브로드캐스트"""
    type: Literal["typing.start", "typing.stop"]
    user_id: int


class WSReadReceiptBroadcast(BaseModel):
    """읽음 표시 브로드캐스트"""
    type: Literal["read"] = "read"
    message_id: int
    user_id: int
    read_at: str


class WSPresence(BaseModel):
    """온라인/오프라인 상태"""
    type: Literal["presence"] = "presence"
    user_id: int
    status: Literal["online", "offline"]
    online_users: Optional[list[int]] = None


class WSError(BaseModel):
    """에러 메시지"""
    type: Literal["error"] = "error"
    message: str
