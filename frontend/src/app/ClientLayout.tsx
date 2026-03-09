"use client";

import { useState, useEffect } from "react";
import Header from "./components/Header/Header";
import Footer from "./components/Footer/Footer";
import Sidebar from "./components/Sidebar/Sidebar";
import ChatBubble from "./components/ChatBubble/ChatBubble";
import { useAuth } from "../lib/auth-context";
import { api } from "../lib/api";
import type { Subscription, Creator, CreatorCategoryMap, CreatorCategory, PaginatedResponse, SidebarCreator } from "./data/types";

export default function ClientLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user, isLoggedIn, isLoading, logout } = useAuth();
  const [sidebarCreators, setSidebarCreators] = useState<SidebarCreator[]>([]);

  useEffect(() => {
    if (!user) {
      setSidebarCreators([]);
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
          setSidebarCreators([]);
          return;
        }

        // 크리에이터 목록 + 카테고리 맵 + 카테고리 병렬 조회
        const [creatorsRes, catMapRes, catsRes] = await Promise.all([
          api.get<PaginatedResponse<Creator>>("/creators/?skip=0&limit=100"),
          api.get<PaginatedResponse<CreatorCategoryMap>>("/creator-category-map/?skip=0&limit=100"),
          api.get<PaginatedResponse<CreatorCategory>>("/creator-categories/?skip=0&limit=100"),
        ]);

        const creatorMap = new Map(creatorsRes.items.map((a) => [a.id, a]));
        const catMapByCreator = new Map(catMapRes.items.map((m) => [m.creator_id, m.category_id]));
        const catById = new Map(catsRes.items.map((c) => [c.id, c.name]));

        const sidebar: SidebarCreator[] = subscribedSubs
          .map((sub) => {
            const creator = creatorMap.get(sub.creator_id);
            if (!creator) return null;
            const catId = catMapByCreator.get(creator.id);
            return {
              id: creator.id,
              name: creator.stage_name,
              slug: creator.slug,
              category: catId ? catById.get(catId) : undefined,
              profileImage: creator.profile_image ?? undefined,
            };
          })
          .filter(Boolean) as SidebarCreator[];

        setSidebarCreators(sidebar);
      } catch {
        setSidebarCreators([]);
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
        subscribedCreators={sidebarCreators}
      />
      <main className="app-main">
        {children}
      </main>
      <Footer isLoggedIn={isLoggedIn} isAdmin={false} />
      {isLoggedIn && <ChatBubble subscribedCreators={sidebarCreators} />}
    </div>
  );
}
