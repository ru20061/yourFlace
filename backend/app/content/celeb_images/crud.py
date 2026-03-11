from app.common.base_crud import BaseCRUD
from app.content.celeb_images.models import CelebImage
from app.content.celeb_images.schemas import CelebImageCreate, CelebImageUpdate

class CRUDCelebImage(BaseCRUD[CelebImage, CelebImageCreate, CelebImageUpdate]):
    pass

celeb_image_crud = CRUDCelebImage(CelebImage)
