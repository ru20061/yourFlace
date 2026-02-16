import re
import unicodedata


def generate_slug(text: str, max_length: int = 100) -> str:
    """텍스트에서 URL-safe slug 생성 (한글 지원)"""
    slug = text.strip().lower()
    # 공백/언더스코어 → 하이픈
    slug = re.sub(r"[\s_]+", "-", slug)
    # 알파벳, 숫자, 한글, 하이픈만 유지
    slug = re.sub(r"[^\w가-힣-]", "", slug, flags=re.UNICODE)
    # 연속 하이픈 제거
    slug = re.sub(r"-{2,}", "-", slug)
    # 앞뒤 하이픈 제거
    slug = slug.strip("-")
    return slug[:max_length] if slug else "untitled"


def make_unique_slug(slug: str, existing_slugs: list[str]) -> str:
    """기존 slug 목록과 겹치면 숫자 접미사 추가"""
    if slug not in existing_slugs:
        return slug
    counter = 2
    while f"{slug}-{counter}" in existing_slugs:
        counter += 1
    return f"{slug}-{counter}"
