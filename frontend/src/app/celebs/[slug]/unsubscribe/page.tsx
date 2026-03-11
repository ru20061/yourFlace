"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "../../../../lib/auth-context";
import { api } from "../../../../lib/api";
import type {
  Celeb,
  Subscription,
  Payment,
  PaginatedResponse,
} from "../../../data/types";
import "./unsubscribe.css";

const CANCEL_REASONS = [
  { code: "too_expensive", label: "가격이 비쌉니다" },
  { code: "not_enough_content", label: "콘텐츠가 부족합니다" },
  { code: "found_alternative", label: "다른 서비스를 이용합니다" },
  { code: "temporary", label: "일시적으로 중단합니다" },
  { code: "other", label: "기타" },
] as const;

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
  user_id: number;
  order_number: string;
  total_amount: number;
  currency: string;
  status: string;
  created_at: string;
}

export default function UnsubscribePage() {
  const params = useParams();
  const router = useRouter();
  const slug = decodeURIComponent(params.slug as string);
  const { user, isLoading: authLoading } = useAuth();

  const [celeb, setCeleb] = useState<Celeb | null>(null);
  const [subscription, setSubscription] = useState<Subscription | null>(null);
  const [payment, setPayment] = useState<Payment | null>(null);
  const [refundAmount, setRefundAmount] = useState(0);
  const [refundCurrency, setRefundCurrency] = useState("KRW");
  const [reasonCode, setReasonCode] = useState("");
  const [reasonDetail, setReasonDetail] = useState("");
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState("");

  // 2단계 플로우: 1 = 취소 사유 선택, 2 = 환불 정보 확인
  const [step, setStep] = useState<1 | 2>(1);

  useEffect(() => {
    if (!user) return;
    (async () => {
      try {
        const celebRes = await api.get<Celeb>(`/celebs/by-slug/${encodeURIComponent(slug)}`);
        setCeleb(celebRes);

        // 내 구독 조회
        const subsRes = await api.get<PaginatedResponse<Subscription>>("/subscriptions?skip=0&limit=100");
        const mySub = subsRes.items.find(
          (s) => s.celeb_id === celebRes.id && s.fan_id === user.id && s.status === "subscribed"
        );

        if (!mySub) {
          router.replace(`/celebs/${slug}`);
          return;
        }
        setSubscription(mySub);

        // 1차: payment에서 subscription 직접 연결된 결제 조회
        let foundPayment: Payment | null = null;
        let foundAmount = 0;
        let foundCurrency = "KRW";

        try {
          const paymentsRes = await api.get<PaginatedResponse<Payment>>("/payments?skip=0&limit=100");
          const subPayment = paymentsRes.items.find(
            (p) =>
              p.user_id === user.id &&
              p.related_id === mySub.id &&
              p.related_type === "subscription" &&
              p.status === "completed"
          );
          if (subPayment) {
            foundPayment = subPayment;
            foundAmount = Number(subPayment.amount);
            foundCurrency = subPayment.currency;
          }
        } catch { /* 무시 */ }

        // 2차: 주문(Order) 기반 결제 조회 — subscription 상품을 통해 구독한 경우
        if (!foundPayment && mySub.payments_type === "paid") {
          try {
            const [ordersRes, orderItemsRes] = await Promise.all([
              api.get<PaginatedResponse<Order>>("/orders?skip=0&limit=200"),
              api.get<PaginatedResponse<OrderItem>>("/order-items?skip=0&limit=500"),
            ]);
            const myOrders = ordersRes.items.filter(
              (o) => o.user_id === user.id && o.status !== "cancelled" && o.status !== "refunded"
            );
            const myOrderIds = new Set(myOrders.map((o) => o.id));
            const subItems = orderItemsRes.items.filter(
              (oi) => myOrderIds.has(oi.order_id)
            );
            if (subItems.length > 0) {
              const latestOrder = myOrders.sort(
                (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
              )[0];
              const latestItems = subItems.filter((oi) => oi.order_id === latestOrder.id);
              if (latestItems.length > 0) {
                foundAmount = latestItems.reduce((sum, oi) => sum + Number(oi.total_price), 0);
                foundCurrency = latestOrder.currency || "KRW";
              }
            }
          } catch { /* 무시 */ }
        }

        setPayment(foundPayment);
        setRefundAmount(foundAmount);
        setRefundCurrency(foundCurrency);
      } catch {
        setCeleb(null);
      } finally {
        setLoading(false);
      }
    })();
  }, [slug, user, router]);

  const formatPrice = (amount: number, currency: string) => {
    if (currency === "KRW") return `${amount.toLocaleString()}원`;
    return `${amount.toLocaleString()} ${currency}`;
  };

  // 남은 구독일 계산 (부분환불 기준)
  const remainingDays = (() => {
    if (!subscription?.end_date) return null;
    const end = new Date(subscription.end_date);
    const now = new Date();
    const diff = Math.max(0, Math.ceil((end.getTime() - now.getTime()) / (1000 * 60 * 60 * 24)));
    return diff;
  })();

  const totalDays = (() => {
    if (!subscription?.start_date || !subscription?.end_date) return null;
    const start = new Date(subscription.start_date);
    const end = new Date(subscription.end_date);
    return Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
  })();

  // 잔여일 비율 기반 환불 금액 계산
  const calculatedRefund = (() => {
    if (!refundAmount || !remainingDays || !totalDays || totalDays === 0) return refundAmount;
    return Math.floor((refundAmount * remainingDays) / totalDays);
  })();

  const isPaid = subscription?.payments_type === "paid" && calculatedRefund > 0;

  // Step 1 → Step 2 이동
  const handleGoToRefund = () => {
    if (!reasonCode) {
      setError("취소 사유를 선택해주세요.");
      return;
    }
    setError("");
    setStep(2);
  };

  // 최종 구독 취소 처리
  const handleCancelAndRefund = async () => {
    if (!user || !celeb || !subscription) return;
    setProcessing(true);
    setError("");

    try {
      // 1. 구독 취소 기록 생성
      await api.post("/subscription-cancellations/", {
        subscription_id: subscription.id,
        user_id: user.id,
        celeb_id: celeb.id,
        reason_code: reasonCode,
        reason_detail: reasonDetail || null,
        subscription_started_at: subscription.start_date,
        refund_amount: calculatedRefund,
        is_refunded: calculatedRefund > 0,
      });

      // 2. 환불 레코드 생성 (결제 내역이 있는 경우)
      if (payment && calculatedRefund > 0) {
        await api.post("/payment-refunds/", {
          payment_id: payment.id,
          user_id: user.id,
          refund_amount: calculatedRefund,
          reason: `${CANCEL_REASONS.find((r) => r.code === reasonCode)?.label || reasonCode}${reasonDetail ? ` - ${reasonDetail}` : ""}`,
          status: "completed",
        });

        // 3. 결제 상태를 환불로 변경
        await api.patch(`/payments/${payment.id}`, { status: "refunded" });
      }

      // 4. 구독 상태를 취소로 변경
      await api.patch(`/subscriptions/${subscription.id}`, { status: "cancelled" });

      // 5. 완료 → 프로필 구독 페이지로 이동
      window.location.href = "/profile/subscriptions";
    } catch {
      setError("처리 중 오류가 발생했습니다. 다시 시도해주세요.");
      setProcessing(false);
    }
  };

  if (loading || authLoading) {
    return (
      <div className="unsubscribe-page">
        <div className="feed-empty">로딩 중...</div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="unsubscribe-page">
        <div className="feed-empty">로그인 후 이용해주세요</div>
      </div>
    );
  }

  if (!celeb || !subscription) {
    return (
      <div className="unsubscribe-page">
        <div className="feed-empty">구독 정보를 찾을 수 없습니다</div>
      </div>
    );
  }

  return (
    <div className="unsubscribe-page">
      {/* 헤더 */}
      <div className="unsubscribe-header">
        {step === 1 ? (
          <Link href="/profile/subscriptions" className="unsubscribe-back-btn">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="15 18 9 12 15 6" />
            </svg>
          </Link>
        ) : (
          <button className="unsubscribe-back-btn" onClick={() => { setStep(1); setError(""); }}>
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="15 18 9 12 15 6" />
            </svg>
          </button>
        )}
        <h1 className="unsubscribe-title">구독 취소</h1>
      </div>

      {/* 단계 표시 */}
      <div className="unsubscribe-steps">
        <div className={`unsubscribe-step ${step === 1 ? "active" : "done"}`}>
          <div className="unsubscribe-step-circle">{step > 1 ? "✓" : "1"}</div>
          <span>취소 사유</span>
        </div>
        <div className="unsubscribe-step-line" />
        <div className={`unsubscribe-step ${step === 2 ? "active" : ""}`}>
          <div className="unsubscribe-step-circle">2</div>
          <span>환불 정보</span>
        </div>
      </div>

      {/* 셀럽 정보 */}
      <div className="unsubscribe-artist-info">
        <div className="unsubscribe-artist-avatar">
          {celeb.profile_image ? (
            <img src={celeb.profile_image} alt={celeb.stage_name} />
          ) : (
            <span>{celeb.stage_name[0]}</span>
          )}
        </div>
        <div className="unsubscribe-artist-name">{celeb.stage_name}</div>
        <div className="unsubscribe-sub-date">
          {subscription.start_date} 구독 시작
          {subscription.end_date && ` · ${subscription.end_date} 만료`}
        </div>
      </div>

      {/* ── Step 1: 취소 사유 선택 ── */}
      {step === 1 && (
        <>
          <div className="unsubscribe-section">
            <h2 className="unsubscribe-section-title">취소 사유를 선택해주세요</h2>
            <div className="unsubscribe-reason-list">
              {CANCEL_REASONS.map((reason) => (
                <button
                  key={reason.code}
                  className={`unsubscribe-reason-item ${reasonCode === reason.code ? "selected" : ""}`}
                  onClick={() => { setReasonCode(reason.code); setError(""); }}
                >
                  <div className={`unsubscribe-reason-radio ${reasonCode === reason.code ? "checked" : ""}`} />
                  <span>{reason.label}</span>
                </button>
              ))}
            </div>

            {reasonCode === "other" && (
              <textarea
                className="unsubscribe-reason-detail"
                placeholder="상세 사유를 입력해주세요"
                value={reasonDetail}
                onChange={(e) => setReasonDetail(e.target.value)}
                rows={3}
              />
            )}
          </div>

          {error && <div className="unsubscribe-error">{error}</div>}

          <div className="unsubscribe-actions">
            <Link href="/profile/subscriptions" className="unsubscribe-cancel-btn">
              돌아가기
            </Link>
            <button className="unsubscribe-confirm-btn" onClick={handleGoToRefund}>
              다음
            </button>
          </div>
        </>
      )}

      {/* ── Step 2: 환불 정보 확인 ── */}
      {step === 2 && (
        <>
          {/* 선택한 취소 사유 요약 */}
          <div className="unsubscribe-reason-summary">
            <span className="unsubscribe-reason-summary-label">취소 사유</span>
            <span className="unsubscribe-reason-summary-value">
              {CANCEL_REASONS.find((r) => r.code === reasonCode)?.label}
              {reasonDetail && ` — ${reasonDetail}`}
            </span>
          </div>

          {/* 환불 정보 — 구독 유형에 관계없이 항상 표시 */}
          <div className="unsubscribe-refund-info">
            <h2 className="unsubscribe-section-title">환불 정보</h2>

            {subscription.payments_type === "free" ? (
              <p style={{ fontSize: 14, color: "var(--text-secondary)", padding: "8px 0" }}>
                무료 구독은 환불 대상이 아닙니다.
              </p>
            ) : refundAmount > 0 ? (
              <>
                <div className="unsubscribe-refund-row">
                  <span>결제 금액</span>
                  <span>{formatPrice(refundAmount, refundCurrency)}</span>
                </div>
                {remainingDays !== null && totalDays !== null && (
                  <div className="unsubscribe-refund-row">
                    <span>남은 기간</span>
                    <span>{remainingDays}일 / {totalDays}일</span>
                  </div>
                )}
                <div className="unsubscribe-refund-row total">
                  <span>환불 예상액</span>
                  <span className="unsubscribe-refund-amount">
                    {formatPrice(calculatedRefund, refundCurrency)}
                  </span>
                </div>
                <p style={{ fontSize: 12, color: "var(--text-tertiary)", marginTop: 8, lineHeight: 1.5 }}>
                  * 잔여 구독 기간에 비례하여 환불됩니다. 환불금은 결제 수단으로 반환됩니다.
                </p>
              </>
            ) : (
              <p style={{ fontSize: 14, color: "var(--text-secondary)", padding: "8px 0" }}>
                결제 내역을 찾을 수 없어 환불이 처리되지 않습니다.
              </p>
            )}
          </div>

          {/* 안내 */}
          <div className="unsubscribe-notice">
            <p>구독을 취소하면 즉시 해당 셀럽의 콘텐츠를 더 이상 이용할 수 없습니다.</p>
            {isPaid && <p>환불 금액은 영업일 기준 3~5일 내 결제 수단으로 반환됩니다.</p>}
          </div>

          {error && <div className="unsubscribe-error">{error}</div>}

          <div className="unsubscribe-actions">
            <button
              className="unsubscribe-cancel-btn"
              onClick={() => { setStep(1); setError(""); }}
            >
              이전
            </button>
            <button
              className="unsubscribe-confirm-btn"
              onClick={handleCancelAndRefund}
              disabled={processing}
            >
              {processing ? "처리 중..." : isPaid ? "구독 취소 및 환불 신청" : "구독 취소"}
            </button>
          </div>
        </>
      )}
    </div>
  );
}
