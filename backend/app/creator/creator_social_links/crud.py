from app.common.base_crud import BaseCRUD
from app.creator.creator_social_links.models import CreatorSocialLink
from app.creator.creator_social_links.schemas import CreatorSocialLinkCreate, CreatorSocialLinkUpdate

class CRUDCreatorSocialLink(BaseCRUD[CreatorSocialLink, CreatorSocialLinkCreate, CreatorSocialLinkUpdate]):
    pass

creator_social_link_crud = CRUDCreatorSocialLink(CreatorSocialLink)
