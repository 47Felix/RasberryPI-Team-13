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
    bubble_trend,
    diversity_aware_feed,
    diversity_score_for_perspective,
    diversity_score_for_political_label,
    dominant_perspective_by_topic,
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

# Optional registration-time survey (see 0004_onboarding_survey.sql/
# 0005_onboarding_per_topic.sql): one pro/contra statement pair per known
# topic, phrased to match the framing already used by the seed posts for
# that topic (see supabase/migrations/0001_init.sql seed data) so a
# skippable self-placement here feels like the same kind of choice as
# picking a post's own perspective, not a separate vocabulary. Each answered
# topic gives the feed an initial per-topic lean before any likes/comments
# on that topic exist - unanswered topics are simply left out of the map.
ONBOARDING_QUESTIONS = [
    {
        "topic": "klima",
        "pro": "CO2-Bepreisung sollte deutlich steigen, auch wenn das kurzfristig teurer wird.",
        "contra": "Klimaauflagen sollten nicht zu stark auf Kosten der Bezahlbarkeit gehen.",
    },
    {
        "topic": "verkehr",
        "pro": "Rad/ÖPNV sollten beim Ausbau Vorrang vor dem Auto bekommen.",
        "contra": "Der Autoverkehr bleibt für viele unverzichtbar und sollte nicht ausgebremst werden.",
    },
    {
        "topic": "wirtschaft",
        "pro": "Höhere Mindestlöhne/kürzere Arbeitszeiten sind mir wichtiger als Kostendruck auf Betriebe.",
        "contra": "Der Kostendruck auf Betriebe sollte stärker gewichtet werden als höhere Lohnnebenkosten.",
    },
    {
        "topic": "digital",
        "pro": "Digitalisierung von Behörden/Open-Source sollte Vorrang vor Datenschutzbedenken bekommen.",
        "contra": "Datenschutzbedenken sollten Vorrang vor schnellerer Digitalisierung bekommen.",
    },
]

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
    preferred_perspective_by_topic = {}
    preferred_political_label = None
    show_political_score = False
    fediverse_posts = []
    fediverse_topic = None
    onboarding_topics_used = set()
    onboarding_political_label_used = False
    # One query covers both the account's per-topic lean
    # (dominant_perspective_by_topic doesn't care about order) and the
    # like-history trend below, instead of fetching the same likes/posts
    # join twice per request.
    liked_history = db.fetch_liked_history(current_user["id"]) if current_user else []
    bubble_trend_data = bubble_trend([item["perspective"] for item in liked_history])

    if posts:
        seed_id = request.args.get("seed_id")
        if seed_id not in {p.id for p in posts}:
            seed_id = posts[0].id
        seed_post = next(p for p in posts if p.id == seed_id)
        fediverse_topic = seed_post.topic
        fediverse_posts = fediverse.fetch_public_posts(fediverse_topic)

        if current_user:
            # Comments count as an engagement signal alongside likes - someone
            # who mostly comments on "pro" posts on a topic leans "pro" on
            # that topic the same way a liker would, even without hitting
            # the like button.
            commented_history = db.fetch_commented_history(current_user["id"])
            commented_labels = db.fetch_commented_political_labels(current_user["id"])
            preferred_perspective_by_topic = dominant_perspective_by_topic(liked_history + commented_history)
            preferred_political_label = dominant_political_label(
                db.fetch_liked_political_labels(current_user["id"]) + commented_labels
            )
            # Fill in topics with no engagement majority yet (or none at all)
            # from the account's own registration-survey answer for that
            # topic, if it gave one - instead of leaving those topics with
            # zero signal until the first like/comment on them. Real
            # engagement above always wins per topic once it exists.
            profile = db.fetch_profile(current_user["id"]) or {}
            onboarding_perspective_by_topic = profile.get("onboarding_perspective_by_topic") or {}
            for topic, perspective in onboarding_perspective_by_topic.items():
                if topic not in preferred_perspective_by_topic:
                    preferred_perspective_by_topic[topic] = perspective
                    onboarding_topics_used.add(topic)
            if preferred_political_label is None:
                preferred_political_label = profile.get("onboarding_political_label")
                onboarding_political_label_used = preferred_political_label is not None
        bias_perspective = preferred_perspective_by_topic.get(seed_post.topic) or seed_post.perspective
        bias_political_label = preferred_political_label or seed_post.political_label

        if mode == "diversity":
            active_feed = diversity_aware_feed(
                posts,
                seed_id,
                diversity_every=diversity_every,
                preferred_perspective_by_topic=preferred_perspective_by_topic,
                preferred_political_label=preferred_political_label,
            )
        else:
            active_feed = standard_feed(
                posts,
                seed_id,
                preferred_perspective_by_topic=preferred_perspective_by_topic,
                preferred_political_label=preferred_political_label,
            )

        feed_items = _decorate_feed(active_feed, extra_meta)
        feed_score = diversity_score_for_perspective(active_feed, bias_perspective)
        political_feed_score = diversity_score_for_political_label(active_feed, bias_political_label)
        # Only surfaced when the account has a genuine political-label
        # signal (real engagement or an onboarding answer) - falling back
        # silently to bias_political_label (which can just be the currently
        # viewed seed post's own label) would present that incidental value
        # as "your" lean, e.g. always showing "rechts" while tied 50/50.
        show_political_score = preferred_political_label is not None

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
        preferred_perspective_by_topic=preferred_perspective_by_topic,
        preferred_political_label=preferred_political_label,
        onboarding_topics_used=onboarding_topics_used,
        onboarding_political_label_used=onboarding_political_label_used,
        bubble_trend_data=bubble_trend_data,
        latest_post_id=posts[0].id if posts else None,
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
                # Survey is entirely optional - unanswered questions for a
                # topic just leave that topic out of the map, same as
                # skipping the whole thing outright.
                onboarding_perspective_by_topic = {}
                for question in ONBOARDING_QUESTIONS:
                    answer = request.form.get(f"onboarding_q_{question['topic']}")
                    if answer in KNOWN_PERSPECTIVES:
                        onboarding_perspective_by_topic[question["topic"]] = answer
                onboarding_political_label = request.form.get("onboarding_political_label")
                if onboarding_political_label not in KNOWN_POLITICAL_LABELS:
                    onboarding_political_label = None

                handle = db.create_unique_profile(
                    user["id"],
                    display_name,
                    onboarding_perspective_by_topic=onboarding_perspective_by_topic,
                    onboarding_political_label=onboarding_political_label,
                )
                session["user_id"] = user["id"]
                session["display_name"] = display_name
                session["handle"] = handle
                return redirect(request.args.get("next") or url_for("index"))
    return render_template(
        "register.html",
        error=error,
        auth_configured=db.auth_configured(),
        onboarding_questions=ONBOARDING_QUESTIONS,
        known_political_labels=KNOWN_POLITICAL_LABELS,
    )


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


@app.route("/posts/latest-id")
def latest_post_id():
    """Polled from the frontend (see templates/index.html) to detect posts
    created by someone else since the page was loaded, without re-running
    the full ranked-feed query every ~15s."""
    return jsonify({"id": db.fetch_latest_post_id()})


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
