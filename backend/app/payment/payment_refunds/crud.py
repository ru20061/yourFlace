from app.common.base_crud import BaseCRUD
from app.payment.payment_refunds.models import PaymentRefund
from app.payment.payment_refunds.schemas import PaymentRefundCreate, PaymentRefundUpdate

class CRUDPaymentRefund(BaseCRUD[PaymentRefund, PaymentRefundCreate, PaymentRefundUpdate]):
    pass

payment_refund_crud = CRUDPaymentRefund(PaymentRefund)
