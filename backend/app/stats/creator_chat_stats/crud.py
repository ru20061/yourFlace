from app.common.base_crud import BaseCRUD
from app.stats.creator_chat_stats.models import CreatorChatStat
from app.stats.creator_chat_stats.schemas import CreatorChatStatCreate, CreatorChatStatUpdate

class CRUDCreatorChatStat(BaseCRUD[CreatorChatStat, CreatorChatStatCreate, CreatorChatStatUpdate]):
    pass

creator_chat_stat_crud = CRUDCreatorChatStat(CreatorChatStat)
