from app.common.base_crud import BaseCRUD
from app.content.artist_image_stats.models import ArtistImageStat
from app.content.artist_image_stats.schemas import ArtistImageStatCreate, ArtistImageStatUpdate

class CRUDArtistImageStat(BaseCRUD[ArtistImageStat, ArtistImageStatCreate, ArtistImageStatUpdate]):
    pass

artist_image_stat_crud = CRUDArtistImageStat(ArtistImageStat)
