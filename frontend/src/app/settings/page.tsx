"use client";

import "./settings.css";

export default function SettingsPage() {
  return (
    <div className="settings-page">
      <h1 className="settings-title">설정</h1>

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
              <div className="theme-option light selected" />
              <div className="theme-option dark" />
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
            <div className="settings-toggle on" />
          </div>
          <div className="settings-item">
            <span className="settings-item-label">채팅 알림</span>
            <div className="settings-toggle on" />
          </div>
          <div className="settings-item">
            <span className="settings-item-label">이벤트 알림</span>
            <div className="settings-toggle" />
          </div>
        </div>
      </div>

      {/* 개인정보 */}
      <div className="settings-section">
        <div className="settings-section-title">개인정보</div>
        <div className="settings-list">
          <div className="settings-item">
            <span className="settings-item-label">프로필 공개</span>
            <div className="settings-toggle on" />
          </div>
          <div className="settings-item">
            <span className="settings-item-label">활동 상태 표시</span>
            <div className="settings-toggle on" />
          </div>
        </div>
      </div>

      {/* 위험 영역 */}
      <div className="settings-danger-zone">
        <button className="settings-danger-btn">회원 탈퇴</button>
      </div>
    </div>
  );
}
