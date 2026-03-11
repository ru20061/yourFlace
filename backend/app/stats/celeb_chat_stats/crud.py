from app.common.base_crud import BaseCRUD
from app.stats.celeb_chat_stats.models import CelebChatStat
from app.stats.celeb_chat_stats.schemas import CelebChatStatCreate, CelebChatStatUpdate

class CRUDCelebChatStat(BaseCRUD[CelebChatStat, CelebChatStatCreate, CelebChatStatUpdate]):
    pass

celeb_chat_stat_crud = CRUDCelebChatStat(CelebChatStat)
