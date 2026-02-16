"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { apiFetch } from "../../../lib/api";
import { getRelativeTime } from "../../../lib/utils";
import type { MagazineDetail } from "../../data/types";
import "./magazine-detail.css";

export default function MagazineDetailPage() {
  const params = useParams();
  const slug = decodeURIComponent(params.slug as string);

  const [magazine, setMagazine] = useState<MagazineDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const data = await apiFetch<MagazineDetail>(
          `/magazines/public/by-slug/${encodeURIComponent(slug)}`
        );
        setMagazine(data);
      } catch {
        setMagazine(null);
      } finally {
        setLoading(false);
      }
    })();
  }, [slug]);

  if (loading) {
    return (
      <div className="magazine-detail-page">
        <div className="feed-empty">로딩 중...</div>
      </div>
    );
  }

  if (!magazine) {
    return (
      <div className="magazine-detail-page">
        <div className="feed-empty">매거진을 찾을 수 없습니다</div>
      </div>
    );
  }

  return (
    <div className="magazine-detail-page">
      {/* 썸네일 */}
      <div className="magazine-cover">
        {magazine.thumbnail_url && (
          <img src={magazine.thumbnail_url} alt={magazine.title} />
        )}
      </div>

      {/* 메타 정보 */}
      <div className="magazine-meta">
        {magazine.category && (
          <span className="magazine-category-badge">{magazine.category}</span>
        )}
        <span className="magazine-date">
          {getRelativeTime(magazine.created_at)}
        </span>
        <span className="magazine-meta-dot">&middot;</span>
        <span className="magazine-views">조회 {magazine.view_count}</span>
      </div>

      {/* 제목 */}
      <h1 className="magazine-title">{magazine.title}</h1>

      {/* 본문 */}
      <div className="magazine-body">
        <p className="magazine-content">{magazine.content}</p>

        {/* 본문 이미지 */}
        {magazine.images.length > 0 && (
          <div className="magazine-images">
            {magazine.images.map((img) => (
              <div key={img.id} className="magazine-image-item">
                <img src={img.url} alt="" />
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 태그 */}
      {magazine.tags && magazine.tags.length > 0 && (
        <div className="magazine-tags">
          {magazine.tags.map((tag) => (
            <span key={tag} className="magazine-tag">
              #{tag}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
