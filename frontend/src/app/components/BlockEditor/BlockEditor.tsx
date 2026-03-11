"use client";

import { useRef, useState, useId } from "react";
import "./block-editor.css";

export type TextEditorBlock = {
  id: string;
  type: "text";
  value: string;
};

export type ImageEditorBlock = {
  id: string;
  type: "image";
  file: File;
  previewUrl: string;
};

export type EditorBlock = TextEditorBlock | ImageEditorBlock;

interface BlockEditorProps {
  blocks: EditorBlock[];
  onChange: (blocks: EditorBlock[]) => void;
}

function uid() {
  return Math.random().toString(36).slice(2) + Date.now().toString(36);
}

export default function BlockEditor({ blocks, onChange }: BlockEditorProps) {
  const [dragIdx, setDragIdx] = useState<number | null>(null);
  const [dragOverIdx, setDragOverIdx] = useState<number | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const insertAfterRef = useRef<number | null>(null); // 어디 다음에 삽입할지

  /* ── 텍스트 변경 ── */
  const handleTextChange = (id: string, value: string) => {
    onChange(blocks.map((b) => (b.id === id ? { ...b, value } : b)));
  };

  /* ── 블록 삭제 ── */
  const handleDelete = (id: string) => {
    const next = blocks.filter((b) => b.id !== id);
    // 최소 하나의 텍스트 블록 유지
    onChange(next.length ? next : [{ id: uid(), type: "text", value: "" }]);
  };

  /* ── 텍스트 블록 삽입 (afterIdx: -1이면 맨 처음) ── */
  const insertTextBlock = (afterIdx: number) => {
    const newBlock: TextEditorBlock = { id: uid(), type: "text", value: "" };
    const next = [...blocks];
    next.splice(afterIdx + 1, 0, newBlock);
    onChange(next);
  };

  /* ── 이미지 블록 삽입 ── */
  const handleImageFiles = (files: FileList | null, afterIdx: number) => {
    if (!files) return;
    const newBlocks: ImageEditorBlock[] = Array.from(files).map((file) => ({
      id: uid(),
      type: "image",
      file,
      previewUrl: URL.createObjectURL(file),
    }));
    const next = [...blocks];
    next.splice(afterIdx + 1, 0, ...newBlocks);
    onChange(next);
  };

  const openImagePicker = (afterIdx: number) => {
    insertAfterRef.current = afterIdx;
    fileInputRef.current?.click();
  };

  /* ── 드래그 앤 드롭 ── */
  const handleDragStart = (idx: number) => {
    setDragIdx(idx);
  };

  const handleDragOver = (e: React.DragEvent, idx: number) => {
    e.preventDefault();
    setDragOverIdx(idx);
  };

  const handleDrop = (e: React.DragEvent, idx: number) => {
    e.preventDefault();
    if (dragIdx === null || dragIdx === idx) {
      setDragIdx(null);
      setDragOverIdx(null);
      return;
    }
    const next = [...blocks];
    const [removed] = next.splice(dragIdx, 1);
    next.splice(idx, 0, removed);
    onChange(next);
    setDragIdx(null);
    setDragOverIdx(null);
  };

  const handleDragEnd = () => {
    setDragIdx(null);
    setDragOverIdx(null);
  };

  return (
    <>
      {/* 숨겨진 파일 인풋 */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/jpeg,image/png,image/gif,image/webp"
        multiple
        style={{ display: "none" }}
        onChange={(e) => {
          handleImageFiles(e.target.files, insertAfterRef.current ?? blocks.length - 1);
          e.target.value = "";
        }}
      />

      <div className="block-editor">
        {blocks.map((block, idx) => (
          <div key={block.id}>
            {/* 블록 상단에 삽입 버튼 행 (첫 번째 블록 앞에만) */}
            {idx === 0 && (
              <div className="block-insert-row">
                <button
                  type="button"
                  className="block-insert-btn"
                  onClick={() => insertTextBlock(-1)}
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                    <line x1="12" y1="5" x2="12" y2="19" />
                    <line x1="5" y1="12" x2="19" y2="12" />
                  </svg>
                  텍스트
                </button>
                <button
                  type="button"
                  className="block-insert-btn"
                  onClick={() => openImagePicker(-1)}
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                    <line x1="12" y1="5" x2="12" y2="19" />
                    <line x1="5" y1="12" x2="19" y2="12" />
                  </svg>
                  이미지
                </button>
              </div>
            )}

            {/* 블록 본체 */}
            <div
              className={`block-item${dragOverIdx === idx ? " drag-over" : ""}${dragIdx === idx ? " dragging" : ""}`}
              onDragOver={(e) => handleDragOver(e, idx)}
              onDrop={(e) => handleDrop(e, idx)}
            >
              {/* 핸들 + 삭제 */}
              <div className="block-header">
                <span
                  className="block-drag-handle"
                  draggable
                  onDragStart={() => handleDragStart(idx)}
                  onDragEnd={handleDragEnd}
                  title="드래그로 순서 변경"
                >
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <circle cx="9" cy="6" r="1.5" />
                    <circle cx="15" cy="6" r="1.5" />
                    <circle cx="9" cy="12" r="1.5" />
                    <circle cx="15" cy="12" r="1.5" />
                    <circle cx="9" cy="18" r="1.5" />
                    <circle cx="15" cy="18" r="1.5" />
                  </svg>
                  {block.type === "text" ? "텍스트" : "이미지"}
                </span>
                <button
                  type="button"
                  className="block-delete-btn"
                  onClick={() => handleDelete(block.id)}
                  title="블록 삭제"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <line x1="18" y1="6" x2="6" y2="18" />
                    <line x1="6" y1="6" x2="18" y2="18" />
                  </svg>
                </button>
              </div>

              {/* 블록 내용 */}
              {block.type === "text" ? (
                <textarea
                  className="block-textarea"
                  placeholder="내용을 입력하세요..."
                  value={block.value}
                  onChange={(e) => handleTextChange(block.id, e.target.value)}
                  rows={3}
                />
              ) : (
                <div className="block-image-wrap">
                  <div className="block-image-preview">
                    <img src={block.previewUrl} alt="첨부 이미지" />
                  </div>
                </div>
              )}
            </div>

            {/* 블록 아래 삽입 버튼 행 */}
            <div className="block-insert-row">
              <button
                type="button"
                className="block-insert-btn"
                onClick={() => insertTextBlock(idx)}
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <line x1="12" y1="5" x2="12" y2="19" />
                  <line x1="5" y1="12" x2="19" y2="12" />
                </svg>
                텍스트
              </button>
              <button
                type="button"
                className="block-insert-btn"
                onClick={() => openImagePicker(idx)}
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <line x1="12" y1="5" x2="12" y2="19" />
                  <line x1="5" y1="12" x2="19" y2="12" />
                </svg>
                이미지
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* 하단 툴바 (블록 전체 아래) */}
      <div className="block-editor-toolbar">
        <button
          type="button"
          className="block-toolbar-btn"
          onClick={() => insertTextBlock(blocks.length - 1)}
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
            <polyline points="14 2 14 8 20 8" />
            <line x1="12" y1="18" x2="12" y2="12" />
            <line x1="9" y1="15" x2="15" y2="15" />
          </svg>
          텍스트 추가
        </button>
        <button
          type="button"
          className="block-toolbar-btn"
          onClick={() => openImagePicker(blocks.length - 1)}
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="3" y="3" width="18" height="18" rx="2" />
            <circle cx="8.5" cy="8.5" r="1.5" />
            <polyline points="21 15 16 10 5 21" />
          </svg>
          이미지 추가
        </button>
      </div>
    </>
  );
}
