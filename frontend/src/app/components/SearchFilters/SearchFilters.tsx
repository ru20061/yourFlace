"use client";

import type { SearchFilterState } from "../../data/types";
import FlaceDatePicker from "../FlaceDatePicker/FlaceDatePicker";
import "./search-filters.css";

interface SearchFiltersProps {
  filters: SearchFilterState;
  onFiltersChange: (filters: SearchFilterState) => void;
  tags: string[];
}

const SORT_OPTIONS = [
  { key: "latest" as const, label: "최신순" },
  { key: "oldest" as const, label: "오래된순" },
  { key: "relevant" as const, label: "관련순" },
];

const VISIBILITY_OPTIONS = [
  { key: "all" as const, label: "전체" },
  { key: "public" as const, label: "공개" },
  { key: "subscribers" as const, label: "구독자 전용" },
];

export default function SearchFilters({ filters, onFiltersChange, tags }: SearchFiltersProps) {
  const toggleTag = (tag: string) => {
    const newTags = filters.tags.includes(tag)
      ? filters.tags.filter((t) => t !== tag)
      : [...filters.tags, tag];
    onFiltersChange({ ...filters, tags: newTags });
  };

  const clearAll = () => {
    onFiltersChange({
      ...filters,
      tags: [],
      sortOrder: "latest",
      dateRange: { start: null, end: null },
      visibility: "all",
    });
  };

  const activeCount =
    filters.tags.length +
    (filters.sortOrder !== "latest" ? 1 : 0) +
    (filters.visibility !== "all" ? 1 : 0) +
    (filters.dateRange.start ? 1 : 0) +
    (filters.dateRange.end ? 1 : 0);

  return (
    <div className="advanced-filters">
      {/* 태그 */}
      <div className="filter-section">
        <div className="filter-section-title">태그</div>
        <div className="filter-tags">
          {tags.map((tag) => (
            <button
              key={tag}
              type="button"
              className={`filter-tag-chip ${filters.tags.includes(tag) ? "active" : ""}`}
              onClick={() => toggleTag(tag)}
            >
              #{tag}
            </button>
          ))}
        </div>
      </div>

      {/* 정렬 */}
      <div className="filter-section">
        <div className="filter-section-title">정렬</div>
        <div className="filter-options">
          {SORT_OPTIONS.map((opt) => (
            <button
              key={opt.key}
              type="button"
              className={`filter-chip ${filters.sortOrder === opt.key ? "active" : ""}`}
              onClick={() => onFiltersChange({ ...filters, sortOrder: opt.key })}
            >
              {opt.label}
            </button>
          ))}
        </div>
      </div>

      {/* 공개 범위 */}
      <div className="filter-section">
        <div className="filter-section-title">공개 범위</div>
        <div className="filter-options">
          {VISIBILITY_OPTIONS.map((opt) => (
            <button
              key={opt.key}
              type="button"
              className={`filter-chip ${filters.visibility === opt.key ? "active" : ""}`}
              onClick={() => onFiltersChange({ ...filters, visibility: opt.key })}
            >
              {opt.label}
            </button>
          ))}
        </div>
      </div>

      {/* 기간 */}
      <div className="filter-section">
        <div className="filter-section-title">기간</div>
        <div className="filter-date-range">
          <FlaceDatePicker
            value={filters.dateRange.start ?? ""}
            onChange={(val) =>
              onFiltersChange({
                ...filters,
                dateRange: { ...filters.dateRange, start: val || null },
              })
            }
            placeholder="시작일"
          />
          <span className="filter-date-separator">~</span>
          <FlaceDatePicker
            value={filters.dateRange.end ?? ""}
            onChange={(val) =>
              onFiltersChange({
                ...filters,
                dateRange: { ...filters.dateRange, end: val || null },
              })
            }
            placeholder="종료일"
          />
        </div>
      </div>

      {/* 초기화 */}
      {activeCount > 0 && (
        <button type="button" className="filter-clear-btn" onClick={clearAll}>
          필터 초기화 ({activeCount})
        </button>
      )}
    </div>
  );
}
