from app.common.base_crud import BaseCRUD
from app.stats.artist_content_stats.models import ArtistContentStat
from app.stats.artist_content_stats.schemas import ArtistContentStatCreate, ArtistContentStatUpdate

class CRUDArtistContentStat(BaseCRUD[ArtistContentStat, ArtistContentStatCreate, ArtistContentStatUpdate]):
    pass

artist_content_stat_crud = CRUDArtistContentStat(ArtistContentStat)
