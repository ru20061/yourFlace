"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "../../lib/auth-context";
import { api } from "../../lib/api";
import type { Product, PaginatedResponse } from "../data/types";
import "./shop.css";

export default function ShopPage() {
  const router = useRouter();
  const { user, isLoading: authLoading } = useAuth();
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) return;
    (async () => {
      try {
        const res = await api.get<PaginatedResponse<Product>>("/products/?skip=0&limit=100");
        const active = res.items.filter((p) => p.status === "active" || p.status === "sold_out");
        setProducts(active);
      } catch {
        // 조회 실패 시 빈 목록 유지
      } finally {
        setLoading(false);
      }
    })();
  }, [user]);

  const formatPrice = (price: number, currency: string) => {
    if (currency === "KRW") return `₩${price.toLocaleString()}`;
    return `${price.toLocaleString()} ${currency}`;
  };

  if (authLoading || loading) {
    return (
      <div className="shop-page">
        <h1 className="shop-title">SHOP</h1>
        <div className="feed-empty">로딩 중...</div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="shop-page">
        <h1 className="shop-title">SHOP</h1>
        <div className="feed-empty">로그인 후 이용해주세요</div>
      </div>
    );
  }

  return (
    <div className="shop-page">
      <h1 className="shop-title">SHOP</h1>
      <div className="product-grid">
        {products.length === 0 ? (
          <div className="feed-empty" style={{ gridColumn: "1 / -1" }}>
            등록된 상품이 없습니다
          </div>
        ) : (
          products.map((product) => (
            <div
              key={product.id}
              className="product-card"
              onClick={() => router.push(`/shop/${product.id}`)}
              style={{ cursor: "pointer" }}
            >
              <div className="product-image">
                <div style={{ width: "100%", height: "100%", background: "var(--background-secondary)" }} />
              </div>
              <div className="product-info">
                <div className="product-name">{product.name}</div>
                {product.category && (
                  <div className="product-artist">{product.category}</div>
                )}
                <div className="product-price">{formatPrice(Number(product.price), product.currency)}</div>
                {product.status === "sold_out" && (
                  <span className="product-badge soldout">품절</span>
                )}
                {product.stock !== null && product.stock > 0 && product.stock <= 10 && (
                  <span className="product-badge limited">잔여 {product.stock}개</span>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
