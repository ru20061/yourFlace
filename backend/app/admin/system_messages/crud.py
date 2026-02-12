from app.common.base_crud import BaseCRUD
from app.admin.system_messages.models import SystemMessage
from app.admin.system_messages.schemas import SystemMessageCreate, SystemMessageUpdate

class CRUDSystemMessage(BaseCRUD[SystemMessage, SystemMessageCreate, SystemMessageUpdate]):
    pass

system_message_crud = CRUDSystemMessage(SystemMessage)
