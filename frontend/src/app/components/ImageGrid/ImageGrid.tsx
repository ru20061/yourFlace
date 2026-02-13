"use client";

import type { ArtistImage } from "../../data/types";
import "./image-grid.css";

interface ImageGridProps {
  images: ArtistImage[];
}

export default function ImageGrid({ images }: ImageGridProps) {
  return (
    <div className="image-grid">
      {images.map((img) => (
        <div key={img.id} className="image-grid-item">
          <div className="image-grid-placeholder">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
              <circle cx="8.5" cy="8.5" r="1.5" />
              <polyline points="21 15 16 10 5 21" />
            </svg>
            {img.image_purpose && (
              <span className="image-grid-label">{img.image_purpose}</span>
            )}
          </div>
          {img.visibility === "subscribers" && (
            <div className="image-grid-lock">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C9.24 2 7 4.24 7 7v3H6a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2v-8a2 2 0 00-2-2h-1V7c0-2.76-2.24-5-5-5zm3 10v8H9v-8h6zm-1-2h-4V7c0-1.66 1.34-3 3-3s3 1.34 3 3v3h-2z" />
              </svg>
            </div>
          )}
          {img.tags && img.tags.length > 0 && (
            <div className="image-grid-tags">
              {img.tags.map((tag) => (
                <span key={tag} className="image-grid-tag">#{tag}</span>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
