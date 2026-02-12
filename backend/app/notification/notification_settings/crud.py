from app.common.base_crud import BaseCRUD
from app.notification.notification_settings.models import NotificationSetting
from app.notification.notification_settings.schemas import NotificationSettingCreate, NotificationSettingUpdate

class CRUDNotificationSetting(BaseCRUD[NotificationSetting, NotificationSettingCreate, NotificationSettingUpdate]):
    pass

notification_setting_crud = CRUDNotificationSetting(NotificationSetting)
