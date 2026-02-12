from app.common.base_crud import BaseCRUD
from app.content.artist_videos.models import ArtistVideo
from app.content.artist_videos.schemas import ArtistVideoCreate, ArtistVideoUpdate

class CRUDArtistVideo(BaseCRUD[ArtistVideo, ArtistVideoCreate, ArtistVideoUpdate]):
    pass

artist_video_crud = CRUDArtistVideo(ArtistVideo)
