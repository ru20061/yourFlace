from app.common.base_crud import BaseCRUD
from app.content.celeb_image_stats.models import CelebImageStat
from app.content.celeb_image_stats.schemas import CelebImageStatCreate, CelebImageStatUpdate

class CRUDCelebImageStat(BaseCRUD[CelebImageStat, CelebImageStatCreate, CelebImageStatUpdate]):
    pass

celeb_image_stat_crud = CRUDCelebImageStat(CelebImageStat)
