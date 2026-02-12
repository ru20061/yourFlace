from app.common.base_crud import BaseCRUD
from app.notification.scheduled_notifications.models import ScheduledNotification
from app.notification.scheduled_notifications.schemas import ScheduledNotificationCreate, ScheduledNotificationUpdate

class CRUDScheduledNotification(BaseCRUD[ScheduledNotification, ScheduledNotificationCreate, ScheduledNotificationUpdate]):
    pass

scheduled_notification_crud = CRUDScheduledNotification(ScheduledNotification)
