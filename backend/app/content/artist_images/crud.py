from app.common.base_crud import BaseCRUD
from app.content.artist_images.models import ArtistImage
from app.content.artist_images.schemas import ArtistImageCreate, ArtistImageUpdate

class CRUDArtistImage(BaseCRUD[ArtistImage, ArtistImageCreate, ArtistImageUpdate]):
    pass

artist_image_crud = CRUDArtistImage(ArtistImage)
