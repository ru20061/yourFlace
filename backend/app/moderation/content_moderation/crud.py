from app.common.base_crud import BaseCRUD
from app.moderation.content_moderation.models import ContentModeration
from app.moderation.content_moderation.schemas import ContentModerationCreate, ContentModerationUpdate

class CRUDContentModeration(BaseCRUD[ContentModeration, ContentModerationCreate, ContentModerationUpdate]):
    pass

content_moderation_crud = CRUDContentModeration(ContentModeration)
