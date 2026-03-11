"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  type ReactNode,
} from "react";
import { api } from "./api";

interface AuthUser {
  id: number;
  email: string;
  nickname: string | null;
  profile_image: string | null;
}

interface ProfileData {
  nickname?: string;
  full_name?: string;
  birth_date?: string;
  gender?: "male" | "female";
  phone?: string;
}

interface AuthContextType {
  user: AuthUser | null;
  isLoggedIn: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, profile?: ProfileData) => Promise<void>;
  checkEmail: (email: string) => Promise<{ available: boolean; message: string }>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  /** 쿠키 기반으로 유저 정보 복원 (/auth/me) */
  const fetchMe = useCallback(async () => {
    try {
      const me = await api.get<AuthUser>("/auth/me");
      setUser(me);
    } catch {
      setUser(null);
    }
  }, []);

  /** 앱 시작 시 /auth/me로 로그인 여부 확인 (쿠키가 있으면 자동 인증) */
  useEffect(() => {
    fetchMe().finally(() => setIsLoading(false));
  }, [fetchMe]);

  /** 로그인 */
  const login = useCallback(
    async (email: string, password: string) => {
      await api.post("/auth/login", { email, password });
      await fetchMe();
    },
    [fetchMe],
  );

  /** 이메일 중복 확인 */
  const checkEmail = useCallback(
    async (email: string) => {
      return api.get<{ available: boolean; message: string }>(
        `/auth/check-email?email=${encodeURIComponent(email)}`,
      );
    },
    [],
  );

  /** 회원가입 */
  const register = useCallback(
    async (email: string, password: string, profile?: ProfileData) => {
      await api.post("/auth/register", { email, password, ...profile });
      await fetchMe();
    },
    [fetchMe],
  );

  /** 로그아웃: 서버에서 쿠키 삭제 */
  const logout = useCallback(async () => {
    await api.post("/auth/logout").catch(() => {});
    setUser(null);
    window.location.href = "/";
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoggedIn: !!user,
        isLoading,
        login,
        register,
        checkEmail,
        logout,
        refreshUser: fetchMe,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
