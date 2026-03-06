"use client";

import { useState, useRef, useCallback } from "react";
import { api } from "../../lib/api";
import { useAuth } from "../../lib/auth-context";
import type { ContentBlock } from "../data/types";

interface WritePostModalProps {
  onClose: () => void;
  onCreated: () => void;
}

interface ImageUploadResponse {
  id: number;
  url: string;
}

export default function WritePostModal({ onClose, onCreated }: WritePostModalProps) {
  const { user } = useAuth();
  const [blocks, setBlocks] = useState<ContentBlock[]>([
    { type: "text", value: "" },
  ]);
  const [title, setTitle] = useState("");
  const [visibility, setVisibility] = useState<"public" | "subscribers" | "private">("public");
  const [tags, setTags] = useState("");
  const [uploading, setUploading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [focusedBlockIndex, setFocusedBlockIndex] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const textareaRefs = useRef<(HTMLTextAreaElement | null)[]>([]);

  /** textarea 자동 높이 조절 */
  const autoResize = useCallback((el: HTMLTextAreaElement | null) => {
    if (!el) return;
    el.style.height = "auto";
    el.style.height = el.scrollHeight + "px";
  }, []);

  /** 텍스트 블록 내용 변경 */
  const updateTextBlock = (index: number, value: string) => {
    setBlocks((prev) => {
      const next = [...prev];
      next[index] = { type: "text", value };
      return next;
    });
  };

  /** 이미지 추가 버튼 클릭 */
  const handleAddImage = (afterIndex: number) => {
    setFocusedBlockIndex(afterIndex);
    fileInputRef.current?.click();
  };

  /** 파일 선택 후 업로드 */
  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // input 초기화 (같은 파일 재선택 허용)
    e.target.value = "";

    setUploading(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const result = await api.upload<ImageUploadResponse>("/images/upload", formData);

      setBlocks((prev) => {
        const next = [...prev];
        const insertAt = focusedBlockIndex + 1;

        // 이미지 블록 삽입
        const imageBlock: ContentBlock = {
          type: "image",
          imageId: result.id,
          url: result.url,
        };

        // 이미지 아래에 빈 텍스트 블록 추가
        const textBlock: ContentBlock = { type: "text", value: "" };

        next.splice(insertAt, 0, imageBlock, textBlock);
        return next;
      });

      // 새 텍스트 블록에 포커스
      setTimeout(() => {
        const newTextIndex = focusedBlockIndex + 2;
        textareaRefs.current[newTextIndex]?.focus();
      }, 50);
    } catch {
      setError("이미지 업로드에 실패했습니다.");
    } finally {
      setUploading(false);
    }
  };

  /** 이미지 블록 삭제 */
  const removeImageBlock = (index: number) => {
    setBlocks((prev) => {
      const next = [...prev];

      // 이미지 블록 위아래의 텍스트 블록 병합
      const above = index > 0 && next[index - 1].type === "text" ? index - 1 : -1;
      const below = index < next.length - 1 && next[index + 1].type === "text" ? index + 1 : -1;

      if (above >= 0 && below >= 0) {
        // 위아래 텍스트 블록 병합
        const aboveBlock = next[above] as { type: "text"; value: string };
        const belowBlock = next[below] as { type: "text"; value: string };
        const merged = aboveBlock.value + (aboveBlock.value && belowBlock.value ? "\n" : "") + belowBlock.value;
        next[above] = { type: "text", value: merged };
        // 이미지 블록과 아래 텍스트 블록 제거
        next.splice(index, 2);
      } else {
        // 이미지 블록만 제거
        next.splice(index, 1);
      }

      // 블록이 비면 빈 텍스트 블록 추가
      if (next.length === 0) {
        next.push({ type: "text", value: "" });
      }

      return next;
    });
  };

  /** 포스트 제출 */
  const handleSubmit = async () => {
    if (!user) {
      setError("로그인이 필요합니다.");
      return;
    }

    // 빈 콘텐츠 검사: 텍스트가 하나라도 있거나 이미지가 하나라도 있어야 함
    const hasContent = blocks.some((b) =>
      b.type === "image" || (b.type === "text" && b.value.trim())
    );
    if (!hasContent) {
      setError("내용을 입력해주세요.");
      return;
    }

    setSubmitting(true);
    setError("");

    try {
      // 빈 텍스트 블록 정리 (앞뒤 빈 텍스트 제거, 연속 빈 텍스트 병합)
      const cleanedBlocks = blocks.filter((b, i) => {
        if (b.type === "image") return true;
        if (b.type === "text" && b.value.trim()) return true;
        // 빈 텍스트 블록: 이미지 사이에 있으면 유지
        const prevIsImage = i > 0 && blocks[i - 1].type === "image";
        const nextIsImage = i < blocks.length - 1 && blocks[i + 1].type === "image";
        return prevIsImage && nextIsImage;
      });

      const parsedTags = tags
        .split(",")
        .map((t) => t.trim())
        .filter(Boolean);

      await api.post("/posts", {
        author_id: user.id,
        author_type: "fan",
        content: cleanedBlocks,
        write_id: user.id,
        write_role: "fan",
        visibility,
        tags: parsedTags.length > 0 ? parsedTags : null,
        title_field: title.trim() || null,
      });

      onCreated();
    } catch {
      setError("포스트 작성에 실패했습니다.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="write-modal-overlay" onClick={onClose}>
      <div className="write-modal" onClick={(e) => e.stopPropagation()}>
        {/* 헤더 */}
        <div className="write-modal-header">
          <h2>글쓰기</h2>
          <button className="write-modal-close" onClick={onClose}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>

        {/* 본문 */}
        <div className="write-modal-body">
          {/* 제목 (선택) */}
          <div className="write-field">
            <label className="write-label">제목 (선택)</label>
            <input
              className="write-input"
              placeholder="제목을 입력하세요"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </div>

          {/* 블록 에디터 */}
          <div className="write-field">
            <label className="write-label">내용</label>
            <div className="write-blocks">
              {blocks.map((block, i) => {
                if (block.type === "text") {
                  return (
                    <div key={i} className="write-block-wrapper">
                      <textarea
                        ref={(el) => {
                          textareaRefs.current[i] = el;
                          autoResize(el);
                        }}
                        className="write-block-text"
                        placeholder="텍스트를 입력하세요..."
                        value={block.value}
                        onFocus={() => setFocusedBlockIndex(i)}
                        onChange={(e) => {
                          updateTextBlock(i, e.target.value);
                          autoResize(e.target);
                        }}
                      />
                      <button
                        type="button"
                        className="write-image-add-btn"
                        onClick={() => handleAddImage(i)}
                        disabled={uploading}
                      >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" width="16" height="16">
                          <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                          <circle cx="8.5" cy="8.5" r="1.5" />
                          <polyline points="21 15 16 10 5 21" />
                        </svg>
                        {uploading ? "업로드 중..." : "이미지 추가"}
                      </button>
                    </div>
                  );
                }

                // 이미지 블록
                return (
                  <div key={i} className="write-block-image">
                    <img src={block.url} alt="업로드된 이미지" />
                    <button
                      type="button"
                      className="write-block-remove"
                      onClick={() => removeImageBlock(i)}
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="16" height="16">
                        <line x1="18" y1="6" x2="6" y2="18" />
                        <line x1="6" y1="6" x2="18" y2="18" />
                      </svg>
                    </button>
                  </div>
                );
              })}
            </div>
          </div>

          {/* 공개 범위 */}
          <div className="write-field">
            <label className="write-label">공개 범위</label>
            <select
              className="write-select"
              value={visibility}
              onChange={(e) => setVisibility(e.target.value as "public" | "subscribers" | "private")}
            >
              <option value="public">전체 공개</option>
              <option value="subscribers">구독자 전용</option>
              <option value="private">비공개</option>
            </select>
          </div>

          {/* 태그 */}
          <div className="write-field">
            <label className="write-label">태그 (쉼표로 구분)</label>
            <input
              className="write-input"
              placeholder="예: 일상, 음악, 공연"
              value={tags}
              onChange={(e) => setTags(e.target.value)}
            />
          </div>

          {error && <div className="write-error">{error}</div>}
        </div>

        {/* 푸터 */}
        <div className="write-modal-footer">
          <button className="write-btn-cancel" onClick={onClose}>
            취소
          </button>
          <button
            className="write-btn-submit"
            onClick={handleSubmit}
            disabled={submitting || uploading}
          >
            {submitting ? "등록 중..." : "등록"}
          </button>
        </div>

        {/* 숨김 파일 입력 */}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/jpeg,image/png,image/gif,image/webp"
          style={{ display: "none" }}
          onChange={handleFileChange}
        />
      </div>
    </div>
  );
}
