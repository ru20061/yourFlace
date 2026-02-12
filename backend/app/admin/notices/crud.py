from app.common.base_crud import BaseCRUD
from app.admin.notices.models import Notice
from app.admin.notices.schemas import NoticeCreate, NoticeUpdate

class CRUDNotice(BaseCRUD[Notice, NoticeCreate, NoticeUpdate]):
    pass

notice_crud = CRUDNotice(Notice)
