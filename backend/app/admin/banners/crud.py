from app.common.base_crud import BaseCRUD
from app.admin.banners.models import Banner
from app.admin.banners.schemas import BannerCreate, BannerUpdate

class CRUDBanner(BaseCRUD[Banner, BannerCreate, BannerUpdate]):
    pass

banner_crud = CRUDBanner(Banner)
