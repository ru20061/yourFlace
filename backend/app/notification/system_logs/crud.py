from app.common.base_crud import BaseCRUD
from app.notification.system_logs.models import SystemLog
from app.notification.system_logs.schemas import SystemLogCreate, SystemLogUpdate

class CRUDSystemLog(BaseCRUD[SystemLog, SystemLogCreate, SystemLogUpdate]):
    pass

system_log_crud = CRUDSystemLog(SystemLog)
