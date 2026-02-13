from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine
from app.core.cache import redis_client
from app.core.storage import init_storage
from app.core.ws_manager import ws_manager

# 모든 라우터 임포트
# Auth
from app.auth.users.router import router as users_router
from app.auth.user_settings.router import router as user_settings_router
from app.auth.profile.router import router as profile_router
from app.auth.user_addresses.router import router as user_addresses_router
from app.auth.user_devices.router import router as user_devices_router
from app.auth.login_logs.router import router as login_logs_router
from app.auth.deleted_users.router import router as deleted_users_router
from app.auth.global_blacklist.router import router as global_blacklist_router
from app.auth.subscription_blacklist.router import router as subscription_blacklist_router

from app.artist.artists.router import router as artists_router
from app.artist.artist_categories.router import router as artist_categories_router
from app.artist.artist_category_map.router import router as artist_category_map_router
from app.artist.artist_social_links.router import router as artist_social_links_router
from app.artist.managers.router import router as managers_router

from app.subscription.subscriptions.router import router as subscriptions_router
from app.subscription.subscription_plans.router import router as subscription_plans_router
from app.subscription.subscription_cancellations.router import router as subscription_cancellations_router

from app.content.posts.router import router as posts_router
from app.content.post_images.router import router as post_images_router
from app.content.post_comments.router import router as post_comments_router
from app.content.post_stats.router import router as post_stats_router
from app.content.images.router import router as images_router
from app.content.artist_images.router import router as artist_images_router
from app.content.artist_image_comments.router import router as artist_image_comments_router
from app.content.artist_image_stats.router import router as artist_image_stats_router
from app.content.artist_videos.router import router as artist_videos_router
from app.content.artist_video_comments.router import router as artist_video_comments_router
from app.content.artist_video_stats.router import router as artist_video_stats_router

from app.search.calendar_searches.router import router as calendar_searches_router
from app.search.saved_search_filters.router import router as saved_search_filters_router

from app.chat.chat_rooms.router import router as chat_rooms_router
from app.chat.chat_messages.router import router as chat_messages_router
from app.chat.chat_images.router import router as chat_images_router
from app.chat.chat_videos.router import router as chat_videos_router
from app.chat.chat_read_receipts.router import router as chat_read_receipts_router
from app.chat.chat_pins.router import router as chat_pins_router
from app.chat.chat_reports.router import router as chat_reports_router
from app.chat.ws.router import router as chat_ws_router

from app.payment.payments.router import router as payments_router
from app.payment.payment_methods.router import router as payment_methods_router
from app.payment.payment_refunds.router import router as payment_refunds_router

from app.event.events.router import router as events_router
from app.event.event_participants.router import router as event_participants_router
from app.event.event_attendance.router import router as event_attendance_router

from app.shop.products.router import router as products_router
from app.shop.product_images.router import router as product_images_router
from app.shop.orders.router import router as orders_router
from app.shop.order_items.router import router as order_items_router

from app.notification.notifications.router import router as notifications_router
from app.notification.notification_settings.router import router as notification_settings_router
from app.notification.notification_templates.router import router as notification_templates_router
from app.notification.scheduled_notifications.router import router as scheduled_notifications_router
from app.notification.system_logs.router import router as system_logs_router

from app.like.fan_likes.router import router as fan_likes_router
from app.like.fan_recommendations.router import router as fan_recommendations_router
from app.like.artist_post_likes.router import router as artist_post_likes_router
from app.like.artist_post_recommendations.router import router as artist_post_recommendations_router

from app.stats.artist_content_stats.router import router as artist_content_stats_router
from app.stats.artist_chat_stats.router import router as artist_chat_stats_router
from app.stats.subscriber_content_stats.router import router as subscriber_content_stats_router
from app.stats.subscriber_chat_stats.router import router as subscriber_chat_stats_router

from app.moderation.moderation_models.router import router as moderation_models_router
from app.moderation.content_moderation.router import router as content_moderation_router

from app.admin.faq.router import router as faq_router
from app.admin.banners.router import router as banners_router
from app.admin.system_messages.router import router as system_messages_router
from app.admin.notices.router import router as notices_router
from app.admin.error_logs.router import router as error_logs_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await redis_client.initialize()
    await init_storage()
    
    yield
    
    # Shutdown
    await ws_manager.close()
    await redis_client.close()
    await engine.dispose()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# API Routes
API_V1_PREFIX = "/yourflace"

# Auth (사용자 관리)
app.include_router(users_router, prefix=f"{API_V1_PREFIX}/users", tags=["users"])
app.include_router(user_settings_router, prefix=f"{API_V1_PREFIX}/user-settings", tags=["user-settings"])
app.include_router(profile_router, prefix=f"{API_V1_PREFIX}/profiles", tags=["profiles"])
app.include_router(user_addresses_router, prefix=f"{API_V1_PREFIX}/user-addresses", tags=["user-addresses"])
app.include_router(user_devices_router, prefix=f"{API_V1_PREFIX}/user-devices", tags=["user-devices"])
app.include_router(login_logs_router, prefix=f"{API_V1_PREFIX}/login-logs", tags=["login-logs"])
app.include_router(deleted_users_router, prefix=f"{API_V1_PREFIX}/deleted-users", tags=["deleted-users"])
app.include_router(global_blacklist_router, prefix=f"{API_V1_PREFIX}/global-blacklist", tags=["global-blacklist"])
app.include_router(subscription_blacklist_router, prefix=f"{API_V1_PREFIX}/subscription-blacklist", tags=["subscription-blacklist"])

# Artist
app.include_router(artists_router, prefix=f"{API_V1_PREFIX}/artists", tags=["artists"])
app.include_router(artist_categories_router, prefix=f"{API_V1_PREFIX}/artist-categories", tags=["artist-categories"])
app.include_router(artist_category_map_router, prefix=f"{API_V1_PREFIX}/artist-category-map", tags=["artist-category-map"])
app.include_router(artist_social_links_router, prefix=f"{API_V1_PREFIX}/artist-social-links", tags=["artist-social-links"])
app.include_router(managers_router, prefix=f"{API_V1_PREFIX}/managers", tags=["managers"])

# Subscription
app.include_router(subscriptions_router, prefix=f"{API_V1_PREFIX}/subscriptions", tags=["subscriptions"])
app.include_router(subscription_plans_router, prefix=f"{API_V1_PREFIX}/subscription-plans", tags=["subscription-plans"])
app.include_router(subscription_cancellations_router, prefix=f"{API_V1_PREFIX}/subscription-cancellations", tags=["subscription-cancellations"])

# Content
app.include_router(posts_router, prefix=f"{API_V1_PREFIX}/posts", tags=["posts"])
app.include_router(post_images_router, prefix=f"{API_V1_PREFIX}/post-images", tags=["post-images"])
app.include_router(post_comments_router, prefix=f"{API_V1_PREFIX}/post-comments", tags=["post-comments"])
app.include_router(post_stats_router, prefix=f"{API_V1_PREFIX}/post-stats", tags=["post-stats"])
app.include_router(images_router, prefix=f"{API_V1_PREFIX}/images", tags=["images"])
app.include_router(artist_images_router, prefix=f"{API_V1_PREFIX}/artist-images", tags=["artist-images"])
app.include_router(artist_image_comments_router, prefix=f"{API_V1_PREFIX}/artist-image-comments", tags=["artist-image-comments"])
app.include_router(artist_image_stats_router, prefix=f"{API_V1_PREFIX}/artist-image-stats", tags=["artist-image-stats"])
app.include_router(artist_videos_router, prefix=f"{API_V1_PREFIX}/artist-videos", tags=["artist-videos"])
app.include_router(artist_video_comments_router, prefix=f"{API_V1_PREFIX}/artist-video-comments", tags=["artist-video-comments"])
app.include_router(artist_video_stats_router, prefix=f"{API_V1_PREFIX}/artist-video-stats", tags=["artist-video-stats"])

# Search
app.include_router(calendar_searches_router, prefix=f"{API_V1_PREFIX}/calendar-searches", tags=["calendar-searches"])
app.include_router(saved_search_filters_router, prefix=f"{API_V1_PREFIX}/saved-search-filters", tags=["saved-search-filters"])

# Chat
app.include_router(chat_rooms_router, prefix=f"{API_V1_PREFIX}/chat-rooms", tags=["chat-rooms"])
app.include_router(chat_messages_router, prefix=f"{API_V1_PREFIX}/chat-messages", tags=["chat-messages"])
app.include_router(chat_images_router, prefix=f"{API_V1_PREFIX}/chat-images", tags=["chat-images"])
app.include_router(chat_videos_router, prefix=f"{API_V1_PREFIX}/chat-videos", tags=["chat-videos"])
app.include_router(chat_read_receipts_router, prefix=f"{API_V1_PREFIX}/chat-read-receipts", tags=["chat-read-receipts"])
app.include_router(chat_pins_router, prefix=f"{API_V1_PREFIX}/chat-pins", tags=["chat-pins"])
app.include_router(chat_reports_router, prefix=f"{API_V1_PREFIX}/chat-reports", tags=["chat-reports"])
app.include_router(chat_ws_router, prefix=f"{API_V1_PREFIX}/chat/ws", tags=["chat-ws"])

# Payment
app.include_router(payments_router, prefix=f"{API_V1_PREFIX}/payments", tags=["payments"])
app.include_router(payment_methods_router, prefix=f"{API_V1_PREFIX}/payment-methods", tags=["payment-methods"])
app.include_router(payment_refunds_router, prefix=f"{API_V1_PREFIX}/payment-refunds", tags=["payment-refunds"])

# Event
app.include_router(events_router, prefix=f"{API_V1_PREFIX}/events", tags=["events"])
app.include_router(event_participants_router, prefix=f"{API_V1_PREFIX}/event-participants", tags=["event-participants"])
app.include_router(event_attendance_router, prefix=f"{API_V1_PREFIX}/event-attendance", tags=["event-attendance"])

# Shop
app.include_router(products_router, prefix=f"{API_V1_PREFIX}/products", tags=["products"])
app.include_router(product_images_router, prefix=f"{API_V1_PREFIX}/product-images", tags=["product-images"])
app.include_router(orders_router, prefix=f"{API_V1_PREFIX}/orders", tags=["orders"])
app.include_router(order_items_router, prefix=f"{API_V1_PREFIX}/order-items", tags=["order-items"])

# Notification
app.include_router(notifications_router, prefix=f"{API_V1_PREFIX}/notifications", tags=["notifications"])
app.include_router(notification_settings_router, prefix=f"{API_V1_PREFIX}/notification-settings", tags=["notification-settings"])
app.include_router(notification_templates_router, prefix=f"{API_V1_PREFIX}/notification-templates", tags=["notification-templates"])
app.include_router(scheduled_notifications_router, prefix=f"{API_V1_PREFIX}/scheduled-notifications", tags=["scheduled-notifications"])
app.include_router(system_logs_router, prefix=f"{API_V1_PREFIX}/system-logs", tags=["system-logs"])

# Like
app.include_router(fan_likes_router, prefix=f"{API_V1_PREFIX}/fan-likes", tags=["fan-likes"])
app.include_router(fan_recommendations_router, prefix=f"{API_V1_PREFIX}/fan-recommendations", tags=["fan-recommendations"])
app.include_router(artist_post_likes_router, prefix=f"{API_V1_PREFIX}/artist-post-likes", tags=["artist-post-likes"])
app.include_router(artist_post_recommendations_router, prefix=f"{API_V1_PREFIX}/artist-post-recommendations", tags=["artist-post-recommendations"])

# Stats
app.include_router(artist_content_stats_router, prefix=f"{API_V1_PREFIX}/artist-content-stats", tags=["artist-content-stats"])
app.include_router(artist_chat_stats_router, prefix=f"{API_V1_PREFIX}/artist-chat-stats", tags=["artist-chat-stats"])
app.include_router(subscriber_content_stats_router, prefix=f"{API_V1_PREFIX}/subscriber-content-stats", tags=["subscriber-content-stats"])
app.include_router(subscriber_chat_stats_router, prefix=f"{API_V1_PREFIX}/subscriber-chat-stats", tags=["subscriber-chat-stats"])

# Moderation
app.include_router(moderation_models_router, prefix=f"{API_V1_PREFIX}/moderation-models", tags=["moderation-models"])
app.include_router(content_moderation_router, prefix=f"{API_V1_PREFIX}/content-moderation", tags=["content-moderation"])

# Admin
app.include_router(faq_router, prefix=f"{API_V1_PREFIX}/faq", tags=["faq"])
app.include_router(banners_router, prefix=f"{API_V1_PREFIX}/banners", tags=["banners"])
app.include_router(system_messages_router, prefix=f"{API_V1_PREFIX}/system-messages", tags=["system-messages"])
app.include_router(notices_router, prefix=f"{API_V1_PREFIX}/notices", tags=["notices"])
app.include_router(error_logs_router, prefix=f"{API_V1_PREFIX}/error-logs", tags=["error-logs"])

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }

@app.get("/")
async def root():
    return {
        "message": "Fanbase Platform API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }
