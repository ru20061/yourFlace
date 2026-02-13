"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "../../../lib/auth-context";
import "./register.css";

export default function RegisterPage() {
  const router = useRouter();
  const { register } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const [nickname, setNickname] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (!email || !password || !passwordConfirm) {
      setError("모든 필수 항목을 입력해주세요.");
      return;
    }
    if (password !== passwordConfirm) {
      setError("비밀번호가 일치하지 않습니다.");
      return;
    }
    if (password.length < 6) {
      setError("비밀번호는 6자 이상이어야 합니다.");
      return;
    }
    setSubmitting(true);
    try {
      await register(email, password, nickname || undefined);
      router.push("/");
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "회원가입에 실패했습니다.";
      setError(msg);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="register-page">
      <h1 className="register-title">회원가입</h1>
      <p className="register-subtitle">yourFlace에서 아티스트를 만나보세요</p>

      <form className="register-form" onSubmit={handleSubmit}>
        <input
          type="email"
          className="register-input"
          placeholder="이메일"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          className="register-input"
          placeholder="비밀번호"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <input
          type="password"
          className="register-input"
          placeholder="비밀번호 확인"
          value={passwordConfirm}
          onChange={(e) => setPasswordConfirm(e.target.value)}
        />
        <input
          type="text"
          className="register-input"
          placeholder="닉네임 (선택)"
          value={nickname}
          onChange={(e) => setNickname(e.target.value)}
        />
        {error && <div style={{ color: "red", fontSize: 13 }}>{error}</div>}
        <button type="submit" className="register-submit" disabled={submitting}>
          {submitting ? "가입 중..." : "가입하기"}
        </button>

        <div className="register-footer">
          이미 계정이 있으신가요? <Link href="/login">로그인</Link>
        </div>
      </form>
    </div>
  );
}
