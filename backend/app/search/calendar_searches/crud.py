from app.common.base_crud import BaseCRUD
from app.search.calendar_searches.models import CalendarSearch
from app.search.calendar_searches.schemas import CalendarSearchCreate, CalendarSearchUpdate

class CRUDCalendarSearch(BaseCRUD[CalendarSearch, CalendarSearchCreate, CalendarSearchUpdate]):
    pass

calendar_search_crud = CRUDCalendarSearch(CalendarSearch)
