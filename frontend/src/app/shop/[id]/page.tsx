"use client";

import "./product-detail.css";

export default function ProductDetailPage() {
  return (
    <div className="product-detail-page">
      <div className="product-detail-image" />

      <div className="product-detail-info">
        <div className="product-detail-artist">아티스트명</div>
        <h1 className="product-detail-name">상품명</h1>
        <div className="product-detail-price">₩0</div>

        <div className="product-quantity">
          <span className="product-quantity-label">수량</span>
          <div className="product-quantity-control">
            <button className="product-quantity-btn">-</button>
            <span className="product-quantity-value">1</span>
            <button className="product-quantity-btn">+</button>
          </div>
        </div>

        <div className="product-detail-desc">
          상품 설명이 여기에 표시됩니다.
        </div>
      </div>

      <div className="product-buy-bar">
        <button className="product-cart-btn">장바구니</button>
        <button className="product-buy-btn">구매하기</button>
      </div>
    </div>
  );
}
