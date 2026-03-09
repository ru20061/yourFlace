from app.common.base_crud import BaseCRUD
from app.content.creator_video_stats.models import CreatorVideoStat
from app.content.creator_video_stats.schemas import CreatorVideoStatCreate, CreatorVideoStatUpdate

class CRUDCreatorVideoStat(BaseCRUD[CreatorVideoStat, CreatorVideoStatCreate, CreatorVideoStatUpdate]):
    pass

creator_video_stat_crud = CRUDCreatorVideoStat(CreatorVideoStat)
