from app.common.base_crud import BaseCRUD
from app.payment.payment_methods.models import PaymentMethod
from app.payment.payment_methods.schemas import PaymentMethodCreate, PaymentMethodUpdate

class CRUDPaymentMethod(BaseCRUD[PaymentMethod, PaymentMethodCreate, PaymentMethodUpdate]):
    pass

payment_method_crud = CRUDPaymentMethod(PaymentMethod)
