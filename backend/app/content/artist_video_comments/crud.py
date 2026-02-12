from app.common.base_crud import BaseCRUD
from app.content.artist_video_comments.models import ArtistVideoComment
from app.content.artist_video_comments.schemas import ArtistVideoCommentCreate, ArtistVideoCommentUpdate

class CRUDArtistVideoComment(BaseCRUD[ArtistVideoComment, ArtistVideoCommentCreate, ArtistVideoCommentUpdate]):
    pass

artist_video_comment_crud = CRUDArtistVideoComment(ArtistVideoComment)
