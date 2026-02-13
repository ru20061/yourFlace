"use client";

import Link from "next/link";
import "./sidebar.css";

interface Artist {
  id: number;
  name: string;
  category?: string;
  profileImage?: string;
}

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  isAdmin?: boolean;
  subscribedArtists?: Artist[];
}

export default function Sidebar({ isOpen, onClose, isAdmin = false, subscribedArtists = [] }: SidebarProps) {
  return (
    <>
      {/* 오버레이 */}
      <div className={`sidebar-overlay ${isOpen ? "open" : ""}`} onClick={onClose} />

      {/* 사이드바 */}
      <aside className={`sidebar ${isOpen ? "open" : ""}`}>
        <div className="sidebar-header">
          <span className="sidebar-title">
            {isAdmin ? "관리 카테고리" : "구독 아티스트"}
          </span>
          <button className="sidebar-close" onClick={onClose} aria-label="닫기">
            ✕
          </button>
        </div>

        {isAdmin ? (
          /* 관리자: 검색 카테고리 */
          <nav className="sidebar-category-list">
            <div className="sidebar-category-title">사용자 관리</div>
            <Link href="/admin" className="sidebar-category-item" onClick={onClose}>사용자 목록</Link>
            <Link href="/admin" className="sidebar-category-item" onClick={onClose}>신고 관리</Link>

            <div className="sidebar-category-title">콘텐츠 관리</div>
            <Link href="/admin" className="sidebar-category-item" onClick={onClose}>게시글 관리</Link>
            <Link href="/admin" className="sidebar-category-item" onClick={onClose}>이미지/영상 관리</Link>

            <div className="sidebar-category-title">운영</div>
            <Link href="/admin/notices" className="sidebar-category-item" onClick={onClose}>공지사항</Link>
            <Link href="/admin/banners" className="sidebar-category-item" onClick={onClose}>배너 관리</Link>
            <Link href="/admin/faq" className="sidebar-category-item" onClick={onClose}>FAQ</Link>
          </nav>
        ) : (
          /* 일반 유저: 구독한 아티스트 목록 */
          <div className="sidebar-artist-list">
            {subscribedArtists.length > 0 ? (
              subscribedArtists.map((artist) => (
                <Link
                  href={`/artists/${artist.id}`}
                  key={artist.id}
                  className="sidebar-artist-item"
                  onClick={onClose}
                >
                  <div className="sidebar-artist-avatar">
                    {artist.profileImage && <img src={artist.profileImage} alt={artist.name} />}
                  </div>
                  <div>
                    <div className="sidebar-artist-name">{artist.name}</div>
                    {artist.category && <div className="sidebar-artist-category">{artist.category}</div>}
                  </div>
                </Link>
              ))
            ) : (
              <p style={{ padding: "24px 16px", color: "var(--text-tertiary)", fontSize: "14px", textAlign: "center" }}>
                구독한 아티스트가 없습니다
              </p>
            )}
          </div>
        )}

        <div className="sidebar-footer">
          <Link href="/settings" className="sidebar-footer-link" onClick={onClose}>설정</Link>
          <Link href="/" className="sidebar-footer-link" onClick={onClose}>고객센터</Link>
        </div>
      </aside>
    </>
  );
}
