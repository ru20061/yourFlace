from app.common.base_crud import BaseCRUD
from app.stats.subscriber_chat_stats.models import SubscriberChatStat
from app.stats.subscriber_chat_stats.schemas import SubscriberChatStatCreate, SubscriberChatStatUpdate

class CRUDSubscriberChatStat(BaseCRUD[SubscriberChatStat, SubscriberChatStatCreate, SubscriberChatStatUpdate]):
    pass

subscriber_chat_stat_crud = CRUDSubscriberChatStat(SubscriberChatStat)
