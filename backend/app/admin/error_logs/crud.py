from app.common.base_crud import BaseCRUD
from app.admin.error_logs.models import ErrorLog
from app.admin.error_logs.schemas import ErrorLogCreate, ErrorLogUpdate

class CRUDErrorLog(BaseCRUD[ErrorLog, ErrorLogCreate, ErrorLogUpdate]):
    pass

error_log_crud = CRUDErrorLog(ErrorLog)
