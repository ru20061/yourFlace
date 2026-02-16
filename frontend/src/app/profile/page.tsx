"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useAuth } from "../../lib/auth-context";
import { api } from "../../lib/api";
import FlaceDatePicker from "../components/FlaceDatePicker/FlaceDatePicker";
import type { Profile, PaginatedResponse } from "../data/types";
import "./profile.css";

export default function ProfilePage() {
  const { user, isLoading: authLoading, refreshUser } = useAuth();

  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);

  // 프로필 편집 모드
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({
    nickname: "",
    full_name: "",
    phone: "",
    gender: "",
    birth_date: "",
    profile_image: "",
  });
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!user) return;
    (async () => {
      try {
        const profilesRes = await api.get<PaginatedResponse<Profile>>(
          `/profiles?skip=0&limit=100`
        );
        const myProfile = profilesRes.items.find((p) => p.user_id === user.id) ?? null;
        setProfile(myProfile);
      } catch {
        // 실패 시 무시
      } finally {
        setLoading(false);
      }
    })();
  }, [user]);

  const startEditing = () => {
    setForm({
      nickname: profile?.nickname ?? user?.nickname ?? "",
      full_name: profile?.full_name ?? "",
      phone: profile?.phone ?? "",
      gender: profile?.gender ?? "",
      birth_date: profile?.birth_date ?? "",
      profile_image: profile?.profile_image ?? user?.profile_image ?? "",
    });
    setEditing(true);
  };

  const cancelEditing = () => {
    setEditing(false);
  };

  const saveProfile = async () => {
    if (!profile) return;
    setSaving(true);
    try {
      const updated = await api.patch<Profile>(`/profiles/${profile.id}`, {
        nickname: form.nickname || null,
        full_name: form.full_name || null,
        phone: form.phone || null,
        gender: form.gender || null,
        birth_date: form.birth_date || null,
        profile_image: form.profile_image || null,
      });
      setProfile(updated);
      await refreshUser();
      setEditing(false);
    } catch {
      alert("프로필 저장에 실패했습니다");
    } finally {
      setSaving(false);
    }
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
      {/* 프로필 헤더 */}
      <div className="profile-header">
        <div className="profile-avatar">
          {user.profile_image ? (
            <img src={user.profile_image} alt="프로필" />
          ) : (
            <span className="profile-avatar-text">
              {(user.nickname ?? user.email)[0].toUpperCase()}
            </span>
          )}
        </div>
        <div className="profile-name">{user.nickname ?? "닉네임 없음"}</div>
        <div className="profile-email">{user.email}</div>
        <button className="profile-edit-btn" onClick={editing ? cancelEditing : startEditing}>
          {editing ? "취소" : "프로필 수정"}
        </button>
      </div>

      {/* 프로필 수정 폼 */}
      {editing && (
        <div className="profile-form">
          <div className="profile-form-group">
            <label className="profile-form-label">닉네임</label>
            <input
              className="profile-form-input"
              value={form.nickname}
              onChange={(e) => setForm((f) => ({ ...f, nickname: e.target.value }))}
              placeholder="닉네임을 입력하세요"
            />
          </div>
          <div className="profile-form-group">
            <label className="profile-form-label">이름</label>
            <input
              className="profile-form-input"
              value={form.full_name}
              onChange={(e) => setForm((f) => ({ ...f, full_name: e.target.value }))}
              placeholder="이름을 입력하세요"
            />
          </div>
          <div className="profile-form-group">
            <label className="profile-form-label">전화번호</label>
            <input
              className="profile-form-input"
              value={form.phone}
              onChange={(e) => setForm((f) => ({ ...f, phone: e.target.value }))}
              placeholder="010-0000-0000"
            />
          </div>
          <div className="profile-form-group">
            <label className="profile-form-label">성별</label>
            <div className="profile-gender-options">
              {["male", "female"].map((g) => (
                <button
                  key={g}
                  type="button"
                  className={`profile-gender-btn ${form.gender === g ? "active" : ""}`}
                  onClick={() => setForm((f) => ({ ...f, gender: g }))}
                >
                  {g === "male" ? "남성" : "여성"}
                </button>
              ))}
            </div>
          </div>
          <div className="profile-form-group">
            <label className="profile-form-label">생년월일</label>
            <FlaceDatePicker
              value={form.birth_date}
              onChange={(val) => setForm((f) => ({ ...f, birth_date: val }))}
              placeholder="생년월일 선택"
            />
          </div>
          <div className="profile-form-group">
            <label className="profile-form-label">프로필 이미지 URL</label>
            <input
              className="profile-form-input"
              value={form.profile_image}
              onChange={(e) => setForm((f) => ({ ...f, profile_image: e.target.value }))}
              placeholder="https://example.com/image.jpg"
            />
          </div>
          <button className="profile-save-btn" onClick={saveProfile} disabled={saving}>
            {saving ? "저장 중..." : "저장"}
          </button>
        </div>
      )}

      {/* 메뉴 */}
      <nav className="profile-menu">
        <Link href="/profile/subscriptions" className="profile-menu-item">
          <div className="profile-menu-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" />
              <circle cx="9" cy="7" r="4" />
              <path d="M23 21v-2a4 4 0 00-3-3.87" />
              <path d="M16 3.13a4 4 0 010 7.75" />
            </svg>
          </div>
          구독별 프로필 설정
          <span className="profile-menu-arrow">&gt;</span>
        </Link>
        <Link href="/profile/addresses" className="profile-menu-item">
          <div className="profile-menu-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z" />
              <circle cx="12" cy="10" r="3" />
            </svg>
          </div>
          배송지 관리
          <span className="profile-menu-arrow">&gt;</span>
        </Link>
        <Link href="/orders" className="profile-menu-item">
          <div className="profile-menu-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="2" y="7" width="20" height="14" rx="2" />
              <path d="M16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16" />
            </svg>
          </div>
          주문 내역
          <span className="profile-menu-arrow">&gt;</span>
        </Link>
        <Link href="/settings" className="profile-menu-item">
          <div className="profile-menu-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="3" />
              <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z" />
            </svg>
          </div>
          설정
          <span className="profile-menu-arrow">&gt;</span>
        </Link>
      </nav>
    </div>
  );
}
