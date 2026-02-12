from app.common.base_crud import BaseCRUD
from app.auth.login_logs.models import LoginLog
from app.auth.login_logs.schemas import LoginLogCreate, LoginLogUpdate

class CRUDLoginLog(BaseCRUD[LoginLog, LoginLogCreate, LoginLogUpdate]):
    pass

login_log_crud = CRUDLoginLog(LoginLog)
