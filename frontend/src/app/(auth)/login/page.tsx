"use client";

import Link from "next/link";
import "./login.css";

export default function LoginPage() {
  return (
    <div className="login-page">
      <div className="login-logo">yourFlace</div>

      <form className="login-form" onSubmit={(e) => e.preventDefault()}>
        <input type="email" className="login-input" placeholder="이메일" />
        <input type="password" className="login-input" placeholder="비밀번호" />
        <button type="submit" className="login-submit">로그인</button>

        <div className="login-divider">또는</div>

        <div className="oauth-buttons">
          <button type="button" className="oauth-btn google">Google로 계속하기</button>
          <button type="button" className="oauth-btn kakao">카카오로 계속하기</button>
          <button type="button" className="oauth-btn naver">네이버로 계속하기</button>
        </div>

        <div className="login-footer">
          아직 계정이 없으신가요? <Link href="/register">회원가입</Link>
        </div>
      </form>
    </div>
  );
}
