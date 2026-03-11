from app.common.base_crud import BaseCRUD
from app.content.celeb_video_stats.models import CelebVideoStat
from app.content.celeb_video_stats.schemas import CelebVideoStatCreate, CelebVideoStatUpdate

class CRUDCelebVideoStat(BaseCRUD[CelebVideoStat, CelebVideoStatCreate, CelebVideoStatUpdate]):
    pass

celeb_video_stat_crud = CRUDCelebVideoStat(CelebVideoStat)
