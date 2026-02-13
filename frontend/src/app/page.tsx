"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "../lib/auth-context";
import { api } from "../lib/api";
import type { Artist, Subscription, ArtistCategory, ArtistCategoryMap, PaginatedResponse } from "./data/types";
import "./home.css";

export default function HomePage() {
  const router = useRouter();
  const { user, isLoggedIn } = useAuth();

  const [allArtists, setAllArtists] = useState<Artist[]>([]);
  const [subscribedIds, setSubscribedIds] = useState<Set<number>>(new Set());
  const [categoryMap, setCategoryMap] = useState<Map<number, string>>(new Map());
  const [subCounts, setSubCounts] = useState<Map<number, number>>(new Map());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        // 아티스트, 구독, 카테고리 맵, 카테고리 병렬 조회
        const [artistsRes, subsRes, catMapRes, catsRes] = await Promise.all([
          api.get<PaginatedResponse<Artist>>("/artists/?skip=0&limit=100"),
          isLoggedIn
            ? api.get<PaginatedResponse<Subscription>>("/subscriptions/?skip=0&limit=100")
            : Promise.resolve({ items: [], total: 0, skip: 0, limit: 0 } as PaginatedResponse<Subscription>),
          api.get<PaginatedResponse<ArtistCategoryMap>>("/artist-category-map/?skip=0&limit=100"),
          api.get<PaginatedResponse<ArtistCategory>>("/artist-categories/?skip=0&limit=100"),
        ]);

        setAllArtists(artistsRes.items.filter((a) => a.status === "active"));

        // 내가 구독한 아티스트 ID
        if (user) {
          const mySubIds = new Set(
            subsRes.items
              .filter((s) => s.fan_id === user.id && s.status === "subscribed")
              .map((s) => s.artist_id)
          );
          setSubscribedIds(mySubIds);
        }

        // 카테고리 맵 (artist_id → category_name)
        const catById = new Map(catsRes.items.map((c) => [c.id, c.name]));
        const artCatMap = new Map<number, string>();
        catMapRes.items.forEach((m) => {
          const catName = catById.get(m.category_id);
          if (catName) artCatMap.set(m.artist_id, catName);
        });
        setCategoryMap(artCatMap);

        // 아티스트별 구독자 수 계산
        const counts = new Map<number, number>();
        subsRes.items
          .filter((s) => s.status === "subscribed")
          .forEach((s) => {
            counts.set(s.artist_id, (counts.get(s.artist_id) || 0) + 1);
          });
        setSubCounts(counts);
      } catch {
        // API 실패 시 빈 상태
      } finally {
        setLoading(false);
      }
    })();
  }, [user, isLoggedIn]);

  const subscribedArtists = allArtists.filter((a) => subscribedIds.has(a.id));
  const otherArtists = allArtists.filter((a) => !subscribedIds.has(a.id));

  if (loading) {
    return (
      <div className="home-page">
        <div className="feed-empty">로딩 중...</div>
      </div>
    );
  }

  return (
    <div className="home-page">
      {/* 구독 아티스트 */}
      <div className="home-section">
        <h1 className="home-title">구독 아티스트</h1>
        <p className="home-subtitle">좋아하는 아티스트의 콘텐츠를 확인하세요</p>
      </div>

      {subscribedArtists.length > 0 ? (
        <div className="artist-selection-grid">
          {subscribedArtists.map((artist) => (
            <button
              key={artist.id}
              className="artist-selection-card"
              onClick={() => router.push(`/artists/${artist.id}`)}
            >
              <div className="artist-selection-cover" />
              <div className="artist-selection-avatar">
                <span className="artist-selection-avatar-text">
                  {artist.stage_name[0]}
                </span>
              </div>
              <div className="artist-selection-info">
                <div className="artist-selection-name">{artist.stage_name}</div>
                {categoryMap.get(artist.id) && (
                  <div className="artist-selection-category">{categoryMap.get(artist.id)}</div>
                )}
                <div className="artist-selection-subs">구독자 {subCounts.get(artist.id) || 0}명</div>
              </div>
              <div className="artist-selection-badge subscribed">구독중</div>
            </button>
          ))}
        </div>
      ) : (
        <div className="feed-empty">
          {isLoggedIn
            ? <>구독한 아티스트가 없습니다.<br />아래에서 아티스트를 구독해보세요!</>
            : <>로그인하고 아티스트를 구독해보세요!</>
          }
        </div>
      )}

      {/* 다른 아티스트 */}
      {otherArtists.length > 0 && (
        <>
          <div className="home-section other">
            <h2 className="home-title-sub">다른 아티스트</h2>
            <p className="home-subtitle">새로운 아티스트를 발견해보세요</p>
          </div>

          <div className="artist-selection-grid">
            {otherArtists.map((artist) => (
              <button
                key={artist.id}
                className="artist-selection-card"
                onClick={() => router.push(`/artists/${artist.id}`)}
              >
                <div className="artist-selection-cover other" />
                <div className="artist-selection-avatar other">
                  <span className="artist-selection-avatar-text">
                    {artist.stage_name[0]}
                  </span>
                </div>
                <div className="artist-selection-info">
                  <div className="artist-selection-name">{artist.stage_name}</div>
                  {categoryMap.get(artist.id) && (
                    <div className="artist-selection-category">{categoryMap.get(artist.id)}</div>
                  )}
                  <div className="artist-selection-subs">구독자 {subCounts.get(artist.id) || 0}명</div>
                </div>
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
