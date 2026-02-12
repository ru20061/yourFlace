from app.common.base_crud import BaseCRUD
from app.stats.subscriber_content_stats.models import SubscriberContentStat
from app.stats.subscriber_content_stats.schemas import SubscriberContentStatCreate, SubscriberContentStatUpdate

class CRUDSubscriberContentStat(BaseCRUD[SubscriberContentStat, SubscriberContentStatCreate, SubscriberContentStatUpdate]):
    pass

subscriber_content_stat_crud = CRUDSubscriberContentStat(SubscriberContentStat)
