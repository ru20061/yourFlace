"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { api } from "../../../lib/api";
import { useAuth } from "../../../lib/auth-context";
import type { Product, Celeb } from "../../data/types";
import "./product-detail.css";

export default function ProductDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { user } = useAuth();
  const id = params.id as string;

  const [product, setProduct] = useState<Product | null>(null);
  const [celeb, setCeleb] = useState<Celeb | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(true);
  const [buying, setBuying] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const p = await api.get<Product>(`/products/${id}`);
        setProduct(p);
        const c = await api.get<Celeb>(`/celebs/${p.celeb_id}`).catch(() => null);
        setCeleb(c);
      } catch {
        setProduct(null);
      } finally {
        setLoading(false);
      }
    })();
  }, [id]);

  const formatPrice = (price: number, currency: string) => {
    if (currency === "KRW") return `₩${(price * quantity).toLocaleString()}`;
    return `${(price * quantity).toLocaleString()} ${currency}`;
  };

  const handleBuy = async () => {
    if (!user || !product || buying) return;
    if (!confirm(`${product.name}을(를) 구매하시겠습니까?`)) return;

    setBuying(true);
    try {
      const totalAmount = Number(product.price) * quantity;
      const orderNumber = `ORD-${Date.now()}`;

      // 주문 생성
      const order = await api.post<{ id: number }>("/orders", {
        user_id: user.id,
        order_number: orderNumber,
        total_amount: totalAmount,
        currency: product.currency || "KRW",
        status: "confirmed",
      });

      // 주문 아이템 생성
      await api.post("/order-items", {
        order_id: order.id,
        product_id: product.id,
        quantity,
        unit_price: Number(product.price),
        total_price: totalAmount,
      });

      // 구독권 상품인 경우 구독 생성
      if (product.category === "subscription" && product.subscription_plan_id) {
        const today = new Date();
        const startDate = today.toISOString().split("T")[0];

        // subscription_plan_id로 플랜 정보 조회
        const plan = await api.get<{ duration_days: number | null; celeb_id: number }>(
          `/subscription-plans/${product.subscription_plan_id}`
        ).catch(() => null);

        const durationDays = plan?.duration_days ?? 30;
        const endDateObj = new Date(today);
        endDateObj.setDate(endDateObj.getDate() + durationDays * quantity);
        const endDate = endDateObj.toISOString().split("T")[0];

        await api.post("/subscriptions", {
          fan_id: user.id,
          celeb_id: product.celeb_id,
          status: "subscribed",
          payments_type: "paid",
          start_date: startDate,
          end_date: endDate,
        });

        alert(`구독이 완료되었습니다!\n${endDate}까지 이용 가능합니다.`);
        if (celeb) {
          router.push(`/celebs/${celeb.slug}`);
        } else {
          router.push("/");
        }
      } else {
        alert("구매가 완료되었습니다!");
        router.push("/orders");
      }
    } catch {
      alert("구매 처리 중 오류가 발생했습니다. 다시 시도해주세요.");
    } finally {
      setBuying(false);
    }
  };

  if (loading) {
    return (
      <div className="product-detail-page">
        <div className="feed-empty">로딩 중...</div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="product-detail-page">
        <div className="feed-empty">상품을 찾을 수 없습니다</div>
      </div>
    );
  }

  const isSoldOut = product.status === "sold_out" || product.stock === 0;
  const isSubscription = product.category === "subscription";

  return (
    <div className="product-detail-page">
      <div className="product-detail-image" />

      <div className="product-detail-info">
        {celeb && (
          <div
            className="product-detail-artist"
            onClick={() => router.push(`/celebs/${celeb.slug}`)}
            style={{ cursor: "pointer" }}
          >
            {celeb.stage_name}
          </div>
        )}
        <h1 className="product-detail-name">{product.name}</h1>
        <div className="product-detail-price">
          {formatPrice(Number(product.price), product.currency)}
        </div>

        {!isSoldOut && !isSubscription && (
          <div className="product-quantity">
            <span className="product-quantity-label">수량</span>
            <div className="product-quantity-control">
              <button
                className="product-quantity-btn"
                onClick={() => setQuantity((q) => Math.max(1, q - 1))}
              >
                -
              </button>
              <span className="product-quantity-value">{quantity}</span>
              <button
                className="product-quantity-btn"
                onClick={() =>
                  setQuantity((q) =>
                    product.stock ? Math.min(product.stock, q + 1) : q + 1
                  )
                }
              >
                +
              </button>
            </div>
            {product.stock !== null && product.stock > 0 && (
              <span style={{ fontSize: "12px", color: "var(--text-tertiary)" }}>
                재고 {product.stock}개
              </span>
            )}
          </div>
        )}

        {product.description && (
          <div className="product-detail-desc">{product.description}</div>
        )}
      </div>

      <div className="product-buy-bar">
        {isSoldOut ? (
          <button className="product-buy-btn" disabled style={{ opacity: 0.4 }}>
            품절
          </button>
        ) : (
          <>
            {!isSubscription && (
              <button className="product-cart-btn" disabled={buying}>장바구니</button>
            )}
            <button
              className="product-buy-btn"
              onClick={handleBuy}
              disabled={buying || !user}
              style={{ opacity: buying ? 0.6 : 1 }}
            >
              {buying ? "처리 중..." : isSubscription ? "구독하기" : "구매하기"}
            </button>
          </>
        )}
      </div>
    </div>
  );
}
