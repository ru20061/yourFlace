"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "../lib/auth-context";
import { api, apiFetch } from "../lib/api";
import { getRelativeTime } from "../lib/utils";
import type { Creator, Subscription, CreatorCategory, CreatorCategoryMap, Magazine, PaginatedResponse } from "./data/types";
import "./home.css";

export default function HomePage() {
  const router = useRouter();
  const { user, isLoggedIn } = useAuth();

  const [allCreators, setAllCreators] = useState<Creator[]>([]);
  const [subscribedIds, setSubscribedIds] = useState<Set<number>>(new Set());
  const [categoryMap, setCategoryMap] = useState<Map<number, string>>(new Map());
  const [subCounts, setSubCounts] = useState<Map<number, number>>(new Map());
  const [news, setNews] = useState<Magazine[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        // 크리에이터, 구독, 카테고리 맵, 카테고리, 뉴스 병렬 조회
        const [creatorsRes, subsRes, catMapRes, catsRes, newsRes] = await Promise.all([
          api.get<PaginatedResponse<Creator>>("/creators/?skip=0&limit=100"),
          isLoggedIn
            ? api.get<PaginatedResponse<Subscription>>("/subscriptions/?skip=0&limit=100")
            : Promise.resolve({ items: [], total: 0, skip: 0, limit: 0 } as PaginatedResponse<Subscription>),
          api.get<PaginatedResponse<CreatorCategoryMap>>("/creator-category-map/?skip=0&limit=100"),
          api.get<PaginatedResponse<CreatorCategory>>("/creator-categories/?skip=0&limit=100"),
          apiFetch<PaginatedResponse<Magazine>>("/magazines/public?skip=0&limit=10")
            .catch(() => ({ items: [], total: 0, skip: 0, limit: 0 } as PaginatedResponse<Magazine>)),
        ]);

        // 전체 크리에이터 (active만)
        setAllCreators(creatorsRes.items.filter((a) => a.status === "active"));

        // 내가 구독한 크리에이터 ID
        if (user) {
          const mySubIds = new Set(
            subsRes.items
              .filter((s) => s.fan_id === user.id && s.status === "subscribed")
              .map((s) => s.creator_id)
          );
          setSubscribedIds(mySubIds);
        }

        // 카테고리 맵 (creator_id → category_name)
        const catById = new Map(catsRes.items.map((c) => [c.id, c.name]));
        const artCatMap = new Map<number, string>();
        catMapRes.items.forEach((m) => {
          const catName = catById.get(m.category_id);
          if (catName) artCatMap.set(m.creator_id, catName);
        });
        setCategoryMap(artCatMap);

        // 크리에이터별 구독자 수 계산
        const counts = new Map<number, number>();
        subsRes.items
          .filter((s) => s.status === "subscribed")
          .forEach((s) => {
            counts.set(s.creator_id, (counts.get(s.creator_id) || 0) + 1);
          });
        setSubCounts(counts);

        // 뉴스
        setNews(newsRes.items);
      } catch {
        // API 실패 시 빈 상태
      } finally {
        setLoading(false);
      }
    })();
  }, [user, isLoggedIn]);

  if (loading) {
    return (
      <div className="home-page">
        <div className="feed-empty">로딩 중...</div>
      </div>
    );
  }

  return (
    <div className="home-page">
      {/* 전체 크리에이터 */}
      <div className="home-section">
        <h1 className="home-title">전체 크리에이터</h1>
        <p className="home-subtitle">좋아하는 크리에이터를 만나보세요</p>
      </div>

      {allCreators.length > 0 ? (
        <div className="artist-selection-grid">
          {allCreators.map((creator) => {
            const isSubscribed = subscribedIds.has(creator.id);
            return (
              <button
                key={creator.id}
                className="artist-selection-card"
                onClick={() => router.push(`/creators/${creator.slug}`)}
              >
                <div className={`artist-selection-cover${isSubscribed ? "" : " other"}`} />
                <div className={`artist-selection-avatar${isSubscribed ? "" : " other"}`}>
                  <span className="artist-selection-avatar-text">
                    {creator.stage_name[0]}
                  </span>
                </div>
                <div className="artist-selection-info">
                  <div className="artist-selection-name">{creator.stage_name}</div>
                  {categoryMap.get(creator.id) && (
                    <div className="artist-selection-category">{categoryMap.get(creator.id)}</div>
                  )}
                  <div className="artist-selection-subs">구독자 {subCounts.get(creator.id) || 0}명</div>
                </div>
                {isSubscribed && (
                  <div className="artist-selection-badge subscribed">구독중</div>
                )}
              </button>
            );
          })}
        </div>
      ) : (
        <div className="feed-empty">등록된 크리에이터가 없습니다.</div>
      )}

      {/* Flace News */}
      <div className="home-section news-section">
        <h2 className="home-title-sub">Flace News</h2>
        <p className="home-subtitle">최신 매거진 소식을 확인하세요</p>
      </div>

      {news.length > 0 ? (
        <div className="news-grid">
          {news.map((item) => (
            <article
              key={item.id}
              className="news-card"
              onClick={() => router.push(`/magazines/${item.slug}`)}
              style={{ cursor: "pointer" }}
            >
              <div className="news-card-badge">NEWS</div>
              <h3 className="news-card-title">{item.title}</h3>
              <p className="news-card-content">
                {(item.summary || item.content).length > 120
                  ? (item.summary || item.content).slice(0, 120) + "..."
                  : (item.summary || item.content)}
              </p>
              <div className="news-card-footer">
                <span className="news-card-date">{getRelativeTime(item.created_at)}</span>
              </div>
            </article>
          ))}
        </div>
      ) : (
        <div className="feed-empty">뉴스가 없습니다.</div>
      )}
    </div>
  );
}
