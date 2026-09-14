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
    data = response.json()
    if not isinstance(data, list):
        # PostgREST answers an ambiguous embed (e.g. two relationships
        # between the same tables) with HTTP 300 and an error object
        # instead of rows - raise_for_status() doesn't treat 300 as an
        # error, so this would otherwise silently iterate over dict keys.
        raise requests.RequestException(f"Unexpected PostgREST response for {path}: {data}")
    return data


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


def create_unique_profile(
    user_id: str,
    display_name: str,
    avatar: str = "🙂",
    onboarding_perspective_by_topic: dict[str, str] | None = None,
    onboarding_political_label: str | None = None,
) -> str:
    """Creates the profiles row for a freshly signed-up account. The handle
    is derived from the display name; on a uniqueness conflict (409) a
    numeric suffix is appended and retried. Returns the handle actually
    used (best-effort fallback to the first attempted handle on network
    errors, since there's nothing better to store in the session then).

    onboarding_perspective_by_topic/onboarding_political_label are the
    optional, skippable registration-survey answers (see
    0004_onboarding_survey.sql/0005_onboarding_per_topic.sql) - the topic map
    stores one pro/contra answer per topic (e.g. {"transport": "pro"}), same
    shape as ranking.dominant_perspective_by_topic() produces from real
    engagement, so app.py can merge the two without converting between
    formats. None/{} just leaves the feed with no initial lean until real
    likes/comments provide one.
    """
    base_handle = "@" + _slugify_handle(display_name)
    handle = base_handle
    suffix = 1
    payload = {
        "id": user_id,
        "display_name": display_name,
        "avatar": avatar,
        "onboarding_perspective_by_topic": onboarding_perspective_by_topic or None,
        "onboarding_political_label": onboarding_political_label,
    }
    while True:
        try:
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/profiles",
                headers=_headers(),
                json={**payload, "handle": handle},
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
        rows = _get(
            "profiles",
            {
                "id": f"eq.{user_id}",
                "select": "display_name,handle,avatar,onboarding_perspective_by_topic,onboarding_political_label",
            },
        )
    except requests.RequestException:
        return None
    return rows[0] if rows else None


def fetch_categories() -> list[str]:
    """All topic names from the categories table, so the "new post" dropdown,
    the /dashboard chip list and post validation all track whatever
    categories actually exist in Supabase - add a row to `categories` and it
    shows up everywhere on the next request, no code change/deploy needed.
    [] if Supabase isn't configured/unreachable, in which case app.py falls
    back to its hardcoded default topic list."""
    if not is_configured():
        return []
    try:
        rows = _get("categories", {"select": "name", "order": "name.asc"})
    except requests.RequestException:
        return []
    return [row["name"] for row in rows]


def fetch_topic_stances() -> dict[str, dict[str, str]]:
    """topic -> {"pro": phrase, "contra": phrase} from categories.pro_label/
    contra_label (see 0008_topic_stance_labels.sql) - same "lives in
    Supabase, editable without a code change" idea as fetch_categories(),
    just for the phrase text stance_label() (app.py) shows instead of the
    bare "pro"/"contra" word. A row missing either label is left out of the
    dict entirely (not included with a None value) so app.py's TOPIC_STANCES
    fallback can fill the gap per-topic. {} if Supabase isn't configured/
    unreachable, in which case app.py falls back to TOPIC_STANCES alone."""
    if not is_configured():
        return {}
    try:
        rows = _get("categories", {"select": "name,pro_label,contra_label"})
    except requests.RequestException:
        return {}
    stances = {}
    for row in rows:
        if row.get("pro_label") and row.get("contra_label"):
            stances[row["name"]] = {"pro": row["pro_label"], "contra": row["contra_label"]}
    return stances


def fetch_all_profiles() -> list[dict]:
    """Every account, for the /dashboard feed-transparency view (see
    app.py) - includes the same onboarding columns as fetch_profile() so the
    dashboard doesn't need a second per-account query just for those."""
    if not is_configured():
        return []
    try:
        rows = _get(
            "profiles",
            {
                "select": "id,display_name,handle,onboarding_perspective_by_topic,onboarding_political_label",
                "order": "display_name.asc",
            },
        )
    except requests.RequestException:
        return []
    return rows


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
                # profiles needs the explicit !posts_user_id_fkey hint: PostgREST
                # also sees posts<->profiles as many-to-many through likes
                # (post_id + user_id both link the two), and refuses to guess
                # which relationship "profiles(...)" should mean.
                "select": (
                    "id,title,content,perspective,political_label,categories(name),"
                    "authors(name,handle,avatar),profiles!posts_user_id_fkey(display_name,handle,avatar),"
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
                "name": profile.get("display_name", "Anonymous"),
                "handle": profile.get("handle", "@anonymous"),
                "avatar": profile.get("avatar") or "🙂",
            }
        else:
            author = {
                "name": legacy_author.get("name", "Anonymous"),
                "handle": legacy_author.get("handle", "@anonymous"),
                "avatar": legacy_author.get("avatar", "📰"),
            }
        result.append(
            {
                "post": Post(
                    id=row["id"],
                    title=row["title"],
                    text=row["content"],
                    topic=category.get("name", "other"),
                    perspective=row["perspective"],
                    political_label=row.get("political_label"),
                ),
                "author": author,
                "likes": like_rows[0]["count"] if like_rows else 0,
                "comments": comment_rows[0]["count"] if comment_rows else 0,
            }
        )
    return result


def insert_post(
    title: str,
    content: str,
    topic: str,
    perspective: str,
    user_id: str | None,
    political_label: str | None = None,
    author_id: str | None = None,
) -> str | None:
    """user_id is the normal path (a real logged-in account, via the "new
    post" form or seed_demo_accounts.py) - author_id is the legacy path,
    for fictional/topic-themed bylines (see supabase/migrations/0001_init.sql
    seed data, ensure_author()) that aren't tied to a
    real Supabase Auth account. fetch_posts() falls back to `authors` for
    display whenever a row has no user_id, so passing author_id without a
    user_id is the normal way to seed bulk demo content without creating
    real accounts for it.

    Returns the new post's id (so create_post() in app.py can seed the
    feed on it directly - with a 300+ post catalogue and an 8-post feed,
    a freshly published post otherwise almost never wins enough
    similarity/perspective ranking to appear on its own, see user report
    2026-09-11), or None on failure.
    """
    if not is_configured():
        return None
    try:
        payload = {
            "title": title,
            "content": content,
            "category_id": _category_id(topic),
            "perspective": perspective,
            "political_label": political_label,
            "user_id": user_id,
            "author_id": author_id,
        }
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/posts",
            headers={**_headers(), "Prefer": "return=representation"},
            json=payload,
            timeout=5,
        )
        response.raise_for_status()
        rows = response.json()
    except requests.RequestException:
        return None
    return rows[0]["id"] if rows else None


def ensure_author(name: str, handle: str, avatar: str) -> str | None:
    """Upserts a legacy fictional byline into `authors` (on_conflict=handle,
    merge-duplicates) and returns its id - idempotent, so seeding scripts
    can declare the same persona every run without creating duplicates.
    None if Supabase isn't configured/reachable."""
    if not is_configured():
        return None
    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/authors",
            headers={**_headers(), "Prefer": "resolution=merge-duplicates,return=representation"},
            params={"on_conflict": "handle"},
            json={"name": name, "handle": handle, "avatar": avatar},
            timeout=5,
        )
        response.raise_for_status()
        rows = response.json()
    except (requests.RequestException, ValueError):
        return None
    return rows[0]["id"] if rows else None


def fetch_latest_post_id() -> str | None:
    """Id of the newest post, for the frontend's new-posts poll (see
    templates/index.html) - deliberately just one narrow column/row instead
    of the full fetch_posts() join, since this gets called every ~15s."""
    if not is_configured():
        return None
    try:
        rows = _get("posts", {"select": "id", "order": "created_at.desc", "limit": "1"})
    except requests.RequestException:
        return None
    return rows[0]["id"] if rows else None


def fetch_commented_history(user_id: str) -> list[dict]:
    """Topic+perspective of every post the account has commented on - same
    shape as fetch_liked_history(), so commenting counts as an engagement
    signal for ranking.dominant_perspective_by_topic() too, not just liking.
    Each item: {"topic":..., "perspective":...}."""
    if not is_configured():
        return []
    try:
        rows = _get("comments", {"user_id": f"eq.{user_id}", "select": "posts(perspective,categories(name))"})
    except requests.RequestException:
        return []
    result = []
    for row in rows:
        post = row.get("posts")
        if not post:
            continue
        category = post.get("categories") or {}
        result.append({"topic": category.get("name"), "perspective": post.get("perspective")})
    return result


def fetch_commented_political_labels(user_id: str) -> list[str]:
    """Same idea as fetch_commented_history(), for the independent
    political_label axis (feeds dominant_political_label())."""
    if not is_configured():
        return []
    try:
        rows = _get("comments", {"user_id": f"eq.{user_id}", "select": "posts(political_label)"})
    except requests.RequestException:
        return []
    return [row["posts"]["political_label"] for row in rows if row.get("posts")]


def fetch_liked_history(user_id: str) -> list[dict]:
    """Topic+perspective+political_label of every post the account has
    liked, oldest first - feeds ranking.dominant_perspective_by_topic()
    (order doesn't matter there), ranking.dominant_political_label() (same),
    ranking.bubble_trend() (order is the whole point, only cares about
    "perspective") and ranking.political_bubble_trend() (same, only cares
    about "political_label"), so callers get all four from one query instead
    of fetching the same likes/posts join twice - political_label used to be
    its own separate fetch_liked_political_labels() query until this
    session, when NIGHTLY_TASK.md's political-axis trend work made that
    duplication one query too many. Each item: {"topic":..., "perspective":
    ..., "political_label":...}. [] if there's no history yet or Supabase is
    unreachable."""
    if not is_configured():
        return []
    try:
        rows = _get(
            "likes",
            {
                "user_id": f"eq.{user_id}",
                "select": "created_at,posts(perspective,political_label,categories(name))",
                "order": "created_at.asc",
            },
        )
    except requests.RequestException:
        return []
    result = []
    for row in rows:
        post = row.get("posts")
        if not post:
            continue
        category = post.get("categories") or {}
        result.append(
            {
                "topic": category.get("name"),
                "perspective": post.get("perspective"),
                "political_label": post.get("political_label"),
            }
        )
    return result


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
    """Each item: {"id", "user_id", "content", "created_at", "author",
    "handle", "avatar"}. user_id lets the frontend show a delete button only
    on the viewer's own comments (see templates/index.html:renderComments)."""
    if not is_configured():
        return []
    try:
        rows = _get(
            "comments",
            {
                "post_id": f"eq.{post_id}",
                "select": "id,user_id,content,created_at,profiles(display_name,handle,avatar)",
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
                "id": row["id"],
                "user_id": row["user_id"],
                "content": row["content"],
                "created_at": row["created_at"],
                "author": profile.get("display_name", "Unknown"),
                "handle": profile.get("handle", "@unknown"),
                "avatar": profile.get("avatar") or "🙂",
            }
        )
    return result


def delete_comment(comment_id: str, user_id: str) -> bool:
    """Deletes the comment only if it belongs to user_id - returns whether a
    row was actually removed (False for "not found" and "not the owner"
    alike, so the caller can't distinguish the two, which is the point)."""
    if not is_configured():
        return False
    try:
        response = requests.delete(
            f"{SUPABASE_URL}/rest/v1/comments",
            headers={**_headers(), "Prefer": "return=representation"},
            params={"id": f"eq.{comment_id}", "user_id": f"eq.{user_id}"},
            timeout=5,
        )
        response.raise_for_status()
    except requests.RequestException:
        return False
    return bool(response.json())
