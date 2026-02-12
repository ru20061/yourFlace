from app.common.base_crud import BaseCRUD
from app.auth.global_blacklist.models import GlobalBlacklist
from app.auth.global_blacklist.schemas import GlobalBlacklistCreate, GlobalBlacklistUpdate

class CRUDGlobalBlacklist(BaseCRUD[GlobalBlacklist, GlobalBlacklistCreate, GlobalBlacklistUpdate]):
    pass

global_blacklist_crud = CRUDGlobalBlacklist(GlobalBlacklist)
