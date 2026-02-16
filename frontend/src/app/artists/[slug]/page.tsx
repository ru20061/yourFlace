"use client";

import { useState, useEffect, useMemo } from "react";
import { useParams, useRouter } from "next/navigation";
import { useAuth } from "../../../lib/auth-context";
import { api } from "../../../lib/api";
import type {
  Artist,
  Post,
  ArtistImage,
  ArtistVideo,
  ArtistSocialLink,
  Subscription,
  Event,
  PaginatedResponse,
  SearchFilterState,
} from "../../data/types";
import PostCard from "../../components/PostCard/PostCard";
import ImageGrid from "../../components/ImageGrid/ImageGrid";
import VideoCard from "../../components/VideoCard/VideoCard";
import Calendar, { type CalendarItem } from "../../components/Calendar/Calendar";
import SearchFilters from "../../components/SearchFilters/SearchFilters";
import "./artist-detail.css";
import "../../search/search.css";

const TABS = ["유저 포스트", "아티스트 포스트", "이미지", "동영상", "이벤트", "검색"] as const;

const SEARCH_CATEGORIES = ["전체", "유저 포스트", "아티스트 포스트", "이미지", "동영상", "이벤트"] as const;

const DEFAULT_FILTERS: SearchFilterState = {
  category: "전체",
  tags: [],
  sortOrder: "latest",
  dateRange: { start: null, end: null },
  visibility: "all",
  query: "",
};

export default function ArtistDetailPage() {
  const params = useParams();
  const router = useRouter();
  const slug = decodeURIComponent(params.slug as string);
  const { user, isLoading: authLoading } = useAuth();

  const [artist, setArtist] = useState<Artist | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);
  const [fanPosts, setFanPosts] = useState<Post[]>([]);
  const [images, setImages] = useState<ArtistImage[]>([]);
  const [videos, setVideos] = useState<ArtistVideo[]>([]);
  const [events, setEvents] = useState<Event[]>([]);
  const [socialLinks, setSocialLinks] = useState<ArtistSocialLink[]>([]);
  const [subscriberCount, setSubscriberCount] = useState(0);
  const [isSubscribed, setIsSubscribed] = useState(false);
  const [mySubId, setMySubId] = useState<number | null>(null);
  const [myFanNickname, setMyFanNickname] = useState<string | null>(null);
  const [myFanProfileImage, setMyFanProfileImage] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<(typeof TABS)[number]>(TABS[0]);
  const [loading, setLoading] = useState(true);

  // 포스트 작성 모달
  const [showWriteModal, setShowWriteModal] = useState(false);
  const [writeContent, setWriteContent] = useState("");
  const [writeVisibility, setWriteVisibility] = useState<"public" | "user">("public");
  const [writeTagsInput, setWriteTagsInput] = useState("");
  const [writeSubmitting, setWriteSubmitting] = useState(false);
  const [writeError, setWriteError] = useState("");

  // 검색 탭 상태
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [dateInputText, setDateInputText] = useState("");
  const [dateError, setDateError] = useState("");
  const [searchFilters, setSearchFilters] = useState<SearchFilterState>(DEFAULT_FILTERS);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [allTags, setAllTags] = useState<string[]>([]);

  useEffect(() => {
    (async () => {
      try {
        // slug로 아티스트 조회
        const artistRes = await api.get<Artist>(`/artists/by-slug/${encodeURIComponent(slug)}`);
        setArtist(artistRes);
        const artistId = artistRes.id;

        const [postsRes, imagesRes, videosRes, linksRes, subsRes, eventsRes, tagsRes] =
          await Promise.all([
            api.get<PaginatedResponse<Post>>(`/posts/?skip=0&limit=100`),
            api.get<PaginatedResponse<ArtistImage>>(`/artist-images/?skip=0&limit=100`),
            api.get<PaginatedResponse<ArtistVideo>>(`/artist-videos/?skip=0&limit=100`),
            api.get<PaginatedResponse<ArtistSocialLink>>(`/artist-social-links/?skip=0&limit=100`),
            api.get<PaginatedResponse<Subscription>>(`/subscriptions/?skip=0&limit=100`),
            api.get<PaginatedResponse<Event>>(`/events/?skip=0&limit=100`),
            api.get<string[]>("/tags").catch(() => [] as string[]),
          ]);

        // 아티스트 포스트 (백엔드에서 author_name 포함)
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

        // 이벤트 (이 아티스트 관련)
        setEvents(
          eventsRes.items
            .filter((e) => e.artist_id === artistId)
            .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
        );

        // 태그
        setAllTags(tagsRes);

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
          setMyFanNickname(mySub?.fan_nickname ?? null);
          setMyFanProfileImage(mySub?.fan_profile_image ?? null);
        }
      } catch {
        setArtist(null);
      } finally {
        setLoading(false);
      }
    })();
  }, [slug, user]);

  const handleSubscribe = () => {
    if (!user || isSubscribed) return;
    router.push(`/artists/${slug}/subscribe`);
  };

  // 포스트 작성
  const handleWritePost = async () => {
    if (!user || !artist || !writeContent.trim()) return;
    setWriteSubmitting(true);
    setWriteError("");
    try {
      const tags = writeTagsInput.split(",").map((t) => t.trim()).filter(Boolean);
      const created = await api.post<Post>("/posts", {
        author_id: artist.id,
        author_type: "fan" as const,
        content: writeContent.trim(),
        write_id: user.id,
        write_role: "fan" as const,
        visibility: writeVisibility,
        tags: tags.length > 0 ? tags : null,
      });
      // 구독 닉네임으로 로컬 목록에 추가
      setFanPosts((prev) => [{
        ...created,
        author_name: myFanNickname ?? user.nickname ?? undefined,
        author_profile_image: myFanProfileImage ?? user.profile_image ?? undefined,
      }, ...prev]);
      setShowWriteModal(false);
      setWriteContent("");
      setWriteVisibility("public");
      setWriteTagsInput("");
    } catch {
      setWriteError("포스트 작성에 실패했습니다. 다시 시도해주세요.");
    } finally {
      setWriteSubmitting(false);
    }
  };

  // 캘린더용 날짜별 콘텐츠 맵 생성
  const calendarDateItems = useMemo(() => {
    const map: Record<string, CalendarItem[]> = {};
    const add = (dateKey: string, item: CalendarItem) => {
      if (!map[dateKey]) map[dateKey] = [];
      map[dateKey].push(item);
    };
    const toDate = (s: string) => s.slice(0, 10);

    for (const p of fanPosts) {
      add(toDate(p.published_date || p.created_at), { type: "fanPost", label: "유저 포스트" });
    }
    for (const p of posts) {
      add(toDate(p.published_date || p.created_at), { type: "artistPost", label: "아티스트 포스트" });
    }
    for (const i of images) {
      add(toDate(i.published_date || i.created_at), { type: "image", label: "이미지" });
    }
    for (const v of videos) {
      add(toDate(v.published_date || v.created_at), { type: "video", label: "동영상" });
    }
    for (const e of events) {
      add(toDate(e.event_date || e.created_at), { type: "event", label: e.title });
    }
    return map;
  }, [fanPosts, posts, images, videos, events]);

  // 텍스트 날짜 파싱
  const handleDateTextSubmit = () => {
    const text = dateInputText.trim();
    if (!text) {
      setSelectedDate(null);
      setDateError("");
      return;
    }
    const isoMatch = text.match(/^(\d{4})-(\d{1,2})-(\d{1,2})$/);
    if (isoMatch) {
      const d = new Date(Number(isoMatch[1]), Number(isoMatch[2]) - 1, Number(isoMatch[3]));
      if (!isNaN(d.getTime())) { setSelectedDate(d); setDateError(""); return; }
    }
    const koMatch = text.match(/(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일/);
    if (koMatch) {
      const d = new Date(Number(koMatch[1]), Number(koMatch[2]) - 1, Number(koMatch[3]));
      if (!isNaN(d.getTime())) { setSelectedDate(d); setDateError(""); return; }
    }
    setDateError("올바른 형식으로 입력하세요 (예: 2026-02-13 또는 2026년 2월 13일)");
  };

  const handleDateSelect = (date: Date) => {
    setSelectedDate(date);
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, "0");
    const d = String(date.getDate()).padStart(2, "0");
    setDateInputText(`${y}-${m}-${d}`);
    setDateError("");
  };

  const clearDate = () => {
    setSelectedDate(null);
    setDateInputText("");
    setDateError("");
  };

  // created_at에서 YYYY-MM-DD 추출
  const toDateStr = (isoStr: string) => isoStr.slice(0, 10);

  // 유효 날짜 추출 (YYYY-MM-DD로 정규화, published_date/event_date 우선 → created_at fallback)
  const postDate = (p: Post) => toDateStr(p.published_date || p.created_at);
  const imageDate = (i: ArtistImage) => toDateStr(i.published_date || i.created_at);
  const videoDate = (v: ArtistVideo) => toDateStr(v.published_date || v.created_at);
  const eventDate = (e: Event) => toDateStr(e.event_date || e.created_at);

  // 검색 탭 필터링
  const searchResults = useMemo(() => {
    const q = searchQuery.toLowerCase();

    let filteredFanPosts = [...fanPosts];
    let filteredArtistPosts = [...posts];
    let filteredImages = [...images];
    let filteredVideos = [...videos];
    let filteredEvents = [...events];

    // 날짜 필터 (달력 선택)
    if (selectedDate) {
      const y = selectedDate.getFullYear();
      const m = String(selectedDate.getMonth() + 1).padStart(2, "0");
      const d = String(selectedDate.getDate()).padStart(2, "0");
      const dateStr = `${y}-${m}-${d}`;
      filteredFanPosts = filteredFanPosts.filter((p) => postDate(p) === dateStr);
      filteredArtistPosts = filteredArtistPosts.filter((p) => postDate(p) === dateStr);
      filteredImages = filteredImages.filter((i) => imageDate(i) === dateStr);
      filteredVideos = filteredVideos.filter((v) => videoDate(v) === dateStr);
      filteredEvents = filteredEvents.filter((e) => eventDate(e) === dateStr);
    }

    // 텍스트 검색
    if (q) {
      const filterPost = (p: Post) =>
        p.content?.toLowerCase().includes(q) ||
        p.title_field?.toLowerCase().includes(q) ||
        p.tags?.some((t) => t.toLowerCase().includes(q)) ||
        p.author_name?.toLowerCase().includes(q);
      filteredFanPosts = filteredFanPosts.filter(filterPost);
      filteredArtistPosts = filteredArtistPosts.filter(filterPost);
      filteredImages = filteredImages.filter(
        (i) =>
          i.image_purpose?.toLowerCase().includes(q) ||
          i.tags?.some((t) => t.toLowerCase().includes(q))
      );
      filteredVideos = filteredVideos.filter(
        (v) =>
          v.title?.toLowerCase().includes(q) ||
          v.description?.toLowerCase().includes(q)
      );
      filteredEvents = filteredEvents.filter(
        (e) =>
          e.title.toLowerCase().includes(q) ||
          e.description?.toLowerCase().includes(q)
      );
    }

    // 태그 필터
    if (searchFilters.tags.length > 0) {
      filteredFanPosts = filteredFanPosts.filter((p) => p.tags?.some((t) => searchFilters.tags.includes(t)));
      filteredArtistPosts = filteredArtistPosts.filter((p) => p.tags?.some((t) => searchFilters.tags.includes(t)));
    }

    // 공개 범위
    if (searchFilters.visibility !== "all") {
      filteredFanPosts = filteredFanPosts.filter((p) => p.visibility === searchFilters.visibility);
      filteredArtistPosts = filteredArtistPosts.filter((p) => p.visibility === searchFilters.visibility);
      filteredImages = filteredImages.filter((i) => i.visibility === searchFilters.visibility);
      filteredVideos = filteredVideos.filter((v) => v.visibility === searchFilters.visibility);
    }

    // 기간 범위
    if (searchFilters.dateRange.start) {
      const start = searchFilters.dateRange.start;
      filteredFanPosts = filteredFanPosts.filter((p) => postDate(p) >= start);
      filteredArtistPosts = filteredArtistPosts.filter((p) => postDate(p) >= start);
      filteredImages = filteredImages.filter((i) => imageDate(i) >= start);
      filteredVideos = filteredVideos.filter((v) => videoDate(v) >= start);
      filteredEvents = filteredEvents.filter((e) => eventDate(e) >= start);
    }
    if (searchFilters.dateRange.end) {
      const end = searchFilters.dateRange.end;
      filteredFanPosts = filteredFanPosts.filter((p) => postDate(p) <= end);
      filteredArtistPosts = filteredArtistPosts.filter((p) => postDate(p) <= end);
      filteredImages = filteredImages.filter((i) => imageDate(i) <= end);
      filteredVideos = filteredVideos.filter((v) => videoDate(v) <= end);
      filteredEvents = filteredEvents.filter((e) => eventDate(e) <= end);
    }

    // 정렬
    const sortFn = searchFilters.sortOrder === "oldest"
      ? (a: Post, b: Post) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
      : (a: Post, b: Post) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
    filteredFanPosts.sort(sortFn);
    filteredArtistPosts.sort(sortFn);

    return { fanPosts: filteredFanPosts, artistPosts: filteredArtistPosts, images: filteredImages, videos: filteredVideos, events: filteredEvents };
  }, [searchQuery, selectedDate, searchFilters, posts, fanPosts, images, videos, events]);

  const hasSearchQuery = searchQuery || selectedDate || searchFilters.category !== "전체" || searchFilters.tags.length > 0 || searchFilters.dateRange.start || searchFilters.dateRange.end || searchFilters.visibility !== "all";

  // 선택된 카테고리에 해당하는 결과만 카운트
  const totalSearchResults = useMemo(() => {
    const cat = searchFilters.category;
    let count = 0;
    if (cat === "전체" || cat === "유저 포스트") count += searchResults.fanPosts.length;
    if (cat === "전체" || cat === "아티스트 포스트") count += searchResults.artistPosts.length;
    if (cat === "전체" || cat === "이미지") count += searchResults.images.length;
    if (cat === "전체" || cat === "동영상") count += searchResults.videos.length;
    if (cat === "전체" || cat === "이벤트") count += searchResults.events.length;
    return count;
  }, [searchFilters.category, searchResults]);

  if (loading) {
    return (
      <div className="artist-detail-page">
        <div className="feed-empty">로딩 중...</div>
      </div>
    );
  }

  if (!authLoading && !user) {
    return (
      <div className="artist-detail-page">
        <div className="feed-empty">로그인 후 이용해주세요</div>
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
          {!isSubscribed && (
            <button
              className="artist-subscribe-btn"
              onClick={handleSubscribe}
            >
              구독하기
            </button>
          )}
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
            disabled={!isSubscribed}
          >
            {tab}
          </button>
        ))}
      </nav>

      {/* 구독 전 콘텐츠 잠금 */}
      {!isSubscribed ? (
        <div className="artist-content-locked">
          <div className="artist-locked-icon">
            <svg viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="currentColor" strokeWidth="1.5">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
              <path d="M7 11V7a5 5 0 0 1 10 0v4" />
            </svg>
          </div>
          <p className="artist-locked-title">구독자 전용 콘텐츠</p>
          <p className="artist-locked-desc">구독 후 {artist.stage_name}의 모든 콘텐츠를 확인할 수 있습니다</p>
          <button
            className="artist-subscribe-btn"
            onClick={() => router.push(`/artists/${slug}/subscribe`)}
          >
            구독하기
          </button>
        </div>
      ) : (
      /* 콘텐츠 피드 */
      <div className="artist-feed-container">
        {activeTab === "유저 포스트" && (
          <div className="artist-feed-list">
            <button
              className="artist-write-post-btn"
              onClick={() => setShowWriteModal(true)}
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="12" y1="5" x2="12" y2="19" />
                <line x1="5" y1="12" x2="19" y2="12" />
              </svg>
              포스트 작성
            </button>
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

        {/* 이벤트 탭 */}
        {activeTab === "이벤트" && (
          <div className="artist-feed-list">
            {events.length > 0 ? (
              events.map((event) => (
                <div key={event.id} className="search-event-card">
                  {event.event_date && (
                    <div className="search-event-date">
                      <div className="search-event-month">
                        {new Date(event.event_date).getMonth() + 1}월
                      </div>
                      <div className="search-event-day">
                        {new Date(event.event_date).getDate()}
                      </div>
                    </div>
                  )}
                  <div className="search-event-info">
                    <div className="search-event-title">{event.title}</div>
                    <div className="search-event-desc">{event.description}</div>
                    <div className="search-event-meta">
                      {event.location && <span>{event.location}</span>}
                      {event.max_participants && (
                        <span>최대 {event.max_participants}명</span>
                      )}
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="feed-empty">이벤트가 아직 없습니다</div>
            )}
          </div>
        )}

        {/* 검색 탭 */}
        {activeTab === "검색" && (
          <div className="search-page">
            {/* 검색바 */}
            <div className="search-bar">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="11" cy="11" r="8" />
                <line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
              <input
                type="text"
                placeholder={`${artist.stage_name}의 콘텐츠 검색...`}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              {searchQuery && (
                <button className="search-clear-btn" onClick={() => setSearchQuery("")} type="button">
                  &times;
                </button>
              )}
            </div>

            {/* 달력 */}
            <Calendar
              selectedDate={selectedDate}
              onDateSelect={handleDateSelect}
              dateItems={calendarDateItems}
            />

            {/* 텍스트 날짜 입력 */}
            <div className="search-date-input">
              <label className="search-date-label">날짜 직접 입력</label>
              <input
                type="text"
                className="search-date-text-input"
                placeholder="예: 2026-02-13 또는 2026년 2월 13일"
                value={dateInputText}
                onChange={(e) => {
                  setDateInputText(e.target.value);
                  setDateError("");
                }}
                onKeyDown={(e) => {
                  if (e.key === "Enter") handleDateTextSubmit();
                }}
              />
              <button className="search-date-apply-btn" onClick={handleDateTextSubmit} type="button">
                적용
              </button>
            </div>
            {dateError && <div className="search-date-error">{dateError}</div>}
            {selectedDate && (
              <div className="search-date-selected">
                <span>
                  선택된 날짜: {selectedDate.getFullYear()}년 {selectedDate.getMonth() + 1}월 {selectedDate.getDate()}일
                </span>
                <button className="search-date-clear" onClick={clearDate} type="button">&times;</button>
              </div>
            )}

            {/* 카테고리 필터 칩 */}
            <div className="search-filters">
              {SEARCH_CATEGORIES.map((cat) => (
                <button
                  key={cat}
                  type="button"
                  className={`search-filter-chip ${searchFilters.category === cat ? "active" : ""}`}
                  onClick={() => setSearchFilters((f) => ({ ...f, category: cat }))}
                >
                  {cat}
                </button>
              ))}
            </div>

            {/* 고급 필터 토글 */}
            <button
              className="search-advanced-toggle"
              onClick={() => setShowAdvanced(!showAdvanced)}
              type="button"
            >
              고급 필터 {showAdvanced ? "▲" : "▼"}
            </button>

            {showAdvanced && (
              <SearchFilters filters={searchFilters} onFiltersChange={setSearchFilters} tags={allTags} />
            )}

            {/* 검색 결과 */}
            <div className="search-results">
              {hasSearchQuery && totalSearchResults > 0 && (
                <div className="search-result-count">검색 결과 {totalSearchResults}건</div>
              )}

              {/* 유저 포스트 결과 */}
              {(searchFilters.category === "전체" || searchFilters.category === "유저 포스트") &&
                searchResults.fanPosts.length > 0 && (
                  <div className="search-result-section">
                    <div className="search-result-section-title">유저 포스트</div>
                    {searchResults.fanPosts.map((post) => (
                      <PostCard key={post.id} post={post} />
                    ))}
                  </div>
                )}

              {/* 아티스트 포스트 결과 */}
              {(searchFilters.category === "전체" || searchFilters.category === "아티스트 포스트") &&
                searchResults.artistPosts.length > 0 && (
                  <div className="search-result-section">
                    <div className="search-result-section-title">아티스트 포스트</div>
                    {searchResults.artistPosts.map((post) => (
                      <PostCard key={post.id} post={post} />
                    ))}
                  </div>
                )}

              {/* 이미지 결과 */}
              {(searchFilters.category === "전체" || searchFilters.category === "이미지") &&
                searchResults.images.length > 0 && (
                  <div className="search-result-section">
                    <div className="search-result-section-title">이미지</div>
                    <ImageGrid images={searchResults.images} />
                  </div>
                )}

              {/* 동영상 결과 */}
              {(searchFilters.category === "전체" || searchFilters.category === "동영상") &&
                searchResults.videos.length > 0 && (
                  <div className="search-result-section">
                    <div className="search-result-section-title">동영상</div>
                    {searchResults.videos.map((video) => (
                      <VideoCard key={video.id} video={video} />
                    ))}
                  </div>
                )}

              {/* 이벤트 결과 */}
              {(searchFilters.category === "전체" || searchFilters.category === "이벤트") &&
                searchResults.events.length > 0 && (
                  <div className="search-result-section">
                    <div className="search-result-section-title">이벤트</div>
                    {searchResults.events.map((event) => (
                      <div key={event.id} className="search-event-card">
                        {event.event_date && (
                          <div className="search-event-date">
                            <div className="search-event-month">
                              {new Date(event.event_date).getMonth() + 1}월
                            </div>
                            <div className="search-event-day">
                              {new Date(event.event_date).getDate()}
                            </div>
                          </div>
                        )}
                        <div className="search-event-info">
                          <div className="search-event-title">{event.title}</div>
                          <div className="search-event-desc">{event.description}</div>
                          <div className="search-event-meta">
                            {event.location && <span>{event.location}</span>}
                            {event.max_participants && (
                              <span>최대 {event.max_participants}명</span>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

              {/* 빈 상태 */}
              {!hasSearchQuery && (
                <div className="feed-empty">검색어를 입력하거나 날짜를 선택하세요</div>
              )}
              {hasSearchQuery && totalSearchResults === 0 && (
                <div className="feed-empty">검색 결과가 없습니다</div>
              )}
            </div>
          </div>
        )}
      </div>
      )}

      {/* 포스트 작성 모달 */}
      {showWriteModal && (
        <div className="write-modal-overlay" onClick={() => setShowWriteModal(false)}>
          <div className="write-modal" onClick={(e) => e.stopPropagation()}>
            <div className="write-modal-header">
              <h2>포스트 작성</h2>
              <button
                className="write-modal-close"
                onClick={() => setShowWriteModal(false)}
                aria-label="닫기"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </div>
            <div className="write-modal-body">
              <textarea
                className="write-textarea"
                placeholder="무슨 이야기를 나누고 싶으신가요?"
                value={writeContent}
                onChange={(e) => setWriteContent(e.target.value)}
                rows={6}
              />
              <div className="write-field">
                <label className="write-label">공개 범위</label>
                <select
                  className="write-select"
                  value={writeVisibility}
                  onChange={(e) => setWriteVisibility(e.target.value as "public" | "user")}
                >
                  <option value="public">전체 공개</option>
                  <option value="user">유저 공개</option>
                </select>
              </div>
              <div className="write-field">
                <label className="write-label">태그</label>
                <input
                  className="write-input"
                  type="text"
                  placeholder="쉼표로 구분 (예: 음악, 일상, 소식)"
                  value={writeTagsInput}
                  onChange={(e) => setWriteTagsInput(e.target.value)}
                />
              </div>
              {writeError && <p className="write-error">{writeError}</p>}
            </div>
            <div className="write-modal-footer">
              <button className="write-btn-cancel" onClick={() => setShowWriteModal(false)}>
                취소
              </button>
              <button
                className="write-btn-submit"
                onClick={handleWritePost}
                disabled={writeSubmitting || !writeContent.trim()}
              >
                {writeSubmitting ? "작성 중..." : "게시하기"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
