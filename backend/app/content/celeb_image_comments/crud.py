from app.common.base_crud import BaseCRUD
from app.content.celeb_image_comments.models import CelebImageComment
from app.content.celeb_image_comments.schemas import CelebImageCommentCreate, CelebImageCommentUpdate

class CRUDCelebImageComment(BaseCRUD[CelebImageComment, CelebImageCommentCreate, CelebImageCommentUpdate]):
    pass

celeb_image_comment_crud = CRUDCelebImageComment(CelebImageComment)
