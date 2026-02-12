from app.common.base_crud import BaseCRUD
from app.moderation.moderation_models.models import ModerationModel
from app.moderation.moderation_models.schemas import ModerationModelCreate, ModerationModelUpdate

class CRUDModerationModel(BaseCRUD[ModerationModel, ModerationModelCreate, ModerationModelUpdate]):
    pass

moderation_model_crud = CRUDModerationModel(ModerationModel)
