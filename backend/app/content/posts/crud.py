from app.common.base_crud import BaseCRUD
from app.content.posts.models import Post
from app.content.posts.schemas import PostCreate, PostUpdate

class CRUDPost(BaseCRUD[Post, PostCreate, PostUpdate]):
    pass

post_crud = CRUDPost(Post)
