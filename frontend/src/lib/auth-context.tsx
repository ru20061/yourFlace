"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  type ReactNode,
} from "react";
import { api, setTokens, clearTokens, getAccessToken } from "./api";

interface AuthUser {
  id: number;
  email: string;
  nickname: string | null;
  profile_image: string | null;
}

interface AuthContextType {
  user: AuthUser | null;
  isLoggedIn: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, nickname?: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  /** 현재 토큰으로 유저 정보 복원 */
  const fetchMe = useCallback(async () => {
    try {
      const me = await api.get<AuthUser>("/auth/me");
      setUser(me);
    } catch {
      clearTokens();
      setUser(null);
    }
  }, []);

  /** 앱 시작 시 토큰이 있으면 유저 정보 복원 */
  useEffect(() => {
    const token = getAccessToken();
    if (token) {
      fetchMe().finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, [fetchMe]);

  /** 로그인 */
  const login = useCallback(
    async (email: string, password: string) => {
      const data = await api.post<{
        access_token: string;
        refresh_token: string;
      }>("/auth/login", { email, password });
      setTokens(data.access_token, data.refresh_token);
      await fetchMe();
    },
    [fetchMe],
  );

  /** 회원가입 */
  const register = useCallback(
    async (email: string, password: string, nickname?: string) => {
      const data = await api.post<{
        access_token: string;
        refresh_token: string;
      }>("/auth/register", { email, password, nickname });
      setTokens(data.access_token, data.refresh_token);
      await fetchMe();
    },
    [fetchMe],
  );

  /** 로그아웃 */
  const logout = useCallback(() => {
    clearTokens();
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoggedIn: !!user,
        isLoading,
        login,
        register,
        logout,
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
