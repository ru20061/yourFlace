from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.base_crud import BaseCRUD
from app.subscription.subscriptions.models import Subscription
from app.subscription.subscriptions.schemas import SubscriptionCreate, SubscriptionUpdate
from app.celeb.celebs.models import Celeb


class CRUDSubscription(BaseCRUD[Subscription, SubscriptionCreate, SubscriptionUpdate]):

    async def is_subscribed(self, db: AsyncSession, fan_id: int, celeb_id: int) -> bool:
        """
        팬이 특정 셀럽을 구독 중인지 확인.
        개인(individual) 셀럽의 경우 직접 구독이 없으면
        소속 그룹(parent_id) 구독 여부도 함께 확인.
        """
        today = date.today()

        # 직접 구독 확인
        result = await db.execute(
            select(Subscription).where(
                Subscription.fan_id == fan_id,
                Subscription.celeb_id == celeb_id,
                Subscription.status == "subscribed",
                (Subscription.end_date == None) | (Subscription.end_date >= today),
            )
        )
        if result.scalars().first():
            return True

        # 셀럽이 individual 멤버인 경우 그룹 구독 확인
        celeb_result = await db.execute(
            select(Celeb).where(Celeb.id == celeb_id)
        )
        celeb = celeb_result.scalars().first()

        if celeb and celeb.celeb_type == "individual" and celeb.parent_id:
            group_result = await db.execute(
                select(Subscription).where(
                    Subscription.fan_id == fan_id,
                    Subscription.celeb_id == celeb.parent_id,
                    Subscription.status == "subscribed",
                    (Subscription.end_date == None) | (Subscription.end_date >= today),
                )
            )
            if group_result.scalars().first():
                return True

        return False


subscription_crud = CRUDSubscription(Subscription)
