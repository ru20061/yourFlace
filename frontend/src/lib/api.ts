const API_BASE = "/api";

/** 401 시 쿠키 토큰 갱신 시도 */
async function tryRefresh(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/auth/refresh`, {
      method: "POST",
      credentials: "include",   // 쿠키 자동 첨부
    });
    return res.ok;
  } catch {
    return false;
  }
}

/** 경로에서 쿼리 앞 trailing slash 제거 (/subscriptions/?skip=0 → /subscriptions?skip=0) */
function normalizePath(path: string): string {
  const qIdx = path.indexOf("?");
  if (qIdx === -1) {
    return path.endsWith("/") ? path.slice(0, -1) : path;
  }
  const base = path.slice(0, qIdx);
  const query = path.slice(qIdx);
  return (base.endsWith("/") ? base.slice(0, -1) : base) + query;
}

/** API fetch 래퍼 (HttpOnly 쿠키 자동 첨부 + 401 시 refresh) */
export async function apiFetch<T = unknown>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const normalizedPath = normalizePath(path);
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  let res = await fetch(`${API_BASE}${normalizedPath}`, {
    ...options,
    headers,
    credentials: "include",   // HttpOnly 쿠키 자동 첨부
  });

  // 401 → refresh 시도 후 재요청
  if (res.status === 401) {
    const refreshed = await tryRefresh();
    if (refreshed) {
      res = await fetch(`${API_BASE}${normalizedPath}`, {
        ...options,
        headers,
        credentials: "include",
      });
    }
  }

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(res.status, body.detail || res.statusText);
  }

  // 204 No Content
  if (res.status === 204) return undefined as T;

  return res.json();
}

/** API 에러 클래스 */
export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

/** FormData 업로드용 fetch 래퍼 */
export async function apiUpload<T = unknown>(
  path: string,
  formData: FormData,
): Promise<T> {
  const normalizedPath = normalizePath(path);

  let res = await fetch(`${API_BASE}${normalizedPath}`, {
    method: "POST",
    body: formData,
    credentials: "include",
  });

  if (res.status === 401) {
    const refreshed = await tryRefresh();
    if (refreshed) {
      res = await fetch(`${API_BASE}${normalizedPath}`, {
        method: "POST",
        body: formData,
        credentials: "include",
      });
    }
  }

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(res.status, body.detail || res.statusText);
  }

  return res.json();
}

/** 편의 함수 */
export const api = {
  get: <T = unknown>(path: string) => apiFetch<T>(path),
  post: <T = unknown>(path: string, body?: unknown) =>
    apiFetch<T>(path, { method: "POST", body: body ? JSON.stringify(body) : undefined }),
  put: <T = unknown>(path: string, body?: unknown) =>
    apiFetch<T>(path, { method: "PUT", body: body ? JSON.stringify(body) : undefined }),
  patch: <T = unknown>(path: string, body?: unknown) =>
    apiFetch<T>(path, { method: "PATCH", body: body ? JSON.stringify(body) : undefined }),
  delete: <T = unknown>(path: string) => apiFetch<T>(path, { method: "DELETE" }),
  upload: <T = unknown>(path: string, formData: FormData) => apiUpload<T>(path, formData),
};
