from app.common.base_crud import BaseCRUD
from app.creator.creators.models import Creator
from app.creator.creators.schemas import CreatorCreate, CreatorUpdate

class CRUDCreator(BaseCRUD[Creator, CreatorCreate, CreatorUpdate]):
    pass

creator_crud = CRUDCreator(Creator)
