"use client";

import { getRelativeTime } from "../../../lib/utils";
import type { Post, ContentBlock } from "../../data/types";
import "./post-card.css";

interface PostCardProps {
  post: Post;
}

/** 블록 배열 또는 문자열 콘텐츠를 렌더링 */
function renderContent(content: ContentBlock[] | string | null) {
  if (!content) return null;

  // 하위 호환: 기존 문자열 콘텐츠
  if (typeof content === "string") {
    return content.split("\n").map((line, i) => (
      <p key={i} className="post-text">
        {line || "\u00A0"}
      </p>
    ));
  }

  // 블록 배열 렌더링
  if (Array.isArray(content)) {
    return content.map((block, i) => {
      if (block.type === "text") {
        if (!block.value?.trim()) return null;
        return block.value.split("\n").map((line, j) => (
          <p key={`${i}-${j}`} className="post-text">
            {line || "\u00A0"}
          </p>
        ));
      }
      if (block.type === "image") {
        return (
          <div key={i} className="post-block-image">
            <img src={block.url} alt="포스트 이미지" />
          </div>
        );
      }
      return null;
    });
  }

  return null;
}

export default function PostCard({ post }: PostCardProps) {
  const isArticle = !!post.title_field;

  return (
    <div className={`post-card ${isArticle ? "post-card-article" : ""}`}>
      <div className="post-header">
        <div className="post-avatar" />
        <div>
          <div className="post-author-name">{post.author_name ?? "익명"}</div>
          <div className="post-time">{getRelativeTime(post.created_at)}</div>
        </div>
        {post.visibility === "subscribers" && (
          <span className="post-badge subscribers">구독자 전용</span>
        )}
      </div>

      {/* 기사형: 제목 */}
      {post.title_field && (
        <h3 className="post-title">{post.title_field}</h3>
      )}

      <div className="post-body">
        {renderContent(post.content)}
      </div>

      {/* 기존 이미지 (하위 호환) */}
      {post.images && post.images.length > 0 && (
        <div className={`post-images ${post.images.length === 1 ? "single" : post.images.length === 2 ? "double" : "multi"}`}>
          {post.images.map((img) => (
            <div key={img.id} className="post-image-item">
              <div className="post-image-placeholder">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                  <circle cx="8.5" cy="8.5" r="1.5" />
                  <polyline points="21 15 16 10 5 21" />
                </svg>
              </div>
              {img.caption && (
                <div className="post-image-caption">{img.caption}</div>
              )}
            </div>
          ))}
        </div>
      )}

      {post.tags && post.tags.length > 0 && (
        <div className="post-tags">
          {post.tags.map((tag) => (
            <span key={tag} className="post-tag">#{tag}</span>
          ))}
        </div>
      )}
      <div className="post-actions">
        <button className="post-action-btn">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z" />
          </svg>
          <span>좋아요</span>
        </button>
        <button className="post-action-btn">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
          </svg>
          <span>댓글</span>
        </button>
      </div>
    </div>
  );
}
