from app.common.base_crud import BaseCRUD
from app.chat.chat_messages.models import ChatMessage
from app.chat.chat_messages.schemas import ChatMessageCreate, ChatMessageUpdate

class CRUDChatMessage(BaseCRUD[ChatMessage, ChatMessageCreate, ChatMessageUpdate]):
    pass

chat_message_crud = CRUDChatMessage(ChatMessage)
