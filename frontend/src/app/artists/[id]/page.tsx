"use client";

import { useState, useEffect, useMemo } from "react";
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
  Event,
  PaginatedResponse,
  SearchFilterState,
} from "../../data/types";
import PostCard from "../../components/PostCard/PostCard";
import ImageGrid from "../../components/ImageGrid/ImageGrid";
import VideoCard from "../../components/VideoCard/VideoCard";
import Calendar from "../../components/Calendar/Calendar";
import SearchFilters from "../../components/SearchFilters/SearchFilters";
import "./artist-detail.css";
import "../../search/search.css";

const TABS = ["유저 포스트", "아티스트 포스트", "이미지", "동영상", "이벤트", "검색"] as const;

const SEARCH_CATEGORIES = ["전체", "게시글", "이미지", "동영상", "이벤트"] as const;

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
  const artistId = Number(params.id);
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
  const [activeTab, setActiveTab] = useState<(typeof TABS)[number]>(TABS[0]);
  const [loading, setLoading] = useState(true);

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
        const [artistRes, postsRes, imagesRes, videosRes, linksRes, subsRes, eventsRes, tagsRes] =
          await Promise.all([
            api.get<Artist>(`/artists/${artistId}`),
            api.get<PaginatedResponse<Post>>(`/posts/?skip=0&limit=100`),
            api.get<PaginatedResponse<ArtistImage>>(`/artist-images/?skip=0&limit=100`),
            api.get<PaginatedResponse<ArtistVideo>>(`/artist-videos/?skip=0&limit=100`),
            api.get<PaginatedResponse<ArtistSocialLink>>(`/artist-social-links/?skip=0&limit=100`),
            api.get<PaginatedResponse<Subscription>>(`/subscriptions/?skip=0&limit=100`),
            api.get<PaginatedResponse<Event>>(`/events/?skip=0&limit=100`),
            api.get<string[]>("/tags").catch(() => [] as string[]),
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

  // 이벤트 날짜 목록 (달력 표시용)
  const eventDates = useMemo(
    () => events.map((e) => e.event_date).filter((d): d is string => d !== null),
    [events],
  );

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

  // 검색 탭 필터링
  const searchResults = useMemo(() => {
    const q = searchQuery.toLowerCase();
    const allPosts = [...posts, ...fanPosts];

    let filteredPosts = [...allPosts];
    let filteredImages = [...images];
    let filteredVideos = [...videos];
    let filteredEvents = [...events];

    // 날짜 필터 (달력 선택)
    if (selectedDate) {
      const y = selectedDate.getFullYear();
      const m = String(selectedDate.getMonth() + 1).padStart(2, "0");
      const d = String(selectedDate.getDate()).padStart(2, "0");
      const dateStr = `${y}-${m}-${d}`;
      filteredPosts = filteredPosts.filter((p) => p.published_date === dateStr);
      filteredEvents = filteredEvents.filter((e) => e.event_date && e.event_date === dateStr);
    }

    // 텍스트 검색
    if (q) {
      filteredPosts = filteredPosts.filter(
        (p) =>
          p.content?.toLowerCase().includes(q) ||
          p.tags?.some((t) => t.toLowerCase().includes(q)) ||
          p.author_name?.toLowerCase().includes(q)
      );
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
      filteredPosts = filteredPosts.filter((p) => p.tags?.some((t) => searchFilters.tags.includes(t)));
    }

    // 공개 범위
    if (searchFilters.visibility !== "all") {
      filteredPosts = filteredPosts.filter((p) => p.visibility === searchFilters.visibility);
      filteredImages = filteredImages.filter((i) => i.visibility === searchFilters.visibility);
      filteredVideos = filteredVideos.filter((v) => v.visibility === searchFilters.visibility);
    }

    // 기간 범위
    if (searchFilters.dateRange.start) {
      filteredPosts = filteredPosts.filter((p) => p.published_date && p.published_date >= searchFilters.dateRange.start!);
      filteredEvents = filteredEvents.filter((e) => e.event_date && e.event_date >= searchFilters.dateRange.start!);
    }
    if (searchFilters.dateRange.end) {
      filteredPosts = filteredPosts.filter((p) => p.published_date && p.published_date <= searchFilters.dateRange.end!);
      filteredEvents = filteredEvents.filter((e) => e.event_date && e.event_date <= searchFilters.dateRange.end!);
    }

    // 정렬
    if (searchFilters.sortOrder === "latest") {
      filteredPosts.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
    } else if (searchFilters.sortOrder === "oldest") {
      filteredPosts.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
    }

    return { posts: filteredPosts, images: filteredImages, videos: filteredVideos, events: filteredEvents };
  }, [searchQuery, selectedDate, searchFilters, posts, fanPosts, images, videos, events]);

  const hasSearchQuery = searchQuery || selectedDate || searchFilters.tags.length > 0 || searchFilters.dateRange.start || searchFilters.dateRange.end || searchFilters.visibility !== "all";
  const totalSearchResults = searchResults.posts.length + searchResults.images.length + searchResults.videos.length + searchResults.events.length;

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
              eventDates={eventDates}
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

              {/* 게시글 결과 */}
              {(searchFilters.category === "전체" || searchFilters.category === "게시글") &&
                searchResults.posts.length > 0 && (
                  <div className="search-result-section">
                    <div className="search-result-section-title">게시글</div>
                    {searchResults.posts.map((post) => (
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
    </div>
  );
}
