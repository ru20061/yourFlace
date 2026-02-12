from app.common.base_crud import BaseCRUD
from app.shop.products.models import Product
from app.shop.products.schemas import ProductCreate, ProductUpdate

class CRUDProduct(BaseCRUD[Product, ProductCreate, ProductUpdate]):
    pass

product_crud = CRUDProduct(Product)
