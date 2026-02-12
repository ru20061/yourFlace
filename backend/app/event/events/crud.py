from app.common.base_crud import BaseCRUD
from app.event.events.models import Event
from app.event.events.schemas import EventCreate, EventUpdate

class CRUDEvent(BaseCRUD[Event, EventCreate, EventUpdate]):
    pass

event_crud = CRUDEvent(Event)
