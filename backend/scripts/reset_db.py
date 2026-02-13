"""
DB 전체 삭제 후 모델 기반으로 재생성 + 시드 데이터 삽입
사용법 (프로젝트 루트에서): python -m backend.scripts.reset_db
"""
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.database import engine, Base
from scripts.seed import seed_data, reset_sequences

# 모든 모델 임포트 (Base.metadata에 등록)
from scripts.seed import (
    User, Profile, UserSetting, UserAddress, UserDevice, LoginLog,
    DeletedUser, GlobalBlacklist, SubscriptionBlacklist,
    Artist, ArtistCategory, ArtistCategoryMap, ArtistSocialLink, Manager,
    Subscription, SubscriptionPlan, SubscriptionCancellation,
    Post, PostImage, PostComment, PostStat,
    Image, ArtistImage, ArtistImageComment, ArtistImageStat,
    ArtistVideo, ArtistVideoComment, ArtistVideoStat,
    ChatRoom, ChatMessage, ChatImage, ChatVideo,
    ChatReadReceipt, ChatPin, ChatReport,
    CalendarSearch, SavedSearchFilter,
    Payment, PaymentMethod, PaymentRefund,
    Event, EventParticipant, EventAttendance,
    Product, ProductImage, Order, OrderItem,
    Notification, NotificationSetting, NotificationTemplate,
    ScheduledNotification, SystemLog,
    FanLike, FanRecommendation, ArtistPostLike, ArtistPostRecommendation,
    ArtistContentStat, ArtistChatStat, SubscriberContentStat, SubscriberChatStat,
    ModerationModel, ContentModeration,
    FAQ, Banner, SystemMessage, Notice, ErrorLog,
)


async def drop_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("[OK] 모든 테이블 삭제 완료")


async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    table_count = len(Base.metadata.tables)
    print(f"[OK] 테이블 {table_count}개 생성 완료")


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
    print("[1/4] 기존 테이블 전체 삭제...")
    await drop_all_tables()

    print("[2/4] 모델 기반 테이블 생성...")
    await create_all_tables()

    print("[3/4] 시드 데이터 삽입...")
    await seed_data()

    print("[4/4] 시퀀스 리셋...")
    await reset_sequences()

    print()
    print("=== 리셋 완료 ===")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
