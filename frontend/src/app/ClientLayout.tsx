"use client";

import { useState, useEffect } from "react";
import Header from "./components/Header/Header";
import Footer from "./components/Footer/Footer";
import Sidebar from "./components/Sidebar/Sidebar";
import ChatBubble from "./components/ChatBubble/ChatBubble";
import { useAuth } from "../lib/auth-context";
import { api } from "../lib/api";
import type { Subscription, Celeb, CelebCategoryMap, CelebCategory, PaginatedResponse, SidebarCeleb } from "./data/types";

export default function ClientLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user, isLoggedIn, isLoading, logout } = useAuth();
  const [sidebarCelebs, setSidebarCelebs] = useState<SidebarCeleb[]>([]);

  useEffect(() => {
    if (!user) {
      setSidebarCelebs([]);
      return;
    }

    (async () => {
      try {
        // 구독 목록 조회
        const subs = await api.get<PaginatedResponse<Subscription>>(
          `/subscriptions/?skip=0&limit=100`
        );
        const subscribedSubs = subs.items.filter(
          (s) => s.fan_id === user.id && s.status === "subscribed"
        );

        if (subscribedSubs.length === 0) {
          setSidebarCelebs([]);
          return;
        }

        // 셀럽 목록 + 카테고리 맵 + 카테고리 병렬 조회
        const [celebsRes, catMapRes, catsRes] = await Promise.all([
          api.get<PaginatedResponse<Celeb>>("/celebs/?skip=0&limit=100"),
          api.get<PaginatedResponse<CelebCategoryMap>>("/celeb-category-map/?skip=0&limit=100"),
          api.get<PaginatedResponse<CelebCategory>>("/celeb-categories/?skip=0&limit=100"),
        ]);

        const celebMap = new Map(celebsRes.items.map((a) => [a.id, a]));
        const catMapByCeleb = new Map(catMapRes.items.map((m) => [m.celeb_id, m.category_id]));
        const catById = new Map(catsRes.items.map((c) => [c.id, c.name]));

        // 직접 구독한 셀럽 ID
        const directSubIds = new Set(subscribedSubs.map((s) => s.celeb_id));

        // 구독된 그룹의 멤버도 포함
        const allSubscribedIds = new Set(directSubIds);
        celebsRes.items
          .filter((c) => c.parent_id != null && directSubIds.has(c.parent_id))
          .forEach((c) => allSubscribedIds.add(c.id));

        const sidebar: SidebarCeleb[] = Array.from(allSubscribedIds)
          .map((celebId) => {
            const celeb = celebMap.get(celebId);
            if (!celeb) return null;
            const catId = catMapByCeleb.get(celeb.id);
            return {
              id: celeb.id,
              name: celeb.stage_name,
              slug: celeb.slug,
              category: catId ? catById.get(catId) : undefined,
              profileImage: celeb.profile_image ?? undefined,
              celeb_type: celeb.celeb_type,
            };
          })
          .filter(Boolean) as SidebarCeleb[];

        setSidebarCelebs(sidebar);
      } catch {
        setSidebarCelebs([]);
      }
    })();
  }, [user]);

  if (isLoading) {
    return (
      <div className="app-layout">
        <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh" }}>
          로딩 중...
        </div>
      </div>
    );
  }

  return (
    <div className="app-layout">
      <Header
        isAdmin={false}
        isLoggedIn={isLoggedIn}
        onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        onLogout={logout}
      />
      <Sidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        isAdmin={false}
        subscribedCelebs={sidebarCelebs}
      />
      <main className="app-main">
        {children}
      </main>
      <Footer isLoggedIn={isLoggedIn} isAdmin={false} />
      {isLoggedIn && <ChatBubble subscribedCelebs={sidebarCelebs} />}
    </div>
  );
}
