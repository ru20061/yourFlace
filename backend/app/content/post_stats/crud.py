from app.common.base_crud import BaseCRUD
from app.content.post_stats.models import PostStat
from app.content.post_stats.schemas import PostStatCreate, PostStatUpdate

class CRUDPostStat(BaseCRUD[PostStat, PostStatCreate, PostStatUpdate]):
    pass

post_stat_crud = CRUDPostStat(PostStat)
