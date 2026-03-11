from app.common.base_crud import BaseCRUD
from app.like.celeb_post_likes.models import CelebPostLike
from app.like.celeb_post_likes.schemas import CelebPostLikeCreate, CelebPostLikeUpdate

class CRUDCelebPostLike(BaseCRUD[CelebPostLike, CelebPostLikeCreate, CelebPostLikeUpdate]):
    pass

celeb_post_like_crud = CRUDCelebPostLike(CelebPostLike)
