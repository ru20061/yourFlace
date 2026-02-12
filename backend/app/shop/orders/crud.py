from app.common.base_crud import BaseCRUD
from app.shop.orders.models import Order
from app.shop.orders.schemas import OrderCreate, OrderUpdate

class CRUDOrder(BaseCRUD[Order, OrderCreate, OrderUpdate]):
    pass

order_crud = CRUDOrder(Order)
