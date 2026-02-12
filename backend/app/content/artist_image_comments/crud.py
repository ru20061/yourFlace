from app.common.base_crud import BaseCRUD
from app.content.artist_image_comments.models import ArtistImageComment
from app.content.artist_image_comments.schemas import ArtistImageCommentCreate, ArtistImageCommentUpdate

class CRUDArtistImageComment(BaseCRUD[ArtistImageComment, ArtistImageCommentCreate, ArtistImageCommentUpdate]):
    pass

artist_image_comment_crud = CRUDArtistImageComment(ArtistImageComment)
