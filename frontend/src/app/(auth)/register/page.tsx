"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "../../../lib/auth-context";
import FlaceDatePicker from "../../components/FlaceDatePicker/FlaceDatePicker";
import "./register.css";

export default function RegisterPage() {
  const router = useRouter();
  const { register, checkEmail } = useAuth();

  // 계정 정보
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");

  // 이메일 중복체크
  const [emailChecked, setEmailChecked] = useState(false);
  const [emailAvailable, setEmailAvailable] = useState(false);
  const [emailMsg, setEmailMsg] = useState("");
  const [checkingEmail, setCheckingEmail] = useState(false);

  // 프로필 정보
  const [fullName, setFullName] = useState("");
  const [nickname, setNickname] = useState("");
  const [birthDate, setBirthDate] = useState("");
  const [gender, setGender] = useState("");
  const [phone, setPhone] = useState("");

  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  // 이메일 변경 시 중복체크 초기화
  const handleEmailChange = (value: string) => {
    setEmail(value);
    setEmailChecked(false);
    setEmailAvailable(false);
    setEmailMsg("");
  };

  // 이메일 중복체크
  const handleCheckEmail = async () => {
    if (!email) {
      setEmailMsg("이메일을 입력해주세요.");
      return;
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setEmailMsg("올바른 이메일 형식을 입력해주세요.");
      return;
    }
    setCheckingEmail(true);
    try {
      const result = await checkEmail(email);
      setEmailChecked(true);
      setEmailAvailable(result.available);
      setEmailMsg(result.message);
    } catch {
      setEmailMsg("이메일 확인 중 오류가 발생했습니다.");
    } finally {
      setCheckingEmail(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!email || !password || !passwordConfirm) {
      setError("이메일, 비밀번호는 필수 항목입니다.");
      return;
    }
    if (!emailChecked || !emailAvailable) {
      setError("이메일 중복확인을 해주세요.");
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
      await register(email, password, {
        nickname: nickname || undefined,
        full_name: fullName || undefined,
        birth_date: birthDate || undefined,
        gender: gender || undefined,
        phone: phone || undefined,
      });
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
        {/* 이메일 + 중복체크 */}
        <div className="register-email-row">
          <input
            type="email"
            className="register-input"
            placeholder="이메일"
            value={email}
            onChange={(e) => handleEmailChange(e.target.value)}
          />
          <button
            type="button"
            className="register-check-btn"
            onClick={handleCheckEmail}
            disabled={checkingEmail || (emailChecked && emailAvailable)}
          >
            {checkingEmail ? "확인 중..." : emailChecked && emailAvailable ? "확인완료" : "중복확인"}
          </button>
        </div>
        {emailMsg && (
          <div className={`register-email-msg ${emailAvailable ? "available" : "unavailable"}`}>
            {emailMsg}
          </div>
        )}

        <input
          type="password"
          className="register-input"
          placeholder="비밀번호 (6자 이상)"
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

        <div className="register-divider">프로필 정보</div>

        <input
          type="text"
          className="register-input"
          placeholder="이름"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
        />
        <input
          type="text"
          className="register-input"
          placeholder="닉네임"
          value={nickname}
          onChange={(e) => setNickname(e.target.value)}
        />
        <FlaceDatePicker
          value={birthDate}
          onChange={setBirthDate}
          placeholder="생년월일"
        />
        <select
          className="register-input"
          value={gender}
          onChange={(e) => setGender(e.target.value)}
        >
          <option value="">성별 선택</option>
          <option value="male">남성</option>
          <option value="female">여성</option>
        </select>
        <input
          type="tel"
          className="register-input"
          placeholder="전화번호"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
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
