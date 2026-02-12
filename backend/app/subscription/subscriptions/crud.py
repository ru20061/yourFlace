from app.common.base_crud import BaseCRUD
from app.subscription.subscriptions.models import Subscription
from app.subscription.subscriptions.schemas import SubscriptionCreate, SubscriptionUpdate

class CRUDSubscription(BaseCRUD[Subscription, SubscriptionCreate, SubscriptionUpdate]):
    pass

subscription_crud = CRUDSubscription(Subscription)
