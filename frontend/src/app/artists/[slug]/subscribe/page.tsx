"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "../../../../lib/auth-context";
import { api } from "../../../../lib/api";
import type {
  Artist,
  SubscriptionPlan,
  Subscription,
  PaginatedResponse,
} from "../../../data/types";
import "./subscribe.css";

interface PaymentResponse {
  id: number;
  status: string;
}

const BILLING_CYCLE_LABEL: Record<string, string> = {
  monthly: "월간",
  yearly: "연간",
  "one-time": "1회",
};

const PAYMENT_METHODS = [
  { id: "card", label: "카드결제", icon: "💳" },
  { id: "simple", label: "간편결제", icon: "📱" },
  { id: "bank", label: "계좌이체", icon: "🏦" },
] as const;

export default function SubscribePage() {
  const params = useParams();
  const router = useRouter();
  const slug = decodeURIComponent(params.slug as string);
  const { user, isLoading: authLoading } = useAuth();

  const [artist, setArtist] = useState<Artist | null>(null);
  const [plans, setPlans] = useState<SubscriptionPlan[]>([]);
  const [selectedPlan, setSelectedPlan] = useState<SubscriptionPlan | null>(null);
  const [paymentMethod, setPaymentMethod] = useState<string>("card");
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const artistRes = await api.get<Artist>(`/artists/by-slug/${encodeURIComponent(slug)}`);
        setArtist(artistRes);

        // 이미 구독 중인지 확인
        const subsRes = await api.get<PaginatedResponse<Subscription>>("/subscriptions?skip=0&limit=100");
        const alreadySubscribed = subsRes.items.some(
          (s) => s.artist_id === artistRes.id && s.fan_id === user?.id && s.status === "subscribed"
        );
        if (alreadySubscribed) {
          router.replace(`/artists/${slug}`);
          return;
        }

        // 아티스트 플랜 조회
        const plansRes = await api.get<PaginatedResponse<SubscriptionPlan>>("/subscription-plans?skip=0&limit=100");
        const artistPlans = plansRes.items.filter(
          (p) => p.artist_id === artistRes.id && p.is_active
        );
        setPlans(artistPlans);
        if (artistPlans.length > 0) {
          setSelectedPlan(artistPlans[0]);
        }
      } catch {
        setArtist(null);
      } finally {
        setLoading(false);
      }
    })();
  }, [slug, user, router]);

  const handlePayment = async () => {
    if (!user || !artist || !selectedPlan) return;
    setProcessing(true);
    setError("");

    try {
      // 1. 구독 먼저 생성
      const today = new Date().toISOString().split("T")[0];
      const subscription = await api.post<Subscription>("/subscriptions/", {
        fan_id: user.id,
        artist_id: artist.id,
        status: "subscribed",
        payments_type: "paid",
        start_date: today,
      });

      // 2. 결제 레코드 생성 (모의 - 즉시 completed, 구독 ID 연결)
      await api.post<PaymentResponse>("/payments/", {
        user_id: user.id,
        payment_type: "subscription",
        related_id: subscription.id,
        related_type: "subscription",
        amount: Number(selectedPlan.price),
        currency: selectedPlan.currency,
        status: "completed",
      });

      // 3. 구독 완료 → 아티스트 페이지로 이동 (새로고침으로 사이드바 갱신)
      window.location.href = `/artists/${slug}`;
    } catch {
      setError("결제 처리 중 오류가 발생했습니다. 다시 시도해주세요.");
      setProcessing(false);
    }
  };

  const formatPrice = (price: number, currency: string) => {
    if (currency === "KRW") {
      return `${price.toLocaleString()}원`;
    }
    return `${price.toLocaleString()} ${currency}`;
  };

  if (loading || authLoading) {
    return (
      <div className="subscribe-page">
        <div className="feed-empty">로딩 중...</div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="subscribe-page">
        <div className="feed-empty">로그인 후 이용해주세요</div>
      </div>
    );
  }

  if (!artist) {
    return (
      <div className="subscribe-page">
        <div className="feed-empty">아티스트를 찾을 수 없습니다</div>
      </div>
    );
  }

  if (plans.length === 0) {
    return (
      <div className="subscribe-page">
        <div className="subscribe-header">
          <Link href={`/artists/${slug}`} className="subscribe-back-btn">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="15 18 9 12 15 6" />
            </svg>
          </Link>
          <h1 className="subscribe-title">구독하기</h1>
        </div>
        <div className="feed-empty">현재 이용 가능한 구독 플랜이 없습니다</div>
      </div>
    );
  }

  return (
    <div className="subscribe-page">
      {/* 헤더 */}
      <div className="subscribe-header">
        <Link href={`/artists/${slug}`} className="subscribe-back-btn">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </Link>
        <h1 className="subscribe-title">구독하기</h1>
      </div>

      {/* 아티스트 정보 */}
      <div className="subscribe-artist-info">
        <div className="subscribe-artist-avatar">
          {artist.profile_image ? (
            <img src={artist.profile_image} alt={artist.stage_name} />
          ) : (
            <span>{artist.stage_name[0]}</span>
          )}
        </div>
        <div className="subscribe-artist-name">{artist.stage_name}</div>
      </div>

      {/* 플랜 선택 */}
      <div className="subscribe-section">
        <h2 className="subscribe-section-title">구독 플랜 선택</h2>
        <div className="subscribe-plan-list">
          {plans.map((plan) => (
            <button
              key={plan.id}
              className={`subscribe-plan-card ${selectedPlan?.id === plan.id ? "selected" : ""}`}
              onClick={() => setSelectedPlan(plan)}
            >
              <div className="subscribe-plan-header">
                <div className="subscribe-plan-name">{plan.name}</div>
                <div className="subscribe-plan-cycle">
                  {BILLING_CYCLE_LABEL[plan.billing_cycle] || plan.billing_cycle}
                </div>
              </div>
              <div className="subscribe-plan-price">
                {formatPrice(plan.price, plan.currency)}
                {plan.billing_cycle === "monthly" && <span className="subscribe-plan-period">/월</span>}
                {plan.billing_cycle === "yearly" && <span className="subscribe-plan-period">/년</span>}
              </div>
              {plan.benefits && (
                <div className="subscribe-plan-benefits">{plan.benefits}</div>
              )}
              {selectedPlan?.id === plan.id && (
                <div className="subscribe-plan-check">
                  <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="3">
                    <polyline points="20 6 9 17 4 12" />
                  </svg>
                </div>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* 결제 수단 선택 */}
      <div className="subscribe-section">
        <h2 className="subscribe-section-title">결제 수단</h2>
        <div className="subscribe-payment-methods">
          {PAYMENT_METHODS.map((method) => (
            <button
              key={method.id}
              className={`subscribe-payment-method ${paymentMethod === method.id ? "selected" : ""}`}
              onClick={() => setPaymentMethod(method.id)}
            >
              <span className="subscribe-payment-icon">{method.icon}</span>
              <span className="subscribe-payment-label">{method.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* 결제 요약 */}
      {selectedPlan && (
        <div className="subscribe-summary">
          <div className="subscribe-summary-row">
            <span>구독 플랜</span>
            <span>{selectedPlan.name}</span>
          </div>
          <div className="subscribe-summary-row">
            <span>결제 주기</span>
            <span>{BILLING_CYCLE_LABEL[selectedPlan.billing_cycle] || selectedPlan.billing_cycle}</span>
          </div>
          <div className="subscribe-summary-row total">
            <span>결제 금액</span>
            <span>{formatPrice(selectedPlan.price, selectedPlan.currency)}</span>
          </div>
        </div>
      )}

      {/* 에러 메시지 */}
      {error && <div className="subscribe-error">{error}</div>}

      {/* 결제 버튼 */}
      <button
        className="subscribe-pay-btn"
        onClick={handlePayment}
        disabled={!selectedPlan || processing}
      >
        {processing ? "결제 처리 중..." : selectedPlan ? `${formatPrice(selectedPlan.price, selectedPlan.currency)} 결제하기` : "플랜을 선택해주세요"}
      </button>
    </div>
  );
}
