"use client";

import { useRef, forwardRef, useImperativeHandle } from "react";
import "./rich-editor.css";

export type RichTextBlock = { type: "text"; value: string };
export type RichImageBlock = { type: "image"; file: File; previewUrl: string };
export type RichEditorBlock = RichTextBlock | RichImageBlock;

export interface RichEditorHandle {
  getBlocks: () => RichEditorBlock[];
  isEmpty: () => boolean;
  clear: () => void;
  getHTML: () => string;
  setHTML: (html: string) => void;
}

interface RichEditorProps {
  placeholder?: string;
  disabled?: boolean;
}

const RichEditor = forwardRef<RichEditorHandle, RichEditorProps>(
  function RichEditor({ placeholder = "내용을 입력하세요...", disabled = false }, ref) {
    const editorRef = useRef<HTMLDivElement>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const savedRange = useRef<Range | null>(null);
    /** objectURL → File 매핑 */
    const imageFileMap = useRef<Map<string, File>>(new Map());

    /* ── 선택 영역 저장 / 복원 ── */
    const saveSelection = () => {
      const sel = window.getSelection();
      if (sel && sel.rangeCount > 0) {
        savedRange.current = sel.getRangeAt(0).cloneRange();
      }
    };

    const restoreSelection = () => {
      const editor = editorRef.current;
      if (!editor) return;
      editor.focus();
      if (savedRange.current) {
        const sel = window.getSelection();
        sel?.removeAllRanges();
        sel?.addRange(savedRange.current);
      }
    };

    /* ── 커서 위치에 이미지 삽입 ── */
    const insertImageAtCursor = (file: File) => {
      const url = URL.createObjectURL(file);
      imageFileMap.current.set(url, file);

      const img = document.createElement("img");
      img.src = url;

      // 이미지 앞뒤 단락 — 이미지 위아래에서 텍스트 입력 가능
      const wrapBefore = document.createElement("p");
      wrapBefore.innerHTML = "<br>";
      const wrapAfter = document.createElement("p");
      wrapAfter.innerHTML = "<br>";

      const sel = window.getSelection();
      const editor = editorRef.current!;

      if (sel && sel.rangeCount > 0) {
        const range = sel.getRangeAt(0);
        range.deleteContents();

        const fragment = document.createDocumentFragment();
        fragment.appendChild(wrapBefore);
        fragment.appendChild(img);
        fragment.appendChild(wrapAfter);
        range.insertNode(fragment);

        // 커서를 이미지 다음 단락으로 이동
        const newRange = document.createRange();
        newRange.setStart(wrapAfter, 0);
        newRange.collapse(true);
        sel.removeAllRanges();
        sel.addRange(newRange);
      } else {
        editor.appendChild(wrapBefore);
        editor.appendChild(img);
        editor.appendChild(wrapAfter);
      }

      editor.focus();
    };

    /* ── 툴바 execCommand 서식 적용 ── */
    const execFormat = (command: string, value?: string) => {
      restoreSelection();
      document.execCommand(command, false, value ?? undefined);
      editorRef.current?.focus();
    };

    /* ── DOM → RichEditorBlock[] 파싱 ── */
    const getBlocks = (): RichEditorBlock[] => {
      const editor = editorRef.current;
      if (!editor) return [];

      const blocks: RichEditorBlock[] = [];
      let textBuffer = "";

      const flush = () => {
        const trimmed = textBuffer.replace(/\n+$/, "").trim();
        if (trimmed) {
          blocks.push({ type: "text", value: trimmed });
        }
        textBuffer = "";
      };

      const walk = (node: Node) => {
        if (node.nodeType === Node.TEXT_NODE) {
          textBuffer += node.textContent ?? "";
          return;
        }
        if (!(node instanceof HTMLElement)) return;

        if (node.tagName === "IMG") {
          flush();
          const src = (node as HTMLImageElement).src;
          const file = imageFileMap.current.get(src);
          if (file) blocks.push({ type: "image", file, previewUrl: src });
          return;
        }
        if (node.tagName === "BR") {
          textBuffer += "\n";
          return;
        }

        node.childNodes.forEach(walk);

        if (["P", "DIV", "LI", "BLOCKQUOTE", "H1", "H2", "H3"].includes(node.tagName)) {
          textBuffer += "\n";
        }
      };

      editor.childNodes.forEach(walk);
      flush();
      return blocks;
    };

    const isEmpty = (): boolean => {
      const editor = editorRef.current;
      if (!editor) return true;
      return !editor.innerText.trim() && !editor.querySelector("img");
    };

    const clear = () => {
      if (editorRef.current) editorRef.current.innerHTML = "";
      imageFileMap.current.clear();
      savedRange.current = null;
    };

    const getHTML = (): string => editorRef.current?.innerHTML ?? "";

    const setHTML = (html: string) => {
      if (editorRef.current) {
        editorRef.current.innerHTML = html;
        imageFileMap.current.clear();
        savedRange.current = null;
      }
    };

    useImperativeHandle(ref, () => ({ getBlocks, isEmpty, clear, getHTML, setHTML }));

    return (
      <div className="rich-editor-wrap">
        {/* 툴바 */}
        <div className="rich-editor-toolbar">
          {/* 이미지 */}
          <button
            type="button"
            className="rich-toolbar-btn"
            title="이미지 삽입"
            disabled={disabled}
            onMouseDown={(e) => { e.preventDefault(); saveSelection(); }}
            onClick={() => fileInputRef.current?.click()}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="3" width="18" height="18" rx="2" />
              <circle cx="8.5" cy="8.5" r="1.5" />
              <polyline points="21 15 16 10 5 21" />
            </svg>
            이미지
          </button>

          <div className="rich-toolbar-divider" />

          {/* 굵게 */}
          <button
            type="button"
            className="rich-toolbar-btn"
            title="굵게 (Ctrl+B)"
            disabled={disabled}
            onMouseDown={(e) => { e.preventDefault(); execFormat("bold"); }}
          >
            <strong>B</strong>
          </button>
          {/* 기울임 */}
          <button
            type="button"
            className="rich-toolbar-btn"
            title="기울임 (Ctrl+I)"
            disabled={disabled}
            onMouseDown={(e) => { e.preventDefault(); execFormat("italic"); }}
          >
            <em>I</em>
          </button>
          {/* 밑줄 */}
          <button
            type="button"
            className="rich-toolbar-btn"
            title="밑줄 (Ctrl+U)"
            disabled={disabled}
            onMouseDown={(e) => { e.preventDefault(); execFormat("underline"); }}
          >
            <u>U</u>
          </button>

          <div className="rich-toolbar-divider" />

          {/* 왼쪽 정렬 */}
          <button
            type="button"
            className="rich-toolbar-btn"
            title="왼쪽 정렬"
            disabled={disabled}
            onMouseDown={(e) => { e.preventDefault(); execFormat("justifyLeft"); }}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="3" y1="6" x2="21" y2="6" />
              <line x1="3" y1="12" x2="15" y2="12" />
              <line x1="3" y1="18" x2="18" y2="18" />
            </svg>
          </button>
          {/* 가운데 정렬 */}
          <button
            type="button"
            className="rich-toolbar-btn"
            title="가운데 정렬"
            disabled={disabled}
            onMouseDown={(e) => { e.preventDefault(); execFormat("justifyCenter"); }}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="3" y1="6" x2="21" y2="6" />
              <line x1="6" y1="12" x2="18" y2="12" />
              <line x1="4" y1="18" x2="20" y2="18" />
            </svg>
          </button>
          {/* 오른쪽 정렬 */}
          <button
            type="button"
            className="rich-toolbar-btn"
            title="오른쪽 정렬"
            disabled={disabled}
            onMouseDown={(e) => { e.preventDefault(); execFormat("justifyRight"); }}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="3" y1="6" x2="21" y2="6" />
              <line x1="9" y1="12" x2="21" y2="12" />
              <line x1="6" y1="18" x2="21" y2="18" />
            </svg>
          </button>

          <div className="rich-toolbar-divider" />

          {/* 실행 취소 */}
          <button
            type="button"
            className="rich-toolbar-btn"
            title="실행 취소 (Ctrl+Z)"
            disabled={disabled}
            onMouseDown={(e) => { e.preventDefault(); execFormat("undo"); }}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="1 4 1 10 7 10" />
              <path d="M3.51 15a9 9 0 1 0 .49-3.54" />
            </svg>
          </button>
          {/* 다시 실행 */}
          <button
            type="button"
            className="rich-toolbar-btn"
            title="다시 실행 (Ctrl+Y)"
            disabled={disabled}
            onMouseDown={(e) => { e.preventDefault(); execFormat("redo"); }}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="23 4 23 10 17 10" />
              <path d="M20.49 15a9 9 0 1 1-.49-3.54" />
            </svg>
          </button>
        </div>

        {/* 에디터 본문 */}
        <div
          ref={editorRef}
          className="rich-editor-body"
          contentEditable={!disabled}
          suppressContentEditableWarning
          data-placeholder={placeholder}
          style={disabled ? { opacity: 0.5, pointerEvents: "none", userSelect: "none" } : undefined}
          onMouseUp={saveSelection}
          onKeyUp={saveSelection}
        />

        {/* 숨겨진 파일 인풋 */}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/jpeg,image/png,image/gif,image/webp"
          multiple
          style={{ display: "none" }}
          onChange={(e) => {
            restoreSelection();
            if (e.target.files) {
              Array.from(e.target.files).forEach(insertImageAtCursor);
            }
            e.target.value = "";
          }}
        />
      </div>
    );
  }
);

export default RichEditor;
