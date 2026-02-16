"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useAuth } from "../../lib/auth-context";
import { api } from "../../lib/api";
import type {
  Subscription,
  Artist,
  ArtistCategoryMap,
  ArtistCategory,
  PaginatedResponse,
} from "../data/types";
import "./subscriptions.css";

interface SubscribedArtist {
  subscription: Subscription;
  artist: Artist;
  categoryName?: string;
}

export default function SubscriptionsPage() {
  const { user, isLoggedIn, isLoading: authLoading } = useAuth();
  const [items, setItems] = useState<SubscribedArtist[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isLoggedIn || !user) {
      setLoading(false);
      return;
    }

    (async () => {
      try {
        const subs = await api.get<PaginatedResponse<Subscription>>(
          "/subscriptions?skip=0&limit=100"
        );
        const mySubs = subs.items.filter(
          (s) => s.fan_id === user.id && s.status === "subscribed"
        );

        if (mySubs.length === 0) {
          setItems([]);
          setLoading(false);
          return;
        }

        const [artistsRes, catMapRes, catsRes] = await Promise.all([
          api.get<PaginatedResponse<Artist>>("/artists?skip=0&limit=200"),
          api.get<PaginatedResponse<ArtistCategoryMap>>("/artist-category-map?skip=0&limit=200"),
          api.get<PaginatedResponse<ArtistCategory>>("/artist-categories?skip=0&limit=100"),
        ]);

        const artistMap = new Map(artistsRes.items.map((a) => [a.id, a]));
        const catMapByArtist = new Map(catMapRes.items.map((m) => [m.artist_id, m.category_id]));
        const catById = new Map(catsRes.items.map((c) => [c.id, c.name]));

        const result: SubscribedArtist[] = mySubs
          .map((sub) => {
            const artist = artistMap.get(sub.artist_id);
            if (!artist) return null;
            const catId = catMapByArtist.get(artist.id);
            return {
              subscription: sub,
              artist,
              categoryName: catId ? catById.get(catId) : undefined,
            };
          })
          .filter(Boolean) as SubscribedArtist[];

        setItems(result);
      } catch {
        setItems([]);
      } finally {
        setLoading(false);
      }
    })();
  }, [isLoggedIn, user]);

  if (authLoading || loading) {
    return (
      <div className="subscriptions-page">
        <h1 className="subscriptions-title">내 구독</h1>
        <div className="feed-empty">로딩 중...</div>
      </div>
    );
  }

  if (!isLoggedIn) {
    return (
      <div className="subscriptions-page">
        <h1 className="subscriptions-title">내 구독</h1>
        <div className="feed-empty">로그인 후 이용해주세요</div>
      </div>
    );
  }

  return (
    <div className="subscriptions-page">
      <h1 className="subscriptions-title">내 구독</h1>
      <div className="subscription-list">
        {items.length > 0 ? (
          items.map(({ subscription, artist, categoryName }) => (
            <Link
              href={`/artists/${artist.slug}`}
              key={subscription.id}
              className="subscription-card"
            >
              <div className="subscription-avatar">
                {artist.profile_image && (
                  <img src={artist.profile_image} alt={artist.stage_name} />
                )}
              </div>
              <div className="subscription-info">
                <div className="subscription-artist-name">{artist.stage_name}</div>
                {categoryName && (
                  <div className="subscription-plan">{categoryName}</div>
                )}
                <div className="subscription-date">
                  {subscription.start_date} 부터 구독
                </div>
              </div>
              <span className="subscription-status active">구독 중</span>
            </Link>
          ))
        ) : (
          <div className="feed-empty">구독 중인 아티스트가 없습니다</div>
        )}
      </div>
    </div>
  );
}
