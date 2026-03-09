from app.common.base_crud import BaseCRUD
from app.content.creator_image_comments.models import CreatorImageComment
from app.content.creator_image_comments.schemas import CreatorImageCommentCreate, CreatorImageCommentUpdate

class CRUDCreatorImageComment(BaseCRUD[CreatorImageComment, CreatorImageCommentCreate, CreatorImageCommentUpdate]):
    pass

creator_image_comment_crud = CRUDCreatorImageComment(CreatorImageComment)
