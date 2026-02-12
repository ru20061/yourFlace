from app.common.base_crud import BaseCRUD
from app.content.images.models import Image
from app.content.images.schemas import ImageCreate, ImageUpdate

class CRUDImage(BaseCRUD[Image, ImageCreate, ImageUpdate]):
    pass

image_crud = CRUDImage(Image)
