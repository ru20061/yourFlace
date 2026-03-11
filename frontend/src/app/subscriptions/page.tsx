"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useAuth } from "../../lib/auth-context";
import { api } from "../../lib/api";
import type {
  Subscription,
  Celeb,
  CelebCategoryMap,
  CelebCategory,
  PaginatedResponse,
} from "../data/types";
import "./subscriptions.css";

interface SubscribedCeleb {
  subscription: Subscription;
  celeb: Celeb;
  categoryName?: string;
}

export default function SubscriptionsPage() {
  const { user, isLoggedIn, isLoading: authLoading } = useAuth();
  const [items, setItems] = useState<SubscribedCeleb[]>([]);
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

        const [celebsRes, catMapRes, catsRes] = await Promise.all([
          api.get<PaginatedResponse<Celeb>>("/celebs?skip=0&limit=200"),
          api.get<PaginatedResponse<CelebCategoryMap>>("/celeb-category-map?skip=0&limit=200"),
          api.get<PaginatedResponse<CelebCategory>>("/celeb-categories?skip=0&limit=100"),
        ]);

        const celebMap = new Map(celebsRes.items.map((a) => [a.id, a]));
        const catMapByCeleb = new Map(catMapRes.items.map((m) => [m.celeb_id, m.category_id]));
        const catById = new Map(catsRes.items.map((c) => [c.id, c.name]));

        const result: SubscribedCeleb[] = mySubs
          .map((sub) => {
            const celeb = celebMap.get(sub.celeb_id);
            if (!celeb) return null;
            const catId = catMapByCeleb.get(celeb.id);
            return {
              subscription: sub,
              celeb,
              categoryName: catId ? catById.get(catId) : undefined,
            };
          })
          .filter(Boolean) as SubscribedCeleb[];

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
          items.map(({ subscription, celeb, categoryName }) => (
            <Link
              href={`/celebs/${celeb.slug}`}
              key={subscription.id}
              className="subscription-card"
            >
              <div className="subscription-avatar">
                {celeb.profile_image && (
                  <img src={celeb.profile_image} alt={celeb.stage_name} />
                )}
              </div>
              <div className="subscription-info">
                <div className="subscription-artist-name">{celeb.stage_name}</div>
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
          <div className="feed-empty">구독 중인 셀럽이 없습니다</div>
        )}
      </div>
    </div>
  );
}
