from app.common.base_crud import BaseCRUD
from app.chat.chat_reports.models import ChatReport
from app.chat.chat_reports.schemas import ChatReportCreate, ChatReportUpdate

class CRUDChatReport(BaseCRUD[ChatReport, ChatReportCreate, ChatReportUpdate]):
    pass

chat_report_crud = CRUDChatReport(ChatReport)
