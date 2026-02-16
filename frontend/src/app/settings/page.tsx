"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "../../lib/auth-context";
import { api } from "../../lib/api";
import "./settings.css";

interface UserSettingResponse {
  id: number;
  user_id: number;
  language: string;
  theme: "light" | "dark";
  show_profile: boolean;
  show_activity_status: boolean;
  receive_system_push: boolean;
  receive_system_app: boolean;
  receive_system_notice: boolean;
}

export default function SettingsPage() {
  const router = useRouter();
  const { logout, isLoggedIn } = useAuth();

  const [theme, setTheme] = useState<"light" | "dark">("light");
  const [pushNotif, setPushNotif] = useState(true);
  const [chatNotif, setChatNotif] = useState(true);
  const [eventNotif, setEventNotif] = useState(false);
  const [profilePublic, setProfilePublic] = useState(true);
  const [activityStatus, setActivityStatus] = useState(true);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isLoggedIn) return;
    (async () => {
      try {
        const data = await api.get<UserSettingResponse>("/user-settings/me");
        setTheme(data.theme);
        setPushNotif(data.receive_system_push);
        setChatNotif(data.receive_system_app);
        setEventNotif(data.receive_system_notice);
        setProfilePublic(data.show_profile);
        setActivityStatus(data.show_activity_status);
        document.documentElement.setAttribute("data-theme", data.theme);
      } catch {
        // 설정이 없으면 기본값 사용
      } finally {
        setLoading(false);
      }
    })();
  }, [isLoggedIn]);

  const handleThemeChange = (selected: "light" | "dark") => {
    setTheme(selected);
    document.documentElement.setAttribute("data-theme", selected);
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await api.patch("/user-settings/me", {
        theme,
        receive_system_push: pushNotif,
        receive_system_app: chatNotif,
        receive_system_notice: eventNotif,
        show_profile: profilePublic,
        show_activity_status: activityStatus,
      });
      alert("저장되었습니다");
      window.location.reload();
    } catch {
      alert("설정 저장에 실패했습니다.");
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteAccount = () => {
    setShowDeleteConfirm(true);
  };

  const confirmDelete = async () => {
    // TODO: API 연동 후 실제 회원 탈퇴 처리
    setShowDeleteConfirm(false);
    logout();
    router.push("/login");
  };

  if (loading) {
    return (
      <div className="settings-page">
        <div className="settings-header">
          <Link href="/profile" className="settings-back-btn">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="15 18 9 12 15 6" />
            </svg>
          </Link>
          <h1 className="settings-title">설정</h1>
        </div>
      </div>
    );
  }

  return (
    <div className="settings-page">
      <div className="settings-header">
        <Link href="/profile" className="settings-back-btn">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </Link>
        <h1 className="settings-title">설정</h1>
      </div>

      {/* 일반 설정 */}
      <div className="settings-section">
        <div className="settings-section-title">일반</div>
        <div className="settings-list">
          <div className="settings-item">
            <span className="settings-item-label">언어</span>
            <span className="settings-item-value">한국어</span>
          </div>
          <div className="settings-item">
            <span className="settings-item-label">테마</span>
            <div className="theme-options">
              <div
                className={`theme-option light ${theme === "light" ? "selected" : ""}`}
                onClick={() => handleThemeChange("light")}
              />
              <div
                className={`theme-option dark ${theme === "dark" ? "selected" : ""}`}
                onClick={() => handleThemeChange("dark")}
              />
            </div>
          </div>
        </div>
      </div>

      {/* 알림 설정 */}
      <div className="settings-section">
        <div className="settings-section-title">알림</div>
        <div className="settings-list">
          <div className="settings-item">
            <span className="settings-item-label">푸시 알림</span>
            <div
              className={`settings-toggle ${pushNotif ? "on" : ""}`}
              onClick={() => setPushNotif(!pushNotif)}
            />
          </div>
          <div className="settings-item">
            <span className="settings-item-label">채팅 알림</span>
            <div
              className={`settings-toggle ${chatNotif ? "on" : ""}`}
              onClick={() => setChatNotif(!chatNotif)}
            />
          </div>
          <div className="settings-item">
            <span className="settings-item-label">이벤트 알림</span>
            <div
              className={`settings-toggle ${eventNotif ? "on" : ""}`}
              onClick={() => setEventNotif(!eventNotif)}
            />
          </div>
        </div>
      </div>

      {/* 개인정보 */}
      <div className="settings-section">
        <div className="settings-section-title">개인정보</div>
        <div className="settings-list">
          <div className="settings-item">
            <span className="settings-item-label">프로필 공개</span>
            <div
              className={`settings-toggle ${profilePublic ? "on" : ""}`}
              onClick={() => setProfilePublic(!profilePublic)}
            />
          </div>
          <div className="settings-item">
            <span className="settings-item-label">활동 상태 표시</span>
            <div
              className={`settings-toggle ${activityStatus ? "on" : ""}`}
              onClick={() => setActivityStatus(!activityStatus)}
            />
          </div>
        </div>
      </div>

      {/* 설정 저장 */}
      <button
        className="settings-save-btn"
        onClick={handleSave}
        disabled={saving}
      >
        {saving ? "저장 중..." : "설정 저장"}
      </button>

      {/* 위험 영역 */}
      <div className="settings-danger-zone">
        <button className="settings-danger-btn" onClick={handleDeleteAccount}>
          회원 탈퇴
        </button>
      </div>

      {/* 회원 탈퇴 확인 모달 */}
      {showDeleteConfirm && (
        <div className="settings-modal-overlay" onClick={() => setShowDeleteConfirm(false)}>
          <div className="settings-modal" onClick={(e) => e.stopPropagation()}>
            <h3 className="settings-modal-title">회원 탈퇴</h3>
            <p className="settings-modal-desc">
              정말 탈퇴하시겠습니까? 이 작업은 되돌릴 수 없으며 모든 데이터가 삭제됩니다.
            </p>
            <div className="settings-modal-actions">
              <button
                className="settings-modal-cancel"
                onClick={() => setShowDeleteConfirm(false)}
              >
                취소
              </button>
              <button className="settings-modal-confirm" onClick={confirmDelete}>
                탈퇴하기
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
