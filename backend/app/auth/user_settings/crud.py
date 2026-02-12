from app.common.base_crud import BaseCRUD
from app.auth.user_settings.models import UserSetting
from app.auth.user_settings.schemas import UserSettingCreate, UserSettingUpdate

class CRUDUserSetting(BaseCRUD[UserSetting, UserSettingCreate, UserSettingUpdate]):
    pass

user_setting_crud = CRUDUserSetting(UserSetting)
