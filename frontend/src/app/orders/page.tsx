"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { api } from "../../lib/api";
import { useAuth } from "../../lib/auth-context";
import "./orders.css";

interface OrderItem {
  id: number;
  order_id: number;
  product_id: number;
  quantity: number;
  unit_price: number;
  total_price: number;
}

interface Order {
  id: number;
  order_number: string;
  total_amount: number;
  currency: string;
  status: string;
  tracking_number: string | null;
  shipped_at: string | null;
  delivered_at: string | null;
  created_at: string;
}

interface Product {
  id: number;
  name: string;
}

const STATUS_LABEL: Record<string, string> = {
  pending: "결제 대기",
  confirmed: "주문 확인",
  processing: "준비 중",
  shipped: "배송 중",
  delivered: "배송 완료",
  cancelled: "취소됨",
  refunded: "환불됨",
};

export default function OrdersPage() {
  const { user } = useAuth();
  const [orders, setOrders] = useState<Order[]>([]);
  const [orderItems, setOrderItems] = useState<Record<number, OrderItem[]>>({});
  const [products, setProducts] = useState<Record<number, Product>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) return;
    (async () => {
      try {
        const res = await api.get<{ items: Order[] }>("/orders");
        const list = res.items ?? [];
        setOrders(list);

        // 각 주문의 아이템 조회
        const itemsMap: Record<number, OrderItem[]> = {};
        const productIds = new Set<number>();

        await Promise.all(
          list.map(async (order) => {
            const r = await api.get<{ items: OrderItem[] }>(
              `/order-items?order_id=${order.id}`
            ).catch(() => ({ items: [] }));
            itemsMap[order.id] = r.items ?? [];
            (r.items ?? []).forEach((it) => productIds.add(it.product_id));
          })
        );
        setOrderItems(itemsMap);

        // 상품명 조회
        const productMap: Record<number, Product> = {};
        await Promise.all(
          Array.from(productIds).map(async (pid) => {
            const p = await api.get<Product>(`/products/${pid}`).catch(() => null);
            if (p) productMap[p.id] = p;
          })
        );
        setProducts(productMap);
      } catch {
        setOrders([]);
      } finally {
        setLoading(false);
      }
    })();
  }, [user]);

  const formatPrice = (amount: number, currency: string) => {
    if (currency === "KRW") return `₩${Number(amount).toLocaleString()}`;
    return `${Number(amount).toLocaleString()} ${currency}`;
  };

  const formatDate = (dateStr: string) => {
    const d = new Date(dateStr);
    return `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, "0")}.${String(d.getDate()).padStart(2, "0")}`;
  };

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
        {loading ? (
          <div className="feed-empty">로딩 중...</div>
        ) : orders.length === 0 ? (
          <div className="feed-empty">주문 내역이 없습니다</div>
        ) : (
          orders.map((order) => {
            const items = orderItems[order.id] ?? [];
            return (
              <div key={order.id} className="order-card">
                <div className="order-card-header">
                  <div>
                    <div className="order-number">{order.order_number}</div>
                    <div className="order-date">{formatDate(order.created_at)}</div>
                  </div>
                  <span className={`order-status ${order.status}`}>
                    {STATUS_LABEL[order.status] ?? order.status}
                  </span>
                </div>

                <div className="order-items">
                  {items.map((item) => (
                    <div key={item.id} className="order-item">
                      <div className="order-item-image" />
                      <span className="order-item-name">
                        {products[item.product_id]?.name ?? `상품 #${item.product_id}`}
                      </span>
                      <span className="order-item-qty">×{item.quantity}</span>
                    </div>
                  ))}
                </div>

                {order.tracking_number && (
                  <div style={{ fontSize: "12px", color: "var(--text-tertiary)", marginTop: "8px" }}>
                    송장번호: {order.tracking_number}
                  </div>
                )}

                <div className="order-total">
                  <span className="order-total-label">합계</span>
                  <span className="order-total-value">
                    {formatPrice(order.total_amount, order.currency)}
                  </span>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
