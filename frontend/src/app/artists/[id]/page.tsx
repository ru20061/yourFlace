"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { useAuth } from "../../../lib/auth-context";
import { api } from "../../../lib/api";
import type {
  Artist,
  Post,
  ArtistImage,
  ArtistVideo,
  ArtistSocialLink,
  Subscription,
  PaginatedResponse,
} from "../../data/types";
import PostCard from "../../components/PostCard/PostCard";
import ImageGrid from "../../components/ImageGrid/ImageGrid";
import VideoCard from "../../components/VideoCard/VideoCard";
import "./artist-detail.css";

const TABS = ["유저 포스트", "아티스트 포스트", "이미지", "동영상"] as const;

export default function ArtistDetailPage() {
  const params = useParams();
  const artistId = Number(params.id);
  const { user } = useAuth();

  const [artist, setArtist] = useState<Artist | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);
  const [fanPosts, setFanPosts] = useState<Post[]>([]);
  const [images, setImages] = useState<ArtistImage[]>([]);
  const [videos, setVideos] = useState<ArtistVideo[]>([]);
  const [socialLinks, setSocialLinks] = useState<ArtistSocialLink[]>([]);
  const [subscriberCount, setSubscriberCount] = useState(0);
  const [isSubscribed, setIsSubscribed] = useState(false);
  const [mySubId, setMySubId] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState<(typeof TABS)[number]>(TABS[0]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const [artistRes, postsRes, imagesRes, videosRes, linksRes, subsRes] =
          await Promise.all([
            api.get<Artist>(`/artists/${artistId}`),
            api.get<PaginatedResponse<Post>>(`/posts/?skip=0&limit=100`),
            api.get<PaginatedResponse<ArtistImage>>(`/artist-images/?skip=0&limit=100`),
            api.get<PaginatedResponse<ArtistVideo>>(`/artist-videos/?skip=0&limit=100`),
            api.get<PaginatedResponse<ArtistSocialLink>>(`/artist-social-links/?skip=0&limit=100`),
            api.get<PaginatedResponse<Subscription>>(`/subscriptions/?skip=0&limit=100`),
          ]);

        setArtist(artistRes);

        // 아티스트 포스트
        const artistPosts = postsRes.items
          .filter((p) => p.author_id === artistId && p.is_artist_post)
          .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
        setPosts(artistPosts);

        // 팬 포스트
        const fPosts = postsRes.items
          .filter((p) => p.author_id === artistId && !p.is_artist_post)
          .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
        setFanPosts(fPosts);

        // 이미지
        setImages(
          imagesRes.items
            .filter((i) => i.artist_id === artistId)
            .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
        );

        // 영상
        setVideos(
          videosRes.items
            .filter((v) => v.artist_id === artistId)
            .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
        );

        // 소셜 링크
        setSocialLinks(
          linksRes.items
            .filter((l) => l.artist_id === artistId && l.is_active)
            .sort((a, b) => a.priority - b.priority)
        );

        // 구독자 수 + 내 구독 여부
        const artistSubs = subsRes.items.filter(
          (s) => s.artist_id === artistId && s.status === "subscribed"
        );
        setSubscriberCount(artistSubs.length);

        if (user) {
          const mySub = artistSubs.find((s) => s.fan_id === user.id);
          setIsSubscribed(!!mySub);
          setMySubId(mySub?.id ?? null);
        }
      } catch {
        setArtist(null);
      } finally {
        setLoading(false);
      }
    })();
  }, [artistId, user]);

  const handleSubscribeToggle = async () => {
    if (!user) return;
    try {
      if (isSubscribed && mySubId) {
        await api.delete(`/subscriptions/${mySubId}`);
        setIsSubscribed(false);
        setMySubId(null);
        setSubscriberCount((c) => Math.max(0, c - 1));
      } else {
        const newSub = await api.post<Subscription>("/subscriptions/", {
          fan_id: user.id,
          artist_id: artistId,
          status: "subscribed",
          payments_type: "free",
          start_date: new Date().toISOString().split("T")[0],
        });
        setIsSubscribed(true);
        setMySubId(newSub.id);
        setSubscriberCount((c) => c + 1);
      }
    } catch {
      // 실패 시 무시
    }
  };

  if (loading) {
    return (
      <div className="artist-detail-page">
        <div className="feed-empty">로딩 중...</div>
      </div>
    );
  }

  if (!artist) {
    return (
      <div className="artist-detail-page">
        <div className="feed-empty">아티스트를 찾을 수 없습니다</div>
      </div>
    );
  }

  return (
    <div className="artist-detail-page">
      {/* 프로필 헤더 */}
      <div className="artist-profile-header">
        <div className="artist-cover" />
        <div className="artist-profile-info">
          <div className="artist-avatar-large">
            <span className="artist-avatar-text">{artist.stage_name[0]}</span>
          </div>
          <h1 className="artist-name">{artist.stage_name}</h1>
          <p className="artist-bio">{artist.notes ?? "소개가 아직 없습니다."}</p>
          {socialLinks.length > 0 && (
            <div className="artist-social-links">
              {socialLinks.map((link) => (
                <a
                  key={link.id}
                  href={link.url}
                  className="artist-social-link"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {link.platform_name}
                </a>
              ))}
            </div>
          )}
          <button
            className={`artist-subscribe-btn ${isSubscribed ? "subscribed" : ""}`}
            onClick={handleSubscribeToggle}
          >
            {isSubscribed ? "구독중" : "구독하기"}
          </button>
        </div>
      </div>

      {/* 통계 */}
      <div className="artist-stats">
        <div className="artist-stat-item">
          <div className="artist-stat-value">{subscriberCount}</div>
          <div className="artist-stat-label">구독자</div>
        </div>
        <div className="artist-stat-item">
          <div className="artist-stat-value">{posts.length}</div>
          <div className="artist-stat-label">게시글</div>
        </div>
        <div className="artist-stat-item">
          <div className="artist-stat-value">{images.length}</div>
          <div className="artist-stat-label">이미지</div>
        </div>
      </div>

      {/* 콘텐츠 탭 */}
      <nav className="artist-content-tabs">
        {TABS.map((tab) => (
          <button
            key={tab}
            className={`artist-content-tab ${activeTab === tab ? "active" : ""}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </button>
        ))}
      </nav>

      {/* 콘텐츠 피드 */}
      <div className="artist-feed-container">
        {activeTab === "유저 포스트" && (
          <div className="artist-feed-list">
            {fanPosts.length > 0 ? (
              fanPosts.map((post) => <PostCard key={post.id} post={post} />)
            ) : (
              <div className="feed-empty">유저 포스트가 아직 없습니다</div>
            )}
          </div>
        )}

        {activeTab === "아티스트 포스트" && (
          <div className="artist-feed-list">
            {posts.length > 0 ? (
              posts.map((post) => <PostCard key={post.id} post={post} />)
            ) : (
              <div className="feed-empty">아티스트 포스트가 아직 없습니다</div>
            )}
          </div>
        )}

        {activeTab === "이미지" &&
          (images.length > 0 ? (
            <ImageGrid images={images} />
          ) : (
            <div className="feed-empty">이미지가 아직 없습니다</div>
          ))}

        {activeTab === "동영상" && (
          <div className="artist-feed-list">
            {videos.length > 0 ? (
              videos.map((video) => <VideoCard key={video.id} video={video} />)
            ) : (
              <div className="feed-empty">동영상이 아직 없습니다</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
