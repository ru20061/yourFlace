from app.common.base_crud import BaseCRUD
from app.chat.chat_images.models import ChatImage
from app.chat.chat_images.schemas import ChatImageCreate, ChatImageUpdate

class CRUDChatImage(BaseCRUD[ChatImage, ChatImageCreate, ChatImageUpdate]):
    pass

chat_image_crud = CRUDChatImage(ChatImage)
