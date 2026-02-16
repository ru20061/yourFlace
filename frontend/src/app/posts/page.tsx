"use client";

import { useState, useEffect, useCallback } from "react";
import { useAuth } from "../../lib/auth-context";
import { api } from "../../lib/api";
import type { Post, PaginatedResponse } from "../data/types";
import PostCard from "../components/PostCard/PostCard";
import "./posts.css";

export default function PostsPage() {
  const { user } = useAuth();

  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchPosts = useCallback(async () => {
    try {
      const postsRes = await api.get<PaginatedResponse<Post>>("/posts/?skip=0&limit=100");

      const sorted = postsRes.items
        .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());

      setPosts(sorted);
    } catch {
      // API 실패 시 빈 상태 유지
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchPosts();
  }, [fetchPosts]);

  if (loading) {
    return (
      <div className="posts-page">
        <div className="posts-empty">로딩 중...</div>
      </div>
    );
  }

  return (
    <div className="posts-page">
      <div className="posts-header">
        <h1 className="posts-title">포스트</h1>
      </div>

      {posts.length > 0 ? (
        <div className="posts-list">
          {posts.map((post) => (
            <PostCard key={post.id} post={post} />
          ))}
        </div>
      ) : (
        <div className="posts-empty">아직 작성된 포스트가 없습니다.</div>
      )}
    </div>
  );
}
