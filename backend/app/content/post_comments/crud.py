from app.common.base_crud import BaseCRUD
from app.content.post_comments.models import PostComment
from app.content.post_comments.schemas import PostCommentCreate, PostCommentUpdate

class CRUDPostComment(BaseCRUD[PostComment, PostCommentCreate, PostCommentUpdate]):
    pass

post_comment_crud = CRUDPostComment(PostComment)
