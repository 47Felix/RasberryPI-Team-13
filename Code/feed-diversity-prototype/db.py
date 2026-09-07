"""Supabase-backed storage for user-submitted posts, likes, comments and
accounts (schema: supabase/migrations/0001_init.sql, 0002_accounts.sql).

Reads/writes to the data tables go through the PostgREST API using the
secret key (server-side only, never sent to the browser) so every table can
stay locked down with row level security and no anon policies at all - the
Flask backend is the only thing that can touch this data. Sign-up/sign-in
instead go through Supabase Auth (GoTrue) directly, using the publishable
key - that's the one Supabase key that's meant to be used for password
auth requests.
"""

import os
import re

import requests
from dotenv import load_dotenv

from ranking import Post

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_SECRET_KEY = os.environ.get("SUPABASE_SECRET_KEY", "")
SUPABASE_PUBLISHABLE_KEY = os.environ.get("SUPABASE_PUBLISHABLE_KEY", "")

# Cache category name -> id lookups for the lifetime of the process; the
# table only changes via the migration seed data, not at runtime.
_category_id_cache: dict[str, str] = {}


def is_configured() -> bool:
    return bool(SUPABASE_URL and SUPABASE_SECRET_KEY)


def auth_configured() -> bool:
    return bool(SUPABASE_URL and SUPABASE_PUBLISHABLE_KEY)


def _headers() -> dict:
    return {
        "apikey": SUPABASE_SECRET_KEY,
        "Authorization": f"Bearer {SUPABASE_SECRET_KEY}",
        "Content-Type": "application/json",
    }


def _auth_headers() -> dict:
    return {
        "apikey": SUPABASE_PUBLISHABLE_KEY,
        "Content-Type": "application/json",
    }


def _get(path: str, params: dict) -> list[dict]:
    response = requests.get(f"{SUPABASE_URL}/rest/v1/{path}", headers=_headers(), params=params, timeout=5)
    response.raise_for_status()
    return response.json()


def _category_id(name: str) -> str | None:
    if name not in _category_id_cache:
        rows = _get("categories", {"name": f"eq.{name}", "select": "id"})
        if not rows:
            return None
        _category_id_cache[name] = rows[0]["id"]
    return _category_id_cache[name]


def _slugify_handle(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "", text.lower())
    return slug or "user"


def sign_up(email: str, password: str) -> dict | None:
    """Creates a Supabase Auth account. Returns {"id", "email"}, or None on
    failure (email already taken, weak password, missing config, network).
    """
    if not auth_configured():
        return None
    try:
        response = requests.post(
            f"{SUPABASE_URL}/auth/v1/signup",
            headers=_auth_headers(),
            json={"email": email, "password": password},
            timeout=5,
        )
    except requests.RequestException:
        return None
    if not response.ok:
        return None
    data = response.json()
    user = data.get("user") or data
    if not user or not user.get("id"):
        return None
    return {"id": user["id"], "email": user.get("email", email)}


def sign_in(email: str, password: str) -> dict | None:
    """Returns {"id", "email"} on success, None on bad credentials, missing
    config or network errors."""
    if not auth_configured():
        return None
    try:
        response = requests.post(
            f"{SUPABASE_URL}/auth/v1/token",
            headers=_auth_headers(),
            params={"grant_type": "password"},
            json={"email": email, "password": password},
            timeout=5,
        )
    except requests.RequestException:
        return None
    if not response.ok:
        return None
    user = response.json().get("user")
    if not user or not user.get("id"):
        return None
    return {"id": user["id"], "email": user.get("email", email)}


def create_unique_profile(user_id: str, display_name: str, avatar: str = "🙂") -> str:
    """Creates the profiles row for a freshly signed-up account. The handle
    is derived from the display name; on a uniqueness conflict (409) a
    numeric suffix is appended and retried. Returns the handle actually
    used (best-effort fallback to the first attempted handle on network
    errors, since there's nothing better to store in the session then).
    """
    base_handle = "@" + _slugify_handle(display_name)
    handle = base_handle
    suffix = 1
    while True:
        try:
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/profiles",
                headers=_headers(),
                json={"id": user_id, "display_name": display_name, "handle": handle, "avatar": avatar},
                timeout=5,
            )
        except requests.RequestException:
            return handle
        if response.ok:
            return handle
        if response.status_code == 409:
            suffix += 1
            handle = f"{base_handle}{suffix}"
            continue
        return handle


def fetch_profile(user_id: str) -> dict | None:
    if not is_configured():
        return None
    try:
        rows = _get("profiles", {"id": f"eq.{user_id}", "select": "display_name,handle,avatar"})
    except requests.RequestException:
        return None
    return rows[0] if rows else None


def fetch_posts() -> list[dict]:
    """Returns [] on any error (missing config, network, table not created
    yet) so the demo keeps working off the static dataset alone. Each item:
    {"post": Post, "author": {"name", "handle", "avatar"}, "likes": int,
    "comments": int}. Author comes from the real account (profiles) for
    posts created after accounts existed, falling back to the fictional
    per-topic/perspective author (authors) for older rows without a user_id.
    """
    if not is_configured():
        return []
    try:
        rows = _get(
            "posts",
            {
                "select": (
                    "id,title,content,perspective,categories(name),"
                    "authors(name,handle,avatar),profiles(display_name,handle,avatar),"
                    "likes(count),comments(count)"
                ),
                "order": "created_at.desc",
            },
        )
    except requests.RequestException:
        return []

    result = []
    for row in rows:
        category = row.get("categories") or {}
        profile = row.get("profiles")
        legacy_author = row.get("authors") or {}
        like_rows = row.get("likes") or []
        comment_rows = row.get("comments") or []
        if profile:
            author = {
                "name": profile.get("display_name", "Anonym"),
                "handle": profile.get("handle", "@anonym"),
                "avatar": profile.get("avatar") or "🙂",
            }
        else:
            author = {
                "name": legacy_author.get("name", "Anonym"),
                "handle": legacy_author.get("handle", "@anonym"),
                "avatar": legacy_author.get("avatar", "📰"),
            }
        result.append(
            {
                "post": Post(
                    id=row["id"],
                    title=row["title"],
                    text=row["content"],
                    topic=category.get("name", "sonstiges"),
                    perspective=row["perspective"],
                ),
                "author": author,
                "likes": like_rows[0]["count"] if like_rows else 0,
                "comments": comment_rows[0]["count"] if comment_rows else 0,
            }
        )
    return result


def insert_post(title: str, content: str, topic: str, perspective: str, user_id: str) -> bool:
    if not is_configured():
        return False
    try:
        payload = {
            "title": title,
            "content": content,
            "category_id": _category_id(topic),
            "perspective": perspective,
            "user_id": user_id,
        }
        response = requests.post(f"{SUPABASE_URL}/rest/v1/posts", headers=_headers(), json=payload, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        return False
    return True


def fetch_liked_post_ids(user_id: str, post_ids: list[str]) -> set[str]:
    if not is_configured() or not post_ids:
        return set()
    try:
        ids_filter = "(" + ",".join(post_ids) + ")"
        rows = _get("likes", {"user_id": f"eq.{user_id}", "post_id": f"in.{ids_filter}", "select": "post_id"})
    except requests.RequestException:
        return set()
    return {row["post_id"] for row in rows}


def toggle_like(post_id: str, user_id: str) -> bool | None:
    """Likes are keyed on the logged-in account (post_id, user_id composite
    key in the DB), so a like is bound to one account per post at most.
    Returns the new liked state, or None on error (network, missing config).
    """
    if not is_configured():
        return None
    try:
        existing = _get("likes", {"post_id": f"eq.{post_id}", "user_id": f"eq.{user_id}", "select": "post_id"})
        if existing:
            response = requests.delete(
                f"{SUPABASE_URL}/rest/v1/likes",
                headers=_headers(),
                params={"post_id": f"eq.{post_id}", "user_id": f"eq.{user_id}"},
                timeout=5,
            )
            response.raise_for_status()
            return False
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/likes",
            headers=_headers(),
            json={"post_id": post_id, "user_id": user_id},
            timeout=5,
        )
        response.raise_for_status()
        return True
    except requests.RequestException:
        return None


def insert_comment(post_id: str, user_id: str, content: str) -> bool:
    if not is_configured():
        return False
    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/comments",
            headers=_headers(),
            json={"post_id": post_id, "user_id": user_id, "content": content},
            timeout=5,
        )
        response.raise_for_status()
    except requests.RequestException:
        return False
    return True


def fetch_comments(post_id: str) -> list[dict]:
    """Each item: {"content", "created_at", "author", "handle", "avatar"}."""
    if not is_configured():
        return []
    try:
        rows = _get(
            "comments",
            {
                "post_id": f"eq.{post_id}",
                "select": "content,created_at,profiles(display_name,handle,avatar)",
                "order": "created_at.asc",
            },
        )
    except requests.RequestException:
        return []
    result = []
    for row in rows:
        profile = row.get("profiles") or {}
        result.append(
            {
                "content": row["content"],
                "created_at": row["created_at"],
                "author": profile.get("display_name", "Unbekannt"),
                "handle": profile.get("handle", "@unbekannt"),
                "avatar": profile.get("avatar") or "🙂",
            }
        )
    return result
