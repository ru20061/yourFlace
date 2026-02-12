from app.common.base_crud import BaseCRUD
from app.artist.artist_categories.models import ArtistCategory
from app.artist.artist_categories.schemas import ArtistCategoryCreate, ArtistCategoryUpdate

class CRUDArtistCategory(BaseCRUD[ArtistCategory, ArtistCategoryCreate, ArtistCategoryUpdate]):
    pass

artist_category_crud = CRUDArtistCategory(ArtistCategory)
