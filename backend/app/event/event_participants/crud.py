from app.common.base_crud import BaseCRUD
from app.event.event_participants.models import EventParticipant
from app.event.event_participants.schemas import EventParticipantCreate, EventParticipantUpdate

class CRUDEventParticipant(BaseCRUD[EventParticipant, EventParticipantCreate, EventParticipantUpdate]):
    pass

event_participant_crud = CRUDEventParticipant(EventParticipant)
