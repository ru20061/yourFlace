from app.common.base_crud import BaseCRUD
from app.chat.chat_rooms.models import ChatRoom
from app.chat.chat_rooms.schemas import ChatRoomCreate, ChatRoomUpdate

class CRUDChatRoom(BaseCRUD[ChatRoom, ChatRoomCreate, ChatRoomUpdate]):
    pass

chat_room_crud = CRUDChatRoom(ChatRoom)
