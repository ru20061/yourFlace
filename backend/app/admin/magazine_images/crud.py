from app.common.base_crud import BaseCRUD
from app.admin.magazine_images.models import MagazineImage
from app.admin.magazine_images.schemas import MagazineImageCreate, MagazineImageUpdate

class CRUDMagazineImage(BaseCRUD[MagazineImage, MagazineImageCreate, MagazineImageUpdate]):
    pass

magazine_image_crud = CRUDMagazineImage(MagazineImage)
