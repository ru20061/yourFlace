"use client";

import "./faq.css";

export default function FaqPage() {
  return (
    <div className="faq-page">
      <h1 className="faq-title">FAQ 관리</h1>
      <div className="faq-list">
        <div className="feed-empty">등록된 FAQ가 없습니다</div>
      </div>
    </div>
  );
}
