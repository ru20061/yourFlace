"use client";

import { formatDuration, getRelativeTime } from "../../../lib/utils";
import type { ArtistVideo } from "../../data/types";
import "./video-card.css";

interface VideoCardProps {
  video: ArtistVideo;
}

export default function VideoCard({ video }: VideoCardProps) {
  return (
    <div className="video-card">
      <div className="video-thumbnail">
        <div className="video-thumbnail-placeholder">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M8 5v14l11-7z" />
          </svg>
        </div>
        {video.duration_seconds && (
          <span className="video-duration">{formatDuration(video.duration_seconds)}</span>
        )}
        {video.visibility === "subscribers" && (
          <span className="video-lock-badge">구독자 전용</span>
        )}
      </div>
      <div className="video-info">
        <div className="video-title">{video.title ?? "제목 없음"}</div>
        {video.description && (
          <div className="video-description">{video.description}</div>
        )}
        <div className="video-meta">
          <span>{getRelativeTime(video.created_at)}</span>
          {video.tags && video.tags.length > 0 && (
            <span className="video-tags">
              {video.tags.map((tag) => `#${tag}`).join(" ")}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
