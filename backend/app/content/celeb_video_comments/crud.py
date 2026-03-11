from app.common.base_crud import BaseCRUD
from app.content.celeb_video_comments.models import CelebVideoComment
from app.content.celeb_video_comments.schemas import CelebVideoCommentCreate, CelebVideoCommentUpdate

class CRUDCelebVideoComment(BaseCRUD[CelebVideoComment, CelebVideoCommentCreate, CelebVideoCommentUpdate]):
    pass

celeb_video_comment_crud = CRUDCelebVideoComment(CelebVideoComment)
