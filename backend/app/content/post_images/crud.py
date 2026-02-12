from app.common.base_crud import BaseCRUD
from app.content.post_images.models import PostImage
from app.content.post_images.schemas import PostImageCreate, PostImageUpdate

class CRUDPostImage(BaseCRUD[PostImage, PostImageCreate, PostImageUpdate]):
    pass

post_image_crud = CRUDPostImage(PostImage)
