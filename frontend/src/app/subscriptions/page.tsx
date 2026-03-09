"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useAuth } from "../../lib/auth-context";
import { api } from "../../lib/api";
import type {
  Subscription,
  Creator,
  CreatorCategoryMap,
  CreatorCategory,
  PaginatedResponse,
} from "../data/types";
import "./subscriptions.css";

interface SubscribedCreator {
  subscription: Subscription;
  creator: Creator;
  categoryName?: string;
}

export default function SubscriptionsPage() {
  const { user, isLoggedIn, isLoading: authLoading } = useAuth();
  const [items, setItems] = useState<SubscribedCreator[]>([]);
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

        const [creatorsRes, catMapRes, catsRes] = await Promise.all([
          api.get<PaginatedResponse<Creator>>("/creators?skip=0&limit=200"),
          api.get<PaginatedResponse<CreatorCategoryMap>>("/creator-category-map?skip=0&limit=200"),
          api.get<PaginatedResponse<CreatorCategory>>("/creator-categories?skip=0&limit=100"),
        ]);

        const creatorMap = new Map(creatorsRes.items.map((a) => [a.id, a]));
        const catMapByCreator = new Map(catMapRes.items.map((m) => [m.creator_id, m.category_id]));
        const catById = new Map(catsRes.items.map((c) => [c.id, c.name]));

        const result: SubscribedCreator[] = mySubs
          .map((sub) => {
            const creator = creatorMap.get(sub.creator_id);
            if (!creator) return null;
            const catId = catMapByCreator.get(creator.id);
            return {
              subscription: sub,
              creator,
              categoryName: catId ? catById.get(catId) : undefined,
            };
          })
          .filter(Boolean) as SubscribedCreator[];

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
          items.map(({ subscription, creator, categoryName }) => (
            <Link
              href={`/creators/${creator.slug}`}
              key={subscription.id}
              className="subscription-card"
            >
              <div className="subscription-avatar">
                {creator.profile_image && (
                  <img src={creator.profile_image} alt={creator.stage_name} />
                )}
              </div>
              <div className="subscription-info">
                <div className="subscription-artist-name">{creator.stage_name}</div>
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
          <div className="feed-empty">구독 중인 크리에이터가 없습니다</div>
        )}
      </div>
    </div>
  );
}
