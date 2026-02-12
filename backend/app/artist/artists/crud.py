from app.common.base_crud import BaseCRUD
from app.artist.artists.models import Artist
from app.artist.artists.schemas import ArtistCreate, ArtistUpdate

class CRUDArtist(BaseCRUD[Artist, ArtistCreate, ArtistUpdate]):
    pass

artist_crud = CRUDArtist(Artist)
