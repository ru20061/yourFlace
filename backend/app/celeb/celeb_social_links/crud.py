from app.common.base_crud import BaseCRUD
from app.celeb.celeb_social_links.models import CelebSocialLink
from app.celeb.celeb_social_links.schemas import CelebSocialLinkCreate, CelebSocialLinkUpdate

class CRUDCelebSocialLink(BaseCRUD[CelebSocialLink, CelebSocialLinkCreate, CelebSocialLinkUpdate]):
    pass

celeb_social_link_crud = CRUDCelebSocialLink(CelebSocialLink)
