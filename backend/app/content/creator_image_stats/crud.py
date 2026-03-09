from app.common.base_crud import BaseCRUD
from app.content.creator_image_stats.models import CreatorImageStat
from app.content.creator_image_stats.schemas import CreatorImageStatCreate, CreatorImageStatUpdate

class CRUDCreatorImageStat(BaseCRUD[CreatorImageStat, CreatorImageStatCreate, CreatorImageStatUpdate]):
    pass

creator_image_stat_crud = CRUDCreatorImageStat(CreatorImageStat)
