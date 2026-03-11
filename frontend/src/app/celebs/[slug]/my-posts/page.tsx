"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { useAuth } from "../../../../lib/auth-context";
import { api } from "../../../../lib/api";
import type { Celeb, Post, PaginatedResponse } from "../../../data/types";
import PostCard from "../../../components/PostCard/PostCard";
import "../celeb-detail.css";

export default function MyPostsPage() {
  const params = useParams();
  const router = useRouter();
  const slug = decodeURIComponent(params.slug as string);
  const { user, isLoading: authLoading } = useAuth();

  const [celeb, setCeleb] = useState<Celeb | null>(null);
  const [myPosts, setMyPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (authLoading) return;
    if (!user) { setLoading(false); return; }

    (async () => {
      try {
        const celebRes = await api.get<Celeb>(`/celebs/by-slug/${encodeURIComponent(slug)}`);
        setCeleb(celebRes);

        const postsRes = await api.get<PaginatedResponse<Post>>(`/posts/?skip=0&limit=100`);
        const filtered = postsRes.items
          .filter((p) => p.author_id === celebRes.id && !p.is_artist_post && p.write_id === user.id)
          .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
        setMyPosts(filtered);
      } catch {
        // ignore
      } finally {
        setLoading(false);
      }
    })();
  }, [slug, user, authLoading]);

  const handleDelete = async (postId: number) => {
    if (!confirm("포스트를 삭제하시겠습니까?")) return;
    try {
      await api.delete(`/posts/${postId}`);
      setMyPosts((prev) => prev.filter((p) => p.id !== postId));
    } catch {
      alert("삭제에 실패했습니다. 다시 시도해주세요.");
    }
  };

  if (loading || authLoading) {
    return (
      <div className="artist-detail-page">
        <div className="feed-empty">로딩 중...</div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="artist-detail-page">
        <div className="feed-empty">로그인 후 이용해주세요</div>
      </div>
    );
  }

  return (
    <div className="artist-detail-page">
      <div className="artist-feed-container">
        <div className="artist-feed-list">
          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 20 }}>
            <button
              onClick={() => router.back()}
              style={{
                background: "none",
                border: "1px solid var(--color-border, #e5e7eb)",
                borderRadius: 8,
                cursor: "pointer",
                padding: "6px 12px",
                color: "var(--color-primary)",
                fontSize: "0.9rem",
              }}
            >
              ← 돌아가기
            </button>
            <h2 style={{ margin: 0, fontSize: "1.1rem", fontWeight: 600 }}>
              {celeb ? `${celeb.stage_name} — 내 포스트` : "내 포스트"}
            </h2>
            <span style={{ marginLeft: "auto", fontSize: "0.85rem", color: "#888" }}>
              총 {myPosts.length}개
            </span>
          </div>

          {myPosts.length > 0 ? (
            myPosts.map((post) => (
              <PostCard
                key={post.id}
                post={post}
                currentUserId={user.id}
                onDelete={handleDelete}
              />
            ))
          ) : (
            <div className="feed-empty">내가 작성한 포스트가 없습니다</div>
          )}
        </div>
      </div>
    </div>
  );
}
