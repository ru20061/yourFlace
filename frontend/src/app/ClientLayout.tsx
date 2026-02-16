"use client";

import { useState, useEffect } from "react";
import Header from "./components/Header/Header";
import Footer from "./components/Footer/Footer";
import Sidebar from "./components/Sidebar/Sidebar";
import ChatBubble from "./components/ChatBubble/ChatBubble";
import { useAuth } from "../lib/auth-context";
import { api } from "../lib/api";
import type { Subscription, Artist, ArtistCategoryMap, ArtistCategory, PaginatedResponse, SidebarArtist } from "./data/types";

export default function ClientLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user, isLoggedIn, isLoading, logout } = useAuth();
  const [sidebarArtists, setSidebarArtists] = useState<SidebarArtist[]>([]);

  useEffect(() => {
    if (!user) {
      setSidebarArtists([]);
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
          setSidebarArtists([]);
          return;
        }

        // 아티스트 목록 + 카테고리 맵 + 카테고리 병렬 조회
        const [artistsRes, catMapRes, catsRes] = await Promise.all([
          api.get<PaginatedResponse<Artist>>("/artists/?skip=0&limit=100"),
          api.get<PaginatedResponse<ArtistCategoryMap>>("/artist-category-map/?skip=0&limit=100"),
          api.get<PaginatedResponse<ArtistCategory>>("/artist-categories/?skip=0&limit=100"),
        ]);

        const artistMap = new Map(artistsRes.items.map((a) => [a.id, a]));
        const catMapByArtist = new Map(catMapRes.items.map((m) => [m.artist_id, m.category_id]));
        const catById = new Map(catsRes.items.map((c) => [c.id, c.name]));

        const sidebar: SidebarArtist[] = subscribedSubs
          .map((sub) => {
            const artist = artistMap.get(sub.artist_id);
            if (!artist) return null;
            const catId = catMapByArtist.get(artist.id);
            return {
              id: artist.id,
              name: artist.stage_name,
              slug: artist.slug,
              category: catId ? catById.get(catId) : undefined,
              profileImage: artist.profile_image ?? undefined,
            };
          })
          .filter(Boolean) as SidebarArtist[];

        setSidebarArtists(sidebar);
      } catch {
        setSidebarArtists([]);
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
        subscribedArtists={sidebarArtists}
      />
      <main className="app-main">
        {children}
      </main>
      <Footer isLoggedIn={isLoggedIn} isAdmin={false} />
      {isLoggedIn && <ChatBubble subscribedArtists={sidebarArtists} />}
    </div>
  );
}
