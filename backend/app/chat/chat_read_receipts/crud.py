from app.common.base_crud import BaseCRUD
from app.chat.chat_read_receipts.models import ChatReadReceipt
from app.chat.chat_read_receipts.schemas import ChatReadReceiptCreate, ChatReadReceiptUpdate

class CRUDChatReadReceipt(BaseCRUD[ChatReadReceipt, ChatReadReceiptCreate, ChatReadReceiptUpdate]):
    pass

chat_read_receipt_crud = CRUDChatReadReceipt(ChatReadReceipt)
