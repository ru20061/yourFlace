from app.common.base_crud import BaseCRUD
from app.celeb.celeb_categories.models import CelebCategory
from app.celeb.celeb_categories.schemas import CelebCategoryCreate, CelebCategoryUpdate

class CRUDCelebCategory(BaseCRUD[CelebCategory, CelebCategoryCreate, CelebCategoryUpdate]):
    pass

celeb_category_crud = CRUDCelebCategory(CelebCategory)
