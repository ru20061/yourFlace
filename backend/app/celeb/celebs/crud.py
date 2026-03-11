from app.common.base_crud import BaseCRUD
from app.celeb.celebs.models import Celeb
from app.celeb.celebs.schemas import CelebCreate, CelebUpdate

class CRUDCeleb(BaseCRUD[Celeb, CelebCreate, CelebUpdate]):
    pass

celeb_crud = CRUDCeleb(Celeb)
