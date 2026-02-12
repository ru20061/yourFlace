from app.common.base_crud import BaseCRUD
from app.subscription.subscription_plans.models import SubscriptionPlan
from app.subscription.subscription_plans.schemas import SubscriptionPlanCreate, SubscriptionPlanUpdate

class CRUDSubscriptionPlan(BaseCRUD[SubscriptionPlan, SubscriptionPlanCreate, SubscriptionPlanUpdate]):
    pass

subscription_plan_crud = CRUDSubscriptionPlan(SubscriptionPlan)
