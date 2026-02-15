from app.common.base_crud import BaseCRUD
from app.admin.magazines.models import Magazine
from app.admin.magazines.schemas import MagazineCreate, MagazineUpdate

class CRUDMagazine(BaseCRUD[Magazine, MagazineCreate, MagazineUpdate]):
    pass

magazine_crud = CRUDMagazine(Magazine)
