"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "../../../../lib/auth-context";
import { api } from "../../../../lib/api";
import type {
  Artist,
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

export default function UnsubscribePage() {
  const params = useParams();
  const router = useRouter();
  const slug = decodeURIComponent(params.slug as string);
  const { user, isLoading: authLoading } = useAuth();

  const [artist, setArtist] = useState<Artist | null>(null);
  const [subscription, setSubscription] = useState<Subscription | null>(null);
  const [payment, setPayment] = useState<Payment | null>(null);
  const [reasonCode, setReasonCode] = useState("");
  const [reasonDetail, setReasonDetail] = useState("");
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const artistRes = await api.get<Artist>(`/artists/by-slug/${encodeURIComponent(slug)}`);
        setArtist(artistRes);

        // 내 구독 조회
        const subsRes = await api.get<PaginatedResponse<Subscription>>("/subscriptions?skip=0&limit=100");
        const mySub = subsRes.items.find(
          (s) => s.artist_id === artistRes.id && s.fan_id === user?.id && s.status === "subscribed"
        );

        if (!mySub) {
          // 구독 중이 아니면 아티스트 페이지로
          router.replace(`/artists/${slug}`);
          return;
        }
        setSubscription(mySub);

        // 해당 구독의 결제 내역 조회
        const paymentsRes = await api.get<PaginatedResponse<Payment>>("/payments?skip=0&limit=100");
        const subPayment = paymentsRes.items.find(
          (p) =>
            p.related_id === mySub.id &&
            p.related_type === "subscription" &&
            p.status === "completed"
        );
        setPayment(subPayment ?? null);
      } catch {
        setArtist(null);
      } finally {
        setLoading(false);
      }
    })();
  }, [slug, user, router]);

  const handleCancelAndRefund = async () => {
    if (!user || !artist || !subscription) return;
    if (!reasonCode) {
      setError("취소 사유를 선택해주세요.");
      return;
    }
    setProcessing(true);
    setError("");

    try {
      const refundAmount = payment ? Number(payment.amount) : 0;

      // 1. 구독 취소 기록 생성
      await api.post("/subscription-cancellations/", {
        subscription_id: subscription.id,
        user_id: user.id,
        artist_id: artist.id,
        reason_code: reasonCode,
        reason_detail: reasonDetail || null,
        subscription_started_at: subscription.start_date,
        refund_amount: refundAmount,
        is_refunded: refundAmount > 0,
      });

      // 2. 환불 레코드 생성 (결제 내역이 있는 경우)
      if (payment && refundAmount > 0) {
        await api.post("/payment-refunds/", {
          payment_id: payment.id,
          user_id: user.id,
          refund_amount: refundAmount,
          reason: `${CANCEL_REASONS.find((r) => r.code === reasonCode)?.label || reasonCode}${reasonDetail ? ` - ${reasonDetail}` : ""}`,
          status: "completed",
        });

        // 3. 결제 상태를 환불로 변경
        await api.patch(`/payments/${payment.id}`, {
          status: "refunded",
        });
      }

      // 4. 구독 상태를 취소로 변경
      await api.patch(`/subscriptions/${subscription.id}`, {
        status: "cancelled",
      });

      // 5. 완료 → 아티스트 페이지로 이동 (새로고침으로 사이드바 갱신)
      window.location.href = `/artists/${slug}`;
    } catch {
      setError("환불 처리 중 오류가 발생했습니다. 다시 시도해주세요.");
      setProcessing(false);
    }
  };

  const formatPrice = (amount: number, currency: string) => {
    if (currency === "KRW") {
      return `${amount.toLocaleString()}원`;
    }
    return `${amount.toLocaleString()} ${currency}`;
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

  if (!artist || !subscription) {
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
        <Link href={`/artists/${slug}`} className="unsubscribe-back-btn">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </Link>
        <h1 className="unsubscribe-title">구독 취소</h1>
      </div>

      {/* 아티스트 정보 */}
      <div className="unsubscribe-artist-info">
        <div className="unsubscribe-artist-avatar">
          {artist.profile_image ? (
            <img src={artist.profile_image} alt={artist.stage_name} />
          ) : (
            <span>{artist.stage_name[0]}</span>
          )}
        </div>
        <div className="unsubscribe-artist-name">{artist.stage_name}</div>
        <div className="unsubscribe-sub-date">
          {subscription.start_date} 부터 구독 중
        </div>
      </div>

      {/* 환불 정보 */}
      {payment && (
        <div className="unsubscribe-refund-info">
          <h2 className="unsubscribe-section-title">환불 정보</h2>
          <div className="unsubscribe-refund-row">
            <span>결제 금액</span>
            <span>{formatPrice(Number(payment.amount), payment.currency)}</span>
          </div>
          <div className="unsubscribe-refund-row total">
            <span>환불 금액</span>
            <span className="unsubscribe-refund-amount">
              {formatPrice(Number(payment.amount), payment.currency)}
            </span>
          </div>
        </div>
      )}

      {/* 취소 사유 */}
      <div className="unsubscribe-section">
        <h2 className="unsubscribe-section-title">취소 사유</h2>
        <div className="unsubscribe-reason-list">
          {CANCEL_REASONS.map((reason) => (
            <button
              key={reason.code}
              className={`unsubscribe-reason-item ${reasonCode === reason.code ? "selected" : ""}`}
              onClick={() => setReasonCode(reason.code)}
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

      {/* 안내 */}
      <div className="unsubscribe-notice">
        <p>구독을 취소하면 해당 아티스트의 콘텐츠를 더 이상 이용할 수 없습니다.</p>
        {payment && <p>환불 금액은 결제 수단으로 반환됩니다.</p>}
      </div>

      {/* 에러 */}
      {error && <div className="unsubscribe-error">{error}</div>}

      {/* 버튼 */}
      <div className="unsubscribe-actions">
        <Link href={`/artists/${slug}`} className="unsubscribe-cancel-btn">
          돌아가기
        </Link>
        <button
          className="unsubscribe-confirm-btn"
          onClick={handleCancelAndRefund}
          disabled={processing}
        >
          {processing
            ? "처리 중..."
            : payment
              ? "구독 취소 및 환불"
              : "구독 취소"}
        </button>
      </div>
    </div>
  );
}
