"""
모든 테이블에 시드 데이터를 삽입하는 스크립트
사용법 (프로젝트 루트에서):
  python -m backend.scripts.seed          # 시드 데이터만 삽입
  python -m backend.scripts.seed --reset  # 테이블 리셋 후 삽입
"""
import sys
import asyncio
from pathlib import Path
from datetime import date, datetime, timedelta
from decimal import Decimal

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from sqlalchemy import text
from app.database import engine, Base, AsyncSessionLocal
from app.core.security import get_password_hash

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

# Artist
from app.artist.artists.models import Artist
from app.artist.artist_categories.models import ArtistCategory
from app.artist.artist_category_map.models import ArtistCategoryMap
from app.artist.artist_social_links.models import ArtistSocialLink
from app.artist.managers.models import Manager

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
from app.content.artist_images.models import ArtistImage
from app.content.artist_image_comments.models import ArtistImageComment
from app.content.artist_image_stats.models import ArtistImageStat
from app.content.artist_videos.models import ArtistVideo
from app.content.artist_video_comments.models import ArtistVideoComment
from app.content.artist_video_stats.models import ArtistVideoStat

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
from app.like.artist_post_likes.models import ArtistPostLike
from app.like.artist_post_recommendations.models import ArtistPostRecommendation

# Stats
from app.stats.artist_content_stats.models import ArtistContentStat
from app.stats.artist_chat_stats.models import ArtistChatStat
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
            User(id=1, email="fan@test.com",      password_hash=pw, status="active"),
            User(id=2, email="luna@artist.com",    password_hash=pw, status="active"),
            User(id=3, email="haru@artist.com",    password_hash=pw, status="active"),
            User(id=4, email="soyul@artist.com",   password_hash=pw, status="active"),
            User(id=5, email="minseo@artist.com",  password_hash=pw, status="active"),
            User(id=6, email="jay@artist.com",     password_hash=pw, status="active"),
            User(id=7, email="yuri@artist.com",    password_hash=pw, status="active"),
            User(id=8, email="admin@test.com",     password_hash=pw, status="active"),
        ]
        db.add_all(users)
        await db.flush()

        profiles = [
            Profile(id=1, user_id=1, nickname="테스트팬", full_name="김팬", birth_date=date(2000, 5, 15), gender="male", phone="010-1234-5678"),
            Profile(id=2, user_id=2, nickname="루나",     full_name="박루나"),
            Profile(id=3, user_id=3, nickname="하루",     full_name="이하루"),
            Profile(id=4, user_id=4, nickname="소율",     full_name="최소율"),
            Profile(id=5, user_id=5, nickname="민서",     full_name="정민서"),
            Profile(id=6, user_id=6, nickname="제이",     full_name="한제이"),
            Profile(id=7, user_id=7, nickname="유리",     full_name="송유리"),
            Profile(id=8, user_id=8, nickname="관리자",   full_name="운영자"),
        ]
        db.add_all(profiles)
        await db.flush()

        user_settings = [
            UserSetting(id=i, user_id=i, language="ko", theme="light")
            for i in range(1, 9)
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
        # 2. ARTIST — artists / categories / category_map / social_links / managers
        # ================================================================
        categories = [
            ArtistCategory(id=1, name="가수"),
            ArtistCategory(id=2, name="댄서"),
            ArtistCategory(id=3, name="일러스트레이터"),
            ArtistCategory(id=4, name="배우"),
        ]
        db.add_all(categories)
        await db.flush()

        artists = [
            Artist(id=1, user_id=2, stage_name="루나", notes="음악으로 세상을 밝히는 아티스트", status="active"),
            Artist(id=2, user_id=3, stage_name="하루", notes="춤으로 하루를 채우는 댄서",       status="active"),
            Artist(id=3, user_id=4, stage_name="소율", notes="그림으로 이야기를 전하는 일러스트레이터", status="active"),
            Artist(id=4, user_id=5, stage_name="민서", notes="연기로 감동을 주는 배우",         status="active"),
            Artist(id=5, user_id=6, stage_name="제이", notes="힙합으로 세상을 흔드는 래퍼",     status="active"),
            Artist(id=6, user_id=7, stage_name="유리", notes="현대무용의 새로운 지평을 여는 댄서", status="active"),
        ]
        db.add_all(artists)
        await db.flush()

        category_maps = [
            ArtistCategoryMap(artist_id=1, category_id=1),
            ArtistCategoryMap(artist_id=2, category_id=2),
            ArtistCategoryMap(artist_id=3, category_id=3),
            ArtistCategoryMap(artist_id=4, category_id=4),
            ArtistCategoryMap(artist_id=5, category_id=1),
            ArtistCategoryMap(artist_id=6, category_id=2),
        ]
        db.add_all(category_maps)
        await db.flush()

        social_links = [
            ArtistSocialLink(artist_id=1, platform_name="YouTube",   url="https://youtube.com/@luna",    display_name="루나 뮤직",      follower_count=12000, priority=1),
            ArtistSocialLink(artist_id=1, platform_name="Instagram", url="https://instagram.com/luna",   display_name="@luna_music",    follower_count=8500,  priority=2),
            ArtistSocialLink(artist_id=2, platform_name="YouTube",   url="https://youtube.com/@haru",    display_name="하루 댄스",      follower_count=9500,  priority=1),
            ArtistSocialLink(artist_id=2, platform_name="TikTok",    url="https://tiktok.com/@haru",     display_name="@haru_dance",    follower_count=23000, priority=2),
            ArtistSocialLink(artist_id=3, platform_name="Instagram", url="https://instagram.com/soyul",  display_name="@soyul_art",     follower_count=15000, priority=1),
            ArtistSocialLink(artist_id=4, platform_name="YouTube",   url="https://youtube.com/@minseo",  display_name="민서 채널",      follower_count=6000,  priority=1),
            ArtistSocialLink(artist_id=5, platform_name="SoundCloud", url="https://soundcloud.com/jay",  display_name="JAY beats",      follower_count=4500,  priority=1),
            ArtistSocialLink(artist_id=6, platform_name="YouTube",   url="https://youtube.com/@yuri",    display_name="유리 댄스",      follower_count=7200,  priority=1),
        ]
        db.add_all(social_links)
        await db.flush()

        managers = [
            Manager(id=1, user_id=8, artist_id=1, role="manager", status="active"),
        ]
        db.add_all(managers)
        await db.flush()

        print("  [OK] Artist (artists, categories, category_map, social_links, managers)")

        # ================================================================
        # 3. SUBSCRIPTION — subscriptions / subscription_plans / subscription_cancellations
        # ================================================================
        subscription_plans = [
            SubscriptionPlan(id=1, artist_id=1, name="루나 베이직",   price=Decimal("0"),     billing_cycle="monthly", benefits="기본 콘텐츠 열람", is_active=True),
            SubscriptionPlan(id=2, artist_id=1, name="루나 프리미엄", price=Decimal("9900"),   billing_cycle="monthly", duration_days=30, benefits="전체 콘텐츠 + 비하인드 + 채팅", is_active=True),
            SubscriptionPlan(id=3, artist_id=2, name="하루 베이직",   price=Decimal("0"),     billing_cycle="monthly", benefits="기본 콘텐츠 열람", is_active=True),
            SubscriptionPlan(id=4, artist_id=2, name="하루 프리미엄", price=Decimal("7900"),   billing_cycle="monthly", duration_days=30, benefits="전체 콘텐츠 + 연습 영상", is_active=True),
            SubscriptionPlan(id=5, artist_id=3, name="소율 베이직",   price=Decimal("0"),     billing_cycle="monthly", benefits="공개 작품 열람", is_active=True),
            SubscriptionPlan(id=6, artist_id=3, name="소율 프리미엄", price=Decimal("5900"),   billing_cycle="monthly", duration_days=30, benefits="전체 작품 + 작업과정 + 채팅", is_active=True),
        ]
        db.add_all(subscription_plans)
        await db.flush()

        subscriptions = [
            Subscription(id=1, fan_id=1, artist_id=1, fan_nickname="테스트팬", status="subscribed", payments_type="free", start_date=today - timedelta(days=30)),
            Subscription(id=2, fan_id=1, artist_id=2, fan_nickname="테스트팬", status="subscribed", payments_type="free", start_date=today - timedelta(days=20)),
            Subscription(id=3, fan_id=1, artist_id=3, fan_nickname="테스트팬", status="subscribed", payments_type="paid", start_date=today - timedelta(days=10)),
            Subscription(id=4, fan_id=1, artist_id=4, fan_nickname="테스트팬", status="cancelled", payments_type="free", start_date=today - timedelta(days=60), end_date=today - timedelta(days=5)),
        ]
        db.add_all(subscriptions)
        await db.flush()

        subscription_cancellations = [
            SubscriptionCancellation(id=1, subscription_id=4, user_id=1, artist_id=4, reason_code="lost_interest", reason_detail="콘텐츠가 자주 올라오지 않아서", subscription_started_at=now - timedelta(days=60)),
        ]
        db.add_all(subscription_cancellations)
        await db.flush()

        print("  [OK] Subscription (subscriptions, plans, cancellations)")

        # ================================================================
        # 4. CONTENT — images / posts / post_images / post_comments / post_stats
        #              artist_images / artist_image_comments / artist_image_stats
        #              artist_videos / artist_video_comments / artist_video_stats
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
            # 아티스트 포스트 (id 1~5)
            Post(id=1,  author_id=1, author_type="artist", content="오늘 새 앨범 작업을 시작했어요! 기대해주세요",                              write_id=2, write_role="artist", visibility="public",      is_artist_post=True,  tags=["음악", "앨범"]),
            Post(id=2,  author_id=1, author_type="artist", content="구독자 여러분만을 위한 비하인드 영상 곧 올라갑니다!",                       write_id=2, write_role="artist", visibility="subscribers", is_artist_post=True,  tags=["비하인드"]),
            Post(id=3,  author_id=2, author_type="artist", content="새로운 안무 연습 중! 이번 주 라이브에서 공개할게요",                        write_id=3, write_role="artist", visibility="public",      is_artist_post=True,  tags=["댄스", "안무"]),
            Post(id=4,  author_id=2, author_type="artist", content="연습실에서 하루종일 땀 흘리는 중... 화이팅!",                               write_id=3, write_role="artist", visibility="subscribers", is_artist_post=True,  tags=["일상", "연습"]),
            Post(id=5,  author_id=3, author_type="artist", content="새로운 일러스트 시리즈 '도시의 밤' 첫 번째 작품을 공개합니다.",             write_id=4, write_role="artist", visibility="public",      is_artist_post=True,  tags=["일러스트", "아트"]),
            # 팬 포스트 (id 6~8)
            Post(id=6,  author_id=1, author_type="fan",    content="루나 노래 진짜 좋아요!! 다음 앨범 기대됩니다",                              write_id=1, write_role="fan",    visibility="public",      is_artist_post=False, tags=["팬레터"]),
            Post(id=7,  author_id=2, author_type="fan",    content="하루님 안무 진짜 대박... 라이브 꼭 볼게요!",                                write_id=1, write_role="fan",    visibility="public",      is_artist_post=False, tags=["응원"]),
            Post(id=8,  author_id=3, author_type="fan",    content="소율 작가님 그림 너무 예뻐요. 굿즈 나오면 바로 구매할게요!",                write_id=1, write_role="fan",    visibility="public",      is_artist_post=False, tags=["팬아트"]),
            # 기사형 포스트 (id 9~11)
            Post(id=9,  author_id=1, author_type="artist", content="지난 금요일 잠실 올림픽경기장에서 열린 루나의 첫 번째 단독 콘서트가 2만 관객을 가득 채우며 성공적으로 막을 내렸습니다.", write_id=2, write_role="artist", visibility="public", is_artist_post=True, tags=["콘서트", "공연"], title_field="루나, 첫 단독 콘서트 2만 관객 매진"),
            Post(id=10, author_id=2, author_type="artist", content="하루가 세계적인 댄스 대회 'World Dance Championship 2026'에서 현대무용 부문 금상을 수상했습니다.", write_id=3, write_role="artist", visibility="public", is_artist_post=True, tags=["수상", "대회"], title_field="하루, 세계 댄스 대회 금상 수상"),
            Post(id=11, author_id=3, author_type="artist", content="소율 작가의 첫 개인전 '꿈의 색채'가 서울 성수동 갤러리에서 오는 3월 1일부터 31일까지 한 달간 개최됩니다.", write_id=4, write_role="artist", visibility="public", is_artist_post=True, tags=["전시", "갤러리"], title_field="소율, 첫 개인전 '꿈의 색채' 개최"),
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
            PostStat(id=i, post_id=i, view_count=(12 - i) * 50, comment_count=2 if i <= 3 else 1, fan_like_count=(12 - i) * 3, artist_like_count=1 if i >= 6 else 0)
            for i in range(1, 12)
        ]
        db.add_all(post_stats)
        await db.flush()

        # Artist Images
        artist_images = [
            ArtistImage(id=1, artist_id=1, image_id=1, write_id=2, write_role="artist", image_purpose="concert",     tags=["콘서트", "무대"],   visibility="public"),
            ArtistImage(id=2, artist_id=1, image_id=2, write_id=2, write_role="artist", image_purpose="behind",      tags=["비하인드"],         visibility="subscribers"),
            ArtistImage(id=3, artist_id=2, image_id=3, write_id=3, write_role="artist", image_purpose="performance", tags=["댄스", "공연"],     visibility="public"),
            ArtistImage(id=4, artist_id=2, image_id=4, write_id=3, write_role="artist", image_purpose="practice",    tags=["연습"],             visibility="subscribers"),
            ArtistImage(id=5, artist_id=3, image_id=5, write_id=4, write_role="artist", image_purpose="artwork",     tags=["일러스트", "작품"], visibility="public"),
            ArtistImage(id=6, artist_id=3, image_id=6, write_id=4, write_role="artist", image_purpose="process",     tags=["작업과정"],         visibility="public"),
        ]
        db.add_all(artist_images)
        await db.flush()

        artist_image_comments = [
            ArtistImageComment(id=1, artist_image_id=1, user_id=1, content="무대 사진 너무 멋져요!",    commenter_role="fan",    status="active"),
            ArtistImageComment(id=2, artist_image_id=1, user_id=2, content="고마워요!",                 commenter_role="artist", status="active", parent_comment_id=1),
            ArtistImageComment(id=3, artist_image_id=3, user_id=1, content="공연 사진 대박이네요",       commenter_role="fan",    status="active"),
            ArtistImageComment(id=4, artist_image_id=5, user_id=1, content="이 작품 원본 사이즈 보고싶어요", commenter_role="fan", status="active"),
        ]
        db.add_all(artist_image_comments)
        await db.flush()

        artist_image_stats = [
            ArtistImageStat(id=i, artist_image_id=i, view_count=(7 - i) * 30, comment_count=2 if i == 1 else 1, fan_like_count=(7 - i) * 5)
            for i in range(1, 7)
        ]
        db.add_all(artist_image_stats)
        await db.flush()

        # Artist Videos
        artist_videos = [
            ArtistVideo(id=1, artist_id=1, write_id=2, write_role="artist", url="/placeholder/video1.mp4", title="루나 - 별빛 아래서 MV",    description="신곡 뮤직비디오",   duration_seconds=245, tags=["뮤직비디오", "신곡"], visibility="public"),
            ArtistVideo(id=2, artist_id=1, write_id=2, write_role="artist", url="/placeholder/video2.mp4", title="앨범 작업 비하인드",        description="스튜디오 비하인드", duration_seconds=600, tags=["비하인드"],           visibility="subscribers"),
            ArtistVideo(id=3, artist_id=2, write_id=3, write_role="artist", url="/placeholder/video3.mp4", title="Gravity 안무 풀버전",       description="대회 출전 안무",    duration_seconds=310, tags=["안무", "풀버전"],     visibility="public"),
            ArtistVideo(id=4, artist_id=2, write_id=3, write_role="artist", url="/placeholder/video4.mp4", title="안무 연습 브이로그",         description="연습실 브이로그",   duration_seconds=900, tags=["브이로그", "연습"],   visibility="public"),
            ArtistVideo(id=5, artist_id=3, write_id=4, write_role="artist", url="/placeholder/video5.mp4", title="작업 타임랩스 - 도시의 밤", description="일러스트 타임랩스", duration_seconds=180, tags=["타임랩스", "작업과정"], visibility="public"),
        ]
        db.add_all(artist_videos)
        await db.flush()

        artist_video_comments = [
            ArtistVideoComment(id=1, artist_video_id=1, user_id=1, content="MV 퀄리티 미쳤어요!",         commenter_role="fan",    status="active"),
            ArtistVideoComment(id=2, artist_video_id=1, user_id=2, content="많이 사랑해주세요!",           commenter_role="artist", status="active", parent_comment_id=1),
            ArtistVideoComment(id=3, artist_video_id=3, user_id=1, content="안무 진짜 소름 돋아요",        commenter_role="fan",    status="active"),
            ArtistVideoComment(id=4, artist_video_id=5, user_id=1, content="타임랩스 보는 재미가 있네요",  commenter_role="fan",    status="active"),
        ]
        db.add_all(artist_video_comments)
        await db.flush()

        artist_video_stats = [
            ArtistVideoStat(id=i, artist_video_id=i, view_count=(6 - i) * 100, comment_count=2 if i == 1 else 1, fan_like_count=(6 - i) * 15)
            for i in range(1, 6)
        ]
        db.add_all(artist_video_stats)
        await db.flush()

        print("  [OK] Content (posts, images, videos, comments, stats)")

        # ================================================================
        # 5. CHAT — chat_rooms / chat_messages / chat_images / chat_videos
        #           chat_read_receipts / chat_pins / chat_reports
        # ================================================================
        chat_rooms = [
            ChatRoom(id=1, room_type="subscription", artist_id=1, room_name="루나 채팅방",  last_message_at=now - timedelta(minutes=5), status="active"),
            ChatRoom(id=2, room_type="subscription", artist_id=2, room_name="하루 채팅방",  last_message_at=now - timedelta(hours=1),   status="active"),
            ChatRoom(id=3, room_type="subscription", artist_id=3, room_name="소율 채팅방",  last_message_at=now - timedelta(hours=3),   status="active"),
        ]
        db.add_all(chat_rooms)
        await db.flush()

        chat_messages = [
            # 루나 채팅방
            ChatMessage(id=1,  chat_room_id=1, sender_id=2, sender_type="artist", message_type="text",  content="안녕하세요! 오늘도 좋은 하루 보내세요", status="active"),
            ChatMessage(id=2,  chat_room_id=1, sender_id=1, sender_type="fan",    message_type="text",  content="루나님 안녕하세요! 새 앨범 기대하고 있어요", status="active"),
            ChatMessage(id=3,  chat_room_id=1, sender_id=2, sender_type="artist", message_type="text",  content="감사합니다! 곧 좋은 소식 들려드릴게요", status="active"),
            ChatMessage(id=4,  chat_room_id=1, sender_id=1, sender_type="fan",    message_type="image", content=None, status="active"),
            ChatMessage(id=5,  chat_room_id=1, sender_id=2, sender_type="artist", message_type="text",  content="이 사진 예쁘네요!", status="active", is_pinned=True),
            # 하루 채팅방
            ChatMessage(id=6,  chat_room_id=2, sender_id=3, sender_type="artist", message_type="text",  content="오늘 연습 끝! 다들 수고했어요", status="active"),
            ChatMessage(id=7,  chat_room_id=2, sender_id=1, sender_type="fan",    message_type="text",  content="하루님 연습 영상 올려주세요!", status="active"),
            ChatMessage(id=8,  chat_room_id=2, sender_id=3, sender_type="artist", message_type="video", content=None, status="active"),
            # 소율 채팅방
            ChatMessage(id=9,  chat_room_id=3, sender_id=4, sender_type="artist", message_type="text",  content="새 작품 작업 중이에요. 조금만 기다려주세요!", status="active"),
            ChatMessage(id=10, chat_room_id=3, sender_id=1, sender_type="fan",    message_type="text",  content="기대하고 있을게요!!", status="active"),
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
            Event(id=1, artist_id=1, title="루나 팬미팅 2026",  description="팬 여러분과 함께하는 특별한 시간",           event_type="fanmeeting", event_date=now + timedelta(days=14), location="서울 강남 이벤트홀", max_participants=200, current_participants=46, status="active"),
            Event(id=2, artist_id=2, title="하루 댄스 챌린지",  description="Gravity 안무 따라하기 챌린지",                event_type="challenge",  event_date=now + timedelta(days=7),  location="온라인",             max_participants=None, current_participants=128, status="active"),
            Event(id=3, artist_id=3, title="소율 라이브 드로잉", description="실시간으로 그림 그리는 과정을 공개합니다",     event_type="live",       event_date=now + timedelta(days=3),  location="유튜브 라이브",      max_participants=None, current_participants=1, status="active"),
            Event(id=4, artist_id=1, title="루나 콘서트 2026",  description="루나 단독 콘서트 — 별빛 아래서",              event_type="concert",    event_date=now - timedelta(days=7),  location="잠실 올림픽경기장",   max_participants=20000, current_participants=20000, status="completed"),
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
            Product(id=1, artist_id=1, name="루나 포토카드 세트",    description="별빛 아래서 콘서트 포토카드 5장", price=Decimal("15000"), stock=100, category="photocard", status="active"),
            Product(id=2, artist_id=1, name="루나 라이트스틱",       description="공식 응원봉",                    price=Decimal("35000"), stock=50,  category="lightstick", status="active"),
            Product(id=3, artist_id=2, name="하루 연습복 티셔츠",    description="하루 시그니처 로고 티셔츠",       price=Decimal("25000"), stock=200, category="apparel",    status="active"),
            Product(id=4, artist_id=3, name="소율 아트프린트 A3",    description="도시의 밤 시리즈 한정판 프린트",  price=Decimal("20000"), stock=30,  category="art",        status="active"),
            Product(id=5, artist_id=3, name="소율 스티커팩",         description="일러스트 스티커 10장 세트",       price=Decimal("5000"),  stock=500, category="sticker",    status="active"),
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
            NotificationTemplate(id=1, template_name="새 포스트",       noti_type="content", title_template="{artist_name}님이 새 포스트를 올렸어요",      message_template="{artist_name}: {preview}", is_active=True),
            NotificationTemplate(id=2, template_name="새 이미지",       noti_type="content", title_template="{artist_name}님이 새 이미지를 올렸어요",      message_template="{artist_name}님의 새 이미지를 확인하세요", is_active=True),
            NotificationTemplate(id=3, template_name="새 영상",         noti_type="content", title_template="{artist_name}님이 새 영상을 올렸어요",        message_template="{video_title}", is_active=True),
            NotificationTemplate(id=4, template_name="댓글 답글",       noti_type="social",  title_template="{user_name}님이 답글을 남겼어요",             message_template="{preview}", is_active=True),
            NotificationTemplate(id=5, template_name="이벤트 오픈",     noti_type="event",   title_template="{artist_name}님의 새 이벤트가 열렸어요",      message_template="{event_title}", is_active=True),
            NotificationTemplate(id=6, template_name="주문 배송 시작",  noti_type="order",   title_template="주문하신 상품이 배송 시작되었어요",            message_template="주문번호 {order_number}", is_active=True),
            NotificationTemplate(id=7, template_name="채팅 메시지",     noti_type="chat",    title_template="{sender_name}님의 메시지",                    message_template="{preview}", is_active=True),
        ]
        db.add_all(notification_templates)
        await db.flush()

        notifications = [
            Notification(id=1,  subscription_id=1, user_id=1, noti_type="content", source_id=1, source_type="post",          event_type="new_post",    target_id=1,  title="루나님이 새 포스트를 올렸어요",         message="오늘 새 앨범 작업을 시작했어요!",            is_read=True,  is_pushed=True),
            Notification(id=2,  subscription_id=1, user_id=1, noti_type="content", source_id=1, source_type="artist_video",   event_type="new_video",   target_id=1,  title="루나님이 새 영상을 올렸어요",           message="루나 - 별빛 아래서 MV",                      is_read=True,  is_pushed=True),
            Notification(id=3,  subscription_id=2, user_id=1, noti_type="content", source_id=2, source_type="post",          event_type="new_post",    target_id=3,  title="하루님이 새 포스트를 올렸어요",         message="새로운 안무 연습 중!",                       is_read=False, is_pushed=True),
            Notification(id=4,  subscription_id=3, user_id=1, noti_type="content", source_id=3, source_type="post",          event_type="new_post",    target_id=5,  title="소율님이 새 포스트를 올렸어요",         message="새로운 일러스트 시리즈 '도시의 밤'",          is_read=False, is_pushed=True),
            Notification(id=5,  user_id=1, noti_type="social",  source_id=2, source_type="user",          event_type="reply",       target_id=1,  title="루나님이 답글을 남겼어요",               message="감사합니다! 열심히 준비할게요",               is_read=False, is_pushed=True),
            Notification(id=6,  user_id=1, noti_type="event",   source_id=1, source_type="event",         event_type="new_event",   target_id=1,  title="루나님의 새 이벤트가 열렸어요",         message="루나 팬미팅 2026",                           is_read=True,  is_pushed=True),
            Notification(id=7,  user_id=1, noti_type="order",   source_id=1, source_type="order",         event_type="shipped",     target_id=1,  title="주문하신 상품이 배송 시작되었어요",     message="주문번호 ORD-2026-0001",                     is_read=True,  is_pushed=True),
            Notification(id=8,  user_id=1, noti_type="chat",    source_id=2, source_type="chat_message",  event_type="new_message", target_id=1,  title="루나님의 메시지",                       message="이 사진 예쁘네요!",                          is_read=False, is_pushed=True),
        ]
        db.add_all(notifications)
        await db.flush()

        notification_settings = [
            NotificationSetting(id=1, subscription_id=1, user_id=1, source_type="artist"),
            NotificationSetting(id=2, subscription_id=2, user_id=1, source_type="artist"),
            NotificationSetting(id=3, subscription_id=3, user_id=1, source_type="artist"),
            NotificationSetting(id=4, user_id=1, source_type="system"),
        ]
        db.add_all(notification_settings)
        await db.flush()

        scheduled_notifications = [
            ScheduledNotification(id=1, notification_template_id=5, receiver_id=1, send_at=now + timedelta(days=1), is_sent=False),
        ]
        db.add_all(scheduled_notifications)
        await db.flush()

        system_logs_data = [
            SystemLog(id=1, sender_id=2, receiver_id=1, channel="push", status="delivered"),
            SystemLog(id=2, sender_id=3, receiver_id=1, channel="push", status="delivered"),
            SystemLog(id=3, sender_id=2, receiver_id=1, channel="push", status="failed", error_message="디바이스 토큰 만료"),
        ]
        db.add_all(system_logs_data)
        await db.flush()

        print("  [OK] Notification (templates, notifications, settings, scheduled, system_logs)")

        # ================================================================
        # 11. LIKE — fan_likes / fan_recommendations / artist_post_likes / artist_post_recommendations
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

        artist_post_likes = [
            ArtistPostLike(id=1, artist_id=1, post_id=6),
            ArtistPostLike(id=2, artist_id=2, post_id=7),
            ArtistPostLike(id=3, artist_id=3, post_id=8),
        ]
        db.add_all(artist_post_likes)
        await db.flush()

        artist_post_recommendations = [
            ArtistPostRecommendation(id=1, artist_id=1, post_id=6),
        ]
        db.add_all(artist_post_recommendations)
        await db.flush()

        print("  [OK] Like (fan_likes, fan_recommendations, artist_post_likes, artist_post_recommendations)")

        # ================================================================
        # 12. STATS — artist_content / artist_chat / subscriber_content / subscriber_chat
        # ================================================================
        artist_content_stats = [
            ArtistContentStat(id=1, artist_id=1, post_count=4,  image_count=2, video_count=2, fan_like_count=3, fan_recommend_count=1),
            ArtistContentStat(id=2, artist_id=2, post_count=3,  image_count=2, video_count=2, fan_like_count=2, fan_recommend_count=1),
            ArtistContentStat(id=3, artist_id=3, post_count=2,  image_count=2, video_count=1, fan_like_count=1, fan_recommend_count=1),
            ArtistContentStat(id=4, artist_id=4, post_count=0,  image_count=0, video_count=0, fan_like_count=0, fan_recommend_count=0),
            ArtistContentStat(id=5, artist_id=5, post_count=0,  image_count=0, video_count=0, fan_like_count=0, fan_recommend_count=0),
            ArtistContentStat(id=6, artist_id=6, post_count=0,  image_count=0, video_count=0, fan_like_count=0, fan_recommend_count=0),
        ]
        db.add_all(artist_content_stats)
        await db.flush()

        artist_chat_stats = [
            ArtistChatStat(id=1, artist_id=1, chat_subscriber_count=1, chat_image_count=0, chat_video_count=0, chat_attendance_days=5),
            ArtistChatStat(id=2, artist_id=2, chat_subscriber_count=1, chat_image_count=0, chat_video_count=1, chat_attendance_days=3),
            ArtistChatStat(id=3, artist_id=3, chat_subscriber_count=1, chat_image_count=0, chat_video_count=0, chat_attendance_days=2),
        ]
        db.add_all(artist_chat_stats)
        await db.flush()

        subscriber_content_stats = [
            SubscriberContentStat(id=1, subscription_id=1, post_count=2, image_count=0, fan_like_count=3, fan_recommend_count=1),
            SubscriberContentStat(id=2, subscription_id=2, post_count=1, image_count=0, fan_like_count=2, fan_recommend_count=1),
            SubscriberContentStat(id=3, subscription_id=3, post_count=1, image_count=0, fan_like_count=1, fan_recommend_count=1),
        ]
        db.add_all(subscriber_content_stats)
        await db.flush()

        subscriber_chat_stats = [
            SubscriberChatStat(id=1, subscription_id=1, messages_sent=3, chat_active_days=5),
            SubscriberChatStat(id=2, subscription_id=2, messages_sent=1, chat_active_days=2),
            SubscriberChatStat(id=3, subscription_id=3, messages_sent=1, chat_active_days=1),
        ]
        db.add_all(subscriber_chat_stats)
        await db.flush()

        print("  [OK] Stats (artist_content, artist_chat, subscriber_content, subscriber_chat)")

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
            ContentModeration(id=1, content_type="post",    content_id=1, creator_ref_type="artist", creator_ref_id=1, model_id=1, result={"score": 0.02, "category": "safe"},       is_flagged=False, reviewed=True, reviewed_by=8),
            ContentModeration(id=2, content_type="comment", content_id=1, creator_ref_type="fan",    creator_ref_id=1, model_id=1, result={"score": 0.01, "category": "safe"},       is_flagged=False, reviewed=False),
            ContentModeration(id=3, content_type="image",   content_id=1, creator_ref_type="artist", creator_ref_id=1, model_id=2, result={"score": 0.05, "category": "safe"},       is_flagged=False, reviewed=False),
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
            FAQ(id=3, category="구독",   question="구독은 어떻게 하나요?",                                 answer="아티스트 프로필 페이지에서 '구독하기' 버튼을 클릭하면 됩니다. 무료/유료 플랜을 선택할 수 있습니다.", priority=1, is_active=True, write_id=8),
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
            Notice(id=1, title="yourFlace 서비스 오픈 안내",        message="yourFlace가 정식 오픈했습니다! 다양한 아티스트를 만나보세요.",                                    write_id=8, write_role="admin", target_type="all", is_active=True),
            Notice(id=2, title="신규 아티스트 루나 합류",            message="인기 가수 루나가 yourFlace에 합류했습니다. 지금 바로 구독하세요!",                                write_id=8, write_role="admin", target_type="all", is_active=True),
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
        # COMMIT
        # ================================================================
        await db.commit()
        print()
        print("=" * 55)
        print("  시드 데이터 삽입 완료!")
        print("=" * 55)
        print()
        print("  테스트 계정: fan@test.com / test1234")
        print("  관리자 계정: admin@test.com / test1234")
        print()
        print("  Users           8명 (팬1 + 아티스트6 + 관리자1)")
        print("  Artists         6명 (루나, 하루, 소율, 민서, 제이, 유리)")
        print("  Subscriptions   4건 (활성3 + 취소1)")
        print("  Sub Plans       6건 (아티스트별 베이직+프리미엄)")
        print("  Posts          11건 (아티스트5 + 팬3 + 기사3)")
        print("  Images         12건 / Artist Images 6건 / Videos 5건")
        print("  Chat Rooms      3개 / Messages 10건")
        print("  Events          4건 (활성3 + 완료1)")
        print("  Products        5건 / Orders 3건")
        print("  Payments        3건 / Refunds 1건")
        print("  Notifications   8건 / Templates 7건")
        print("  Fan Likes       8건 / Recommendations 3건")
        print("  FAQ             7건 / Banners 3건 / Notices 3건")
        print("  Moderation      2 models / 3 results")
        print("  + settings, addresses, devices, stats, logs 등")


async def reset_sequences():
    """auto-increment 시퀀스를 시드 데이터 이후부터 시작하도록 리셋"""
    async with AsyncSessionLocal() as db:
        tables = [
            ("users", 20), ("profile", 20), ("user_settings", 20),
            ("user_addresses", 10), ("user_devices", 10), ("login_logs", 10),
            ("artist_categories", 10), ("artists", 10),
            ("artist_category_map", 10), ("artist_social_links", 20),
            ("managers", 10),
            ("subscription_plans", 10), ("subscriptions", 10),
            ("subscription_cancellations", 10),
            ("images", 20), ("posts", 20), ("post_images", 10),
            ("post_comments", 10), ("post_stats", 20),
            ("artist_images", 10), ("artist_image_comments", 10), ("artist_image_stats", 10),
            ("artist_videos", 10), ("artist_video_comments", 10), ("artist_video_stats", 10),
            ("chat_rooms", 10), ("chat_messages", 20),
            ("chat_images", 10), ("chat_videos", 10),
            ("chat_read_receipts", 10), ("chat_pins", 10), ("chat_reports", 10),
            ("calendar_searches", 10), ("saved_search_filters", 10),
            ("payment_methods", 10), ("payments", 10), ("payment_refunds", 10),
            ("events", 10), ("event_participants", 10), ("event_attendance", 10),
            ("products", 10), ("product_images", 10),
            ("orders", 10), ("order_items", 10),
            ("notification_templates", 10), ("notifications", 20),
            ("notification_settings", 10), ("scheduled_notifications", 10),
            ("system_logs", 10),
            ("fan_likes", 20), ("fan_recommendations", 10),
            ("artist_post_likes", 10), ("artist_post_recommendations", 10),
            ("artist_content_stats", 10), ("artist_chat_stats", 10),
            ("subscriber_content_stats", 10), ("subscriber_chat_stats", 10),
            ("moderation_models", 10), ("content_moderation", 10),
            ("faq", 10), ("banners", 10), ("system_messages", 10),
            ("notices", 10), ("error_logs", 10),
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
    parser = argparse.ArgumentParser(description="yourFlace 시드 데이터")
    parser.add_argument("--reset", action="store_true", help="테이블 전체 리셋 후 시드 삽입")
    args = parser.parse_args()

    print()
    print("=" * 55)
    print("  yourFlace Seed Data")
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

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        table_count = len(Base.metadata.tables)
        print(f"[OK] 테이블 {table_count}개 생성")
        print()

    print("[시드 데이터 삽입 중...]")
    await seed_data()
    await reset_sequences()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
