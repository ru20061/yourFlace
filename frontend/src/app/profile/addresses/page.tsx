"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useAuth } from "../../../lib/auth-context";
import { api } from "../../../lib/api";
import type { UserAddress, PaginatedResponse } from "../../data/types";
import "./addresses.css";
import "../profile.css";

interface AddressForm {
  address_name: string;
  recipient_name: string;
  recipient_phone: string;
  postal_code: string;
  base_address: string;
  detail_address: string;
  memo: string;
  is_default: boolean;
}

const EMPTY_FORM: AddressForm = {
  address_name: "",
  recipient_name: "",
  recipient_phone: "",
  postal_code: "",
  base_address: "",
  detail_address: "",
  memo: "",
  is_default: false,
};

export default function AddressesPage() {
  const { user, isLoading: authLoading } = useAuth();

  const [addresses, setAddresses] = useState<UserAddress[]>([]);
  const [loading, setLoading] = useState(true);

  // 추가/수정 폼
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [form, setForm] = useState<AddressForm>(EMPTY_FORM);
  const [saving, setSaving] = useState(false);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  useEffect(() => {
    if (!user) return;
    loadAddresses();
  }, [user]);

  const loadAddresses = async () => {
    try {
      const res = await api.get<PaginatedResponse<UserAddress>>(
        `/user-addresses?skip=0&limit=100`
      );
      setAddresses(res.items);
    } catch {
      // 실패 시 무시
    } finally {
      setLoading(false);
    }
  };

  // 새 배송지 추가 폼 열기
  const openAddForm = () => {
    setForm(EMPTY_FORM);
    setEditingId(null);
    setShowForm(true);
  };

  // 수정 폼 열기
  const openEditForm = (addr: UserAddress) => {
    setForm({
      address_name: addr.address_name ?? "",
      recipient_name: addr.recipient_name,
      recipient_phone: addr.recipient_phone,
      postal_code: addr.postal_code,
      base_address: addr.base_address,
      detail_address: addr.detail_address ?? "",
      memo: addr.memo ?? "",
      is_default: addr.is_default,
    });
    setEditingId(addr.id);
    setShowForm(true);
  };

  const closeForm = () => {
    setShowForm(false);
    setEditingId(null);
  };

  // 저장 (추가 or 수정)
  const handleSave = async () => {
    if (!form.recipient_name || !form.recipient_phone || !form.postal_code || !form.base_address) {
      alert("수령인, 연락처, 우편번호, 기본주소는 필수입니다.");
      return;
    }
    setSaving(true);
    try {
      const body = {
        address_name: form.address_name || null,
        recipient_name: form.recipient_name,
        recipient_phone: form.recipient_phone,
        postal_code: form.postal_code,
        base_address: form.base_address,
        detail_address: form.detail_address || null,
        memo: form.memo || null,
        is_default: form.is_default,
      };

      if (editingId) {
        await api.patch<UserAddress>(`/user-addresses/${editingId}`, body);
      } else {
        await api.post<UserAddress>(`/user-addresses`, { ...body, user_id: user!.id });
      }
      await loadAddresses();
      closeForm();
    } catch {
      alert("배송지 저장에 실패했습니다.");
    } finally {
      setSaving(false);
    }
  };

  // 삭제
  const handleDelete = async (id: number) => {
    if (!confirm("이 배송지를 삭제하시겠습니까?")) return;
    setDeletingId(id);
    try {
      await api.delete(`/user-addresses/${id}`);
      setAddresses((prev) => prev.filter((a) => a.id !== id));
    } catch {
      alert("배송지 삭제에 실패했습니다.");
    } finally {
      setDeletingId(null);
    }
  };

  // 기본배송지 설정
  const setDefault = async (id: number) => {
    try {
      await api.patch<UserAddress>(`/user-addresses/${id}`, { is_default: true });
      await loadAddresses();
    } catch {
      alert("기본배송지 설정에 실패했습니다.");
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
      {/* 헤더 */}
      <div className="profile-sub-page-header">
        <Link href="/profile" className="profile-sub-back">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </Link>
        <h1 className="profile-sub-page-title">배송지 관리</h1>
      </div>

      {/* 새 배송지 추가 버튼 */}
      {!showForm && (
        <button className="addr-add-btn" onClick={openAddForm}>
          + 새 배송지 추가
        </button>
      )}

      {/* 추가/수정 폼 */}
      {showForm && (
        <div className="addr-form-card">
          <div className="addr-form-title">
            {editingId ? "배송지 수정" : "새 배송지 추가"}
          </div>

          <div className="profile-form-group">
            <label className="profile-form-label">배송지명</label>
            <input
              className="profile-form-input"
              value={form.address_name}
              onChange={(e) => setForm((f) => ({ ...f, address_name: e.target.value }))}
              placeholder="예: 집, 회사"
            />
          </div>

          <div className="profile-form-group">
            <label className="profile-form-label">수령인 *</label>
            <input
              className="profile-form-input"
              value={form.recipient_name}
              onChange={(e) => setForm((f) => ({ ...f, recipient_name: e.target.value }))}
              placeholder="수령인 이름"
            />
          </div>

          <div className="profile-form-group">
            <label className="profile-form-label">연락처 *</label>
            <input
              className="profile-form-input"
              value={form.recipient_phone}
              onChange={(e) => setForm((f) => ({ ...f, recipient_phone: e.target.value }))}
              placeholder="010-0000-0000"
            />
          </div>

          <div className="profile-form-group">
            <label className="profile-form-label">우편번호 *</label>
            <input
              className="profile-form-input"
              value={form.postal_code}
              onChange={(e) => setForm((f) => ({ ...f, postal_code: e.target.value }))}
              placeholder="우편번호"
            />
          </div>

          <div className="profile-form-group">
            <label className="profile-form-label">기본주소 *</label>
            <input
              className="profile-form-input"
              value={form.base_address}
              onChange={(e) => setForm((f) => ({ ...f, base_address: e.target.value }))}
              placeholder="시/도, 구/군, 동/읍/면"
            />
          </div>

          <div className="profile-form-group">
            <label className="profile-form-label">상세주소</label>
            <input
              className="profile-form-input"
              value={form.detail_address}
              onChange={(e) => setForm((f) => ({ ...f, detail_address: e.target.value }))}
              placeholder="아파트, 동/호수 등"
            />
          </div>

          <div className="profile-form-group">
            <label className="profile-form-label">배송 메모</label>
            <input
              className="profile-form-input"
              value={form.memo}
              onChange={(e) => setForm((f) => ({ ...f, memo: e.target.value }))}
              placeholder="부재 시 문 앞에 놓아주세요"
            />
          </div>

          <label className="addr-default-check">
            <input
              type="checkbox"
              checked={form.is_default}
              onChange={(e) => setForm((f) => ({ ...f, is_default: e.target.checked }))}
            />
            <span>기본 배송지로 설정</span>
          </label>

          <div className="addr-form-actions">
            <button className="addr-form-cancel" onClick={closeForm}>
              취소
            </button>
            <button className="addr-form-save" onClick={handleSave} disabled={saving}>
              {saving ? "저장 중..." : "저장"}
            </button>
          </div>
        </div>
      )}

      {/* 배송지 목록 */}
      {addresses.length === 0 && !showForm ? (
        <div className="addr-empty">
          <div className="addr-empty-icon">
            <svg viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
              <circle cx="12" cy="10" r="3" />
            </svg>
          </div>
          <p className="addr-empty-text">등록된 배송지가 없습니다</p>
          <button className="addr-empty-add-btn" onClick={openAddForm}>
            + 새 배송지 추가
          </button>
        </div>
      ) : (
        <div className="addr-list">
          {addresses.map((addr) => (
            <div key={addr.id} className="addr-card">
              <div className="addr-card-header">
                <div className="addr-card-name">
                  {addr.address_name || "배송지"}
                  {addr.is_default && <span className="addr-default-badge">기본</span>}
                </div>
                <div className="addr-card-actions">
                  <button
                    className="addr-action-btn"
                    onClick={() => openEditForm(addr)}
                  >
                    수정
                  </button>
                  <button
                    className="addr-action-btn danger"
                    onClick={() => handleDelete(addr.id)}
                    disabled={deletingId === addr.id}
                  >
                    {deletingId === addr.id ? "삭제 중" : "삭제"}
                  </button>
                </div>
              </div>

              <div className="addr-card-body">
                <div className="addr-card-recipient">
                  {addr.recipient_name} · {addr.recipient_phone}
                </div>
                <div className="addr-card-address">
                  [{addr.postal_code}] {addr.base_address}
                  {addr.detail_address && `, ${addr.detail_address}`}
                </div>
                {addr.memo && (
                  <div className="addr-card-memo">{addr.memo}</div>
                )}
              </div>

              {!addr.is_default && (
                <button
                  className="addr-set-default-btn"
                  onClick={() => setDefault(addr.id)}
                >
                  기본 배송지로 설정
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
