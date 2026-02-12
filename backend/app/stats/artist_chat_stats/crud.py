from app.common.base_crud import BaseCRUD
from app.stats.artist_chat_stats.models import ArtistChatStat
from app.stats.artist_chat_stats.schemas import ArtistChatStatCreate, ArtistChatStatUpdate

class CRUDArtistChatStat(BaseCRUD[ArtistChatStat, ArtistChatStatCreate, ArtistChatStatUpdate]):
    pass

artist_chat_stat_crud = CRUDArtistChatStat(ArtistChatStat)
