from app.common.base_crud import BaseCRUD
from app.auth.users.models import User
from app.auth.users.schemas import UserCreate, UserUpdate

class CRUDUser(BaseCRUD[User, UserCreate, UserUpdate]):
    pass

user_crud = CRUDUser(User)
