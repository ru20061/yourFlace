from app.common.base_crud import BaseCRUD
from app.like.fan_recommendations.models import FanRecommendation
from app.like.fan_recommendations.schemas import FanRecommendationCreate, FanRecommendationUpdate

class CRUDFanRecommendation(BaseCRUD[FanRecommendation, FanRecommendationCreate, FanRecommendationUpdate]):
    pass

fan_recommendation_crud = CRUDFanRecommendation(FanRecommendation)
