// 백엔드 스키마 기반 TypeScript 인터페이스

/** 백엔드 페이지네이션 응답 공통 형식 */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}

export interface Artist {
  id: number;
  user_id: number;
  stage_name: string;
  slug: string | null;
  notes: string | null;
  profile_image: string | null;
  cover_image: string | null;
  status: "active" | "inactive";
  // 프론트 편의용 (API 응답에는 없고, category_map에서 조인)
  category_id?: number;
  search_text?: string | null;
  created_at: string;
  updated_at: string;
}

export interface ArtistCategory {
  id: number;
  name: string;
  description: string | null;
  is_active: boolean;
}

export interface ArtistSocialLink {
  id: number;
  artist_id: number;
  platform_name: string;
  url: string;
  display_name: string | null;
  follower_count: number;
  priority: number;
  is_active: boolean;
}

export interface Subscription {
  id: number;
  fan_id: number;
  artist_id: number;
  fan_nickname: string | null;
  fan_profile_image: string | null;
  status: "subscribed" | "cancelled" | "expired";
  payments_type: "free" | "paid";
  start_date: string;
  end_date: string | null;
  created_at: string;
  updated_at: string;
}

export interface Post {
  id: number;
  author_id: number;
  author_type: "fan" | "artist";
  content: string | null;
  write_id: number;
  write_role: "fan" | "artist" | "manager";
  visibility: "public" | "subscribers" | "private";
  is_visible: boolean;
  is_artist_post: boolean;
  published_date: string | null;
  tags: string[] | null;
  title_field: string | null;
  created_at: string;
  updated_at: string;
  // 프론트 표시용 비정규화 필드
  author_name?: string;
  author_profile_image?: string;
  // 기사형 포스트용 이미지 (텍스트 사이에 삽입)
  images?: PostImage[];
}

export interface PostImage {
  id: number;
  url: string;
  caption?: string;
  width?: number;
  height?: number;
}

export interface ArtistImage {
  id: number;
  artist_id: number;
  image_id: number;
  image_purpose: string | null;
  published_date: string | null;
  tags: string[] | null;
  visibility: "public" | "subscribers" | "private";
  is_visible: boolean;
  created_at: string;
  updated_at: string;
  // 프론트 표시용
  image_url: string;
  thumbnail_url: string;
}

export interface ArtistVideo {
  id: number;
  artist_id: number;
  url: string;
  thumbnail_url: string | null;
  title: string | null;
  description: string | null;
  duration_seconds: number | null;
  published_date: string | null;
  tags: string[] | null;
  visibility: "public" | "subscribers" | "private";
  is_visible: boolean;
  created_at: string;
  updated_at: string;
}

export interface ArtistCategoryMap {
  id: number;
  artist_id: number;
  category_id: number;
  created_at: string;
}

export interface Event {
  id: number;
  artist_id: number;
  title: string;
  description: string | null;
  event_type: string | null;
  event_date: string | null;
  location: string | null;
  max_participants: number | null;
  current_participants: number;
  status: "active" | "cancelled" | "completed" | "full";
  created_at: string;
  updated_at: string;
}

export interface Profile {
  id: number;
  user_id: number;
  full_name: string | null;
  nickname: string | null;
  birth_date: string | null;
  gender: "male" | "female" | null;
  phone: string | null;
  profile_image: string | null;
  created_at: string;
  updated_at: string;
}

export interface SearchFilterState {
  category: string;
  tags: string[];
  sortOrder: "latest" | "oldest" | "relevant";
  dateRange: {
    start: string | null;
    end: string | null;
  };
  visibility: "all" | "public" | "subscribers";
  query: string;
}

export interface SidebarArtist {
  id: number;
  name: string;
  slug: string | null;
  category?: string;
  profileImage?: string;
}

export interface Notice {
  id: number;
  title: string;
  message: string;
  write_id: number;
  write_role: string | null;
  target_type: string | null;
  target_id: number | null;
  start_at: string | null;
  end_at: string | null;
  is_active: boolean;
  search_text: string | null;
  created_at: string;
  updated_at: string;
}

export interface ChatRoom {
  id: number;
  room_type: string;
  artist_id: number | null;
  room_name: string | null;
  room_image: string | null;
  last_message_at: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Magazine {
  id: number;
  title: string;
  slug: string | null;
  content: string;
  summary: string | null;
  thumbnail_url: string | null;
  category: string | null;
  artist_id: number | null;
  write_id: number;
  tags: string[] | null;
  is_active: boolean;
  view_count: number;
  created_at: string;
  updated_at: string;
}

export interface MagazineImage {
  id: number;
  url: string;
  width: number | null;
  height: number | null;
  sort_order: number;
}

export interface MagazineDetail extends Magazine {
  images: MagazineImage[];
}

export interface UserAddress {
  id: number;
  user_id: number;
  address_name: string | null;
  recipient_name: string;
  recipient_phone: string;
  postal_code: string;
  base_address: string;
  detail_address: string | null;
  is_default: boolean;
  memo: string | null;
  created_at: string;
  updated_at: string;
}

export interface NotificationSetting {
  id: number;
  subscription_id: number | null;
  user_id: number;
  source_type: string | null;
  notify_all: boolean;
  notify_post: boolean;
  notify_comment: boolean;
  notify_reply: boolean;
  notify_notice: boolean;
  notify_payment: boolean;
  notify_warning: boolean;
  receive_app: boolean;
  receive_push: boolean;
  receive_email: boolean;
  created_at: string;
  updated_at: string;
}

export interface SubscriptionPlan {
  id: number;
  artist_id: number;
  name: string;
  price: number;
  currency: string;
  billing_cycle: "monthly" | "yearly" | "one-time";
  duration_days: number | null;
  benefits: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Payment {
  id: number;
  user_id: number;
  payment_type: string;
  related_id: number | null;
  related_type: string | null;
  amount: number;
  currency: string;
  status: "pending" | "completed" | "failed" | "cancelled" | "refunded";
  transaction_id: string | null;
  payment_method_id: number | null;
  paid_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface ChatMessage {
  id: number;
  chat_room_id: number;
  sender_id: number;
  sender_type: string;
  message_type: string;
  content: string | null;
  is_pinned: boolean;
  status: string;
  created_at: string;
  updated_at: string;
}
