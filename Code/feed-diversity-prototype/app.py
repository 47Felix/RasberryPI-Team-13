"""Flask demo: standard vs. diversity-aware feed ranking side by side.

Case 3 (DTEW Hamburg 2026, digi&demo e.V.): feed/recommender design against
filter-bubble reinforcement. See ObsidianGehirn/10 DTEW Workshop/ for the
full problem statements (PS1 for persona "Mia", PS2 for persona "Tom").
"""

import hashlib
import json
import os
import uuid
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

import db
from ranking import Post, diversity_aware_feed, diversity_score, standard_feed, suggest_category

app = Flask(__name__)
# Only guards the session cookie (an anonymous per-browser id for likes), not
# any real auth - a fixed dev fallback is fine for a workshop prototype, but
# set FLASK_SECRET_KEY in .env for anything longer-lived than a demo.
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-not-secret")

DATA_PATH = Path(__file__).parent / "data" / "posts.json"

# Known (topic, perspective) pairs so the "new post" form offers a dropdown
# instead of free-text topics fragmenting the feed into one-off categories.
KNOWN_TOPICS = ["klima", "verkehr", "wirtschaft", "digital"]
KNOWN_PERSPECTIVES = ["pro", "contra"]

# Quick persona presets so the demo directly maps back to Mia/Tom instead of
# requiring visitors to guess a meaningful seed post from the dropdown.
PERSONA_SEEDS = {
    "mia": "klima-1",  # Mia: only ever sees "pro" climate posts, doesn't notice the bubble
    "tom": "wirtschaft-3",  # Tom: stuck in "contra" economy posts, wants out
}

DEFAULT_DIVERSITY_EVERY = 3
MIN_DIVERSITY_EVERY = 2
MAX_DIVERSITY_EVERY = 6

DEFAULT_MODE = "standard"
VALID_MODES = {"standard", "diversity"}

# One fake "account" per (topic, perspective) pair, so the feed reads like a
# real timeline made of different pages/creators instead of anonymous
# database rows. This is what makes a bubble *visible* while scrolling: in
# the standard feed the same one or two accounts repeat over and over, in
# the diversity-aware feed different accounts interrupt that pattern.
# User-submitted posts get their author/handle/avatar straight from the DB
# (db.fetch_posts(), same values, see supabase/migrations/0001_init.sql
# seed data) instead of this dict - it only covers the static dataset.
AUTHOR_META = {
    ("klima", "pro"): {"avatar": "🌱", "name": "Klimaschutz Jetzt", "handle": "@klimajetzt"},
    ("klima", "contra"): {"avatar": "⚡", "name": "Energie Realistisch", "handle": "@energierealistisch"},
    ("verkehr", "pro"): {"avatar": "🚲", "name": "Mobilitätswende", "handle": "@mobilwende"},
    ("verkehr", "contra"): {"avatar": "🚗", "name": "Freie Fahrt", "handle": "@freiefahrt"},
    ("wirtschaft", "pro"): {"avatar": "🧾", "name": "Faire Löhne", "handle": "@fairelöhne"},
    ("wirtschaft", "contra"): {"avatar": "🏭", "name": "Mittelstand Stimme", "handle": "@mittelstandstimme"},
    ("digital", "pro"): {"avatar": "🔒", "name": "Digitale Rechte", "handle": "@digitalerechte"},
    ("digital", "contra"): {"avatar": "🚀", "name": "Tech Standort", "handle": "@techstandort"},
}

# Feed order == recency, like a real timeline: the top post is "just now",
# further down is "older". Purely cosmetic, no real clock involved.
TIME_LABELS = ["gerade eben", "2 Std", "4 Std", "7 Std", "10 Std", "1 Tag", "1 Tag", "2 Tage"]

# Fallback for any (topic, perspective) pair not covered above, so a future
# dataset addition degrades gracefully instead of a KeyError/500.
DEFAULT_AUTHOR_META = {"avatar": "📰", "name": "Feed-Beitrag", "handle": "@perspektiv"}


def _fake_engagement(post_id: str) -> dict:
    """Deterministic, stable-looking comment/repost counts per static post so
    the feed doesn't look like an empty developer fixture. Not randomized per
    request (hashlib, not random) so the numbers don't jump on every reload.
    Only comments/reposts - likes for static posts are fake same as before,
    DB posts get a real count from db.fetch_posts() instead.
    """
    digest = int(hashlib.sha256(post_id.encode()).hexdigest(), 16)
    return {
        "likes": 20 + digest % 260,
        "comments": 2 + (digest // 260) % 45,
        "reposts": 1 + (digest // 11_700) % 20,
    }


def _session_id() -> str:
    if "session_id" not in session:
        session["session_id"] = uuid.uuid4().hex
    return session["session_id"]


def _decorate_feed(feed: list[dict], extra_meta: dict) -> list[dict]:
    decorated = []
    for index, item in enumerate(feed):
        post = item["post"]
        meta = extra_meta.get(post.id)
        if meta:
            engagement = {"likes": meta["likes"], "comments": 0, "reposts": 0}
            author = meta["author"]
            is_db_post = True
        else:
            engagement = _fake_engagement(post.id)
            author = AUTHOR_META.get((post.topic, post.perspective), DEFAULT_AUTHOR_META)
            is_db_post = False
        decorated.append(
            {
                **item,
                "avatar": author["avatar"],
                "author": author["name"],
                "handle": author["handle"],
                "time_label": TIME_LABELS[min(index, len(TIME_LABELS) - 1)],
                "is_db_post": is_db_post,
                **engagement,
            }
        )
    return decorated


def load_posts() -> tuple[list[Post], dict]:
    """Returns (all posts, extra metadata for DB-backed posts keyed by id).

    User-submitted posts from Supabase are appended after the curated
    dataset. db.fetch_posts() returns [] if Supabase isn't configured or
    unreachable, so the demo keeps working off the static dataset alone.
    """
    with open(DATA_PATH, encoding="utf-8") as f:
        raw = json.load(f)
    static_posts = [Post(**item) for item in raw]

    db_rows = db.fetch_posts()
    db_posts = [row["post"] for row in db_rows]
    extra_meta = {row["post"].id: {"author": row["author"], "likes": row["likes"]} for row in db_rows}

    return static_posts + db_posts, extra_meta


def _parse_diversity_every(raw: str | None) -> int:
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return DEFAULT_DIVERSITY_EVERY
    return max(MIN_DIVERSITY_EVERY, min(value, MAX_DIVERSITY_EVERY))


@app.route("/")
def index():
    posts, extra_meta = load_posts()

    persona = request.args.get("persona")
    seed_id = PERSONA_SEEDS.get(persona, request.args.get("seed_id", posts[0].id))
    if seed_id not in {p.id for p in posts}:
        seed_id = posts[0].id
    seed_post = next(p for p in posts if p.id == seed_id)

    diversity_every = _parse_diversity_every(request.args.get("mix"))

    mode = request.args.get("mode")
    if mode not in VALID_MODES:
        mode = DEFAULT_MODE

    if mode == "diversity":
        active_feed = diversity_aware_feed(posts, seed_id, diversity_every=diversity_every)
    else:
        active_feed = standard_feed(posts, seed_id)

    feed_items = _decorate_feed(active_feed, extra_meta)

    db_post_ids = [item["post"].id for item in feed_items if item["is_db_post"]]
    liked_ids = db.fetch_liked_post_ids(_session_id(), db_post_ids) if db_post_ids else set()
    for item in feed_items:
        item["liked"] = item["post"].id in liked_ids

    return render_template(
        "index.html",
        posts=posts,
        seed_id=seed_id,
        persona=persona,
        mix=diversity_every,
        mode=mode,
        feed_items=feed_items,
        feed_score=diversity_score(active_feed, seed_post),
        known_topics=KNOWN_TOPICS,
        known_perspectives=KNOWN_PERSPECTIVES,
        db_configured=db.is_configured(),
    )


@app.route("/posts", methods=["POST"])
def create_post():
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    topic = request.form.get("topic", "")
    perspective = request.form.get("perspective", "")

    if title and content and topic in KNOWN_TOPICS and perspective in KNOWN_PERSPECTIVES:
        db.insert_post(title, content, topic, perspective)

    return redirect(url_for("index", mode=request.form.get("mode"), mix=request.form.get("mix")))


@app.route("/posts/suggest-category", methods=["POST"])
def suggest_category_endpoint():
    """Called via fetch() while typing in the "new post" form (see
    templates/index.html) to pre-select a category. Purely a suggestion -
    the dropdown stays editable, this never blocks post creation.
    """
    payload = request.get_json(silent=True) or {}
    title = (payload.get("title") or "").strip()
    content = (payload.get("content") or "").strip()
    if not title and not content:
        return jsonify({"topic": None})

    posts, _ = load_posts()
    return jsonify({"topic": suggest_category(title, content, posts)})


@app.route("/posts/<post_id>/like", methods=["POST"])
def like_post(post_id):
    liked = db.toggle_like(post_id, _session_id())
    if liked is None:
        return jsonify({"error": "Supabase nicht erreichbar"}), 503
    return jsonify({"liked": liked})


if __name__ == "__main__":
    app.run(debug=True, port=5050)
