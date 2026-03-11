from app.common.base_crud import BaseCRUD
from app.content.celeb_videos.models import CelebVideo
from app.content.celeb_videos.schemas import CelebVideoCreate, CelebVideoUpdate

class CRUDCelebVideo(BaseCRUD[CelebVideo, CelebVideoCreate, CelebVideoUpdate]):
    pass

celeb_video_crud = CRUDCelebVideo(CelebVideo)
