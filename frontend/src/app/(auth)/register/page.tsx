"use client";

import Link from "next/link";
import "./register.css";

export default function RegisterPage() {
  return (
    <div className="register-page">
      <h1 className="register-title">회원가입</h1>
      <p className="register-subtitle">yourFlace에서 아티스트를 만나보세요</p>

      <form className="register-form" onSubmit={(e) => e.preventDefault()}>
        <input type="email" className="register-input" placeholder="이메일" />
        <input type="password" className="register-input" placeholder="비밀번호" />
        <input type="password" className="register-input" placeholder="비밀번호 확인" />
        <input type="text" className="register-input" placeholder="닉네임" />
        <button type="submit" className="register-submit">가입하기</button>

        <div className="register-footer">
          이미 계정이 있으신가요? <Link href="/login">로그인</Link>
        </div>
      </form>
    </div>
  );
}
