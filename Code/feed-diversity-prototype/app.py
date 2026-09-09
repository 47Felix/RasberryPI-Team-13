"""Flask demo: standard vs. diversity-aware feed ranking side by side.

Case 3 (DTEW Hamburg 2026, digi&demo e.V.): feed/recommender design against
filter-bubble reinforcement. See ObsidianGehirn/10 DTEW Workshop/ for the
full problem statements.
"""

import os
import secrets
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
    political_bubble_trend,
    standard_feed,
    suggest_category,
)

app = Flask(__name__)
# Signs the session cookie that now holds the logged-in account's user_id -
# set FLASK_SECRET_KEY in .env for anything longer-lived than a demo, the
# fixed dev fallback lets sessions survive a restart but isn't a secret.
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-not-secret")

# Fallback topic list for when Supabase isn't configured/reachable (static
# dataset demo mode) - otherwise known_topics() below reads the live list
# from the categories table, so a category added there (e.g. via the
# Supabase SQL editor) shows up in the dropdown/dashboard/validation on the
# next request without touching this file.
DEFAULT_TOPICS = ["klima", "verkehr", "wirtschaft", "digital"]
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

# What "pro" / "contra" actually mean per topic. On its own a bare
# "pro"/"contra" ("klima: pro") says almost nothing without the post in
# front of you, so every place that shows a stance (feed chip, /dashboard,
# the per-post reason line) runs it through stance_label() for a short
# phrase instead. Framing follows the seed posts / ONBOARDING_QUESTIONS:
# "pro" = more ambition / more protection / more openness on the topic,
# "contra" = more weight on cost, feasibility, the market or the status quo.
# A topic with no entry (e.g. a category added later) just falls back to the
# bare word.
TOPIC_STANCES = {
    "klima":         {"pro": "mehr Klimaschutz, schneller",        "contra": "mehr Rücksicht auf Kosten/Bezahlbarkeit"},
    "verkehr":       {"pro": "Vorrang für Rad, ÖPNV und Schiene",   "contra": "Vorrang fürs Auto / Status quo"},
    "wirtschaft":    {"pro": "mehr Umverteilung und Schutz für Beschäftigte", "contra": "Vorrang für Betriebe und Standort"},
    "digital":       {"pro": "Grundrechte und Datenschutz zuerst",  "contra": "weniger Regeln / mehr Ermittlungsbefugnisse"},
    "bildung":       {"pro": "mehr Umverteilung, längeres gemeinsames Lernen", "contra": "mehr Leistung und Gliederung"},
    "gesundheit":    {"pro": "solidarisch, mehr staatliche Steuerung", "contra": "mehr Wettbewerb und Eigenanteil"},
    "migration":     {"pro": "offener, mehr Aufnahme und Teilhabe",  "contra": "stärker begrenzen und kontrollieren"},
    "wohnen":        {"pro": "mehr Mietregulierung und Sozialbau",   "contra": "weniger Auflagen, auf Neubau setzen"},
    "sicherheit":    {"pro": "mehr Präsenz und Befugnisse",          "contra": "Prävention und Bürgerrechte zuerst"},
    "soziales":      {"pro": "höhere, verlässlichere Leistungen",    "contra": "mehr Eigenverantwortung und Anreize"},
    "europa":        {"pro": "mehr gemeinsame EU-Zuständigkeit",     "contra": "mehr nationale Kontrolle"},
    "aussenpolitik": {"pro": "Diplomatie und zivile Mittel zuerst",  "contra": "Abschreckung und Verteidigung zuerst"},
}


def stance_label(topic: str, perspective: str) -> str:
    """Short human phrase for a (topic, perspective) pair - "mehr Klimaschutz,
    schneller" instead of just "pro". Falls back to the bare perspective for
    topics not in TOPIC_STANCES."""
    entry = TOPIC_STANCES.get(topic)
    if entry and perspective in entry:
        return entry[perspective]
    return perspective


# Templates (feed chips, /dashboard) call this directly.
app.jinja_env.globals["stance_label"] = stance_label


DEFAULT_DIVERSITY_EVERY = 3
MIN_DIVERSITY_EVERY = 2
MAX_DIVERSITY_EVERY = 6

DEFAULT_MODE = "standard"
VALID_MODES = {"standard", "diversity"}

# How many posts one feed view shows, and how many recently-shown post ids
# to keep in the session so a plain browser reload rotates on to posts the
# viewer hasn't seen yet (see index()). The cap stays well below a typical
# dataset size so there are always unseen posts to rotate to; oldest ids
# fall off first once it's full.
FEED_SIZE = 8
SEEN_HISTORY_CAP = 60
# Below this many unseen posts, skip the rotation filter and just show the
# normal top slice - otherwise a tiny dataset would starve the feed.
MIN_UNSEEN_FOR_ROTATION = 12

# Feed order == recency, like a real timeline: the top post is "just now",
# further down is "older". Purely cosmetic, no real clock involved.
TIME_LABELS = ["gerade eben", "2 Std", "4 Std", "7 Std", "10 Std", "1 Tag", "1 Tag", "2 Tage"]


def known_topics() -> list[str]:
    """Live topic list from Supabase (falls back to DEFAULT_TOPICS if
    unconfigured/unreachable/empty) - the single source every view/route
    that needs "all topics" reads from, so a category added directly in
    Supabase appears in the post form, /dashboard and validation together
    instead of only some of them."""
    return db.fetch_categories() or DEFAULT_TOPICS


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


def compute_preferences(user_id: str, liked_history: list[dict] | None = None) -> dict:
    """The full "why does this account's feed look like this" breakdown -
    shared by index() (biases/explains one account's own feed) and
    /dashboard (explains every account's feed side by side), so the two
    views can't quietly drift apart on how a preference is derived.

    Returns:
      perspective_by_topic: {topic: "pro"/"contra"}, merged from real
        engagement (likes/comments, wins per topic) and the registration
        survey (fills in topics engagement has no majority for yet).
      perspective_source: {topic: "engagement"/"onboarding"} - which of the
        two backed each entry above.
      political_label: "links"/"mitte"/"rechts"/None, same
        engagement-wins-over-onboarding rule, but account-wide rather than
        per topic (see ranking.dominant_political_label()).
      political_label_source: "engagement"/"onboarding"/None.
      liked_history: passed through (or freshly fetched) so callers that
        also need it for bubble_trend() don't fetch it twice.
    """
    if liked_history is None:
        liked_history = db.fetch_liked_history(user_id)
    commented_history = db.fetch_commented_history(user_id)
    engagement_by_topic = dominant_perspective_by_topic(liked_history + commented_history)
    engagement_political_label = dominant_political_label(
        [item["political_label"] for item in liked_history] + db.fetch_commented_political_labels(user_id)
    )

    profile = db.fetch_profile(user_id) or {}
    onboarding_by_topic = profile.get("onboarding_perspective_by_topic") or {}
    onboarding_political_label = profile.get("onboarding_political_label")

    perspective_by_topic = dict(engagement_by_topic)
    perspective_source = {topic: "engagement" for topic in engagement_by_topic}
    for topic, perspective in onboarding_by_topic.items():
        if topic not in perspective_by_topic:
            perspective_by_topic[topic] = perspective
            perspective_source[topic] = "onboarding"

    if engagement_political_label is not None:
        political_label, political_label_source = engagement_political_label, "engagement"
    elif onboarding_political_label is not None:
        political_label, political_label_source = onboarding_political_label, "onboarding"
    else:
        political_label, political_label_source = None, None

    return {
        "perspective_by_topic": perspective_by_topic,
        "perspective_source": perspective_source,
        "political_label": political_label,
        "political_label_source": political_label_source,
        "liked_history": liked_history,
    }


def _feed_item_reason(item: dict, preferred_perspective_by_topic: dict, perspective_source: dict) -> str:
    """One short, human-readable sentence for why this specific post is in
    the feed at this position - the per-post half of "was welcher User
    wieso angezeigt bekommt", the account-wide half is /dashboard."""
    post = item["post"]
    bias = preferred_perspective_by_topic.get(post.topic)
    if item.get("is_diverse_pick"):
        return f"Diversity-Pick: bewusste Gegenmeinung zu {post.topic} („{stance_label(post.topic, post.perspective)}“)"
    if bias is None:
        return f"kein Signal zu {post.topic} – nach inhaltlicher Ähnlichkeit sortiert"
    source = perspective_source.get(post.topic)
    source_label = "Fragebogen-Angabe" if source == "onboarding" else "Likes/Kommentare"
    bias_phrase = stance_label(post.topic, bias)
    if post.perspective == bias:
        return f"verstärkt deine {source_label}-basierte Neigung bei {post.topic}: „{bias_phrase}“"
    return f"widerspricht deiner {source_label}-basierten Neigung bei {post.topic}: „{bias_phrase}“"


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
    # One query covers the account's per-topic perspective lean, its
    # political-label lean and both trend views below, instead of fetching
    # the same likes/posts join multiple times per request.
    liked_history = db.fetch_liked_history(current_user["id"]) if current_user else []
    bubble_trend_data = bubble_trend([item["perspective"] for item in liked_history])
    political_bubble_trend_data = political_bubble_trend(
        [item["political_label"] for item in liked_history]
    )

    rotation_active = False
    if posts:
        post_ids = [p.id for p in posts]
        post_id_set = set(post_ids)
        # Post ids shown in recent reloads, kept in the session. A plain
        # browser reload (no ?seed_id=) then rotates the feed on to posts the
        # viewer hasn't seen yet, so "aktualisieren" brings up new content
        # instead of the identical top slice every time.
        seen_post_ids = [pid for pid in session.get("seen_post_ids", []) if pid in post_id_set]
        explicit_seed = request.args.get("seed_id")
        if explicit_seed in post_id_set:
            # An explicit ?seed_id= (tab switch, settings, "Ausgangs-Post"
            # dropdown) pins the feed - only a plain reload rotates.
            seed_id = explicit_seed
        else:
            unseen = [pid for pid in post_ids if pid not in seen_post_ids]
            if not unseen:
                # Whole catalogue has been shown once - start the rotation
                # over so reloading keeps surfacing "new" posts.
                seen_post_ids = []
                unseen = post_ids
            seed_id = unseen[0]
        seed_post = next(p for p in posts if p.id == seed_id)
        fediverse_topic = seed_post.topic
        fediverse_posts = fediverse.fetch_public_posts(fediverse_topic)

        perspective_source = {}
        if current_user:
            prefs = compute_preferences(current_user["id"], liked_history=liked_history)
            preferred_perspective_by_topic = prefs["perspective_by_topic"]
            perspective_source = prefs["perspective_source"]
            preferred_political_label = prefs["political_label"]
            onboarding_topics_used = {t for t, s in perspective_source.items() if s == "onboarding"}
            onboarding_political_label_used = prefs["political_label_source"] == "onboarding"
        bias_perspective = preferred_perspective_by_topic.get(seed_post.topic) or seed_post.perspective
        bias_political_label = preferred_political_label or seed_post.political_label

        unseen_count = sum(1 for pid in post_ids if pid not in seen_post_ids)
        # Only drop seen posts from the feed body on a plain reload, and only
        # while there's still a healthy pool of unseen ones - a pinned seed
        # (explicit ?seed_id=) keeps the body stable so the two modes stay
        # comparable.
        rotation_active = explicit_seed not in post_id_set and unseen_count >= MIN_UNSEEN_FOR_ROTATION
        exclude_ids = set(seen_post_ids) if rotation_active else None

        if mode == "diversity":
            active_feed = diversity_aware_feed(
                posts,
                seed_id,
                limit=FEED_SIZE,
                diversity_every=diversity_every,
                preferred_perspective_by_topic=preferred_perspective_by_topic,
                preferred_political_label=preferred_political_label,
                exclude_ids=exclude_ids,
            )
        else:
            active_feed = standard_feed(
                posts,
                seed_id,
                limit=FEED_SIZE,
                preferred_perspective_by_topic=preferred_perspective_by_topic,
                preferred_political_label=preferred_political_label,
                exclude_ids=exclude_ids,
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
            if current_user:
                item["reason"] = _feed_item_reason(item, preferred_perspective_by_topic, perspective_source)

        # Remember the seed plus everything just shown, so the next plain
        # reload rotates further. Cap keeps the session cookie small; oldest
        # ids drop off first.
        shown_now = [seed_id] + db_post_ids
        merged_seen = seen_post_ids + [pid for pid in shown_now if pid not in seen_post_ids]
        session["seen_post_ids"] = merged_seen[-SEEN_HISTORY_CAP:]

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
        known_topics=known_topics(),
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
        political_bubble_trend_data=political_bubble_trend_data,
        latest_post_id=posts[0].id if posts else None,
        rotation_active=rotation_active,
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


@app.route("/dashboard")
def dashboard():
    """Team-facing transparency view: every account side by side with its
    current per-topic bias and where each came from (real engagement vs.
    onboarding survey) - the account-wide half of "was welcher User wieso
    angezeigt bekommt", the per-post half is the "reason" tag on each feed
    item in index() (see _feed_item_reason()).

    Gated behind ADMIN_DASHBOARD_TOKEN (.env) instead of being open to any
    visitor: this necessarily exposes every account's derived political
    lean, which is sensitive even for demo accounts, doubly so once the
    prototype is reachable from the public internet (see deploy/README.md).
    Unset/empty token means "not configured", not "open" - the dashboard
    stays locked either way, never defaults to accessible.

    A correct ?token=... is remembered in the session, so the plain
    "Dashboard" nav link (templates/index.html, no token attached - it's
    shown to every visitor, not just admins) works on every visit after the
    first one instead of hitting "falscher Zugangs-Token" every time. Only
    downside: rotating ADMIN_DASHBOARD_TOKEN doesn't retroactively log out
    sessions that already authorized under the old value - acceptable here,
    not worth a session-versioning scheme for a demo admin view.

    Defaults to showing only the logged-in account's own row (?scope=me,
    implicit) - the all-accounts comparison is still there (?scope=all) for
    when someone actually wants the team-wide transparency view, just not
    the first thing every admin sees every time they only want their own
    feed-bias breakdown. Falls back to "all" if nobody's logged in, since
    there's no "own row" to show then.
    """
    admin_token = os.environ.get("ADMIN_DASHBOARD_TOKEN", "")
    configured = bool(admin_token)
    if configured and secrets.compare_digest(request.args.get("token", ""), admin_token):
        session["dashboard_authorized"] = True
    authorized = configured and session.get("dashboard_authorized", False)
    if not authorized:
        return render_template("dashboard.html", authorized=False, configured=configured, accounts=[])

    current_user = _current_user()
    scope = "all" if request.args.get("scope") == "all" or not current_user else "me"
    topics = known_topics()

    profiles = db.fetch_all_profiles()
    if scope == "me":
        profiles = [profile for profile in profiles if profile["id"] == current_user["id"]]

    accounts = []
    for profile in profiles:
        prefs = compute_preferences(profile["id"])
        perspective_by_topic = prefs["perspective_by_topic"]
        pro_count = sum(1 for topic in topics if perspective_by_topic.get(topic) == "pro")
        contra_count = sum(1 for topic in topics if perspective_by_topic.get(topic) == "contra")
        accounts.append(
            {
                "display_name": profile["display_name"],
                "handle": profile["handle"],
                "perspective_by_topic": perspective_by_topic,
                "perspective_source": prefs["perspective_source"],
                "political_label": prefs["political_label"],
                "political_label_source": prefs["political_label_source"],
                "pro_count": pro_count,
                "contra_count": contra_count,
                "none_count": len(topics) - pro_count - contra_count,
            }
        )
    return render_template(
        "dashboard.html",
        authorized=True,
        configured=True,
        accounts=accounts,
        known_topics=topics,
        scope=scope,
        can_show_mine=bool(current_user),
        token=admin_token,
    )


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
        and topic in known_topics()
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
