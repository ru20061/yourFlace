"use client";

import "./shop.css";

export default function ShopPage() {
  return (
    <div className="shop-page">
      <h1 className="shop-title">SHOP</h1>
      <div className="product-grid">
        <div className="feed-empty" style={{ gridColumn: "1 / -1" }}>
          등록된 상품이 없습니다
        </div>
      </div>
    </div>
  );
}
