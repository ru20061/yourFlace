from app.common.base_crud import BaseCRUD
from app.payment.payments.models import Payment
from app.payment.payments.schemas import PaymentCreate, PaymentUpdate

class CRUDPayment(BaseCRUD[Payment, PaymentCreate, PaymentUpdate]):
    pass

payment_crud = CRUDPayment(Payment)
