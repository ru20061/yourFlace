from app.common.base_crud import BaseCRUD
from app.chat.chat_pins.models import ChatPin
from app.chat.chat_pins.schemas import ChatPinCreate, ChatPinUpdate

class CRUDChatPin(BaseCRUD[ChatPin, ChatPinCreate, ChatPinUpdate]):
    pass

chat_pin_crud = CRUDChatPin(ChatPin)
