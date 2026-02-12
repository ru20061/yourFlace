from app.common.base_crud import BaseCRUD
from app.chat.chat_videos.models import ChatVideo
from app.chat.chat_videos.schemas import ChatVideoCreate, ChatVideoUpdate

class CRUDChatVideo(BaseCRUD[ChatVideo, ChatVideoCreate, ChatVideoUpdate]):
    pass

chat_video_crud = CRUDChatVideo(ChatVideo)
