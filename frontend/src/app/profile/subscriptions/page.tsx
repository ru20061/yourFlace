"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useAuth } from "../../../lib/auth-context";
import { api } from "../../../lib/api";
import type {
  Subscription,
  Artist,
  NotificationSetting,
  PaginatedResponse,
} from "../../data/types";
import "../profile.css";

interface SubWithArtist extends Subscription {
  artist_name: string;
  artist_image: string | null;
  notifSetting: NotificationSetting | null;
}

export default function SubscriptionProfilesPage() {
  const { user, isLoading: authLoading } = useAuth();

  const [subs, setSubs] = useState<SubWithArtist[]>([]);
  const [loading, setLoading] = useState(true);

  // 프로필 편집 상태
  const [editingSubId, setEditingSubId] = useState<number | null>(null);
  const [subForm, setSubForm] = useState({ fan_nickname: "", fan_profile_image: "" });
  const [savingSub, setSavingSub] = useState(false);

  // 알림 토글 로딩
  const [togglingNotif, setTogglingNotif] = useState<number | null>(null);

  // 구독 해지
  const [cancellingId, setCancellingId] = useState<number | null>(null);

  useEffect(() => {
    if (!user) return;
    (async () => {
      try {
        // 구독 + 아티스트는 필수, 알림 설정은 실패해도 진행
        const [subsRes, artistsRes] = await Promise.all([
          api.get<PaginatedResponse<Subscription>>(`/subscriptions?skip=0&limit=100`),
          api.get<PaginatedResponse<Artist>>(`/artists?skip=0&limit=200`),
        ]);

        let notifItems: NotificationSetting[] = [];
        try {
          const notifRes = await api.get<PaginatedResponse<NotificationSetting>>(
            `/notification-settings?skip=0&limit=100`
          );
          notifItems = notifRes.items;
        } catch {
          // 알림 설정 조회 실패 시 빈 배열로 진행
        }

        const mySubs = subsRes.items.filter(
          (s) => s.fan_id === user.id && s.status === "subscribed"
        );
        const artistMap = new Map(
          artistsRes.items.map((a) => [a.id, { name: a.stage_name, image: a.profile_image }])
        );
        const notifBySubId = new Map(
          notifItems
            .filter((n) => n.user_id === user.id && n.subscription_id)
            .map((n) => [n.subscription_id!, n])
        );

        setSubs(
          mySubs.map((s) => ({
            ...s,
            artist_name: artistMap.get(s.artist_id)?.name ?? `아티스트 #${s.artist_id}`,
            artist_image: artistMap.get(s.artist_id)?.image ?? null,
            notifSetting: notifBySubId.get(s.id) ?? null,
          }))
        );
      } catch {
        // 필수 API 실패 시 무시
      } finally {
        setLoading(false);
      }
    })();
  }, [user]);

  // 프로필 편집
  const startEditing = (sub: SubWithArtist) => {
    setEditingSubId(sub.id);
    setSubForm({
      fan_nickname: sub.fan_nickname ?? "",
      fan_profile_image: sub.fan_profile_image ?? "",
    });
  };

  const cancelEditing = () => setEditingSubId(null);

  const saveProfile = async (subId: number) => {
    setSavingSub(true);
    try {
      const updated = await api.patch<Subscription>(`/subscriptions/${subId}`, {
        fan_nickname: subForm.fan_nickname || null,
        fan_profile_image: subForm.fan_profile_image || null,
      });
      setSubs((prev) =>
        prev.map((s) =>
          s.id === subId
            ? { ...s, fan_nickname: updated.fan_nickname, fan_profile_image: updated.fan_profile_image }
            : s
        )
      );
      setEditingSubId(null);
    } catch {
      alert("프로필 저장에 실패했습니다");
    } finally {
      setSavingSub(false);
    }
  };

  // 알림 전체 토글
  const toggleNotification = async (sub: SubWithArtist) => {
    if (!user) return;
    setTogglingNotif(sub.id);
    try {
      if (sub.notifSetting) {
        const newVal = !sub.notifSetting.notify_all;
        const updated = await api.patch<NotificationSetting>(
          `/notification-settings/${sub.notifSetting.id}`,
          {
            notify_all: newVal,
            notify_post: newVal,
            notify_comment: newVal,
            notify_reply: newVal,
            notify_notice: newVal,
          }
        );
        setSubs((prev) =>
          prev.map((s) => (s.id === sub.id ? { ...s, notifSetting: updated } : s))
        );
      } else {
        const created = await api.post<NotificationSetting>("/notification-settings", {
          subscription_id: sub.id,
          user_id: user.id,
          source_type: "subscription",
          notify_all: true,
          notify_post: true,
          notify_comment: true,
          notify_reply: true,
          notify_notice: true,
          notify_payment: true,
          notify_warning: true,
          receive_app: true,
          receive_push: true,
          receive_email: true,
        });
        setSubs((prev) =>
          prev.map((s) => (s.id === sub.id ? { ...s, notifSetting: created } : s))
        );
      }
    } catch {
      alert("알림 설정 변경에 실패했습니다");
    } finally {
      setTogglingNotif(null);
    }
  };

  // 개별 알림 토글
  const toggleNotifField = async (
    sub: SubWithArtist,
    field: "notify_post" | "notify_comment" | "notify_reply" | "notify_notice"
  ) => {
    if (!sub.notifSetting || !user) return;
    setTogglingNotif(sub.id);
    try {
      const newVal = !sub.notifSetting[field];
      const updated = await api.patch<NotificationSetting>(
        `/notification-settings/${sub.notifSetting.id}`,
        { [field]: newVal }
      );
      setSubs((prev) =>
        prev.map((s) => (s.id === sub.id ? { ...s, notifSetting: updated } : s))
      );
    } catch {
      alert("알림 설정 변경에 실패했습니다");
    } finally {
      setTogglingNotif(null);
    }
  };

  // 구독 해지
  const handleCancelSub = async (sub: SubWithArtist) => {
    if (!confirm(`${sub.artist_name} 구독을 해지하시겠습니까?`)) return;
    setCancellingId(sub.id);
    try {
      await api.patch(`/subscriptions/${sub.id}`, { status: "cancelled" });
      setSubs((prev) => prev.filter((s) => s.id !== sub.id));
    } catch {
      alert("구독 해지에 실패했습니다");
    } finally {
      setCancellingId(null);
    }
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString("ko-KR", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  if (authLoading || loading) {
    return (
      <div className="profile-page">
        <div className="feed-empty">로딩 중...</div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="profile-page">
        <div className="feed-empty">로그인 후 이용해주세요</div>
      </div>
    );
  }

  return (
    <div className="profile-page">
      {/* 헤더 */}
      <div className="profile-sub-page-header">
        <Link href="/profile" className="profile-sub-back">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </Link>
        <h1 className="profile-sub-page-title">구독별 프로필 설정</h1>
      </div>

      <p className="profile-sub-desc">
        아티스트별로 다른 닉네임, 프로필 이미지, 알림을 설정할 수 있습니다
      </p>

      {subs.length === 0 ? (
        <div className="feed-empty">구독 중인 아티스트가 없습니다</div>
      ) : (
        <div className="profile-sub-list">
          {subs.map((sub) => (
            <div key={sub.id} className="profile-sub-item">
              {/* 아티스트 정보 + 편집 버튼 */}
              <div className="profile-sub-header">
                <div className="profile-sub-avatar">
                  {sub.artist_image ? (
                    <img src={sub.artist_image} alt="" />
                  ) : (
                    <span>{sub.artist_name[0]}</span>
                  )}
                </div>
                <div className="profile-sub-info">
                  <div className="profile-sub-artist">{sub.artist_name}</div>
                  <div className="profile-sub-nickname">
                    {sub.fan_nickname ? `닉네임: ${sub.fan_nickname}` : "기본 닉네임 사용 중"}
                  </div>
                </div>
                <button
                  className="profile-sub-edit-btn"
                  onClick={() =>
                    editingSubId === sub.id ? cancelEditing() : startEditing(sub)
                  }
                >
                  {editingSubId === sub.id ? "취소" : "편집"}
                </button>
              </div>

              {/* 구독 정보 */}
              <div className="sub-meta">
                <span className={`sub-badge ${sub.payments_type}`}>
                  {sub.payments_type === "paid" ? "유료" : "무료"}
                </span>
                <span className="sub-meta-date">
                  {formatDate(sub.start_date)} ~
                  {sub.end_date ? ` ${formatDate(sub.end_date)}` : " 구독 중"}
                </span>
              </div>

              {/* 프로필 편집 폼 */}
              {editingSubId === sub.id && (
                <div className="profile-sub-form">
                  {/* 이미지 미리보기 */}
                  {subForm.fan_profile_image && (
                    <div className="sub-image-preview">
                      <img
                        src={subForm.fan_profile_image}
                        alt="미리보기"
                        onError={(e) => { (e.target as HTMLImageElement).style.display = "none"; }}
                      />
                    </div>
                  )}
                  <div className="profile-form-group">
                    <label className="profile-form-label">팬 닉네임</label>
                    <input
                      className="profile-form-input"
                      value={subForm.fan_nickname}
                      onChange={(e) =>
                        setSubForm((f) => ({ ...f, fan_nickname: e.target.value }))
                      }
                      placeholder="이 아티스트에서 사용할 닉네임"
                      maxLength={50}
                    />
                  </div>
                  <div className="profile-form-group">
                    <label className="profile-form-label">팬 프로필 이미지 URL</label>
                    <input
                      className="profile-form-input"
                      value={subForm.fan_profile_image}
                      onChange={(e) =>
                        setSubForm((f) => ({ ...f, fan_profile_image: e.target.value }))
                      }
                      placeholder="https://example.com/image.jpg"
                    />
                  </div>
                  <button
                    className="profile-save-btn"
                    onClick={() => saveProfile(sub.id)}
                    disabled={savingSub}
                  >
                    {savingSub ? "저장 중..." : "저장"}
                  </button>
                </div>
              )}

              {/* 알림 설정 */}
              <div className="sub-notif-section">
                <div className="sub-notif-row">
                  <span className="sub-notif-label">알림 전체</span>
                  <button
                    className={`sub-toggle ${sub.notifSetting?.notify_all ? "on" : "off"}`}
                    onClick={() => toggleNotification(sub)}
                    disabled={togglingNotif === sub.id}
                  >
                    <span className="sub-toggle-thumb" />
                  </button>
                </div>

                {sub.notifSetting?.notify_all && (
                  <>
                    {([
                      ["notify_post", "새 게시글"],
                      ["notify_comment", "댓글"],
                      ["notify_reply", "답글"],
                      ["notify_notice", "공지사항"],
                    ] as const).map(([field, label]) => (
                      <div key={field} className="sub-notif-row sub-notif-detail">
                        <span className="sub-notif-label">{label}</span>
                        <button
                          className={`sub-toggle small ${sub.notifSetting?.[field] ? "on" : "off"}`}
                          onClick={() => toggleNotifField(sub, field)}
                          disabled={togglingNotif === sub.id}
                        >
                          <span className="sub-toggle-thumb" />
                        </button>
                      </div>
                    ))}
                  </>
                )}
              </div>

              {/* 구독 해지 */}
              <button
                className="sub-cancel-btn"
                onClick={() => handleCancelSub(sub)}
                disabled={cancellingId === sub.id}
              >
                {cancellingId === sub.id ? "해지 중..." : "구독 해지"}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
