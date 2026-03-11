from app.common.base_crud import BaseCRUD
from app.stats.celeb_content_stats.models import CelebContentStat
from app.stats.celeb_content_stats.schemas import CelebContentStatCreate, CelebContentStatUpdate

class CRUDCelebContentStat(BaseCRUD[CelebContentStat, CelebContentStatCreate, CelebContentStatUpdate]):
    pass

celeb_content_stat_crud = CRUDCelebContentStat(CelebContentStat)
