from app.common.base_crud import BaseCRUD
from app.stats.creator_content_stats.models import CreatorContentStat
from app.stats.creator_content_stats.schemas import CreatorContentStatCreate, CreatorContentStatUpdate

class CRUDCreatorContentStat(BaseCRUD[CreatorContentStat, CreatorContentStatCreate, CreatorContentStatUpdate]):
    pass

creator_content_stat_crud = CRUDCreatorContentStat(CreatorContentStat)
