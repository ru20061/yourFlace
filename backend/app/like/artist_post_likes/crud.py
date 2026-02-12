from app.common.base_crud import BaseCRUD
from app.like.artist_post_likes.models import ArtistPostLike
from app.like.artist_post_likes.schemas import ArtistPostLikeCreate, ArtistPostLikeUpdate

class CRUDArtistPostLike(BaseCRUD[ArtistPostLike, ArtistPostLikeCreate, ArtistPostLikeUpdate]):
    pass

artist_post_like_crud = CRUDArtistPostLike(ArtistPostLike)
