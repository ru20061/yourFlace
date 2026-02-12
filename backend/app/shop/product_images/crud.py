from app.common.base_crud import BaseCRUD
from app.shop.product_images.models import ProductImage
from app.shop.product_images.schemas import ProductImageCreate, ProductImageUpdate

class CRUDProductImage(BaseCRUD[ProductImage, ProductImageCreate, ProductImageUpdate]):
    pass

product_image_crud = CRUDProductImage(ProductImage)
