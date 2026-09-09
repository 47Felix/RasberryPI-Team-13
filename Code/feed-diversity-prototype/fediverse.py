"""Read-only Fediverse integration: shows public Mastodon posts for a
topic-relevant hashtag as an extra, clearly-external perspective source
alongside the app's own Supabase posts.

Deliberately NOT an ActivityPub implementation (no actor, no WebFinger, no
HTTP Signatures, no inbox/outbox) - see the feasibility note in
ObsidianGehirn/10 DTEW Workshop/Fediverse ActivityPub - Machbarkeitseinschaetzung.md
for why a full ActivityPub client/server wasn't attempted. This uses
Mastodon's public REST API instead, which needs no authentication for
reading public content and is what most "Fediverse integration" projects
actually use in practice for read-only access.

Same fail-open pattern as db.py: any network error, timeout or unexpected
response just yields an empty list, so a slow/unreachable Mastodon instance
never breaks the page - the section simply shows nothing instead of an error.
"""

import html
import os
import re
import time

import requests

DEFAULT_INSTANCE = os.environ.get("FEDIVERSE_INSTANCE", "mastodon.social")

# index() calls fetch_public_posts() on every "/" request, but a hashtag
# timeline doesn't change fast enough to justify one live Mastodon fetch per
# page view (see NIGHTLY_TASK.md) - cache successful responses per
# (hashtag, limit) for this long before fetching again.
CACHE_TTL_SECONDS = int(os.environ.get("FEDIVERSE_CACHE_SECONDS", "300"))

# {(hashtag, limit): (fetched_at_monotonic, result)}
_cache: dict[tuple[str, int], tuple[float, list[dict]]] = {}


def clear_cache() -> None:
    """Drops all cached responses immediately - used by tests, and available
    for a future admin/ops action if a stale cache ever needs a manual kick."""
    _cache.clear()

# One hashtag per topic, so the "aus dem Fediverse" section can follow
# whichever topic the visitor is currently looking at. Rough,
# German-language-leaning picks - meant as a starting point for the team to
# adjust, not a researched-perfect mapping (see feasibility note). Topics
# without an entry fall back to the topic name itself as a hashtag (see
# _hashtag_for()), so a category added later still shows *something* instead
# of an empty section.
TOPIC_HASHTAGS = {
    "klima": "klimapolitik",
    "verkehr": "verkehrswende",
    "wirtschaft": "wirtschaftspolitik",
    "digital": "digitalpolitik",
    "bildung": "bildungspolitik",
    "gesundheit": "gesundheitspolitik",
    "migration": "migrationspolitik",
    "wohnen": "mietenwahnsinn",
    "sicherheit": "innenpolitik",
    "soziales": "sozialpolitik",
    "europa": "europapolitik",
    "aussenpolitik": "aussenpolitik",
}

_HASHTAG_CLEAN_RE = re.compile(r"[^a-z0-9]+")


def _hashtag_for(topic: str) -> str | None:
    """Mapped hashtag for `topic`, or a sanitised version of the topic name
    as a fallback (letters/digits only) so an unmapped category still gets a
    best-effort timeline instead of nothing. None only for an empty topic."""
    mapped = TOPIC_HASHTAGS.get(topic)
    if mapped:
        return mapped
    fallback = _HASHTAG_CLEAN_RE.sub("", (topic or "").lower())
    return fallback or None

REQUEST_TIMEOUT = 5

_TAG_RE = re.compile(r"<[^>]+>")


def _strip_html(raw: str) -> str:
    """Mastodon's `content` field is HTML from a third-party post - never
    rendered with Jinja's `|safe` (that would be an XSS vector for
    arbitrary external content), so this reduces it to plain text instead
    of showing literal '<p>' tags to the escaped-by-default template."""
    without_tags = _TAG_RE.sub(" ", raw)
    return " ".join(html.unescape(without_tags).split())


def fetch_public_posts(topic: str, limit: int = 3) -> list[dict]:
    """Returns up to `limit` public posts for the hashtag mapped to `topic`,
    each as {"content", "url", "account_handle", "created_at"}. Empty list
    if the topic has no mapped hashtag, the instance is unreachable, or the
    response isn't the JSON list format expected - never raises.

    Cached per (hashtag, limit) for CACHE_TTL_SECONDS instead of hitting
    Mastodon on every call (see NIGHTLY_TASK.md) - a stale cache entry is
    still served if a later live fetch fails (network blip, instance
    briefly down), same fail-open spirit as the rest of this module: better
    to keep showing the last known-good posts than blank the section over a
    transient error. Only an *empty* cache on failure falls back to [].
    """
    hashtag = _hashtag_for(topic)
    if not hashtag:
        return []
    cache_key = (hashtag, limit)
    cached = _cache.get(cache_key)
    now = time.monotonic()
    if cached is not None and now - cached[0] < CACHE_TTL_SECONDS:
        return cached[1]

    try:
        response = requests.get(
            f"https://{DEFAULT_INSTANCE}/api/v1/timelines/tag/{hashtag}",
            # Over-fetch a bit: reblogs and text-less posts get filtered out
            # below, so ask for more than `limit` to still land `limit`
            # readable ones. Capped so a bad topic can't pull a huge page.
            params={"limit": min(limit * 4, 40)},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        posts = response.json()
    except (requests.RequestException, ValueError):
        return cached[1] if cached is not None else []
    if not isinstance(posts, list):
        return cached[1] if cached is not None else []

    result = []
    for post in posts:
        if len(result) >= limit:
            break
        # Tag timelines include boosts/reblogs (the "post" is just a wrapper
        # around someone else's) and media-only posts with no text - neither
        # is useful as a readable outside perspective, so skip both.
        if post.get("reblog"):
            continue
        content = _strip_html(post.get("content", ""))
        if not content:
            continue
        account = post.get("account") or {}
        url = post.get("url", "")
        result.append(
            {
                "content": content if len(content) <= 280 else content[:277].rstrip() + "…",
                # Only ever render as a link if it's actually http(s) - a
                # post is untrusted external data, and Jinja auto-escaping
                # doesn't stop a "javascript:" scheme from ending up in href.
                "url": url if url.startswith(("http://", "https://")) else "",
                "account_handle": account.get("acct", "unbekannt"),
                "created_at": post.get("created_at", ""),
            }
        )
    _cache[cache_key] = (now, result)
    return result
