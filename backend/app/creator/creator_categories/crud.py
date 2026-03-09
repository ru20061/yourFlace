from app.common.base_crud import BaseCRUD
from app.creator.creator_categories.models import CreatorCategory
from app.creator.creator_categories.schemas import CreatorCategoryCreate, CreatorCategoryUpdate

class CRUDCreatorCategory(BaseCRUD[CreatorCategory, CreatorCategoryCreate, CreatorCategoryUpdate]):
    pass

creator_category_crud = CRUDCreatorCategory(CreatorCategory)
