"""
DB 전체 삭제 후 모델 기반으로 재생성 + 시드 데이터 삽입
사용법 (프로젝트 루트에서): python -m backend.scripts.reset_db
"""
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text
from app.database import engine, Base
from scripts.seed import seed_data, reset_sequences

# 모든 모델 임포트 (Base.metadata에 등록)
from app.auth.users.models import User
from app.auth.profile.models import Profile
from app.auth.user_settings.models import UserSetting
from app.auth.user_addresses.models import UserAddress
from app.auth.user_devices.models import UserDevice
from app.auth.login_logs.models import LoginLog
from app.auth.deleted_users.models import DeletedUser
from app.auth.global_blacklist.models import GlobalBlacklist
from app.auth.subscription_blacklist.models import SubscriptionBlacklist

from app.artist.artists.models import Artist
from app.artist.artist_categories.models import ArtistCategory
from app.artist.artist_category_map.models import ArtistCategoryMap
from app.artist.artist_social_links.models import ArtistSocialLink
from app.artist.managers.models import Manager

from app.subscription.subscriptions.models import Subscription
from app.subscription.subscription_plans.models import SubscriptionPlan
from app.subscription.subscription_cancellations.models import SubscriptionCancellation

from app.content.posts.models import Post
from app.content.post_images.models import PostImage
from app.content.post_comments.models import PostComment
from app.content.post_stats.models import PostStat
from app.content.images.models import Image
from app.content.artist_images.models import ArtistImage
from app.content.artist_image_comments.models import ArtistImageComment
from app.content.artist_image_stats.models import ArtistImageStat
from app.content.artist_videos.models import ArtistVideo
from app.content.artist_video_comments.models import ArtistVideoComment
from app.content.artist_video_stats.models import ArtistVideoStat

from app.chat.chat_rooms.models import ChatRoom
from app.chat.chat_messages.models import ChatMessage
from app.chat.chat_images.models import ChatImage
from app.chat.chat_videos.models import ChatVideo
from app.chat.chat_read_receipts.models import ChatReadReceipt
from app.chat.chat_pins.models import ChatPin
from app.chat.chat_reports.models import ChatReport

from app.search.calendar_searches.models import CalendarSearch
from app.search.saved_search_filters.models import SavedSearchFilter

from app.payment.payments.models import Payment
from app.payment.payment_methods.models import PaymentMethod
from app.payment.payment_refunds.models import PaymentRefund

from app.event.events.models import Event
from app.event.event_participants.models import EventParticipant
from app.event.event_attendance.models import EventAttendance

from app.shop.products.models import Product
from app.shop.product_images.models import ProductImage
from app.shop.orders.models import Order
from app.shop.order_items.models import OrderItem

from app.notification.notifications.models import Notification
from app.notification.notification_settings.models import NotificationSetting
from app.notification.notification_templates.models import NotificationTemplate
from app.notification.scheduled_notifications.models import ScheduledNotification
from app.notification.system_logs.models import SystemLog

from app.like.fan_likes.models import FanLike
from app.like.fan_recommendations.models import FanRecommendation
from app.like.artist_post_likes.models import ArtistPostLike
from app.like.artist_post_recommendations.models import ArtistPostRecommendation

from app.stats.artist_content_stats.models import ArtistContentStat
from app.stats.artist_chat_stats.models import ArtistChatStat
from app.stats.subscriber_content_stats.models import SubscriberContentStat
from app.stats.subscriber_chat_stats.models import SubscriberChatStat

from app.moderation.moderation_models.models import ModerationModel
from app.moderation.content_moderation.models import ContentModeration

from app.admin.faq.models import FAQ
from app.admin.banners.models import Banner
from app.admin.system_messages.models import SystemMessage
from app.admin.notices.models import Notice
from app.admin.error_logs.models import ErrorLog
from app.admin.magazines.models import Magazine
from app.admin.magazine_images.models import MagazineImage


async def drop_all_tables():
    """public 스키마를 CASCADE로 완전 삭제 후 재생성 (FK 제약조건 문제 방지)"""
    async with engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA public CASCADE"))
        await conn.execute(text("CREATE SCHEMA public"))
        await conn.execute(text("GRANT ALL ON SCHEMA public TO public"))
    print("[OK] 모든 테이블 삭제 완료 (DROP SCHEMA CASCADE)")


async def create_all_tables():
    """Base.metadata 기반으로 테이블 + 컬럼 생성"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    table_count = len(Base.metadata.tables)
    total_columns = sum(len(table.columns) for table in Base.metadata.tables.values())
    print(f"[OK] 테이블 {table_count}개 / 컬럼 {total_columns}개 생성 완료")


async def verify_tables():
    """DB에서 실제 테이블·컬럼 수를 조회하여 검증"""
    async with engine.begin() as conn:
        result = await conn.execute(text("""
            SELECT table_name, COUNT(column_name) as col_count
            FROM information_schema.columns
            WHERE table_schema = 'public'
            GROUP BY table_name
            ORDER BY table_name
        """))
        rows = result.fetchall()

    if not rows:
        print("[WARNING] DB에 테이블이 없습니다!")
        return

    print(f"[검증] DB 테이블 {len(rows)}개 확인:")
    for table_name, col_count in rows:
        print(f"  - {table_name}: {col_count}개 컬럼")

    # 모델 정의와 DB 실제 컬럼 수 비교
    db_tables = {row[0]: row[1] for row in rows}
    mismatches = []
    for table in Base.metadata.tables.values():
        expected = len(table.columns)
        actual = db_tables.get(table.name, 0)
        if actual == 0:
            mismatches.append(f"  [MISSING] {table.name}: 테이블 없음")
        elif actual != expected:
            mismatches.append(f"  [MISMATCH] {table.name}: 모델 {expected}개 vs DB {actual}개")

    if mismatches:
        print()
        print("[WARNING] 불일치 항목:")
        for m in mismatches:
            print(m)
    else:
        print("[OK] 모든 테이블·컬럼 검증 통과")


async def main():
    print()
    print("=" * 50)
    print("  yourFlace DB 리셋")
    print("=" * 50)
    print()

    confirm = input("모든 테이블과 데이터가 삭제됩니다. 계속하시겠습니까? (yes/no): ")
    if confirm.strip().lower() != "yes":
        print("[취소] 작업을 취소했습니다.")
        return

    print()
    print("[1/5] 기존 테이블 전체 삭제...")
    await drop_all_tables()

    print("[2/5] 모델 기반 테이블·컬럼 생성...")
    await create_all_tables()

    print("[3/5] 테이블·컬럼 검증...")
    await verify_tables()

    print("[4/5] 시드 데이터 삽입...")
    await seed_data()

    print("[5/5] 시퀀스 리셋...")
    await reset_sequences()

    print()
    print("=== 리셋 완료 ===")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
