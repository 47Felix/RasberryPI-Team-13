"""Flask demo: standard vs. diversity-aware feed ranking side by side.

Case 3 (DTEW Hamburg 2026, digi&demo e.V.): feed/recommender design against
filter-bubble reinforcement. See ObsidianGehirn/10 DTEW Workshop/ for the
full problem statements.
"""

import os
from functools import wraps

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

import db
import fediverse
from ranking import (
    Post,
    diversity_aware_feed,
    diversity_score_for_perspective,
    diversity_score_for_political_label,
    dominant_perspective,
    dominant_political_label,
    standard_feed,
    suggest_category,
)

app = Flask(__name__)
# Signs the session cookie that now holds the logged-in account's user_id -
# set FLASK_SECRET_KEY in .env for anything longer-lived than a demo, the
# fixed dev fallback lets sessions survive a restart but isn't a secret.
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-not-secret")

# Known (topic, perspective) pairs so the "new post" form offers a dropdown
# instead of free-text topics fragmenting the feed into one-off categories.
KNOWN_TOPICS = ["klima", "verkehr", "wirtschaft", "digital"]
KNOWN_PERSPECTIVES = ["pro", "contra"]
# Self-chosen political label, independent of the topic's pro/contra
# perspective - see README ("Politische Einordnung") for why this is a
# user-chosen label rather than an automatically detected one.
KNOWN_POLITICAL_LABELS = ["links", "mitte", "rechts"]

DEFAULT_DIVERSITY_EVERY = 3
MIN_DIVERSITY_EVERY = 2
MAX_DIVERSITY_EVERY = 6

DEFAULT_MODE = "standard"
VALID_MODES = {"standard", "diversity"}

# Feed order == recency, like a real timeline: the top post is "just now",
# further down is "older". Purely cosmetic, no real clock involved.
TIME_LABELS = ["gerade eben", "2 Std", "4 Std", "7 Std", "10 Std", "1 Tag", "1 Tag", "2 Tage"]


def _current_user() -> dict | None:
    if "user_id" not in session:
        return None
    return {"id": session["user_id"], "display_name": session.get("display_name"), "handle": session.get("handle")}


def login_required_json(view):
    """For fetch()-driven endpoints: a JSON 401 instead of a redirect, so the
    frontend can send the browser to /login itself (see toggleLike/submitComment
    in templates/index.html)."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "login_required"}), 401
        return view(*args, **kwargs)

    return wrapped


def _decorate_feed(feed: list[dict], extra_meta: dict) -> list[dict]:
    decorated = []
    for index, item in enumerate(feed):
        meta = extra_meta[item["post"].id]
        decorated.append(
            {
                **item,
                "avatar": meta["author"]["avatar"],
                "author": meta["author"]["name"],
                "handle": meta["author"]["handle"],
                "time_label": TIME_LABELS[min(index, len(TIME_LABELS) - 1)],
                "likes": meta["likes"],
                "comments": meta["comments"],
            }
        )
    return decorated


def load_posts() -> tuple[list[Post], dict]:
    """Returns (all posts, extra metadata keyed by id). Posts come exclusively
    from Supabase now (no more curated static dataset) - db.fetch_posts()
    returns [] if Supabase isn't configured/unreachable/empty, in which case
    the feed just shows an empty state (see index()).
    """
    db_rows = db.fetch_posts()
    posts = [row["post"] for row in db_rows]
    extra_meta = {
        row["post"].id: {"author": row["author"], "likes": row["likes"], "comments": row["comments"]}
        for row in db_rows
    }
    return posts, extra_meta


def _parse_diversity_every(raw: str | None) -> int:
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return DEFAULT_DIVERSITY_EVERY
    return max(MIN_DIVERSITY_EVERY, min(value, MAX_DIVERSITY_EVERY))


@app.route("/")
def index():
    posts, extra_meta = load_posts()
    current_user = _current_user()
    diversity_every = _parse_diversity_every(request.args.get("mix"))
    mode = request.args.get("mode") if request.args.get("mode") in VALID_MODES else DEFAULT_MODE

    seed_id = None
    feed_items = []
    feed_score = 0
    political_feed_score = 0
    preferred_perspective = None
    preferred_political_label = None
    show_political_score = False
    fediverse_posts = []
    fediverse_topic = None

    if posts:
        seed_id = request.args.get("seed_id")
        if seed_id not in {p.id for p in posts}:
            seed_id = posts[0].id
        seed_post = next(p for p in posts if p.id == seed_id)
        fediverse_topic = seed_post.topic
        fediverse_posts = fediverse.fetch_public_posts(fediverse_topic)

        if current_user:
            preferred_perspective = dominant_perspective(db.fetch_liked_perspectives(current_user["id"]))
            preferred_political_label = dominant_political_label(db.fetch_liked_political_labels(current_user["id"]))
        bias_perspective = preferred_perspective or seed_post.perspective
        bias_political_label = preferred_political_label or seed_post.political_label

        if mode == "diversity":
            active_feed = diversity_aware_feed(
                posts,
                seed_id,
                diversity_every=diversity_every,
                preferred_perspective=preferred_perspective,
                preferred_political_label=preferred_political_label,
            )
        else:
            active_feed = standard_feed(
                posts,
                seed_id,
                preferred_perspective=preferred_perspective,
                preferred_political_label=preferred_political_label,
            )

        feed_items = _decorate_feed(active_feed, extra_meta)
        feed_score = diversity_score_for_perspective(active_feed, bias_perspective)
        political_feed_score = diversity_score_for_political_label(active_feed, bias_political_label)
        show_political_score = bias_political_label is not None

        db_post_ids = [item["post"].id for item in feed_items]
        liked_ids = db.fetch_liked_post_ids(current_user["id"], db_post_ids) if current_user else set()
        for item in feed_items:
            item["liked"] = item["post"].id in liked_ids

    return render_template(
        "index.html",
        posts=posts,
        seed_id=seed_id,
        mix=diversity_every,
        mode=mode,
        feed_items=feed_items,
        feed_score=feed_score,
        political_feed_score=political_feed_score,
        show_political_score=show_political_score,
        known_topics=KNOWN_TOPICS,
        known_perspectives=KNOWN_PERSPECTIVES,
        known_political_labels=KNOWN_POLITICAL_LABELS,
        db_configured=db.is_configured(),
        current_user=current_user,
        fediverse_posts=fediverse_posts,
        fediverse_topic=fediverse_topic,
        preferred_perspective=preferred_perspective,
        preferred_political_label=preferred_political_label,
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        display_name = request.form.get("display_name", "").strip()
        if not email or not password or not display_name:
            error = "Bitte alle Felder ausfüllen."
        elif len(password) < 6:
            error = "Passwort muss mindestens 6 Zeichen haben."
        else:
            user = db.sign_up(email, password)
            if user is None:
                error = "Registrierung fehlgeschlagen (E-Mail evtl. schon vergeben, oder Supabase nicht erreichbar)."
            else:
                handle = db.create_unique_profile(user["id"], display_name)
                session["user_id"] = user["id"]
                session["display_name"] = display_name
                session["handle"] = handle
                return redirect(request.args.get("next") or url_for("index"))
    return render_template("register.html", error=error, auth_configured=db.auth_configured())


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        user = db.sign_in(email, password)
        if user is None:
            error = "E-Mail oder Passwort falsch."
        else:
            profile = db.fetch_profile(user["id"]) or {}
            session["user_id"] = user["id"]
            session["display_name"] = profile.get("display_name", user["email"])
            session["handle"] = profile.get("handle", "@" + user["email"].split("@")[0])
            return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html", error=error, auth_configured=db.auth_configured())


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/posts", methods=["POST"])
def create_post():
    if "user_id" not in session:
        return redirect(url_for("login", next=url_for("index")))

    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    topic = request.form.get("topic", "")
    perspective = request.form.get("perspective", "")
    political_label = request.form.get("political_label", "")

    if (
        title
        and content
        and topic in KNOWN_TOPICS
        and perspective in KNOWN_PERSPECTIVES
        and political_label in KNOWN_POLITICAL_LABELS
    ):
        db.insert_post(title, content, topic, perspective, session["user_id"], political_label)

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
@login_required_json
def like_post(post_id):
    liked = db.toggle_like(post_id, session["user_id"])
    if liked is None:
        return jsonify({"error": "Supabase nicht erreichbar"}), 503
    return jsonify({"liked": liked})


@app.route("/posts/<post_id>/comments", methods=["GET"])
def list_comments(post_id):
    return jsonify({"comments": db.fetch_comments(post_id)})


@app.route("/posts/<post_id>/comments", methods=["POST"])
@login_required_json
def create_comment(post_id):
    payload = request.get_json(silent=True) or {}
    content = (payload.get("content") or "").strip()
    if not content:
        return jsonify({"error": "empty"}), 400
    if not db.insert_comment(post_id, session["user_id"], content):
        return jsonify({"error": "Supabase nicht erreichbar"}), 503
    return jsonify({"ok": True})


@app.route("/comments/<comment_id>", methods=["DELETE"])
@login_required_json
def delete_comment(comment_id):
    """Ownership is enforced in db.delete_comment() itself (WHERE id AND
    user_id), not just by hiding the button in the UI - the secret key
    bypasses RLS, so the backend is the only thing standing between a
    request and someone else's comment."""
    if not db.delete_comment(comment_id, session["user_id"]):
        return jsonify({"error": "not_found_or_forbidden"}), 404
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True, port=5050)
