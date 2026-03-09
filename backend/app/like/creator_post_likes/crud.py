from app.common.base_crud import BaseCRUD
from app.like.creator_post_likes.models import CreatorPostLike
from app.like.creator_post_likes.schemas import CreatorPostLikeCreate, CreatorPostLikeUpdate

class CRUDCreatorPostLike(BaseCRUD[CreatorPostLike, CreatorPostLikeCreate, CreatorPostLikeUpdate]):
    pass

creator_post_like_crud = CRUDCreatorPostLike(CreatorPostLike)
