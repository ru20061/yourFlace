from app.common.base_crud import BaseCRUD
from app.event.event_attendance.models import EventAttendance
from app.event.event_attendance.schemas import EventAttendanceCreate, EventAttendanceUpdate

class CRUDEventAttendance(BaseCRUD[EventAttendance, EventAttendanceCreate, EventAttendanceUpdate]):
    pass

event_attendance_crud = CRUDEventAttendance(EventAttendance)
