from app.common.base_crud import BaseCRUD
from app.artist.artist_social_links.models import ArtistSocialLink
from app.artist.artist_social_links.schemas import ArtistSocialLinkCreate, ArtistSocialLinkUpdate

class CRUDArtistSocialLink(BaseCRUD[ArtistSocialLink, ArtistSocialLinkCreate, ArtistSocialLinkUpdate]):
    pass

artist_social_link_crud = CRUDArtistSocialLink(ArtistSocialLink)
