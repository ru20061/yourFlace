"""
DB 테이블 생성 + 시드 데이터 삽입 스크립트
사용법 (프로젝트 루트에서):
  python -m backend.scripts.seed          # 테이블 생성 + 시드 데이터 삽입
  python -m backend.scripts.seed --reset  # 테이블 전체 리셋 후 삽입
"""
import sys
import asyncio
from pathlib import Path
from datetime import date, datetime, timedelta
from decimal import Decimal

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text
from app.database import engine, Base, AsyncSessionLocal
from app.core.security import get_password_hash
from app.core.slug import generate_slug

# ── 모든 모델 임포트 ──
# Auth
from app.auth.users.models import User
from app.auth.profile.models import Profile
from app.auth.user_settings.models import UserSetting
from app.auth.user_addresses.models import UserAddress
from app.auth.user_devices.models import UserDevice
from app.auth.login_logs.models import LoginLog
from app.auth.deleted_users.models import DeletedUser
from app.auth.global_blacklist.models import GlobalBlacklist
from app.auth.subscription_blacklist.models import SubscriptionBlacklist

# Celeb
from app.celeb.celebs.models import Celeb
from app.celeb.celeb_categories.models import CelebCategory
from app.celeb.celeb_category_map.models import CelebCategoryMap
from app.celeb.celeb_social_links.models import CelebSocialLink
from app.celeb.managers.models import Manager

# Subscription
from app.subscription.subscriptions.models import Subscription
from app.subscription.subscription_plans.models import SubscriptionPlan
from app.subscription.subscription_cancellations.models import SubscriptionCancellation

# Content
from app.content.posts.models import Post
from app.content.post_images.models import PostImage
from app.content.post_comments.models import PostComment
from app.content.post_stats.models import PostStat
from app.content.images.models import Image
from app.content.celeb_images.models import CelebImage
from app.content.celeb_image_comments.models import CelebImageComment
from app.content.celeb_image_stats.models import CelebImageStat
from app.content.celeb_videos.models import CelebVideo
from app.content.celeb_video_comments.models import CelebVideoComment
from app.content.celeb_video_stats.models import CelebVideoStat

# Search
from app.search.calendar_searches.models import CalendarSearch
from app.search.saved_search_filters.models import SavedSearchFilter

# Chat
from app.chat.chat_rooms.models import ChatRoom
from app.chat.chat_messages.models import ChatMessage
from app.chat.chat_images.models import ChatImage
from app.chat.chat_videos.models import ChatVideo
from app.chat.chat_read_receipts.models import ChatReadReceipt
from app.chat.chat_pins.models import ChatPin
from app.chat.chat_reports.models import ChatReport

# Payment
from app.payment.payments.models import Payment
from app.payment.payment_methods.models import PaymentMethod
from app.payment.payment_refunds.models import PaymentRefund

# Event
from app.event.events.models import Event
from app.event.event_participants.models import EventParticipant
from app.event.event_attendance.models import EventAttendance

# Shop
from app.shop.products.models import Product
from app.shop.product_images.models import ProductImage
from app.shop.orders.models import Order
from app.shop.order_items.models import OrderItem

# Notification
from app.notification.notifications.models import Notification
from app.notification.notification_settings.models import NotificationSetting
from app.notification.notification_templates.models import NotificationTemplate
from app.notification.scheduled_notifications.models import ScheduledNotification
from app.notification.system_logs.models import SystemLog

# Like
from app.like.fan_likes.models import FanLike
from app.like.fan_recommendations.models import FanRecommendation
from app.like.celeb_post_likes.models import CelebPostLike
from app.like.celeb_post_recommendations.models import CelebPostRecommendation

# Stats
from app.stats.celeb_content_stats.models import CelebContentStat
from app.stats.celeb_chat_stats.models import CelebChatStat
from app.stats.subscriber_content_stats.models import SubscriberContentStat
from app.stats.subscriber_chat_stats.models import SubscriberChatStat

# Moderation
from app.moderation.moderation_models.models import ModerationModel
from app.moderation.content_moderation.models import ContentModeration

# Admin
from app.admin.faq.models import FAQ
from app.admin.banners.models import Banner
from app.admin.system_messages.models import SystemMessage
from app.admin.notices.models import Notice
from app.admin.error_logs.models import ErrorLog
from app.admin.magazines.models import Magazine
from app.admin.magazine_images.models import MagazineImage


# ============================================================
#  시드 데이터 삽입
# ============================================================

async def seed_data():
    """모든 테이블에 테스트 데이터 삽입 (fan@test.com / test1234 로 전 기능 확인 가능)"""
    async with AsyncSessionLocal() as db:
        # 이미 데이터가 있으면 스킵
        result = await db.execute(text("SELECT COUNT(*) FROM users"))
        if result.scalar() > 0:
            print("[SKIP] 이미 데이터가 존재합니다. --reset 옵션을 사용하세요.")
            return

        now = datetime.utcnow()
        today = date.today()
        pw = get_password_hash("test1234")

        # ================================================================
        # 1. AUTH — users / profile / user_settings / user_addresses / user_devices / login_logs
        # ================================================================
        users = [
            User(id=1,  email="fan@test.com",        password_hash=pw, status="active"),
            User(id=2,  email="luna@artist.com",      password_hash=pw, status="active"),
            User(id=3,  email="haru@artist.com",      password_hash=pw, status="active"),
            User(id=4,  email="soyul@artist.com",     password_hash=pw, status="active"),
            User(id=5,  email="minseo@artist.com",    password_hash=pw, status="active"),
            User(id=6,  email="jay@artist.com",       password_hash=pw, status="active"),
            User(id=7,  email="yuri@artist.com",      password_hash=pw, status="active"),
            User(id=8,  email="admin@test.com",       password_hash=pw, status="active"),
            User(id=9,  email="guest@test.com",       password_hash=pw, status="active"),
            # 크리에이터 유형 확장
            User(id=10, email="jisoo@creator.com",    password_hash=pw, status="active"),
            User(id=11, email="minji@creator.com",    password_hash=pw, status="active"),
            User(id=12, email="seungwoo@creator.com", password_hash=pw, status="active"),
            User(id=13, email="nara@creator.com",     password_hash=pw, status="active"),
            User(id=14, email="hyeonseok@creator.com",password_hash=pw, status="active"),
            User(id=15, email="chaewon@creator.com",  password_hash=pw, status="active"),
        ]
        db.add_all(users)
        await db.flush()

        profiles = [
            Profile(id=1,  user_id=1,  nickname="테스트팬", full_name="김팬",   birth_date=date(2000, 5, 15), gender="male",   phone="010-1234-5678"),
            Profile(id=2,  user_id=2,  nickname="루나",     full_name="박루나"),
            Profile(id=3,  user_id=3,  nickname="하루",     full_name="이하루"),
            Profile(id=4,  user_id=4,  nickname="소율",     full_name="최소율"),
            Profile(id=5,  user_id=5,  nickname="민서",     full_name="정민서"),
            Profile(id=6,  user_id=6,  nickname="제이",     full_name="한제이"),
            Profile(id=7,  user_id=7,  nickname="유리",     full_name="송유리"),
            Profile(id=8,  user_id=8,  nickname="관리자",   full_name="운영자"),
            Profile(id=9,  user_id=9,  nickname="게스트",   full_name="이게스트", birth_date=date(1998, 3, 20), gender="female", phone="010-9876-5432"),
            Profile(id=10, user_id=10, nickname="지수",     full_name="김지수"),
            Profile(id=11, user_id=11, nickname="민지",     full_name="박민지"),
            Profile(id=12, user_id=12, nickname="승우",     full_name="이승우"),
            Profile(id=13, user_id=13, nickname="나라",     full_name="최나라"),
            Profile(id=14, user_id=14, nickname="현석",     full_name="정현석"),
            Profile(id=15, user_id=15, nickname="채원",     full_name="오채원"),
        ]
        db.add_all(profiles)
        await db.flush()

        user_settings = [
            UserSetting(id=i, user_id=i, language="ko", theme="light")
            for i in range(1, 16)
        ]
        db.add_all(user_settings)
        await db.flush()

        user_addresses = [
            UserAddress(id=1, user_id=1, address_name="집",   recipient_name="김팬", recipient_phone="010-1234-5678", postal_code="06134", base_address="서울 강남구 테헤란로 123", detail_address="101동 1001호", is_default=True),
            UserAddress(id=2, user_id=1, address_name="회사", recipient_name="김팬", recipient_phone="010-1234-5678", postal_code="04524", base_address="서울 중구 세종대로 110",   detail_address="5층",           is_default=False),
        ]
        db.add_all(user_addresses)
        await db.flush()

        user_devices = [
            UserDevice(id=1, user_id=1, device_type="ios",     device_token="test-ios-token-fan-001",    app_version="1.0.0", os_version="iOS 18.0", is_active=True),
            UserDevice(id=2, user_id=2, device_type="android", device_token="test-android-token-luna-001", app_version="1.0.0", os_version="Android 15", is_active=True),
        ]
        db.add_all(user_devices)
        await db.flush()

        login_logs = [
            LoginLog(id=1, user_id=1, ip_address="127.0.0.1", device_type="ios",     device_info="iPhone 16 Pro", status="success"),
            LoginLog(id=2, user_id=1, ip_address="127.0.0.1", device_type="web",     device_info="Chrome 130",    status="success"),
            LoginLog(id=3, user_id=2, ip_address="127.0.0.1", device_type="android", device_info="Galaxy S25",    status="success"),
            LoginLog(id=4, user_id=1, ip_address="192.168.0.1", device_type="web",   device_info="Chrome 130",    status="fail", fail_reason="비밀번호 오류"),
        ]
        db.add_all(login_logs)
        await db.flush()

        print("  [OK] Auth (users, profile, settings, addresses, devices, login_logs)")

        # ================================================================
        # 2. CELEB — celebs / categories / category_map / social_links / managers
        # ================================================================
        categories = [
            CelebCategory(id=1,  name="가수"),
            CelebCategory(id=2,  name="댄서"),
            CelebCategory(id=3,  name="일러스트레이터"),
            CelebCategory(id=4,  name="배우"),
            CelebCategory(id=5,  name="시인"),
            CelebCategory(id=6,  name="유튜버"),
            CelebCategory(id=7,  name="소설가"),
            CelebCategory(id=8,  name="사진작가"),
            CelebCategory(id=9,  name="웹툰작가"),
            CelebCategory(id=10, name="요리연구가"),
        ]
        db.add_all(categories)
        await db.flush()

        artists = [
            Celeb(id=1,  user_id=2,  stage_name="루나",   slug=generate_slug("루나"),   notes="음악으로 세상을 밝히는 싱어송라이터. 감성적인 멜로디와 진솔한 가사로 많은 팬들의 사랑을 받고 있습니다.", status="active"),
            Celeb(id=2,  user_id=3,  stage_name="하루",   slug=generate_slug("하루"),   notes="춤으로 하루를 채우는 댄서. 현대무용과 팝핀을 결합한 독창적인 스타일로 주목받고 있습니다.", status="active"),
            Celeb(id=3,  user_id=4,  stage_name="소율",   slug=generate_slug("소율"),   notes="그림으로 이야기를 전하는 일러스트레이터. 도시의 감성을 담은 작품으로 많은 사랑을 받고 있습니다.", status="active"),
            Celeb(id=4,  user_id=5,  stage_name="민서",   slug=generate_slug("민서"),   notes="연기로 감동을 주는 배우. 다양한 장르를 넘나드는 연기력으로 주목받는 신진 배우입니다.", status="active"),
            Celeb(id=5,  user_id=6,  stage_name="제이",   slug=generate_slug("제이"),   notes="힙합으로 세상을 흔드는 래퍼. 날카로운 가사와 강렬한 퍼포먼스로 언더그라운드를 평정했습니다.", status="active"),
            Celeb(id=6,  user_id=7,  stage_name="유리",   slug=generate_slug("유리"),   notes="현대무용의 새로운 지평을 여는 댄서. 몸으로 쓰는 시인이라는 평가를 받습니다.", status="active"),
            # 셀럽 유형 확장
            Celeb(id=7,  user_id=10, stage_name="김지수", slug=generate_slug("김지수"), notes="일상의 틈에서 시를 건지는 시인. 쉽고 따뜻한 언어로 독자의 마음을 어루만지는 작품을 씁니다.", status="active"),
            Celeb(id=8,  user_id=11, stage_name="박민지", slug=generate_slug("박민지"), notes="구독자 120만 뷰튜버. 여행·일상·브이로그 콘텐츠로 많은 사랑을 받고 있는 유튜버입니다.", status="active"),
            Celeb(id=9,  user_id=12, stage_name="이승우", slug=generate_slug("이승우"), notes="베스트셀러 소설 '밤의 언어'로 데뷔한 소설가. 서정적인 문체와 탄탄한 서사로 독자를 사로잡습니다.", status="active"),
            Celeb(id=10, user_id=13, stage_name="최나라", slug=generate_slug("최나라"), notes="빛과 감성을 담는 사진작가. 필름 카메라 특유의 질감으로 일상을 예술로 만들어냅니다.", status="active"),
            Celeb(id=11, user_id=14, stage_name="정현석", slug=generate_slug("정현석"), notes="네이버 웹툰 '우리 사이의 거리' 연재 중인 웹툰작가. 청춘의 감성과 유머로 많은 팬을 보유하고 있습니다.", status="active"),
            Celeb(id=12, user_id=15, stage_name="오채원", slug=generate_slug("오채원"), notes="집밥의 따뜻함을 전하는 요리연구가. 쉽고 맛있는 레시피로 요리 초보자도 따라할 수 있는 콘텐츠를 제공합니다.", status="active"),
        ]
        db.add_all(artists)
        await db.flush()

        category_maps = [
            CelebCategoryMap(celeb_id=1,  category_id=1),
            CelebCategoryMap(celeb_id=2,  category_id=2),
            CelebCategoryMap(celeb_id=3,  category_id=3),
            CelebCategoryMap(celeb_id=4,  category_id=4),
            CelebCategoryMap(celeb_id=5,  category_id=1),
            CelebCategoryMap(celeb_id=6,  category_id=2),
            CelebCategoryMap(celeb_id=7,  category_id=5),
            CelebCategoryMap(celeb_id=8,  category_id=6),
            CelebCategoryMap(celeb_id=9,  category_id=7),
            CelebCategoryMap(celeb_id=10, category_id=8),
            CelebCategoryMap(celeb_id=11, category_id=9),
            CelebCategoryMap(celeb_id=12, category_id=10),
        ]
        db.add_all(category_maps)
        await db.flush()

        social_links = [
            CelebSocialLink(celeb_id=1,  platform_name="YouTube",    url="https://youtube.com/@luna",       display_name="루나 뮤직",        follower_count=12000,  priority=1),
            CelebSocialLink(celeb_id=1,  platform_name="Instagram",  url="https://instagram.com/luna",      display_name="@luna_music",      follower_count=8500,   priority=2),
            CelebSocialLink(celeb_id=2,  platform_name="YouTube",    url="https://youtube.com/@haru",       display_name="하루 댄스",        follower_count=9500,   priority=1),
            CelebSocialLink(celeb_id=2,  platform_name="TikTok",     url="https://tiktok.com/@haru",        display_name="@haru_dance",      follower_count=23000,  priority=2),
            CelebSocialLink(celeb_id=3,  platform_name="Instagram",  url="https://instagram.com/soyul",     display_name="@soyul_art",       follower_count=15000,  priority=1),
            CelebSocialLink(celeb_id=4,  platform_name="YouTube",    url="https://youtube.com/@minseo",     display_name="민서 채널",        follower_count=6000,   priority=1),
            CelebSocialLink(celeb_id=5,  platform_name="SoundCloud", url="https://soundcloud.com/jay",      display_name="JAY beats",        follower_count=4500,   priority=1),
            CelebSocialLink(celeb_id=6,  platform_name="YouTube",    url="https://youtube.com/@yuri",       display_name="유리 댄스",        follower_count=7200,   priority=1),
            # 신규 셀럽 소셜 링크
            CelebSocialLink(celeb_id=7,  platform_name="Instagram",  url="https://instagram.com/jisoo_poem",display_name="@지수의 시",       follower_count=32000,  priority=1),
            CelebSocialLink(celeb_id=7,  platform_name="브런치",     url="https://brunch.co.kr/@jisoo",     display_name="김지수 브런치",    follower_count=18500,  priority=2),
            CelebSocialLink(celeb_id=8,  platform_name="YouTube",    url="https://youtube.com/@minji_vlog", display_name="박민지 브이로그",  follower_count=1200000,priority=1),
            CelebSocialLink(celeb_id=8,  platform_name="Instagram",  url="https://instagram.com/minji_vlog",display_name="@minji_vlog",      follower_count=450000, priority=2),
            CelebSocialLink(celeb_id=9,  platform_name="브런치",     url="https://brunch.co.kr/@seungwoo",  display_name="이승우 브런치",    follower_count=25000,  priority=1),
            CelebSocialLink(celeb_id=9,  platform_name="Instagram",  url="https://instagram.com/seungwoo_w",display_name="@seungwoo_writer", follower_count=14000,  priority=2),
            CelebSocialLink(celeb_id=10, platform_name="Instagram",  url="https://instagram.com/nara_photo",display_name="@나라의 필름",     follower_count=89000,  priority=1),
            CelebSocialLink(celeb_id=10, platform_name="500px",      url="https://500px.com/nara",          display_name="Nara Photography", follower_count=12000,  priority=2),
            CelebSocialLink(celeb_id=11, platform_name="네이버 웹툰", url="https://webtoon.naver.com/hyeonseok", display_name="우리 사이의 거리", follower_count=580000, priority=1),
            CelebSocialLink(celeb_id=11, platform_name="Twitter",    url="https://twitter.com/hyeonseok_wt",display_name="@hyeonseok_wt",    follower_count=42000,  priority=2),
            CelebSocialLink(celeb_id=12, platform_name="YouTube",    url="https://youtube.com/@chaewon_cook",display_name="오채원의 집밥",    follower_count=340000, priority=1),
            CelebSocialLink(celeb_id=12, platform_name="Instagram",  url="https://instagram.com/chaewon_cook",display_name="@chaewon_cook",   follower_count=120000, priority=2),
        ]
        db.add_all(social_links)
        await db.flush()

        managers = [
            Manager(id=1, user_id=8, celeb_id=1, role="manager", status="active"),
        ]
        db.add_all(managers)
        await db.flush()

        print("  [OK] Celeb (celebs, categories, category_map, social_links, managers)")

        # ================================================================
        # 3. SUBSCRIPTION — subscriptions / subscription_plans / subscription_cancellations
        # ================================================================
        subscription_plans = [
            SubscriptionPlan(id=1,  celeb_id=1,  name="루나 베이직",    price=Decimal("0"),    billing_cycle="monthly", benefits="기본 콘텐츠 열람", is_active=True),
            SubscriptionPlan(id=2,  celeb_id=1,  name="루나 프리미엄",  price=Decimal("9900"), billing_cycle="monthly", duration_days=30, benefits="전체 콘텐츠 + 비하인드 + 채팅", is_active=True),
            SubscriptionPlan(id=3,  celeb_id=2,  name="하루 베이직",    price=Decimal("0"),    billing_cycle="monthly", benefits="기본 콘텐츠 열람", is_active=True),
            SubscriptionPlan(id=4,  celeb_id=2,  name="하루 프리미엄",  price=Decimal("7900"), billing_cycle="monthly", duration_days=30, benefits="전체 콘텐츠 + 연습 영상", is_active=True),
            SubscriptionPlan(id=5,  celeb_id=3,  name="소율 베이직",    price=Decimal("0"),    billing_cycle="monthly", benefits="공개 작품 열람", is_active=True),
            SubscriptionPlan(id=6,  celeb_id=3,  name="소율 프리미엄",  price=Decimal("5900"), billing_cycle="monthly", duration_days=30, benefits="전체 작품 + 작업과정 + 채팅", is_active=True),
            SubscriptionPlan(id=7,  celeb_id=4,  name="민서 베이직",    price=Decimal("0"),    billing_cycle="monthly", benefits="기본 콘텐츠 열람", is_active=True),
            SubscriptionPlan(id=8,  celeb_id=4,  name="민서 프리미엄",  price=Decimal("8900"), billing_cycle="monthly", duration_days=30, benefits="전체 콘텐츠 + 비하인드 + 채팅", is_active=True),
            SubscriptionPlan(id=9,  celeb_id=5,  name="제이 베이직",    price=Decimal("0"),    billing_cycle="monthly", benefits="기본 콘텐츠 열람", is_active=True),
            SubscriptionPlan(id=10, celeb_id=5,  name="제이 프리미엄",  price=Decimal("6900"), billing_cycle="monthly", duration_days=30, benefits="전체 콘텐츠 + 비트 + 채팅", is_active=True),
            SubscriptionPlan(id=11, celeb_id=6,  name="유리 베이직",    price=Decimal("0"),    billing_cycle="monthly", benefits="기본 콘텐츠 열람", is_active=True),
            SubscriptionPlan(id=12, celeb_id=6,  name="유리 프리미엄",  price=Decimal("7900"), billing_cycle="monthly", duration_days=30, benefits="전체 콘텐츠 + 연습 영상 + 채팅", is_active=True),
            # 신규 셀럽 구독 플랜
            SubscriptionPlan(id=13, celeb_id=7,  name="지수 베이직",    price=Decimal("0"),    billing_cycle="monthly", benefits="공개 시 열람", is_active=True),
            SubscriptionPlan(id=14, celeb_id=7,  name="지수 프리미엄",  price=Decimal("4900"), billing_cycle="monthly", duration_days=30, benefits="전체 시 + 필사 가이드 + 채팅", is_active=True),
            SubscriptionPlan(id=15, celeb_id=8,  name="민지 베이직",    price=Decimal("0"),    billing_cycle="monthly", benefits="공개 영상 시청", is_active=True),
            SubscriptionPlan(id=16, celeb_id=8,  name="민지 프리미엄",  price=Decimal("6900"), billing_cycle="monthly", duration_days=30, benefits="멤버십 전용 영상 + 비하인드 + 채팅", is_active=True),
            SubscriptionPlan(id=17, celeb_id=9,  name="승우 베이직",    price=Decimal("0"),    billing_cycle="monthly", benefits="공개 글 열람", is_active=True),
            SubscriptionPlan(id=18, celeb_id=9,  name="승우 프리미엄",  price=Decimal("5900"), billing_cycle="monthly", duration_days=30, benefits="연재 소설 전편 + 창작 노트 + 채팅", is_active=True),
            SubscriptionPlan(id=19, celeb_id=10, name="나라 베이직",    price=Decimal("0"),    billing_cycle="monthly", benefits="공개 사진 열람", is_active=True),
            SubscriptionPlan(id=20, celeb_id=10, name="나라 프리미엄",  price=Decimal("7900"), billing_cycle="monthly", duration_days=30, benefits="고화질 원본 + 촬영 노하우 + 채팅", is_active=True),
            SubscriptionPlan(id=21, celeb_id=11, name="현석 베이직",    price=Decimal("0"),    billing_cycle="monthly", benefits="공개 회차 열람", is_active=True),
            SubscriptionPlan(id=22, celeb_id=11, name="현석 프리미엄",  price=Decimal("5900"), billing_cycle="monthly", duration_days=30, benefits="미리보기 + 스케치 + 채팅", is_active=True),
            SubscriptionPlan(id=23, celeb_id=12, name="채원 베이직",    price=Decimal("0"),    billing_cycle="monthly", benefits="공개 레시피 열람", is_active=True),
            SubscriptionPlan(id=24, celeb_id=12, name="채원 프리미엄",  price=Decimal("4900"), billing_cycle="monthly", duration_days=30, benefits="전체 레시피 + 장보기 리스트 + 채팅", is_active=True),
        ]
        db.add_all(subscription_plans)
        await db.flush()

        subscriptions = [
            Subscription(id=1,  fan_id=1, celeb_id=1,  fan_nickname="테스트팬", status="subscribed", payments_type="free", start_date=today - timedelta(days=30)),
            Subscription(id=2,  fan_id=1, celeb_id=2,  fan_nickname="테스트팬", status="subscribed", payments_type="free", start_date=today - timedelta(days=20)),
            Subscription(id=3,  fan_id=1, celeb_id=3,  fan_nickname="테스트팬", status="subscribed", payments_type="paid", start_date=today - timedelta(days=10)),
            Subscription(id=4,  fan_id=1, celeb_id=4,  fan_nickname="테스트팬", status="subscribed", payments_type="free", start_date=today - timedelta(days=15)),
            Subscription(id=5,  fan_id=1, celeb_id=5,  fan_nickname="테스트팬", status="subscribed", payments_type="free", start_date=today - timedelta(days=7)),
            Subscription(id=6,  fan_id=1, celeb_id=6,  fan_nickname="테스트팬", status="subscribed", payments_type="free", start_date=today - timedelta(days=5)),
            # 신규 셀럽 구독
            Subscription(id=7,  fan_id=1, celeb_id=7,  fan_nickname="테스트팬", status="subscribed", payments_type="paid", start_date=today - timedelta(days=14)),
            Subscription(id=8,  fan_id=1, celeb_id=8,  fan_nickname="테스트팬", status="subscribed", payments_type="free", start_date=today - timedelta(days=25)),
            Subscription(id=9,  fan_id=1, celeb_id=9,  fan_nickname="테스트팬", status="subscribed", payments_type="paid", start_date=today - timedelta(days=8)),
            Subscription(id=10, fan_id=1, celeb_id=10, fan_nickname="테스트팬", status="subscribed", payments_type="free", start_date=today - timedelta(days=12)),
            Subscription(id=11, fan_id=1, celeb_id=11, fan_nickname="테스트팬", status="subscribed", payments_type="free", start_date=today - timedelta(days=3)),
            Subscription(id=12, fan_id=1, celeb_id=12, fan_nickname="테스트팬", status="subscribed", payments_type="paid", start_date=today - timedelta(days=18)),
        ]
        db.add_all(subscriptions)
        await db.flush()

        subscription_cancellations = []
        db.add_all(subscription_cancellations)
        await db.flush()

        print("  [OK] Subscription (subscriptions, plans, cancellations)")

        # ================================================================
        # 4. CONTENT — images / posts / post_images / post_comments / post_stats
        #              celeb_images / celeb_image_comments / celeb_image_stats
        #              celeb_videos / celeb_video_comments / celeb_video_stats
        # ================================================================
        images = [
            Image(id=1,  url="/placeholder/concert1.jpg", width=1200, height=800, mime_type="image/jpeg"),
            Image(id=2,  url="/placeholder/concert2.jpg", width=1200, height=800, mime_type="image/jpeg"),
            Image(id=3,  url="/placeholder/dance1.jpg",   width=1200, height=800, mime_type="image/jpeg"),
            Image(id=4,  url="/placeholder/dance2.jpg",   width=1200, height=800, mime_type="image/jpeg"),
            Image(id=5,  url="/placeholder/art1.jpg",     width=1200, height=800, mime_type="image/jpeg"),
            Image(id=6,  url="/placeholder/art2.jpg",     width=1200, height=800, mime_type="image/jpeg"),
            Image(id=7,  url="/placeholder/product1.jpg", width=800,  height=800, mime_type="image/jpeg"),
            Image(id=8,  url="/placeholder/product2.jpg", width=800,  height=800, mime_type="image/jpeg"),
            Image(id=9,  url="/placeholder/product3.jpg", width=800,  height=800, mime_type="image/jpeg"),
            Image(id=10, url="/placeholder/banner1.jpg",  width=1920, height=600, mime_type="image/jpeg"),
            Image(id=11, url="/placeholder/banner2.jpg",  width=1920, height=600, mime_type="image/jpeg"),
            Image(id=12, url="/placeholder/chat1.jpg",    width=600,  height=600, mime_type="image/jpeg"),
        ]
        db.add_all(images)
        await db.flush()

        posts = [
            # 크리에이터 포스트 (id 1~5)
            Post(id=1,  author_id=1,  author_type="artist", content="오늘 새 앨범 작업을 시작했어요! 기대해주세요",                              write_id=2,  write_role="artist", visibility="public",      is_artist_post=True,  tags=["음악", "앨범"]),
            Post(id=2,  author_id=1,  author_type="artist", content="구독자 여러분만을 위한 비하인드 영상 곧 올라갑니다!",                       write_id=2,  write_role="artist", visibility="subscribers", is_artist_post=True,  tags=["비하인드"]),
            Post(id=3,  author_id=2,  author_type="artist", content="새로운 안무 연습 중! 이번 주 라이브에서 공개할게요",                        write_id=3,  write_role="artist", visibility="public",      is_artist_post=True,  tags=["댄스", "안무"]),
            Post(id=4,  author_id=2,  author_type="artist", content="연습실에서 하루종일 땀 흘리는 중... 화이팅!",                               write_id=3,  write_role="artist", visibility="subscribers", is_artist_post=True,  tags=["일상", "연습"]),
            Post(id=5,  author_id=3,  author_type="artist", content="새로운 일러스트 시리즈 '도시의 밤' 첫 번째 작품을 공개합니다.",             write_id=4,  write_role="artist", visibility="public",      is_artist_post=True,  tags=["일러스트", "아트"]),
            # 팬 포스트 (id 6~8)
            Post(id=6,  author_id=1,  author_type="fan",    content="루나 노래 진짜 좋아요!! 다음 앨범 기대됩니다",                              write_id=1,  write_role="fan",    visibility="public",      is_artist_post=False, tags=["팬레터"]),
            Post(id=7,  author_id=2,  author_type="fan",    content="하루님 안무 진짜 대박... 라이브 꼭 볼게요!",                                write_id=1,  write_role="fan",    visibility="public",      is_artist_post=False, tags=["응원"]),
            Post(id=8,  author_id=3,  author_type="fan",    content="소율 작가님 그림 너무 예뻐요. 굿즈 나오면 바로 구매할게요!",                write_id=1,  write_role="fan",    visibility="public",      is_artist_post=False, tags=["팬아트"]),
            # 기사형 포스트 (id 9~11)
            Post(id=9,  author_id=1,  author_type="artist", content="지난 금요일 잠실 올림픽경기장에서 열린 루나의 첫 번째 단독 콘서트가 2만 관객을 가득 채우며 성공적으로 막을 내렸습니다.", write_id=2, write_role="artist", visibility="public", is_artist_post=True, tags=["콘서트", "공연"], title_field="루나, 첫 단독 콘서트 2만 관객 매진"),
            Post(id=10, author_id=2,  author_type="artist", content="하루가 세계적인 댄스 대회 'World Dance Championship 2026'에서 현대무용 부문 금상을 수상했습니다.", write_id=3, write_role="artist", visibility="public", is_artist_post=True, tags=["수상", "대회"], title_field="하루, 세계 댄스 대회 금상 수상"),
            Post(id=11, author_id=3,  author_type="artist", content="소율 작가의 첫 개인전 '꿈의 색채'가 서울 성수동 갤러리에서 오는 3월 1일부터 31일까지 한 달간 개최됩니다.", write_id=4, write_role="artist", visibility="public", is_artist_post=True, tags=["전시", "갤러리"], title_field="소율, 첫 개인전 '꿈의 색채' 개최"),
            # 신규 크리에이터 포스트 (id 12~23)
            Post(id=12, author_id=7,  author_type="artist", content="봄비\n\n빗소리를 들으며\n창가에 앉아\n당신 생각을 했습니다\n\n빗물처럼\n조용히 스며드는\n그런 사람이 있다는 게\n얼마나 다행인지", write_id=10, write_role="artist", visibility="public",      is_artist_post=True, tags=["시", "봄", "일상시"]),
            Post(id=13, author_id=7,  author_type="artist", content="구독자 여러분, 이번 달 필사 가이드를 공유드려요. 손으로 직접 써보면 시의 리듬이 더 잘 느껴진답니다 ✍️", write_id=10, write_role="artist", visibility="subscribers", is_artist_post=True, tags=["필사", "가이드"]),
            Post(id=14, author_id=8,  author_type="artist", content="도쿄 여행 브이로그 올라왔어요! 아키하바라 → 신주쿠 → 하라주쿠 코스 추천드립니다. 유튜브 링크는 프로필에 🎥", write_id=11, write_role="artist", visibility="public",      is_artist_post=True, tags=["여행", "도쿄", "브이로그"]),
            Post(id=15, author_id=8,  author_type="artist", content="멤버십 전용! 편집할 때 쓰는 장비 세팅 공개합니다. 카메라, 마이크, 조명까지 전부 알려드릴게요 📸", write_id=11, write_role="artist", visibility="subscribers", is_artist_post=True, tags=["장비", "유튜브", "촬영"]),
            Post(id=16, author_id=9,  author_type="artist", content="'밤의 언어' 연재 7화가 올라왔습니다. 이번 화에서 드디어 준혁과 하은이 마주치게 됩니다. 많이 기대해주세요!", write_id=12, write_role="artist", visibility="public",      is_artist_post=True, tags=["소설", "연재", "밤의언어"]),
            Post(id=17, author_id=9,  author_type="artist", content="소설 쓰면서 영감을 얻는 방법 (창작 노트 공개). 제가 글을 쓸 때 습관적으로 하는 세 가지 루틴을 공유합니다.", write_id=12, write_role="artist", visibility="subscribers", is_artist_post=True, tags=["창작", "소설쓰기", "루틴"]),
            Post(id=18, author_id=10, author_type="artist", content="서울의 새벽 4시. 아무도 없는 골목에서 찍은 사진들을 공개합니다. 고요함 속에 담긴 도시의 숨소리.", write_id=13, write_role="artist", visibility="public",      is_artist_post=True, tags=["사진", "서울", "새벽", "필름"]),
            Post(id=19, author_id=10, author_type="artist", content="구독자 전용 — 고화질 원본 파일 공유 + 이번 달 촬영 세팅 노하우. 조리개값과 필름 시뮬레이션 세팅 전부 공개!", write_id=13, write_role="artist", visibility="subscribers", is_artist_post=True, tags=["원본", "노하우", "필름카메라"]),
            Post(id=20, author_id=11, author_type="artist", content="'우리 사이의 거리' 42화 업로드 완료! 이번 화 진짜 많이 울었어요... 독자분들 반응이 기대되네요 😭", write_id=14, write_role="artist", visibility="public",      is_artist_post=True, tags=["웹툰", "연재", "우리사이의거리"]),
            Post(id=21, author_id=11, author_type="artist", content="43화 스케치 미리보기 공개! 다음 전개가 궁금하시면 구독 후 확인해주세요 🎨", write_id=14, write_role="artist", visibility="subscribers", is_artist_post=True, tags=["스케치", "미리보기", "웹툰"]),
            Post(id=22, author_id=12, author_type="artist", content="봄 제철 재료로 만드는 쑥 된장국 레시피 공개! 재료 딱 5가지, 15분 안에 완성되는 집밥이에요 🍲", write_id=15, write_role="artist", visibility="public",      is_artist_post=True, tags=["레시피", "봄요리", "된장국"]),
            Post(id=23, author_id=12, author_type="artist", content="이번 달 장보기 리스트 + 5만원으로 일주일 식단 짜는 법 (구독자 전용). 마트 할인 정보까지 포함!", write_id=15, write_role="artist", visibility="subscribers", is_artist_post=True, tags=["장보기", "절약", "식단"]),
        ]
        db.add_all(posts)
        await db.flush()

        post_images = [
            PostImage(id=1, post_id=1,  image_id=1, sort_order=0),
            PostImage(id=2, post_id=1,  image_id=2, sort_order=1),
            PostImage(id=3, post_id=3,  image_id=3, sort_order=0),
            PostImage(id=4, post_id=5,  image_id=5, sort_order=0),
            PostImage(id=5, post_id=9,  image_id=1, sort_order=0),
            PostImage(id=6, post_id=10, image_id=3, sort_order=0),
            PostImage(id=7, post_id=11, image_id=5, sort_order=0),
        ]
        db.add_all(post_images)
        await db.flush()

        post_comments = [
            PostComment(id=1, post_id=1, user_id=1, content="새 앨범 너무 기대돼요!",           commenter_role="fan",    status="active"),
            PostComment(id=2, post_id=1, user_id=2, content="감사합니다! 열심히 준비할게요",      commenter_role="artist", status="active", parent_comment_id=1),
            PostComment(id=3, post_id=3, user_id=1, content="안무 미리보기 영상 올려주세요!",    commenter_role="fan",    status="active"),
            PostComment(id=4, post_id=5, user_id=1, content="우와 분위기 너무 좋아요",           commenter_role="fan",    status="active"),
            PostComment(id=5, post_id=6, user_id=2, content="응원 감사합니다! 더 열심히 할게요", commenter_role="artist", status="active"),
            PostComment(id=6, post_id=9, user_id=1, content="콘서트 정말 최고였어요!",           commenter_role="fan",    status="active"),
        ]
        db.add_all(post_comments)
        await db.flush()

        post_stats = [
            PostStat(id=i, post_id=i, view_count=(24 - i) * 50, comment_count=2 if i <= 3 else 1, fan_like_count=(24 - i) * 3, artist_like_count=1 if i >= 6 else 0)
            for i in range(1, 24)
        ]
        db.add_all(post_stats)
        await db.flush()

        # Celeb Images
        celeb_images = [
            CelebImage(id=1, celeb_id=1, image_id=1, write_id=2, write_role="artist", image_purpose="concert",     tags=["콘서트", "무대"],   visibility="public"),
            CelebImage(id=2, celeb_id=1, image_id=2, write_id=2, write_role="artist", image_purpose="behind",      tags=["비하인드"],         visibility="subscribers"),
            CelebImage(id=3, celeb_id=2, image_id=3, write_id=3, write_role="artist", image_purpose="performance", tags=["댄스", "공연"],     visibility="public"),
            CelebImage(id=4, celeb_id=2, image_id=4, write_id=3, write_role="artist", image_purpose="practice",    tags=["연습"],             visibility="subscribers"),
            CelebImage(id=5, celeb_id=3, image_id=5, write_id=4, write_role="artist", image_purpose="artwork",     tags=["일러스트", "작품"], visibility="public"),
            CelebImage(id=6, celeb_id=3, image_id=6, write_id=4, write_role="artist", image_purpose="process",     tags=["작업과정"],         visibility="public"),
        ]
        db.add_all(celeb_images)
        await db.flush()

        celeb_image_comments = [
            CelebImageComment(id=1, celeb_image_id=1, user_id=1, content="무대 사진 너무 멋져요!",    commenter_role="fan",    status="active"),
            CelebImageComment(id=2, celeb_image_id=1, user_id=2, content="고마워요!",                 commenter_role="artist", status="active", parent_comment_id=1),
            CelebImageComment(id=3, celeb_image_id=3, user_id=1, content="공연 사진 대박이네요",       commenter_role="fan",    status="active"),
            CelebImageComment(id=4, celeb_image_id=5, user_id=1, content="이 작품 원본 사이즈 보고싶어요", commenter_role="fan", status="active"),
        ]
        db.add_all(celeb_image_comments)
        await db.flush()

        celeb_image_stats = [
            CelebImageStat(id=i, celeb_image_id=i, view_count=(7 - i) * 30, comment_count=2 if i == 1 else 1, fan_like_count=(7 - i) * 5)
            for i in range(1, 7)
        ]
        db.add_all(celeb_image_stats)
        await db.flush()

        # Celeb Videos
        celeb_videos = [
            CelebVideo(id=1, celeb_id=1, write_id=2, write_role="artist", url="/placeholder/video1.mp4", title="루나 - 별빛 아래서 MV",    description="신곡 뮤직비디오",   duration_seconds=245, tags=["뮤직비디오", "신곡"], visibility="public"),
            CelebVideo(id=2, celeb_id=1, write_id=2, write_role="artist", url="/placeholder/video2.mp4", title="앨범 작업 비하인드",        description="스튜디오 비하인드", duration_seconds=600, tags=["비하인드"],           visibility="subscribers"),
            CelebVideo(id=3, celeb_id=2, write_id=3, write_role="artist", url="/placeholder/video3.mp4", title="Gravity 안무 풀버전",       description="대회 출전 안무",    duration_seconds=310, tags=["안무", "풀버전"],     visibility="public"),
            CelebVideo(id=4, celeb_id=2, write_id=3, write_role="artist", url="/placeholder/video4.mp4", title="안무 연습 브이로그",         description="연습실 브이로그",   duration_seconds=900, tags=["브이로그", "연습"],   visibility="public"),
            CelebVideo(id=5, celeb_id=3, write_id=4, write_role="artist", url="/placeholder/video5.mp4", title="작업 타임랩스 - 도시의 밤", description="일러스트 타임랩스", duration_seconds=180, tags=["타임랩스", "작업과정"], visibility="public"),
        ]
        db.add_all(celeb_videos)
        await db.flush()

        celeb_video_comments = [
            CelebVideoComment(id=1, celeb_video_id=1, user_id=1, content="MV 퀄리티 미쳤어요!",         commenter_role="fan",    status="active"),
            CelebVideoComment(id=2, celeb_video_id=1, user_id=2, content="많이 사랑해주세요!",           commenter_role="artist", status="active", parent_comment_id=1),
            CelebVideoComment(id=3, celeb_video_id=3, user_id=1, content="안무 진짜 소름 돋아요",        commenter_role="fan",    status="active"),
            CelebVideoComment(id=4, celeb_video_id=5, user_id=1, content="타임랩스 보는 재미가 있네요",  commenter_role="fan",    status="active"),
        ]
        db.add_all(celeb_video_comments)
        await db.flush()

        celeb_video_stats = [
            CelebVideoStat(id=i, celeb_video_id=i, view_count=(6 - i) * 100, comment_count=2 if i == 1 else 1, fan_like_count=(6 - i) * 15)
            for i in range(1, 6)
        ]
        db.add_all(celeb_video_stats)
        await db.flush()

        print("  [OK] Content (posts, images, videos, comments, stats)")

        # ================================================================
        # 5. CHAT — chat_rooms / chat_messages / chat_images / chat_videos
        #           chat_read_receipts / chat_pins / chat_reports
        # ================================================================
        chat_rooms = [
            ChatRoom(id=1, room_type="subscription", celeb_id=1,  room_name="루나 채팅방",    last_message_at=now - timedelta(minutes=5),  status="active"),
            ChatRoom(id=2, room_type="subscription", celeb_id=2,  room_name="하루 채팅방",    last_message_at=now - timedelta(hours=1),    status="active"),
            ChatRoom(id=3, room_type="subscription", celeb_id=3,  room_name="소율 채팅방",    last_message_at=now - timedelta(hours=3),    status="active"),
            ChatRoom(id=4, room_type="subscription", celeb_id=7,  room_name="지수 시인 채팅", last_message_at=now - timedelta(hours=2),    status="active"),
            ChatRoom(id=5, room_type="subscription", celeb_id=8,  room_name="민지 유튜버 채팅",last_message_at=now - timedelta(minutes=30), status="active"),
            ChatRoom(id=6, room_type="subscription", celeb_id=12, room_name="채원 채팅방",    last_message_at=now - timedelta(hours=5),    status="active"),
        ]
        db.add_all(chat_rooms)
        await db.flush()

        chat_messages = [
            # 루나 채팅방
            ChatMessage(id=1,  chat_room_id=1, sender_id=2,  sender_type="artist", message_type="text",  content="안녕하세요! 오늘도 좋은 하루 보내세요", status="active"),
            ChatMessage(id=2,  chat_room_id=1, sender_id=1,  sender_type="fan",    message_type="text",  content="루나님 안녕하세요! 새 앨범 기대하고 있어요", status="active"),
            ChatMessage(id=3,  chat_room_id=1, sender_id=2,  sender_type="artist", message_type="text",  content="감사합니다! 곧 좋은 소식 들려드릴게요", status="active"),
            ChatMessage(id=4,  chat_room_id=1, sender_id=1,  sender_type="fan",    message_type="image", content=None, status="active"),
            ChatMessage(id=5,  chat_room_id=1, sender_id=2,  sender_type="artist", message_type="text",  content="이 사진 예쁘네요!", status="active", is_pinned=True),
            # 하루 채팅방
            ChatMessage(id=6,  chat_room_id=2, sender_id=3,  sender_type="artist", message_type="text",  content="오늘 연습 끝! 다들 수고했어요", status="active"),
            ChatMessage(id=7,  chat_room_id=2, sender_id=1,  sender_type="fan",    message_type="text",  content="하루님 연습 영상 올려주세요!", status="active"),
            ChatMessage(id=8,  chat_room_id=2, sender_id=3,  sender_type="artist", message_type="video", content=None, status="active"),
            # 소율 채팅방
            ChatMessage(id=9,  chat_room_id=3, sender_id=4,  sender_type="artist", message_type="text",  content="새 작품 작업 중이에요. 조금만 기다려주세요!", status="active"),
            ChatMessage(id=10, chat_room_id=3, sender_id=1,  sender_type="fan",    message_type="text",  content="기대하고 있을게요!!", status="active"),
            # 지수 시인 채팅방
            ChatMessage(id=11, chat_room_id=4, sender_id=10, sender_type="artist", message_type="text",  content="오늘 새 시 한 편 썼어요. 봄비 소리를 들으며 쓴 시인데, 구독자분들께 먼저 보여드릴게요 🌧️", status="active"),
            ChatMessage(id=12, chat_room_id=4, sender_id=1,  sender_type="fan",    message_type="text",  content="지수님 시 너무 좋아요... 오늘도 읽으면서 위로받았어요", status="active"),
            ChatMessage(id=13, chat_room_id=4, sender_id=10, sender_type="artist", message_type="text",  content="그 말이 저한테 큰 힘이 돼요. 감사합니다 🙏", status="active"),
            # 민지 유튜버 채팅방
            ChatMessage(id=14, chat_room_id=5, sender_id=11, sender_type="artist", message_type="text",  content="도쿄 브이로그 편집 중이에요! 내일 오후에 올라갈 예정 🎬", status="active"),
            ChatMessage(id=15, chat_room_id=5, sender_id=1,  sender_type="fan",    message_type="text",  content="오 대박!! 도쿄 어디어디 갔어요?", status="active"),
            ChatMessage(id=16, chat_room_id=5, sender_id=11, sender_type="artist", message_type="text",  content="아키하바라, 하라주쿠, 신주쿠 갔어요! 영상에서 코스 다 알려드릴게요 😊", status="active"),
            # 채원 채팅방
            ChatMessage(id=17, chat_room_id=6, sender_id=15, sender_type="artist", message_type="text",  content="오늘 레시피 질문 받아요! 요즘 봄나물 제철이니까 뭐든 물어보세요 🌿", status="active"),
            ChatMessage(id=18, chat_room_id=6, sender_id=1,  sender_type="fan",    message_type="text",  content="쑥 된장국 끓일 때 쑥 데쳐야 하나요?", status="active"),
            ChatMessage(id=19, chat_room_id=6, sender_id=15, sender_type="artist", message_type="text",  content="네! 살짝 데친 후 찬물에 헹궈서 쓴맛 빼주시면 더 맛있어요 😋", status="active"),
        ]
        db.add_all(chat_messages)
        await db.flush()

        chat_images_data = [
            ChatImage(id=1, chat_message_id=4, image_id=12),
        ]
        db.add_all(chat_images_data)
        await db.flush()

        chat_videos_data = [
            ChatVideo(id=1, chat_message_id=8, url="/placeholder/chat_video1.mp4", duration_seconds=30),
        ]
        db.add_all(chat_videos_data)
        await db.flush()

        chat_read_receipts = [
            ChatReadReceipt(id=1, chat_message_id=5, user_id=1),
            ChatReadReceipt(id=2, chat_message_id=5, user_id=2),
            ChatReadReceipt(id=3, chat_message_id=7, user_id=1),
            ChatReadReceipt(id=4, chat_message_id=7, user_id=3),
            ChatReadReceipt(id=5, chat_message_id=10, user_id=1),
        ]
        db.add_all(chat_read_receipts)
        await db.flush()

        chat_pins = [
            ChatPin(id=1, chat_room_id=1, chat_message_id=5, pinned_by=2),
        ]
        db.add_all(chat_pins)
        await db.flush()

        chat_reports = [
            ChatReport(id=1, chat_message_id=7, reported_by=1, reason="테스트 신고", status="pending"),
        ]
        db.add_all(chat_reports)
        await db.flush()

        print("  [OK] Chat (rooms, messages, images, videos, read_receipts, pins, reports)")

        # ================================================================
        # 6. SEARCH — calendar_searches / saved_search_filters
        # ================================================================
        calendar_searches = [
            CalendarSearch(id=1, user_id=1, search_query="루나 콘서트", filters={"category": "가수", "date_range": "2026-03"}, result_count=3),
            CalendarSearch(id=2, user_id=1, search_query="댄스 챌린지", filters={"category": "댄서"}, result_count=5),
        ]
        db.add_all(calendar_searches)
        await db.flush()

        saved_search_filters = [
            SavedSearchFilter(id=1, user_id=1, filter_name="내 구독 아티스트", filter_data={"subscribed_only": True, "content_type": "all"}, is_default=True),
            SavedSearchFilter(id=2, user_id=1, filter_name="음악 카테고리",    filter_data={"category": "가수", "sort": "latest"}, is_default=False),
        ]
        db.add_all(saved_search_filters)
        await db.flush()

        print("  [OK] Search (calendar_searches, saved_search_filters)")

        # ================================================================
        # 7. PAYMENT — payment_methods / payments / payment_refunds
        # ================================================================
        payment_methods = [
            PaymentMethod(id=1, user_id=1, method_type="card",   provider="toss", account_info={"card_last4": "1234", "card_brand": "Visa"}, is_default=True, is_active=True),
            PaymentMethod(id=2, user_id=1, method_type="kakaopay", provider="kakao", account_info={"account_id": "kakao_test_001"},          is_default=False, is_active=True),
        ]
        db.add_all(payment_methods)
        await db.flush()

        payments = [
            Payment(id=1, user_id=1, payment_type="subscription", related_id=3, related_type="subscription", amount=Decimal("5900"), currency="KRW", status="completed", transaction_id="TXN-TEST-001", payment_method_id=1, paid_at=now - timedelta(days=10)),
            Payment(id=2, user_id=1, payment_type="shop",         related_id=1, related_type="order",        amount=Decimal("35000"), currency="KRW", status="completed", transaction_id="TXN-TEST-002", payment_method_id=1, paid_at=now - timedelta(days=5)),
            Payment(id=3, user_id=1, payment_type="shop",         related_id=2, related_type="order",        amount=Decimal("25000"), currency="KRW", status="refunded",  transaction_id="TXN-TEST-003", payment_method_id=2, paid_at=now - timedelta(days=3)),
        ]
        db.add_all(payments)
        await db.flush()

        payment_refunds = [
            PaymentRefund(id=1, payment_id=3, user_id=1, refund_amount=Decimal("25000"), reason="단순 변심", status="completed", processed_at=now - timedelta(days=2)),
        ]
        db.add_all(payment_refunds)
        await db.flush()

        print("  [OK] Payment (methods, payments, refunds)")

        # ================================================================
        # 8. EVENT — events / event_participants / event_attendance
        # ================================================================
        events = [
            Event(id=1, celeb_id=1,  title="루나 팬미팅 2026",        description="팬 여러분과 함께하는 특별한 시간",                                         event_type="fanmeeting", event_date=now + timedelta(days=14), location="서울 강남 이벤트홀",         max_participants=200,   current_participants=46,    status="active"),
            Event(id=2, celeb_id=2,  title="하루 댄스 챌린지",         description="Gravity 안무 따라하기 챌린지",                                              event_type="challenge",  event_date=now + timedelta(days=7),  location="온라인",                     max_participants=None,  current_participants=128,   status="active"),
            Event(id=3, celeb_id=3,  title="소율 라이브 드로잉",        description="실시간으로 그림 그리는 과정을 공개합니다",                                  event_type="live",       event_date=now + timedelta(days=3),  location="유튜브 라이브",              max_participants=None,  current_participants=1,     status="active"),
            Event(id=4, celeb_id=1,  title="루나 콘서트 2026",         description="루나 단독 콘서트 — 별빛 아래서",                                            event_type="concert",    event_date=now - timedelta(days=7),  location="잠실 올림픽경기장",          max_participants=20000, current_participants=20000, status="completed"),
            # 신규 셀럽 이벤트
            Event(id=5, celeb_id=7,  title="김지수 시인과의 대화",      description="시인 김지수와 함께 시 읽기, 필사, Q&A를 진행하는 소규모 모임입니다. 구독자 우선 신청 가능.", event_type="meetup",  event_date=now + timedelta(days=21), location="서울 마포구 독립서점 '책방 달'", max_participants=30,    current_participants=22,    status="active"),
            Event(id=6, celeb_id=8,  title="박민지 크리에이터 클래스",  description="유튜브 채널 운영부터 영상 편집까지! 박민지의 노하우를 직접 배울 수 있는 워크숍입니다.",    event_type="workshop", event_date=now + timedelta(days=10), location="서울 강남구 스튜디오 M",       max_participants=20,    current_participants=20,    status="full"),
            Event(id=7, celeb_id=11, title="정현석 사인회 & 독자 간담회", description="웹툰 '우리 사이의 거리' 100화 기념 특별 사인회. 작가와 직접 이야기를 나눌 수 있는 자리입니다.", event_type="signing", event_date=now + timedelta(days=28), location="서울 종로구 교보문고 광화문점", max_participants=100,   current_participants=67,    status="active"),
            Event(id=8, celeb_id=12, title="오채원 요리 클래스 — 봄 제철 요리",description="봄 제철 재료로 만드는 건강 집밥 3가지를 직접 요리해보는 오프라인 클래스입니다.",   event_type="class",    event_date=now + timedelta(days=5),  location="서울 성동구 요리 스튜디오",   max_participants=12,    current_participants=10,    status="active"),
        ]
        db.add_all(events)
        await db.flush()

        event_participants = [
            EventParticipant(id=1, event_id=1, user_id=1, status="registered"),
            EventParticipant(id=2, event_id=2, user_id=1, status="registered"),
            EventParticipant(id=3, event_id=3, user_id=1, status="registered"),
            EventParticipant(id=4, event_id=4, user_id=1, status="attended"),
        ]
        db.add_all(event_participants)
        await db.flush()

        event_attendances = [
            EventAttendance(id=1, event_id=4, participant_id=4, checked_in_by=2),
        ]
        db.add_all(event_attendances)
        await db.flush()

        print("  [OK] Event (events, participants, attendance)")

        # ================================================================
        # 9. SHOP — products / product_images / orders / order_items
        # ================================================================
        products = [
            Product(id=1,  celeb_id=1,  name="루나 포토카드 세트",         description="별빛 아래서 콘서트 포토카드 5장",                                  price=Decimal("15000"), stock=100, category="photocard", status="active"),
            Product(id=2,  celeb_id=1,  name="루나 라이트스틱",             description="공식 응원봉",                                                      price=Decimal("35000"), stock=50,  category="lightstick", status="active"),
            Product(id=3,  celeb_id=2,  name="하루 연습복 티셔츠",          description="하루 시그니처 로고 티셔츠",                                        price=Decimal("25000"), stock=200, category="apparel",    status="active"),
            Product(id=4,  celeb_id=3,  name="소율 아트프린트 A3",          description="도시의 밤 시리즈 한정판 프린트",                                   price=Decimal("20000"), stock=30,  category="art",        status="active"),
            Product(id=5,  celeb_id=3,  name="소율 스티커팩",               description="일러스트 스티커 10장 세트",                                        price=Decimal("5000"),  stock=500, category="sticker",    status="active"),
            # 신규 셀럽 상품
            Product(id=6,  celeb_id=7,  name="김지수 시집 '봄을 기다리며'", description="시인 김지수의 첫 번째 시집. 총 72편 수록, 작가 친필 사인 포함 (한정 100부)", price=Decimal("18000"), stock=100, category="book",       status="active"),
            Product(id=7,  celeb_id=7,  name="필사 노트 세트",              description="김지수 시인 추천 필사 노트 + 캘리그래피 펜 세트. 감성 패키지 포장.", price=Decimal("22000"), stock=150, category="stationery", status="active"),
            Product(id=8,  celeb_id=8,  name="박민지 브이로그 캘린더",      description="2026년 박민지 여행 사진으로 만든 탁상 캘린더 (12개월)",             price=Decimal("12000"), stock=300, category="calendar",   status="active"),
            Product(id=9,  celeb_id=9,  name="이승우 소설 '밤의 언어'",    description="베스트셀러 소설 단행본. 작가 친필 사인 + 엽서 3종 포함 (한정판)",    price=Decimal("16800"), stock=200, category="book",       status="active"),
            Product(id=10, celeb_id=10, name="최나라 포토북 '서울의 새벽'", description="사진작가 최나라의 첫 번째 포토북. 필름 사진 80컷 수록, 하드커버 양장.", price=Decimal("38000"), stock=50,  category="photobook",  status="active"),
            Product(id=11, celeb_id=11, name="'우리 사이의 거리' 단행본 1권", description="네이버 웹툰 단행본. 1~25화 수록, 미공개 에피소드 포함.",          price=Decimal("13000"), stock=400, category="book",       status="active"),
            Product(id=12, celeb_id=12, name="오채원 레시피북 '집밥의 온도'", description="인기 레시피 100가지 수록. 계절별 제철 재료 활용법 + QR코드 영상 제공.", price=Decimal("19800"), stock=250, category="book",       status="active"),
        ]
        db.add_all(products)
        await db.flush()

        product_images = [
            ProductImage(id=1, product_id=1, image_id=7,  is_primary=True,  sort_order=0),
            ProductImage(id=2, product_id=2, image_id=8,  is_primary=True,  sort_order=0),
            ProductImage(id=3, product_id=3, image_id=9,  is_primary=True,  sort_order=0),
            ProductImage(id=4, product_id=4, image_id=5,  is_primary=True,  sort_order=0),
            ProductImage(id=5, product_id=5, image_id=6,  is_primary=True,  sort_order=0),
        ]
        db.add_all(product_images)
        await db.flush()

        orders = [
            Order(id=1, user_id=1, order_number="ORD-2026-0001", total_amount=Decimal("35000"), status="delivered",  payment_id=2, shipping_address_id=1, tracking_number="CJ1234567890", shipped_at=now - timedelta(days=4), delivered_at=now - timedelta(days=2)),
            Order(id=2, user_id=1, order_number="ORD-2026-0002", total_amount=Decimal("25000"), status="refunded",   payment_id=3, shipping_address_id=1),
            Order(id=3, user_id=1, order_number="ORD-2026-0003", total_amount=Decimal("20000"), status="pending",    shipping_address_id=2),
        ]
        db.add_all(orders)
        await db.flush()

        order_items = [
            OrderItem(id=1, order_id=1, product_id=2, quantity=1, unit_price=Decimal("35000"), total_price=Decimal("35000")),
            OrderItem(id=2, order_id=2, product_id=3, quantity=1, unit_price=Decimal("25000"), total_price=Decimal("25000")),
            OrderItem(id=3, order_id=3, product_id=4, quantity=1, unit_price=Decimal("20000"), total_price=Decimal("20000")),
        ]
        db.add_all(order_items)
        await db.flush()

        print("  [OK] Shop (products, product_images, orders, order_items)")

        # ================================================================
        # 10. NOTIFICATION — templates / notifications / settings / scheduled / system_logs
        # ================================================================
        notification_templates = [
            NotificationTemplate(id=1,  template_name="새 포스트",       noti_type="content", title_template="{artist_name}님이 새 포스트를 올렸어요",      message_template="{artist_name}: {preview}", is_active=True),
            NotificationTemplate(id=2,  template_name="새 이미지",       noti_type="content", title_template="{artist_name}님이 새 이미지를 올렸어요",      message_template="{artist_name}님의 새 이미지를 확인하세요", is_active=True),
            NotificationTemplate(id=3,  template_name="새 영상",         noti_type="content", title_template="{artist_name}님이 새 영상을 올렸어요",        message_template="{video_title}", is_active=True),
            NotificationTemplate(id=4,  template_name="댓글 답글",       noti_type="social",  title_template="{user_name}님이 답글을 남겼어요",             message_template="{preview}", is_active=True),
            NotificationTemplate(id=5,  template_name="이벤트 오픈",     noti_type="event",   title_template="{artist_name}님의 새 이벤트가 열렸어요",      message_template="{event_title}", is_active=True),
            NotificationTemplate(id=6,  template_name="주문 배송 시작",  noti_type="order",   title_template="주문하신 상품이 배송 시작되었어요",            message_template="주문번호 {order_number}", is_active=True),
            NotificationTemplate(id=7,  template_name="채팅 메시지",     noti_type="chat",    title_template="{sender_name}님의 메시지",                    message_template="{preview}", is_active=True),
            NotificationTemplate(id=8,  template_name="결제 완료",       noti_type="payment", title_template="결제가 완료되었어요",                          message_template="{amount}원 결제 완료", is_active=True),
            NotificationTemplate(id=9,  template_name="공지사항",        noti_type="notice",  title_template="새 공지사항이 등록되었어요",                   message_template="{title}", is_active=True),
            NotificationTemplate(id=10, template_name="댓글 알림",       noti_type="comment", title_template="{user_name}님이 댓글을 남겼어요",              message_template="{preview}", is_active=True),
            NotificationTemplate(id=11, template_name="구독 만료 예정",  noti_type="payment", title_template="구독이 곧 만료돼요",                          message_template="{artist_name} 구독이 {days}일 후 만료됩니다", is_active=True),
            NotificationTemplate(id=12, template_name="시스템 점검",     noti_type="system",  title_template="시스템 점검 안내",                             message_template="{message}", is_active=True),
            NotificationTemplate(id=13, template_name="주문 배송 완료",  noti_type="order",   title_template="주문하신 상품이 배송 완료되었어요",             message_template="주문번호 {order_number}", is_active=True),
            NotificationTemplate(id=14, template_name="좋아요 알림",     noti_type="social",  title_template="{user_name}님이 회원님의 글을 좋아해요",       message_template="{preview}", is_active=True),
        ]
        db.add_all(notification_templates)
        await db.flush()

        notifications = [
            # 콘텐츠 알림 — 읽음/안읽음 혼합
            Notification(id=1,  subscription_id=1, user_id=1, noti_type="content", source_id=1, source_type="post",          event_type="new_post",    target_id=1,  title="루나님이 새 포스트를 올렸어요",         message="오늘 새 앨범 작업을 시작했어요!",            is_read=True,  is_pushed=True,  created_at=now - timedelta(days=5)),
            Notification(id=2,  subscription_id=1, user_id=1, noti_type="content", source_id=1, source_type="artist_video",   event_type="new_video",   target_id=1,  title="루나님이 새 영상을 올렸어요",           message="루나 - 별빛 아래서 MV",                      is_read=True,  is_pushed=True,  created_at=now - timedelta(days=4)),
            Notification(id=3,  subscription_id=2, user_id=1, noti_type="content", source_id=2, source_type="post",          event_type="new_post",    target_id=3,  title="하루님이 새 포스트를 올렸어요",         message="새로운 안무 연습 중!",                       is_read=False, is_pushed=True,  created_at=now - timedelta(days=3)),
            Notification(id=4,  subscription_id=3, user_id=1, noti_type="content", source_id=3, source_type="post",          event_type="new_post",    target_id=5,  title="소율님이 새 포스트를 올렸어요",         message="새로운 일러스트 시리즈 '도시의 밤'",          is_read=False, is_pushed=True,  created_at=now - timedelta(days=2)),
            # 소셜 알림 — 답글, 댓글, 좋아요
            Notification(id=5,  user_id=1, noti_type="social",  source_id=2, source_type="user",          event_type="reply",       target_id=1,  title="루나님이 답글을 남겼어요",               message="감사합니다! 열심히 준비할게요",               is_read=False, is_pushed=True,  created_at=now - timedelta(days=2, hours=5)),
            Notification(id=9,  user_id=1, noti_type="comment", source_id=3, source_type="user",          event_type="comment",     target_id=3,  title="하루님이 댓글을 남겼어요",               message="응원 감사합니다!",                           is_read=False, is_pushed=True,  created_at=now - timedelta(days=1, hours=8)),
            Notification(id=10, user_id=1, noti_type="social",  source_id=4, source_type="user",          event_type="like",        target_id=8,  title="소율님이 회원님의 글을 좋아해요",        message="소율 작가님 그림 너무 예뻐요...",             is_read=False, is_pushed=True,  created_at=now - timedelta(hours=12)),
            Notification(id=11, user_id=1, noti_type="reply",   source_id=2, source_type="user",          event_type="reply",       target_id=6,  title="루나님이 답글을 남겼어요",               message="응원 감사합니다! 더 열심히 할게요",           is_read=True,  is_pushed=True,  created_at=now - timedelta(days=3, hours=2)),
            # 이벤트 알림
            Notification(id=6,  user_id=1, noti_type="event",   source_id=1, source_type="event",         event_type="new_event",   target_id=1,  title="루나님의 새 이벤트가 열렸어요",         message="루나 팬미팅 2026",                           is_read=True,  is_pushed=True,  created_at=now - timedelta(days=7)),
            Notification(id=12, user_id=1, noti_type="event",   source_id=2, source_type="event",         event_type="new_event",   target_id=2,  title="하루님의 새 이벤트가 열렸어요",         message="하루 댄스 챌린지",                           is_read=False, is_pushed=True,  created_at=now - timedelta(days=1, hours=3)),
            Notification(id=13, user_id=1, noti_type="event",   source_id=3, source_type="event",         event_type="reminder",    target_id=3,  title="소율 라이브 드로잉이 곧 시작돼요",      message="3일 후 유튜브 라이브에서 만나요!",            is_read=False, is_pushed=True,  created_at=now - timedelta(hours=6)),
            # 주문/배송 알림
            Notification(id=7,  user_id=1, noti_type="order",   source_id=1, source_type="order",         event_type="shipped",     target_id=1,  title="주문하신 상품이 배송 시작되었어요",     message="주문번호 ORD-2026-0001",                     is_read=True,  is_pushed=True,  created_at=now - timedelta(days=4)),
            Notification(id=14, user_id=1, noti_type="order",   source_id=1, source_type="order",         event_type="delivered",   target_id=1,  title="주문하신 상품이 배송 완료되었어요",     message="주문번호 ORD-2026-0001 — 루나 라이트스틱",   is_read=True,  is_pushed=True,  created_at=now - timedelta(days=2)),
            Notification(id=15, user_id=1, noti_type="order",   source_id=3, source_type="order",         event_type="pending",     target_id=3,  title="주문이 접수되었어요",                   message="주문번호 ORD-2026-0003 — 결제 대기 중",      is_read=False, is_pushed=False, created_at=now - timedelta(hours=3)),
            # 채팅 알림
            Notification(id=8,  user_id=1, noti_type="chat",    source_id=2, source_type="chat_message",  event_type="new_message", target_id=1,  title="루나님의 메시지",                       message="이 사진 예쁘네요!",                          is_read=False, is_pushed=True,  created_at=now - timedelta(minutes=30)),
            Notification(id=16, user_id=1, noti_type="chat",    source_id=3, source_type="chat_message",  event_type="new_message", target_id=2,  title="하루님의 메시지",                       message="오늘 연습 끝! 다들 수고했어요",               is_read=False, is_pushed=True,  created_at=now - timedelta(hours=1)),
            # 결제 알림
            Notification(id=17, user_id=1, noti_type="payment", source_id=1, source_type="payment",       event_type="completed",   target_id=1,  title="결제가 완료되었어요",                   message="소율 프리미엄 구독 5,900원 결제 완료",       is_read=True,  is_pushed=True,  created_at=now - timedelta(days=10)),
            Notification(id=18, user_id=1, noti_type="payment", source_id=3, source_type="payment",       event_type="refunded",    target_id=3,  title="환불이 완료되었어요",                   message="25,000원 환불 완료 (하루 연습복 티셔츠)",     is_read=True,  is_pushed=True,  created_at=now - timedelta(days=2)),
            Notification(id=19, user_id=1, noti_type="payment", source_id=3, source_type="subscription",  event_type="expiring",    target_id=3,  title="구독이 곧 만료돼요",                    message="소율 프리미엄 구독이 3일 후 만료됩니다",      is_read=False, is_pushed=True,  created_at=now - timedelta(hours=2)),
            # 공지사항 알림
            Notification(id=20, user_id=1, noti_type="notice",  source_id=1, source_type="notice",        event_type="new_notice",  target_id=1,  title="새 공지사항이 등록되었어요",             message="yourFlace 서비스 오픈 안내",                  is_read=True,  is_pushed=True,  created_at=now - timedelta(days=14)),
            Notification(id=21, user_id=1, noti_type="notice",  source_id=3, source_type="notice",        event_type="new_notice",  target_id=3,  title="새 공지사항이 등록되었어요",             message="앱 업데이트 안내 (v1.1.0)",                   is_read=False, is_pushed=True,  created_at=now - timedelta(days=1)),
            # 시스템 알림
            Notification(id=22, user_id=1, noti_type="system",  source_id=1, source_type="system",        event_type="maintenance", target_id=None, title="시스템 점검 안내",                    message="3월 1일 02:00~06:00 서비스 점검 예정",        is_read=True,  is_pushed=True,  created_at=now - timedelta(days=6)),
            Notification(id=23, user_id=1, noti_type="system",  source_id=2, source_type="system",        event_type="update",      target_id=None, title="개인정보 처리방침 변경 안내",          message="3월 15일부터 변경된 개인정보 처리방침 적용",   is_read=False, is_pushed=True,  created_at=now - timedelta(hours=18)),
            # 경고 알림
            Notification(id=24, user_id=1, noti_type="warning",  source_id=1, source_type="system",       event_type="security",    target_id=None, title="새로운 기기에서 로그인되었어요",       message="iPhone 16 Pro에서 로그인이 감지되었습니다",    is_read=True,  is_pushed=True,  created_at=now - timedelta(days=8)),
            # 콘텐츠 알림 — 아티스트 이미지/영상 추가
            Notification(id=25, subscription_id=1, user_id=1, noti_type="content", source_id=1, source_type="artist_image",  event_type="new_image",   target_id=1,  title="루나님이 새 이미지를 올렸어요",         message="콘서트 무대 비하인드 사진",                   is_read=False, is_pushed=True,  created_at=now - timedelta(hours=4)),
            Notification(id=26, subscription_id=2, user_id=1, noti_type="content", source_id=2, source_type="artist_video",  event_type="new_video",   target_id=3,  title="하루님이 새 영상을 올렸어요",           message="Gravity 안무 풀버전",                        is_read=False, is_pushed=True,  created_at=now - timedelta(hours=8)),
            Notification(id=27, subscription_id=3, user_id=1, noti_type="content", source_id=3, source_type="artist_image",  event_type="new_image",   target_id=5,  title="소율님이 새 이미지를 올렸어요",         message="'도시의 밤' 시리즈 신작 공개",                is_read=False, is_pushed=True,  created_at=now - timedelta(hours=1)),
        ]
        db.add_all(notifications)
        await db.flush()

        notification_settings = [
            NotificationSetting(id=1, subscription_id=1, user_id=1, source_type="artist"),
            NotificationSetting(id=2, subscription_id=2, user_id=1, source_type="artist"),
            NotificationSetting(id=3, subscription_id=3, user_id=1, source_type="artist"),
            NotificationSetting(id=4, user_id=1, source_type="system"),
            NotificationSetting(id=5, user_id=1, source_type="payment", notify_all=True, receive_push=True, receive_email=True),
            NotificationSetting(id=6, user_id=1, source_type="event",   notify_all=True, receive_push=True, receive_email=False),
        ]
        db.add_all(notification_settings)
        await db.flush()

        scheduled_notifications = [
            ScheduledNotification(id=1, notification_template_id=5, receiver_id=1, send_at=now + timedelta(days=1), is_sent=False),
            ScheduledNotification(id=2, notification_template_id=11, receiver_id=1, send_at=now + timedelta(days=3), is_sent=False),
            ScheduledNotification(id=3, notification_template_id=12, receiver_id=1, send_at=now + timedelta(hours=12), is_sent=False),
            ScheduledNotification(id=4, notification_template_id=9,  receiver_id=1, send_at=now - timedelta(hours=6), is_sent=True, sent_at=now - timedelta(hours=6)),
        ]
        db.add_all(scheduled_notifications)
        await db.flush()

        system_logs_data = [
            SystemLog(id=1, scheduled_notification_id=4, sender_id=2, receiver_id=1, channel="push",  status="delivered"),
            SystemLog(id=2, sender_id=3, receiver_id=1, channel="push",  status="delivered"),
            SystemLog(id=3, sender_id=2, receiver_id=1, channel="push",  status="failed", error_message="디바이스 토큰 만료"),
            SystemLog(id=4, sender_id=4, receiver_id=1, channel="app",   status="success"),
            SystemLog(id=5, sender_id=2, receiver_id=1, channel="email", status="success"),
            SystemLog(id=6, sender_id=2, receiver_id=1, channel="email", status="pending"),
        ]
        db.add_all(system_logs_data)
        await db.flush()

        print("  [OK] Notification (templates, notifications, settings, scheduled, system_logs)")

        # ================================================================
        # 11. LIKE — fan_likes / fan_recommendations / celeb_post_likes / celeb_post_recommendations
        # ================================================================
        fan_likes = [
            FanLike(id=1, subscription_id=1, target_type="post",         target_id=1),
            FanLike(id=2, subscription_id=1, target_type="post",         target_id=9),
            FanLike(id=3, subscription_id=2, target_type="post",         target_id=3),
            FanLike(id=4, subscription_id=1, target_type="artist_image", target_id=1),
            FanLike(id=5, subscription_id=2, target_type="artist_image", target_id=3),
            FanLike(id=6, subscription_id=1, target_type="artist_video", target_id=1),
            FanLike(id=7, subscription_id=2, target_type="artist_video", target_id=3),
            FanLike(id=8, subscription_id=3, target_type="post",         target_id=5),
        ]
        db.add_all(fan_likes)
        await db.flush()

        fan_recommendations = [
            FanRecommendation(id=1, subscription_id=1, target_type="post",         target_id=1),
            FanRecommendation(id=2, subscription_id=2, target_type="artist_video", target_id=3),
            FanRecommendation(id=3, subscription_id=3, target_type="post",         target_id=5),
        ]
        db.add_all(fan_recommendations)
        await db.flush()

        celeb_post_likes = [
            CelebPostLike(id=1, celeb_id=1, post_id=6),
            CelebPostLike(id=2, celeb_id=2, post_id=7),
            CelebPostLike(id=3, celeb_id=3, post_id=8),
        ]
        db.add_all(celeb_post_likes)
        await db.flush()

        celeb_post_recommendations = [
            CelebPostRecommendation(id=1, celeb_id=1, post_id=6),
        ]
        db.add_all(celeb_post_recommendations)
        await db.flush()

        print("  [OK] Like (fan_likes, fan_recommendations, celeb_post_likes, celeb_post_recommendations)")

        # ================================================================
        # 12. STATS — celeb_content / celeb_chat / subscriber_content / subscriber_chat
        # ================================================================
        celeb_content_stats = [
            CelebContentStat(id=1,  celeb_id=1,  post_count=4,  image_count=2, video_count=2, fan_like_count=3, fan_recommend_count=1),
            CelebContentStat(id=2,  celeb_id=2,  post_count=3,  image_count=2, video_count=2, fan_like_count=2, fan_recommend_count=1),
            CelebContentStat(id=3,  celeb_id=3,  post_count=2,  image_count=2, video_count=1, fan_like_count=1, fan_recommend_count=1),
            CelebContentStat(id=4,  celeb_id=4,  post_count=0,  image_count=0, video_count=0, fan_like_count=0, fan_recommend_count=0),
            CelebContentStat(id=5,  celeb_id=5,  post_count=0,  image_count=0, video_count=0, fan_like_count=0, fan_recommend_count=0),
            CelebContentStat(id=6,  celeb_id=6,  post_count=0,  image_count=0, video_count=0, fan_like_count=0, fan_recommend_count=0),
            CelebContentStat(id=7,  celeb_id=7,  post_count=2,  image_count=0, video_count=0, fan_like_count=4, fan_recommend_count=2),
            CelebContentStat(id=8,  celeb_id=8,  post_count=2,  image_count=0, video_count=0, fan_like_count=8, fan_recommend_count=3),
            CelebContentStat(id=9,  celeb_id=9,  post_count=2,  image_count=0, video_count=0, fan_like_count=5, fan_recommend_count=2),
            CelebContentStat(id=10, celeb_id=10, post_count=2,  image_count=0, video_count=0, fan_like_count=6, fan_recommend_count=2),
            CelebContentStat(id=11, celeb_id=11, post_count=2,  image_count=0, video_count=0, fan_like_count=9, fan_recommend_count=4),
            CelebContentStat(id=12, celeb_id=12, post_count=2,  image_count=0, video_count=0, fan_like_count=7, fan_recommend_count=3),
        ]
        db.add_all(celeb_content_stats)
        await db.flush()

        celeb_chat_stats = [
            CelebChatStat(id=1, celeb_id=1, chat_subscriber_count=1, chat_image_count=0, chat_video_count=0, chat_attendance_days=5),
            CelebChatStat(id=2, celeb_id=2, chat_subscriber_count=1, chat_image_count=0, chat_video_count=1, chat_attendance_days=3),
            CelebChatStat(id=3, celeb_id=3, chat_subscriber_count=1, chat_image_count=0, chat_video_count=0, chat_attendance_days=2),
        ]
        db.add_all(celeb_chat_stats)
        await db.flush()

        subscriber_content_stats = [
            SubscriberContentStat(id=1,  subscription_id=1,  post_count=2, image_count=0, fan_like_count=3, fan_recommend_count=1),
            SubscriberContentStat(id=2,  subscription_id=2,  post_count=1, image_count=0, fan_like_count=2, fan_recommend_count=1),
            SubscriberContentStat(id=3,  subscription_id=3,  post_count=1, image_count=0, fan_like_count=1, fan_recommend_count=1),
            SubscriberContentStat(id=7,  subscription_id=7,  post_count=1, image_count=0, fan_like_count=2, fan_recommend_count=1),
            SubscriberContentStat(id=8,  subscription_id=8,  post_count=1, image_count=0, fan_like_count=3, fan_recommend_count=1),
            SubscriberContentStat(id=9,  subscription_id=9,  post_count=1, image_count=0, fan_like_count=2, fan_recommend_count=1),
            SubscriberContentStat(id=10, subscription_id=10, post_count=1, image_count=0, fan_like_count=2, fan_recommend_count=1),
            SubscriberContentStat(id=11, subscription_id=11, post_count=1, image_count=0, fan_like_count=3, fan_recommend_count=2),
            SubscriberContentStat(id=12, subscription_id=12, post_count=1, image_count=0, fan_like_count=2, fan_recommend_count=1),
        ]
        db.add_all(subscriber_content_stats)
        await db.flush()

        subscriber_chat_stats = [
            SubscriberChatStat(id=1,  subscription_id=1,  messages_sent=3, chat_active_days=5),
            SubscriberChatStat(id=2,  subscription_id=2,  messages_sent=1, chat_active_days=2),
            SubscriberChatStat(id=3,  subscription_id=3,  messages_sent=1, chat_active_days=1),
            SubscriberChatStat(id=7,  subscription_id=7,  messages_sent=2, chat_active_days=3),
            SubscriberChatStat(id=8,  subscription_id=8,  messages_sent=2, chat_active_days=4),
            SubscriberChatStat(id=12, subscription_id=12, messages_sent=2, chat_active_days=2),
        ]
        db.add_all(subscriber_chat_stats)
        await db.flush()

        print("  [OK] Stats (celeb_content, celeb_chat, subscriber_content, subscriber_chat)")

        # ================================================================
        # 13. MODERATION — moderation_models / content_moderation
        # ================================================================
        moderation_models_data = [
            ModerationModel(id=1, model_name="text-safety-v1",  description="텍스트 안전성 검사 모델",  is_active=True),
            ModerationModel(id=2, model_name="image-safety-v1", description="이미지 안전성 검사 모델",  is_active=True),
        ]
        db.add_all(moderation_models_data)
        await db.flush()

        content_moderations = [
            ContentModeration(id=1, content_type="post",    content_id=1, celeb_ref_type="artist", celeb_ref_id=1, model_id=1, result={"score": 0.02, "category": "safe"},       is_flagged=False, reviewed=True, reviewed_by=8),
            ContentModeration(id=2, content_type="comment", content_id=1, celeb_ref_type="fan",    celeb_ref_id=1, model_id=1, result={"score": 0.01, "category": "safe"},       is_flagged=False, reviewed=False),
            ContentModeration(id=3, content_type="image",   content_id=1, celeb_ref_type="artist", celeb_ref_id=1, model_id=2, result={"score": 0.05, "category": "safe"},       is_flagged=False, reviewed=False),
        ]
        db.add_all(content_moderations)
        await db.flush()

        print("  [OK] Moderation (moderation_models, content_moderation)")

        # ================================================================
        # 14. ADMIN — faq / banners / system_messages / notices / error_logs
        # ================================================================
        faqs = [
            FAQ(id=1, category="계정",   question="비밀번호를 잊어버렸어요. 어떻게 해야 하나요?",         answer="로그인 화면에서 '비밀번호 찾기'를 클릭하고 가입한 이메일을 입력하시면 재설정 링크가 발송됩니다.", priority=1, is_active=True, write_id=8),
            FAQ(id=2, category="계정",   question="회원 탈퇴는 어떻게 하나요?",                           answer="설정 > 계정 관리 > 회원 탈퇴에서 진행할 수 있습니다. 탈퇴 후 30일간 데이터가 보관됩니다.",     priority=2, is_active=True, write_id=8),
            FAQ(id=3, category="구독",   question="구독은 어떻게 하나요?",                                 answer="크리에이터 프로필 페이지에서 '구독하기' 버튼을 클릭하면 됩니다. 무료/유료 플랜을 선택할 수 있습니다.", priority=1, is_active=True, write_id=8),
            FAQ(id=4, category="구독",   question="구독을 취소하면 환불이 되나요?",                        answer="유료 구독의 경우, 남은 기간에 대해 일할 계산으로 환불이 가능합니다.",                           priority=2, is_active=True, write_id=8),
            FAQ(id=5, category="결제",   question="어떤 결제 수단을 사용할 수 있나요?",                    answer="신용/체크카드, 카카오페이, 토스페이를 지원합니다.",                                             priority=1, is_active=True, write_id=8),
            FAQ(id=6, category="쇼핑",   question="배송은 얼마나 걸리나요?",                               answer="결제 완료 후 2~5 영업일 이내에 배송됩니다. 제주/도서산간 지역은 추가 1~2일이 소요될 수 있습니다.", priority=1, is_active=True, write_id=8),
            FAQ(id=7, category="채팅",   question="채팅방에서 사진/영상을 보낼 수 있나요?",                answer="네, 채팅방 하단의 첨부 버튼을 통해 이미지와 동영상을 전송할 수 있습니다.",                      priority=1, is_active=True, write_id=8),
        ]
        db.add_all(faqs)
        await db.flush()

        banners = [
            Banner(id=1, position="main_top",    title="루나 첫 단독 콘서트", image_url="/placeholder/banner1.jpg", link_url="/events/4", priority=1, start_at=now - timedelta(days=7), end_at=now + timedelta(days=30), is_active=True, write_id=8),
            Banner(id=2, position="main_top",    title="소율 개인전 안내",     image_url="/placeholder/banner2.jpg", link_url="/events/3", priority=2, start_at=now,                     end_at=now + timedelta(days=60), is_active=True, write_id=8),
            Banner(id=3, position="main_bottom", title="신규 가입 이벤트",     image_url="/placeholder/banner1.jpg", link_url="/events",   priority=1, start_at=now - timedelta(days=30), end_at=now + timedelta(days=90), is_active=True, write_id=8),
        ]
        db.add_all(banners)
        await db.flush()

        system_messages_data = [
            SystemMessage(id=1, title="서비스 점검 안내",       message="2026년 3월 1일 02:00~06:00 서비스 점검이 예정되어 있습니다.",                  target_type="all", start_at=now, end_at=now + timedelta(days=15), is_active=True, write_id=8),
            SystemMessage(id=2, title="개인정보 처리방침 변경", message="2026년 3월 15일부터 변경된 개인정보 처리방침이 적용됩니다. 자세한 내용은 공지사항을 확인해주세요.", target_type="all", start_at=now, end_at=now + timedelta(days=30), is_active=True, write_id=8),
        ]
        db.add_all(system_messages_data)
        await db.flush()

        notices = [
            Notice(id=1, title="yourFlace 서비스 오픈 안내",        message="yourFlace가 정식 오픈했습니다! 시인, 유튜버, 작가, 사진작가 등 다양한 크리에이터를 만나보세요.",   write_id=8, write_role="admin", target_type="all", is_active=True),
            Notice(id=2, title="신규 크리에이터 합류 안내",          message="시인 김지수, 유튜버 박민지, 소설가 이승우 등 6명의 신규 크리에이터가 yourFlace에 합류했습니다!",      write_id=8, write_role="admin", target_type="all", is_active=True),
            Notice(id=3, title="앱 업데이트 안내 (v1.1.0)",          message="채팅 기능이 개선되고 다크모드가 추가되었습니다. 업데이트 후 이용해주세요.",                        write_id=8, write_role="admin", target_type="all", is_active=True),
        ]
        db.add_all(notices)
        await db.flush()

        error_logs = [
            ErrorLog(id=1, error_type="PaymentGatewayError",  message="Toss 결제 게이트웨이 타임아웃",     severity="warning", source_module="payment.payments",  user_id=1, resolved=True, resolved_at=now - timedelta(days=1)),
            ErrorLog(id=2, error_type="StorageUploadError",   message="R2 업로드 실패: 파일 크기 초과",    severity="error",   source_module="core.storage",      user_id=2, resolved=False),
        ]
        db.add_all(error_logs)
        await db.flush()

        print("  [OK] Admin (faq, banners, system_messages, notices, error_logs)")

        # ================================================================
        # 15. MAGAZINE — magazines
        # ================================================================
        magazines = [
            Magazine(id=1, title="루나, 첫 단독 콘서트 2만 관객 매진 성공",            slug=generate_slug("루나 첫 단독 콘서트 2만 관객 매진 성공"), content="지난 금요일 잠실 올림픽경기장에서 열린 루나의 첫 번째 단독 콘서트 '별빛 아래서'가 2만 관객을 가득 채우며 성공적으로 막을 내렸습니다. 데뷔 3년 만에 이룬 단독 콘서트는 루나의 성장을 보여주는 무대였습니다.", summary="루나의 첫 단독 콘서트가 2만 석 매진을 기록하며 성황리에 마무리되었습니다.", thumbnail_url="/placeholder/concert1.jpg", category="공연",      celeb_id=1, write_id=8, tags=["콘서트", "루나", "매진"], is_active=True, view_count=1520),
            Magazine(id=2, title="하루, 세계 댄스 대회 금상 수상 쾌거",               slug=generate_slug("하루 세계 댄스 대회 금상 수상 쾌거"), content="하루가 세계적인 댄스 대회 'World Dance Championship 2026'에서 현대무용 부문 금상을 수상했습니다. 한국 댄서 최초로 해당 부문에서 금상을 차지하며 큰 주목을 받고 있습니다.", summary="하루가 WDC 2026 현대무용 부문 금상을 수상했습니다.", thumbnail_url="/placeholder/dance1.jpg", category="수상",      celeb_id=2, write_id=8, tags=["하루", "수상", "댄스대회"], is_active=True, view_count=980),
            Magazine(id=3, title="소율, 첫 개인전 '꿈의 색채' 3월 개최",              slug=generate_slug("소율 첫 개인전 꿈의 색채 3월 개최"), content="일러스트레이터 소율의 첫 개인전 '꿈의 색채'가 서울 성수동 갤러리에서 오는 3월 1일부터 31일까지 한 달간 개최됩니다. 이번 전시에서는 '도시의 밤' 시리즈를 포함한 30여 점의 신작이 공개될 예정입니다.", summary="소율 작가의 첫 개인전이 성수동 갤러리에서 열립니다.", thumbnail_url="/placeholder/art1.jpg", category="전시",      celeb_id=3, write_id=8, tags=["소율", "개인전", "갤러리"], is_active=True, view_count=650),
            Magazine(id=4, title="yourFlace, 셀럽과 팬을 잇는 새로운 플랫폼 정식 오픈", slug=generate_slug("yourflace 셀럽과 팬을 잇는 새로운 플랫폼 정식 오픈"), content="팬과 셀럽을 더 가깝게 연결하는 플랫폼 yourFlace가 정식 오픈했습니다. 가수, 댄서, 시인, 유튜버, 작가, 사진작가 등 다양한 분야의 셀럽들이 함께합니다. 구독 기반의 독점 콘텐츠, 실시간 채팅, 굿즈 쇼핑 등 다양한 기능을 통해 팬과 셀럽 간의 소통을 지원합니다.", summary="yourFlace 플랫폼이 정식 오픈했습니다. 다양한 분야의 셀럽을 만나보세요.", thumbnail_url="/placeholder/banner1.jpg", category="플랫폼",    celeb_id=None, write_id=8, tags=["yourFlace", "오픈", "플랫폼", "셀럽"], is_active=True, view_count=2100),
            Magazine(id=5, title="제이, 새 믹스테이프 '야간비행' 발매 예고",            slug=generate_slug("제이 새 믹스테이프 야간비행 발매 예고"), content="래퍼 제이가 새 믹스테이프 '야간비행'의 발매를 예고했습니다. 총 8트랙으로 구성되며 다양한 프로듀서와의 협업이 포함되어 있어 팬들의 기대를 모으고 있습니다.", summary="제이의 새 믹스테이프 '야간비행'이 곧 발매됩니다.", thumbnail_url="/placeholder/concert2.jpg", category="음악",      celeb_id=5, write_id=8, tags=["제이", "믹스테이프", "신보"], is_active=True, view_count=430),
            Magazine(
                id=6,
                title="루나의 콘서트 비하인드 — 무대 뒤 24시간",
                slug=generate_slug("루나의 콘서트 비하인드 무대 뒤 24시간"),
                content="""<style>
.highlight-box { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; padding: 20px; border-radius: 12px; margin: 20px 0; font-size: 18px; line-height: 1.6; }
.photo-caption { text-align: center; color: #888; font-size: 13px; margin-top: 6px; font-style: italic; }
.quote-block { border-left: 4px solid #764ba2; padding: 12px 20px; margin: 24px 0; background: #f8f6ff; font-size: 16px; color: #333; }
.section-title { font-size: 22px; font-weight: 700; margin: 32px 0 12px; color: #1a1a1a; }
</style>

<div class="highlight-box">
2만 관객의 함성 뒤에는 루나와 스태프들의 치열한 24시간이 있었습니다.
</div>

<p class="section-title">리허설 — 완벽을 향한 집념</p>
<p>콘서트 당일 오전 8시, 루나는 이미 잠실 올림픽경기장에 도착해 있었습니다. 총 18곡의 셋리스트를 처음부터 끝까지 두 번 반복하며, 동선 하나하나를 점검했습니다.</p>

<img src="/placeholder/concert1.jpg" alt="리허설 현장" style="width:100%; border-radius:8px; margin:16px 0;" />
<p class="photo-caption">오전 리허설 중인 루나 — 스태프 촬영</p>

<div class="quote-block">
"무대에 서면 떨림이 사라져요. 연습한 만큼 몸이 기억하니까요." — 루나
</div>

<p class="section-title">백스테이지 — 팬에게 보내는 손편지</p>
<p>공연 시작 2시간 전, 루나는 대기실에서 팬들에게 보낼 손편지를 쓰고 있었습니다. 한 장 한 장 정성스럽게 적은 편지는 객석 랜덤 좌석에 놓였습니다.</p>

<img src="/placeholder/concert2.jpg" alt="백스테이지" style="width:100%; border-radius:8px; margin:16px 0;" />
<p class="photo-caption">백스테이지에서 준비 중인 모습</p>

<p class="section-title">앙코르 — 눈물의 무대</p>
<p>마지막 곡 '별빛 아래서'가 끝난 뒤, 2만 관객이 일제히 외친 앙코르 함성에 루나는 눈물을 참지 못했습니다. 예정에 없던 어쿠스틱 버전의 데뷔곡을 부르며, 팬과 아티스트가 하나 되는 순간이 만들어졌습니다.</p>

<div class="highlight-box" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); text-align:center;">
"여러분이 있어 제가 여기 설 수 있어요. 고마워요, 사랑해요." — 루나
</div>""",
                summary="루나 첫 단독 콘서트의 비하인드 스토리를 공개합니다.",
                thumbnail_url="/placeholder/concert1.jpg",
                category="비하인드",
                celeb_id=1,
                write_id=8,
                tags=["루나", "비하인드", "콘서트", "HTML테스트"],
                is_active=True,
                view_count=320,
            ),
        ]
        db.add_all(magazines)
        await db.flush()

        magazine_images = [
            MagazineImage(id=1, magazine_id=1, image_id=1,  sort_order=0),
            MagazineImage(id=2, magazine_id=1, image_id=2,  sort_order=1),
            MagazineImage(id=3, magazine_id=2, image_id=3,  sort_order=0),
            MagazineImage(id=4, magazine_id=2, image_id=4,  sort_order=1),
            MagazineImage(id=5, magazine_id=3, image_id=5,  sort_order=0),
            MagazineImage(id=6, magazine_id=3, image_id=6,  sort_order=1),
            MagazineImage(id=7, magazine_id=4, image_id=10, sort_order=0),
            MagazineImage(id=8, magazine_id=4, image_id=11, sort_order=1),
            MagazineImage(id=9, magazine_id=5, image_id=1,  sort_order=0),
            MagazineImage(id=10, magazine_id=6, image_id=1, sort_order=0),
            MagazineImage(id=11, magazine_id=6, image_id=2, sort_order=1),
        ]
        db.add_all(magazine_images)
        await db.flush()

        print("  [OK] Magazine (magazines, magazine_images)")

        # ================================================================
        # COMMIT
        # ================================================================
        await db.commit()
        print()
        print("=" * 55)
        print("  시드 데이터 삽입 완료!")
        print("=" * 55)
        print()
        print("  팬 계정(전체 구독): fan@test.com / test1234")
        print("  팬 계정(구독 없음): guest@test.com / test1234")
        print("  관리자 계정:        admin@test.com / test1234")
        print()
        print("  Users          15명 (팬2 + 셀럽12 + 관리자1)")
        print("  Celebs         12명 (루나, 하루, 소율, 민서, 제이, 유리 + 시인, 유튜버, 소설가, 사진작가, 웹툰작가, 요리연구가)")
        print("  Categories     10개 (가수, 댄서, 일러스트레이터, 배우 + 시인, 유튜버, 소설가, 사진작가, 웹툰작가, 요리연구가)")
        print("  Subscriptions  12건 (fan@test.com → 전체 셀럽 구독)")
        print("  Sub Plans      24건 (셀럽별 베이직+프리미엄)")
        print("  Posts          23건 (셀럽11 + 팬3 + 기사3 + 신규6×2)")
        print("  Images         12건 / Celeb Images 6건 / Videos 5건")
        print("  Chat Rooms      6개 / Messages 19건")
        print("  Events          8건 (활성6 + 완료1 + 마감1)")
        print("  Products       12건 / Orders 3건")
        print("  Payments        3건 / Refunds 1건")
        print("  Notifications  27건 / Templates 14건")
        print("  Fan Likes       8건 / Recommendations 3건")
        print("  FAQ             7건 / Banners 3건 / Notices 3건")
        print("  Moderation      2 models / 3 results")
        print("  Magazines       6건 (HTML 콘텐츠 포함 1건)")
        print("  + settings, addresses, devices, stats, logs 등")


async def reset_sequences():
    """auto-increment 시퀀스를 시드 데이터 이후부터 시작하도록 리셋"""
    async with AsyncSessionLocal() as db:
        tables = [
            ("users", 30), ("profile", 30), ("user_settings", 30),
            ("user_addresses", 10), ("user_devices", 10), ("login_logs", 10),
            ("celeb_categories", 20), ("celebs", 20),
            ("celeb_category_map", 20), ("celeb_social_links", 30),
            ("managers", 10),
            ("subscription_plans", 30), ("subscriptions", 20),
            ("subscription_cancellations", 10),
            ("images", 20), ("posts", 30), ("post_images", 10),
            ("post_comments", 10), ("post_stats", 30),
            ("celeb_images", 10), ("celeb_image_comments", 10), ("celeb_image_stats", 10),
            ("celeb_videos", 10), ("celeb_video_comments", 10), ("celeb_video_stats", 10),
            ("chat_rooms", 10), ("chat_messages", 30),
            ("chat_images", 10), ("chat_videos", 10),
            ("chat_read_receipts", 10), ("chat_pins", 10), ("chat_reports", 10),
            ("calendar_searches", 10), ("saved_search_filters", 10),
            ("payment_methods", 10), ("payments", 10), ("payment_refunds", 10),
            ("events", 20), ("event_participants", 10), ("event_attendance", 10),
            ("products", 20), ("product_images", 20),
            ("orders", 10), ("order_items", 10),
            ("notification_templates", 20), ("notifications", 30),
            ("notification_settings", 10), ("scheduled_notifications", 10),
            ("system_logs", 10),
            ("fan_likes", 20), ("fan_recommendations", 10),
            ("celeb_post_likes", 10), ("celeb_post_recommendations", 10),
            ("celeb_content_stats", 20), ("celeb_chat_stats", 10),
            ("subscriber_content_stats", 20), ("subscriber_chat_stats", 20),
            ("moderation_models", 10), ("content_moderation", 10),
            ("faq", 10), ("banners", 10), ("system_messages", 10),
            ("notices", 10), ("error_logs", 10),
            ("magazines", 10), ("magazine_images", 20),
        ]
        for table, next_val in tables:
            try:
                await db.execute(text(
                    f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), {next_val}, false)"
                ))
            except Exception:
                pass
        await db.commit()
    print("[OK] 시퀀스 리셋 완료")


# ============================================================
#  CLI
# ============================================================

async def main():
    import argparse
    parser = argparse.ArgumentParser(description="yourFlace DB 초기화 + 시드 데이터")
    parser.add_argument("--reset", action="store_true", help="테이블 전체 리셋 후 삽입")
    args = parser.parse_args()

    print()
    print("=" * 55)
    print("  yourFlace DB Init + Seed")
    print("=" * 55)
    print()

    if args.reset:
        confirm = input("모든 테이블과 데이터가 삭제됩니다. 계속? (yes/no): ")
        if confirm.strip().lower() != "yes":
            print("[취소]")
            return

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        print("[OK] 모든 테이블 삭제")

    # 테이블 생성 (이미 존재하는 테이블은 스킵)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    table_count = len(Base.metadata.tables)
    print(f"[OK] 테이블 {table_count}개 확인/생성")
    print()

    print("[시드 데이터 삽입 중...]")
    await seed_data()
    await reset_sequences()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
