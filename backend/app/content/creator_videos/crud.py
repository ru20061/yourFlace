from app.common.base_crud import BaseCRUD
from app.content.creator_videos.models import CreatorVideo
from app.content.creator_videos.schemas import CreatorVideoCreate, CreatorVideoUpdate

class CRUDCreatorVideo(BaseCRUD[CreatorVideo, CreatorVideoCreate, CreatorVideoUpdate]):
    pass

creator_video_crud = CRUDCreatorVideo(CreatorVideo)
