from app.common.base_crud import BaseCRUD
from app.content.creator_images.models import CreatorImage
from app.content.creator_images.schemas import CreatorImageCreate, CreatorImageUpdate

class CRUDCreatorImage(BaseCRUD[CreatorImage, CreatorImageCreate, CreatorImageUpdate]):
    pass

creator_image_crud = CRUDCreatorImage(CreatorImage)
