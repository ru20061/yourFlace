"use client";

import { useState, useEffect, useCallback } from "react";
import { useAuth } from "../../lib/auth-context";
import { api } from "../../lib/api";
import type { Post, PaginatedResponse } from "../data/types";
import PostCard from "../components/PostCard/PostCard";
import WritePostModal from "./WritePostModal";
import "./posts.css";

export default function PostsPage() {
  const { user } = useAuth();

  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [showWriteModal, setShowWriteModal] = useState(false);

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

  const handlePostCreated = () => {
    setShowWriteModal(false);
    fetchPosts();
  };

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

      {/* 글쓰기 FAB */}
      {user && (
        <button className="write-fab" onClick={() => setShowWriteModal(true)}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
          글쓰기
        </button>
      )}

      {/* 글쓰기 모달 */}
      {showWriteModal && (
        <WritePostModal
          onClose={() => setShowWriteModal(false)}
          onCreated={handlePostCreated}
        />
      )}
    </div>
  );
}
