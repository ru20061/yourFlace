"use client";

import "./post-detail.css";

export default function PostDetailPage() {
  return (
    <div className="post-detail-page">
      <div className="post-detail-card">
        <div className="post-header" style={{ display: "flex", alignItems: "center", gap: 10, padding: "12px 16px" }}>
          <div style={{ width: 36, height: 36, borderRadius: "50%", background: "var(--background-secondary)", border: "2px solid var(--color-main)" }} />
          <div>
            <div style={{ fontSize: 14, fontWeight: 700 }}>작성자</div>
            <div style={{ fontSize: 12, color: "var(--text-tertiary)" }}>방금 전</div>
          </div>
        </div>
        <div style={{ padding: "0 16px 12px" }}>
          <p style={{ fontSize: 14, lineHeight: 1.6 }}>게시글 상세 내용이 여기에 표시됩니다.</p>
        </div>

        <div className="comments-section">
          <div className="comments-title">댓글</div>
          <div className="comment-item">
            <div className="comment-avatar" />
            <div className="comment-content">
              <div className="comment-author">닉네임</div>
              <div className="comment-text">댓글 내용이 여기에 표시됩니다.</div>
              <div className="comment-meta">
                <span>1시간 전</span>
                <button>답글</button>
                <button>좋아요</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="comment-input-bar">
        <input className="comment-input" placeholder="댓글을 입력하세요..." />
        <button className="comment-send-btn">전송</button>
      </div>
    </div>
  );
}
