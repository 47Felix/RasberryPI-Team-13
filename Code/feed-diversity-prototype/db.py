"""Supabase-backed storage for user-submitted posts, likes, categories and
authors (schema: supabase/migrations/0001_init.sql).

Reads/writes go through the PostgREST API using the secret key (server-side
only, never sent to the browser) so every table can stay locked down with
row level security and no anon policies at all - the Flask backend is the
only thing that can touch this data.
"""

import os

import requests
from dotenv import load_dotenv

from ranking import Post

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_SECRET_KEY = os.environ.get("SUPABASE_SECRET_KEY", "")

# Matches the seed data in supabase/migrations/0001_init.sql, which mirrors
# app.py:AUTHOR_META so a user-submitted post plugs into the same "feels
# like a real account per topic/perspective" design as the static dataset.
AUTHOR_HANDLE_BY_TOPIC_PERSPECTIVE = {
    ("klima", "pro"): "@klimajetzt",
    ("klima", "contra"): "@energierealistisch",
    ("verkehr", "pro"): "@mobilwende",
    ("verkehr", "contra"): "@freiefahrt",
    ("wirtschaft", "pro"): "@fairelöhne",
    ("wirtschaft", "contra"): "@mittelstandstimme",
    ("digital", "pro"): "@digitalerechte",
    ("digital", "contra"): "@techstandort",
}

# Cache category/author name -> id lookups for the lifetime of the process;
# both tables only change via the migration seed data, not at runtime.
_category_id_cache: dict[str, str] = {}
_author_id_cache: dict[str, str] = {}


def is_configured() -> bool:
    return bool(SUPABASE_URL and SUPABASE_SECRET_KEY)


def _headers() -> dict:
    return {
        "apikey": SUPABASE_SECRET_KEY,
        "Authorization": f"Bearer {SUPABASE_SECRET_KEY}",
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


def _author_id(topic: str, perspective: str) -> str | None:
    handle = AUTHOR_HANDLE_BY_TOPIC_PERSPECTIVE.get((topic, perspective))
    if handle is None:
        return None
    if handle not in _author_id_cache:
        rows = _get("authors", {"handle": f"eq.{handle}", "select": "id"})
        if not rows:
            return None
        _author_id_cache[handle] = rows[0]["id"]
    return _author_id_cache[handle]


def fetch_posts() -> list[dict]:
    """Returns [] on any error (missing config, network, table not created
    yet) so the demo keeps working off the static dataset alone. Each item:
    {"post": Post, "author": {"name", "handle", "avatar"}, "likes": int}.
    """
    if not is_configured():
        return []
    try:
        rows = _get(
            "posts",
            {
                "select": "id,title,content,perspective,categories(name),authors(name,handle,avatar),likes(count)",
                "order": "created_at.desc",
            },
        )
    except requests.RequestException:
        return []

    result = []
    for row in rows:
        category = row.get("categories") or {}
        author = row.get("authors") or {}
        like_rows = row.get("likes") or []
        result.append(
            {
                "post": Post(
                    id=row["id"],
                    title=row["title"],
                    text=row["content"],
                    topic=category.get("name", "sonstiges"),
                    perspective=row["perspective"],
                ),
                "author": {
                    "name": author.get("name", "Anonym"),
                    "handle": author.get("handle", "@anonym"),
                    "avatar": author.get("avatar", "📰"),
                },
                "likes": like_rows[0]["count"] if like_rows else 0,
            }
        )
    return result


def insert_post(title: str, content: str, topic: str, perspective: str) -> bool:
    if not is_configured():
        return False
    try:
        payload = {
            "title": title,
            "content": content,
            "category_id": _category_id(topic),
            "author_id": _author_id(topic, perspective),
            "perspective": perspective,
        }
        response = requests.post(f"{SUPABASE_URL}/rest/v1/posts", headers=_headers(), json=payload, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        return False
    return True


def fetch_liked_post_ids(session_id: str, post_ids: list[str]) -> set[str]:
    if not is_configured() or not post_ids:
        return set()
    try:
        ids_filter = "(" + ",".join(post_ids) + ")"
        rows = _get("likes", {"session_id": f"eq.{session_id}", "post_id": f"in.{ids_filter}", "select": "post_id"})
    except requests.RequestException:
        return set()
    return {row["post_id"] for row in rows}


def toggle_like(post_id: str, session_id: str) -> bool | None:
    """Likes are keyed on a Flask session cookie, not a real login - good
    enough to make the toggle idempotent per browser for a workshop demo.
    Returns the new liked state, or None on error (network, missing config).
    """
    if not is_configured():
        return None
    try:
        existing = _get("likes", {"post_id": f"eq.{post_id}", "session_id": f"eq.{session_id}", "select": "post_id"})
        if existing:
            response = requests.delete(
                f"{SUPABASE_URL}/rest/v1/likes",
                headers=_headers(),
                params={"post_id": f"eq.{post_id}", "session_id": f"eq.{session_id}"},
                timeout=5,
            )
            response.raise_for_status()
            return False
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/likes",
            headers=_headers(),
            json={"post_id": post_id, "session_id": session_id},
            timeout=5,
        )
        response.raise_for_status()
        return True
    except requests.RequestException:
        return None
