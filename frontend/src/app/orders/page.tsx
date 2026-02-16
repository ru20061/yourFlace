"use client";

import Link from "next/link";
import "./orders.css";

export default function OrdersPage() {
  return (
    <div className="orders-page">
      <div className="orders-header">
        <Link href="/profile" className="orders-back-btn">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </Link>
        <h1 className="orders-title">주문 내역</h1>
      </div>
      <div className="order-list">
        <div className="feed-empty">주문 내역이 없습니다</div>
      </div>
    </div>
  );
}
