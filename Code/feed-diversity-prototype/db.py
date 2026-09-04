"""Supabase-backed storage for user-submitted posts.

Reads/writes go through the PostgREST API using the secret key (server-side
only, never sent to the browser) so the table itself can stay locked down
with row level security and no public policies at all.
"""

import os

import requests
from dotenv import load_dotenv

from ranking import Post

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_SECRET_KEY = os.environ.get("SUPABASE_SECRET_KEY", "")

_TABLE_URL = f"{SUPABASE_URL}/rest/v1/posts"


def is_configured() -> bool:
    return bool(SUPABASE_URL and SUPABASE_SECRET_KEY)


def _headers() -> dict:
    return {
        "apikey": SUPABASE_SECRET_KEY,
        "Authorization": f"Bearer {SUPABASE_SECRET_KEY}",
        "Content-Type": "application/json",
    }


def fetch_posts() -> list[Post]:
    """Returns [] on any error (missing config, network, table not created
    yet) so the demo keeps working off the static dataset alone."""
    if not is_configured():
        return []
    try:
        response = requests.get(
            _TABLE_URL,
            headers=_headers(),
            params={"select": "id,title,content,topic,perspective", "order": "created_at.desc"},
            timeout=5,
        )
        response.raise_for_status()
    except requests.RequestException:
        return []
    return [
        Post(id=row["id"], title=row["title"], text=row["content"], topic=row["topic"], perspective=row["perspective"])
        for row in response.json()
    ]


def insert_post(title: str, content: str, topic: str, perspective: str) -> bool:
    if not is_configured():
        return False
    try:
        response = requests.post(
            _TABLE_URL,
            headers=_headers(),
            json={"title": title, "content": content, "topic": topic, "perspective": perspective},
            timeout=5,
        )
        response.raise_for_status()
    except requests.RequestException:
        return False
    return True
