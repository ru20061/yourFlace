from app.common.base_crud import BaseCRUD
from app.content.creator_video_comments.models import CreatorVideoComment
from app.content.creator_video_comments.schemas import CreatorVideoCommentCreate, CreatorVideoCommentUpdate

class CRUDCreatorVideoComment(BaseCRUD[CreatorVideoComment, CreatorVideoCommentCreate, CreatorVideoCommentUpdate]):
    pass

creator_video_comment_crud = CRUDCreatorVideoComment(CreatorVideoComment)
