from app.common.base_crud import BaseCRUD
from app.auth.deleted_users.models import DeletedUser
from app.auth.deleted_users.schemas import DeletedUserCreate, DeletedUserUpdate

class CRUDDeletedUser(BaseCRUD[DeletedUser, DeletedUserCreate, DeletedUserUpdate]):
    pass

deleted_user_crud = CRUDDeletedUser(DeletedUser)
