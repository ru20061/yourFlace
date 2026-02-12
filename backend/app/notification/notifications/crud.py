from app.common.base_crud import BaseCRUD
from app.notification.notifications.models import Notification
from app.notification.notifications.schemas import NotificationCreate, NotificationUpdate

class CRUDNotification(BaseCRUD[Notification, NotificationCreate, NotificationUpdate]):
    pass

notification_crud = CRUDNotification(Notification)
