from app.common.base_crud import BaseCRUD
from app.shop.order_items.models import OrderItem
from app.shop.order_items.schemas import OrderItemCreate, OrderItemUpdate

class CRUDOrderItem(BaseCRUD[OrderItem, OrderItemCreate, OrderItemUpdate]):
    pass

order_item_crud = CRUDOrderItem(OrderItem)
