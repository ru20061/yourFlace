from app.common.base_crud import BaseCRUD
from app.auth.profile.models import Profile
from app.auth.profile.schemas import ProfileCreate, ProfileUpdate

class CRUDProfile(BaseCRUD[Profile, ProfileCreate, ProfileUpdate]):
    pass

profile_crud = CRUDProfile(Profile)
