from app.common.base_crud import BaseCRUD
from app.celeb.celeb_category_map.models import CelebCategoryMap
from app.celeb.celeb_category_map.schemas import CelebCategoryMapCreate, CelebCategoryMapUpdate

class CRUDCelebCategoryMap(BaseCRUD[CelebCategoryMap, CelebCategoryMapCreate, CelebCategoryMapUpdate]):
    pass

celeb_category_map_crud = CRUDCelebCategoryMap(CelebCategoryMap)
