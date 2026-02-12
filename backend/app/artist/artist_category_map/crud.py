from app.common.base_crud import BaseCRUD
from app.artist.artist_category_map.models import ArtistCategoryMap
from app.artist.artist_category_map.schemas import ArtistCategoryMapCreate, ArtistCategoryMapUpdate

class CRUDArtistCategoryMap(BaseCRUD[ArtistCategoryMap, ArtistCategoryMapCreate, ArtistCategoryMapUpdate]):
    pass

artist_category_map_crud = CRUDArtistCategoryMap(ArtistCategoryMap)
