from app.common.base_crud import BaseCRUD
from app.artist.managers.models import Manager
from app.artist.managers.schemas import ManagerCreate, ManagerUpdate

class CRUDManager(BaseCRUD[Manager, ManagerCreate, ManagerUpdate]):
    pass

manager_crud = CRUDManager(Manager)
