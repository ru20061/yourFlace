from app.common.base_crud import BaseCRUD
from app.notification.notification_templates.models import NotificationTemplate
from app.notification.notification_templates.schemas import NotificationTemplateCreate, NotificationTemplateUpdate

class CRUDNotificationTemplate(BaseCRUD[NotificationTemplate, NotificationTemplateCreate, NotificationTemplateUpdate]):
    pass

notification_template_crud = CRUDNotificationTemplate(NotificationTemplate)
