from app.common.base_crud import BaseCRUD
from app.auth.subscription_blacklist.models import SubscriptionBlacklist
from app.auth.subscription_blacklist.schemas import SubscriptionBlacklistCreate, SubscriptionBlacklistUpdate

class CRUDSubscriptionBlacklist(BaseCRUD[SubscriptionBlacklist, SubscriptionBlacklistCreate, SubscriptionBlacklistUpdate]):
    pass

subscription_blacklist_crud = CRUDSubscriptionBlacklist(SubscriptionBlacklist)
