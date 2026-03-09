from app.common.base_crud import BaseCRUD
from app.creator.managers.models import Manager
from app.creator.managers.schemas import ManagerCreate, ManagerUpdate

class CRUDManager(BaseCRUD[Manager, ManagerCreate, ManagerUpdate]):
    pass

manager_crud = CRUDManager(Manager)
