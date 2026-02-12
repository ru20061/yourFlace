from app.common.base_crud import BaseCRUD
from app.like.fan_likes.models import FanLike
from app.like.fan_likes.schemas import FanLikeCreate, FanLikeUpdate

class CRUDFanLike(BaseCRUD[FanLike, FanLikeCreate, FanLikeUpdate]):
    pass

fan_like_crud = CRUDFanLike(FanLike)
