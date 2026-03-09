from app.common.base_crud import BaseCRUD
from app.creator.creator_category_map.models import CreatorCategoryMap
from app.creator.creator_category_map.schemas import CreatorCategoryMapCreate, CreatorCategoryMapUpdate

class CRUDCreatorCategoryMap(BaseCRUD[CreatorCategoryMap, CreatorCategoryMapCreate, CreatorCategoryMapUpdate]):
    pass

creator_category_map_crud = CRUDCreatorCategoryMap(CreatorCategoryMap)
