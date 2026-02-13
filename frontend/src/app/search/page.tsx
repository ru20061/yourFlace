"use client";

import { useState, useEffect, useMemo } from "react";
import Link from "next/link";
import Calendar from "../components/Calendar/Calendar";
import PostCard from "../components/PostCard/PostCard";
import SearchFilters from "../components/SearchFilters/SearchFilters";
import { api } from "../../lib/api";
import type { Artist, Post, Event, PaginatedResponse, SearchFilterState } from "../data/types";
import "./search.css";

const CATEGORIES = ["전체", "아티스트", "게시글", "이벤트", "상품"] as const;

const DEFAULT_FILTERS: SearchFilterState = {
  category: "전체",
  tags: [],
  sortOrder: "latest",
  dateRange: { start: null, end: null },
  visibility: "all",
  query: "",
};

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [dateInputText, setDateInputText] = useState("");
  const [dateError, setDateError] = useState("");
  const [filters, setFilters] = useState<SearchFilterState>(DEFAULT_FILTERS);
  const [showAdvanced, setShowAdvanced] = useState(false);

  const [allPosts, setAllPosts] = useState<Post[]>([]);
  const [allArtists, setAllArtists] = useState<Artist[]>([]);
  const [allEvents, setAllEvents] = useState<Event[]>([]);
  const [allTags, setAllTags] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const [postsRes, artistsRes, eventsRes, tagsRes] = await Promise.all([
          api.get<PaginatedResponse<Post>>("/posts/?limit=200"),
          api.get<PaginatedResponse<Artist>>("/artists/?limit=200"),
          api.get<PaginatedResponse<Event>>("/events/?limit=200"),
          api.get<string[]>("/tags"),
        ]);
        setAllPosts(postsRes.items);
        setAllArtists(artistsRes.items);
        setAllEvents(eventsRes.items);
        setAllTags(tagsRes);
      } catch {
        console.error("검색 데이터 로드 실패");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const eventDates = useMemo(
    () => allEvents.map((e) => e.event_date).filter((d): d is string => d !== null),
    [allEvents],
  );

  // 텍스트 날짜 파싱
  const handleDateTextSubmit = () => {
    const text = dateInputText.trim();
    if (!text) {
      setSelectedDate(null);
      setDateError("");
      return;
    }

    // ISO 형식: 2026-02-13 또는 2026-2-3
    const isoMatch = text.match(/^(\d{4})-(\d{1,2})-(\d{1,2})$/);
    if (isoMatch) {
      const d = new Date(Number(isoMatch[1]), Number(isoMatch[2]) - 1, Number(isoMatch[3]));
      if (!isNaN(d.getTime())) {
        setSelectedDate(d);
        setDateError("");
        return;
      }
    }

    // 한국어 형식: 2026년 2월 13일
    const koMatch = text.match(/(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일/);
    if (koMatch) {
      const d = new Date(Number(koMatch[1]), Number(koMatch[2]) - 1, Number(koMatch[3]));
      if (!isNaN(d.getTime())) {
        setSelectedDate(d);
        setDateError("");
        return;
      }
    }

    setDateError("올바른 형식으로 입력하세요 (예: 2026-02-13 또는 2026년 2월 13일)");
  };

  // 달력에서 날짜 선택
  const handleDateSelect = (date: Date) => {
    setSelectedDate(date);
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, "0");
    const d = String(date.getDate()).padStart(2, "0");
    setDateInputText(`${y}-${m}-${d}`);
    setDateError("");
  };

  // 날짜 선택 해제
  const clearDate = () => {
    setSelectedDate(null);
    setDateInputText("");
    setDateError("");
  };

  // 필터링 로직
  const filteredResults = useMemo(() => {
    const q = query.toLowerCase();

    let posts = [...allPosts];
    let artists = [...allArtists];
    let events = [...allEvents];

    // 텍스트 검색
    if (q) {
      posts = posts.filter(
        (p) =>
          p.content?.toLowerCase().includes(q) ||
          p.tags?.some((t) => t.toLowerCase().includes(q)) ||
          p.author_name?.toLowerCase().includes(q)
      );
      artists = artists.filter(
        (a) =>
          a.stage_name.toLowerCase().includes(q) ||
          a.notes?.toLowerCase().includes(q)
      );
      events = events.filter(
        (e) =>
          e.title.toLowerCase().includes(q) ||
          e.description?.toLowerCase().includes(q)
      );
    }

    // 날짜 필터
    if (selectedDate) {
      const y = selectedDate.getFullYear();
      const m = String(selectedDate.getMonth() + 1).padStart(2, "0");
      const d = String(selectedDate.getDate()).padStart(2, "0");
      const dateStr = `${y}-${m}-${d}`;
      posts = posts.filter((p) => p.published_date === dateStr);
      events = events.filter((e) => e.event_date && e.event_date === dateStr);
    }

    // 태그 필터 (OR)
    if (filters.tags.length > 0) {
      posts = posts.filter((p) => p.tags?.some((t) => filters.tags.includes(t)));
    }

    // 공개 범위
    if (filters.visibility !== "all") {
      posts = posts.filter((p) => p.visibility === filters.visibility);
    }

    // 기간 범위
    if (filters.dateRange.start) {
      posts = posts.filter((p) => p.published_date && p.published_date >= filters.dateRange.start!);
      events = events.filter((e) => e.event_date && e.event_date >= filters.dateRange.start!);
    }
    if (filters.dateRange.end) {
      posts = posts.filter((p) => p.published_date && p.published_date <= filters.dateRange.end!);
      events = events.filter((e) => e.event_date && e.event_date <= filters.dateRange.end!);
    }

    // 정렬
    if (filters.sortOrder === "latest") {
      posts.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
    } else if (filters.sortOrder === "oldest") {
      posts.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
    }

    return { posts, artists, events };
  }, [query, selectedDate, filters, allPosts, allArtists, allEvents]);

  const hasQuery = query || selectedDate || filters.tags.length > 0 || filters.dateRange.start || filters.dateRange.end || filters.visibility !== "all";
  const totalResults = filteredResults.posts.length + filteredResults.artists.length + filteredResults.events.length;

  if (loading) {
    return <div className="search-page"><div className="feed-empty">로딩 중...</div></div>;
  }

  return (
    <div className="search-page">
      <h1 className="search-title">검색</h1>

      {/* 검색바 */}
      <div className="search-bar">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
        <input
          type="text"
          placeholder="아티스트, 이벤트, 게시글 검색..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        {query && (
          <button className="search-clear-btn" onClick={() => setQuery("")} type="button">
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
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            type="button"
            className={`search-filter-chip ${filters.category === cat ? "active" : ""}`}
            onClick={() => setFilters((f) => ({ ...f, category: cat }))}
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
        <SearchFilters filters={filters} onFiltersChange={setFilters} tags={allTags} />
      )}

      {/* 검색 결과 */}
      <div className="search-results">
        {hasQuery && totalResults > 0 && (
          <div className="search-result-count">검색 결과 {totalResults}건</div>
        )}

        {/* 아티스트 결과 */}
        {(filters.category === "전체" || filters.category === "아티스트") &&
          filteredResults.artists.length > 0 && (
            <div className="search-result-section">
              <div className="search-result-section-title">아티스트</div>
              {filteredResults.artists.map((artist) => (
                <Link
                  key={artist.id}
                  href={`/artists/${artist.id}`}
                  className="search-artist-card"
                >
                  <div className="search-artist-avatar">
                    {artist.stage_name[0]}
                  </div>
                  <div className="search-artist-info">
                    <div className="search-artist-name">{artist.stage_name}</div>
                    <div className="search-artist-bio">{artist.notes}</div>
                  </div>
                </Link>
              ))}
            </div>
          )}

        {/* 게시글 결과 */}
        {(filters.category === "전체" || filters.category === "게시글") &&
          filteredResults.posts.length > 0 && (
            <div className="search-result-section">
              <div className="search-result-section-title">게시글</div>
              {filteredResults.posts.map((post) => (
                <PostCard key={post.id} post={post} />
              ))}
            </div>
          )}

        {/* 이벤트 결과 */}
        {(filters.category === "전체" || filters.category === "이벤트") &&
          filteredResults.events.length > 0 && (
            <div className="search-result-section">
              <div className="search-result-section-title">이벤트</div>
              {filteredResults.events.map((event) => (
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
        {!hasQuery && (
          <div className="feed-empty">검색어를 입력하거나 날짜를 선택하세요</div>
        )}
        {hasQuery && totalResults === 0 && (
          <div className="feed-empty">검색 결과가 없습니다</div>
        )}
      </div>
    </div>
  );
}
