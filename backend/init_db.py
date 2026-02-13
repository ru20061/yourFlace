"""
DB 테이블 생성 + 시드 데이터 삽입 스크립트
사용법: cd backend && python init_db.py
"""
import asyncio
from datetime import date, datetime, timedelta
from sqlalchemy import text

from app.database import engine, Base, AsyncSessionLocal
from app.core.security import get_password_hash

# 모든 모델 임포트 (테이블 생성에 필요)
from app.auth.users.models import User
from app.auth.profile.models import Profile
from app.auth.user_settings.models import *
from app.auth.user_addresses.models import *
from app.auth.user_devices.models import *
from app.auth.login_logs.models import *
from app.auth.deleted_users.models import *
from app.auth.global_blacklist.models import *
from app.auth.subscription_blacklist.models import *

from app.artist.artists.models import Artist
from app.artist.artist_categories.models import ArtistCategory
from app.artist.artist_category_map.models import ArtistCategoryMap
from app.artist.artist_social_links.models import ArtistSocialLink
from app.artist.managers.models import *

from app.subscription.subscriptions.models import Subscription
from app.subscription.subscription_plans.models import *
from app.subscription.subscription_cancellations.models import *

from app.content.posts.models import Post
from app.content.post_images.models import *
from app.content.post_comments.models import *
from app.content.post_stats.models import *
from app.content.images.models import Image
from app.content.artist_images.models import ArtistImage
from app.content.artist_image_comments.models import *
from app.content.artist_image_stats.models import *
from app.content.artist_videos.models import ArtistVideo
from app.content.artist_video_comments.models import *
from app.content.artist_video_stats.models import *

from app.search.calendar_searches.models import *
from app.search.saved_search_filters.models import *

from app.chat.chat_rooms.models import *
from app.chat.chat_messages.models import *
from app.chat.chat_images.models import *
from app.chat.chat_videos.models import *
from app.chat.chat_read_receipts.models import *
from app.chat.chat_pins.models import *
from app.chat.chat_reports.models import *

from app.payment.payments.models import *
from app.payment.payment_methods.models import *
from app.payment.payment_refunds.models import *

from app.event.events.models import Event
from app.event.event_participants.models import *
from app.event.event_attendance.models import *

from app.shop.products.models import *
from app.shop.product_images.models import *
from app.shop.orders.models import *
from app.shop.order_items.models import *

from app.notification.notifications.models import *
from app.notification.notification_settings.models import *
from app.notification.notification_templates.models import *
from app.notification.scheduled_notifications.models import *
from app.notification.system_logs.models import *

from app.like.fan_likes.models import *
from app.like.fan_recommendations.models import *
from app.like.artist_post_likes.models import *
from app.like.artist_post_recommendations.models import *

from app.stats.artist_content_stats.models import *
from app.stats.artist_chat_stats.models import *
from app.stats.subscriber_content_stats.models import *
from app.stats.subscriber_chat_stats.models import *

from app.moderation.moderation_models.models import *
from app.moderation.content_moderation.models import *

from app.admin.faq.models import *
from app.admin.banners.models import *
from app.admin.system_messages.models import *
from app.admin.notices.models import *
from app.admin.error_logs.models import *


async def create_tables():
    """모든 테이블 생성"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("[OK] 모든 테이블 생성 완료")


async def seed_data():
    """시드 데이터 삽입"""
    async with AsyncSessionLocal() as db:
        # 이미 시드 데이터가 있는지 확인
        result = await db.execute(text("SELECT COUNT(*) FROM users"))
        count = result.scalar()
        if count and count > 0:
            print("[SKIP] 이미 시드 데이터가 존재합니다")
            return

        now = datetime.utcnow()
        today = date.today()

        # ── 1. 유저 7명 (테스트 팬 1명 + 아티스트 계정 6명) ──
        test_password = get_password_hash("test1234")
        users = [
            User(id=1, email="fan@test.com", password_hash=test_password, status="active"),
            User(id=2, email="luna@artist.com", password_hash=test_password, status="active"),
            User(id=3, email="haru@artist.com", password_hash=test_password, status="active"),
            User(id=4, email="soyul@artist.com", password_hash=test_password, status="active"),
            User(id=5, email="minseo@artist.com", password_hash=test_password, status="active"),
            User(id=6, email="jay@artist.com", password_hash=test_password, status="active"),
            User(id=7, email="yuri@artist.com", password_hash=test_password, status="active"),
        ]
        db.add_all(users)
        await db.flush()

        # ── 2. 프로필 ──
        profiles = [
            Profile(user_id=1, nickname="테스트팬"),
            Profile(user_id=2, nickname="루나"),
            Profile(user_id=3, nickname="하루"),
            Profile(user_id=4, nickname="소율"),
            Profile(user_id=5, nickname="민서"),
            Profile(user_id=6, nickname="제이"),
            Profile(user_id=7, nickname="유리"),
        ]
        db.add_all(profiles)
        await db.flush()

        # ── 3. 카테고리 ──
        categories = [
            ArtistCategory(id=1, name="가수"),
            ArtistCategory(id=2, name="댄서"),
            ArtistCategory(id=3, name="일러스트레이터"),
            ArtistCategory(id=4, name="배우"),
        ]
        db.add_all(categories)
        await db.flush()

        # ── 4. 아티스트 6명 ──
        artists = [
            Artist(id=1, user_id=2, stage_name="루나", notes="음악으로 세상을 밝히는 아티스트", status="active"),
            Artist(id=2, user_id=3, stage_name="하루", notes="춤으로 하루를 채우는 댄서", status="active"),
            Artist(id=3, user_id=4, stage_name="소율", notes="그림으로 이야기를 전하는 일러스트레이터", status="active"),
            Artist(id=4, user_id=5, stage_name="민서", notes="연기로 감동을 주는 배우", status="active"),
            Artist(id=5, user_id=6, stage_name="제이", notes="힙합으로 세상을 흔드는 래퍼", status="active"),
            Artist(id=6, user_id=7, stage_name="유리", notes="현대무용의 새로운 지평을 여는 댄서", status="active"),
        ]
        db.add_all(artists)
        await db.flush()

        # ── 5. 아티스트-카테고리 매핑 ──
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

        # ── 6. 소셜 링크 ──
        social_links = [
            ArtistSocialLink(artist_id=1, platform_name="YouTube", url="https://youtube.com/@luna", display_name="루나 뮤직", follower_count=12000, priority=1),
            ArtistSocialLink(artist_id=1, platform_name="Instagram", url="https://instagram.com/luna", display_name="@luna_music", follower_count=8500, priority=2),
            ArtistSocialLink(artist_id=2, platform_name="YouTube", url="https://youtube.com/@haru", display_name="하루 댄스", follower_count=9500, priority=1),
            ArtistSocialLink(artist_id=2, platform_name="TikTok", url="https://tiktok.com/@haru", display_name="@haru_dance", follower_count=23000, priority=2),
            ArtistSocialLink(artist_id=3, platform_name="Instagram", url="https://instagram.com/soyul", display_name="@soyul_art", follower_count=15000, priority=1),
        ]
        db.add_all(social_links)
        await db.flush()

        # ── 7. 구독 (fan_id=1이 아티스트 1,2,3 구독) ──
        subscriptions = [
            Subscription(fan_id=1, artist_id=1, status="subscribed", payments_type="free", start_date=today - timedelta(days=30)),
            Subscription(fan_id=1, artist_id=2, status="subscribed", payments_type="free", start_date=today - timedelta(days=20)),
            Subscription(fan_id=1, artist_id=3, status="subscribed", payments_type="paid", start_date=today - timedelta(days=10)),
        ]
        db.add_all(subscriptions)
        await db.flush()

        # ── 8. 포스트 (아티스트 포스트 + 팬 포스트 + 기사형) ──
        posts = [
            # 아티스트 포스트
            Post(author_id=1, author_type="artist", content="오늘 새 앨범 작업을 시작했어요! 기대해주세요 🎵", write_id=2, write_role="artist", visibility="public", is_artist_post=True, tags=["음악", "앨범"], title_field=None),
            Post(author_id=1, author_type="artist", content="구독자 여러분만을 위한 비하인드 영상 곧 올라갑니다!", write_id=2, write_role="artist", visibility="subscribers", is_artist_post=True, tags=["비하인드"], title_field=None),
            Post(author_id=2, author_type="artist", content="새로운 안무 연습 중! 이번 주 라이브에서 공개할게요 💃", write_id=3, write_role="artist", visibility="public", is_artist_post=True, tags=["댄스", "안무"], title_field=None),
            Post(author_id=2, author_type="artist", content="연습실에서 하루종일 땀 흘리는 중... 화이팅!", write_id=3, write_role="artist", visibility="subscribers", is_artist_post=True, tags=["일상", "연습"], title_field=None),
            Post(author_id=3, author_type="artist", content="새로운 일러스트 시리즈 '도시의 밤' 첫 번째 작품을 공개합니다.", write_id=4, write_role="artist", visibility="public", is_artist_post=True, tags=["일러스트", "아트"], title_field=None),

            # 팬 포스트
            Post(author_id=1, author_type="fan", content="루나 노래 진짜 좋아요!! 다음 앨범 기대됩니다 ❤️", write_id=1, write_role="fan", visibility="public", is_artist_post=False, tags=["팬레터"], title_field=None),
            Post(author_id=2, author_type="fan", content="하루님 안무 진짜 대박... 라이브 꼭 볼게요!", write_id=1, write_role="fan", visibility="public", is_artist_post=False, tags=["응원"], title_field=None),
            Post(author_id=3, author_type="fan", content="소율 작가님 그림 너무 예뻐요. 굿즈 나오면 바로 구매할게요!", write_id=1, write_role="fan", visibility="public", is_artist_post=False, tags=["팬아트"], title_field=None),

            # 기사형 포스트
            Post(author_id=1, author_type="artist", content="지난 금요일 잠실 올림픽경기장에서 열린 루나의 첫 번째 단독 콘서트가 2만 관객을 가득 채우며 성공적으로 막을 내렸습니다.\n\n이번 공연에서 루나는 신곡 '별빛 아래서'를 최초 공개하며 팬들에게 특별한 선물을 전했습니다.\n\n3시간 동안 이어진 공연에서 총 25곡을 선보였으며, 앵콜 무대에서는 감동적인 팬 이벤트도 진행되었습니다.", write_id=2, write_role="artist", visibility="public", is_artist_post=True, tags=["콘서트", "공연"], title_field="루나, 첫 단독 콘서트 2만 관객 매진"),
            Post(author_id=2, author_type="artist", content="하루가 세계적인 댄스 대회 'World Dance Championship 2026'에서 현대무용 부문 금상을 수상했습니다.\n\n이번 대회에는 45개국에서 300팀 이상이 참가했으며, 하루는 'Gravity'라는 작품으로 심사위원 만장일치 최고점을 획득했습니다.\n\n하루는 수상 소감에서 '팬 여러분의 응원이 가장 큰 힘이었다'고 전했습니다.", write_id=3, write_role="artist", visibility="public", is_artist_post=True, tags=["수상", "대회"], title_field="하루, 세계 댄스 대회 금상 수상"),
            Post(author_id=3, author_type="artist", content="소율 작가의 첫 개인전 '꿈의 색채'가 서울 성수동 갤러리에서 오는 3월 1일부터 31일까지 한 달간 개최됩니다.\n\n이번 전시에서는 디지털 아트 30점과 수채화 15점을 포함한 총 45점의 작품이 전시됩니다.\n\n구독자를 위한 사전 관람 이벤트도 준비되어 있으니 많은 관심 부탁드립니다.", write_id=4, write_role="artist", visibility="public", is_artist_post=True, tags=["전시", "갤러리"], title_field="소율, 첫 개인전 '꿈의 색채' 개최"),
        ]
        db.add_all(posts)
        await db.flush()

        # ── 9. 이미지 (images 테이블 + artist_images 매핑) ──
        images = [
            Image(id=1, url="/placeholder/concert1.jpg", width=1200, height=800, mime_type="image/jpeg"),
            Image(id=2, url="/placeholder/concert2.jpg", width=1200, height=800, mime_type="image/jpeg"),
            Image(id=3, url="/placeholder/dance1.jpg", width=1200, height=800, mime_type="image/jpeg"),
            Image(id=4, url="/placeholder/dance2.jpg", width=1200, height=800, mime_type="image/jpeg"),
            Image(id=5, url="/placeholder/art1.jpg", width=1200, height=800, mime_type="image/jpeg"),
            Image(id=6, url="/placeholder/art2.jpg", width=1200, height=800, mime_type="image/jpeg"),
        ]
        db.add_all(images)
        await db.flush()

        artist_images = [
            ArtistImage(artist_id=1, image_id=1, write_id=2, write_role="artist", image_purpose="concert", tags=["콘서트", "무대"], visibility="public"),
            ArtistImage(artist_id=1, image_id=2, write_id=2, write_role="artist", image_purpose="behind", tags=["비하인드"], visibility="subscribers"),
            ArtistImage(artist_id=2, image_id=3, write_id=3, write_role="artist", image_purpose="performance", tags=["댄스", "공연"], visibility="public"),
            ArtistImage(artist_id=2, image_id=4, write_id=3, write_role="artist", image_purpose="practice", tags=["연습"], visibility="subscribers"),
            ArtistImage(artist_id=3, image_id=5, write_id=4, write_role="artist", image_purpose="artwork", tags=["일러스트", "작품"], visibility="public"),
            ArtistImage(artist_id=3, image_id=6, write_id=4, write_role="artist", image_purpose="process", tags=["작업과정"], visibility="public"),
        ]
        db.add_all(artist_images)
        await db.flush()

        # ── 10. 영상 ──
        videos = [
            ArtistVideo(artist_id=1, write_id=2, write_role="artist", url="/placeholder/video1.mp4", title="루나 - 별빛 아래서 MV", description="신곡 뮤직비디오", duration_seconds=245, tags=["뮤직비디오", "신곡"], visibility="public"),
            ArtistVideo(artist_id=1, write_id=2, write_role="artist", url="/placeholder/video2.mp4", title="앨범 작업 비하인드", description="스튜디오 비하인드", duration_seconds=600, tags=["비하인드"], visibility="subscribers"),
            ArtistVideo(artist_id=2, write_id=3, write_role="artist", url="/placeholder/video3.mp4", title="Gravity 안무 풀버전", description="대회 출전 안무", duration_seconds=310, tags=["안무", "풀버전"], visibility="public"),
            ArtistVideo(artist_id=2, write_id=3, write_role="artist", url="/placeholder/video4.mp4", title="안무 연습 브이로그", description="연습실 브이로그", duration_seconds=900, tags=["브이로그", "연습"], visibility="public"),
            ArtistVideo(artist_id=3, write_id=4, write_role="artist", url="/placeholder/video5.mp4", title="작업 타임랩스 - 도시의 밤", description="일러스트 타임랩스", duration_seconds=180, tags=["타임랩스", "작업과정"], visibility="public"),
        ]
        db.add_all(videos)
        await db.flush()

        # ── 11. 이벤트 ──
        events = [
            Event(artist_id=1, title="루나 팬미팅 2026", description="팬 여러분과 함께하는 특별한 시간", event_type="fanmeeting", event_date=now + timedelta(days=14), location="서울 강남 이벤트홀", max_participants=200, current_participants=45, status="active"),
            Event(artist_id=2, title="하루 댄스 챌린지", description="Gravity 안무 따라하기 챌린지", event_type="challenge", event_date=now + timedelta(days=7), location="온라인", max_participants=None, current_participants=128, status="active"),
            Event(artist_id=3, title="소율 라이브 드로잉", description="실시간으로 그림 그리는 과정을 공개합니다", event_type="live", event_date=now + timedelta(days=3), location="유튜브 라이브", max_participants=None, current_participants=0, status="active"),
        ]
        db.add_all(events)
        await db.flush()

        await db.commit()
        print("[OK] 시드 데이터 삽입 완료")
        print("  - 유저 7명 (fan@test.com / test1234)")
        print("  - 카테고리 4개")
        print("  - 아티스트 6명 (루나, 하루, 소율, 민서, 제이, 유리)")
        print("  - 구독 3건 (fan → 루나, 하루, 소율)")
        print("  - 포스트 11개 (아티스트5 + 팬3 + 기사3)")
        print("  - 이미지 6개, 영상 5개, 이벤트 3개")


async def reset_sequences():
    """시퀀스 리셋 (auto-increment가 시드 데이터 이후부터 시작하도록)"""
    async with AsyncSessionLocal() as db:
        tables_with_ids = [
            ("users", 10),
            ("profile", 10),
            ("artist_categories", 10),
            ("artists", 10),
            ("artist_category_map", 10),
            ("artist_social_links", 10),
            ("subscriptions", 10),
            ("posts", 20),
            ("images", 10),
            ("artist_images", 10),
            ("artist_videos", 10),
            ("events", 10),
        ]
        for table, next_val in tables_with_ids:
            try:
                await db.execute(text(f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), {next_val}, false)"))
            except Exception:
                pass
        await db.commit()
    print("[OK] 시퀀스 리셋 완료")


async def main():
    print("=== yourFlace DB 초기화 시작 ===")
    await create_tables()
    await seed_data()
    await reset_sequences()
    print("=== 완료 ===")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
