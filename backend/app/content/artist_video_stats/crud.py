from app.common.base_crud import BaseCRUD
from app.content.artist_video_stats.models import ArtistVideoStat
from app.content.artist_video_stats.schemas import ArtistVideoStatCreate, ArtistVideoStatUpdate

class CRUDArtistVideoStat(BaseCRUD[ArtistVideoStat, ArtistVideoStatCreate, ArtistVideoStatUpdate]):
    pass

artist_video_stat_crud = CRUDArtistVideoStat(ArtistVideoStat)
