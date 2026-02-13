"use client";

import "./orders.css";

export default function OrdersPage() {
  return (
    <div className="orders-page">
      <h1 className="orders-title">주문 내역</h1>
      <div className="order-list">
        <div className="feed-empty">주문 내역이 없습니다</div>
      </div>
    </div>
  );
}
