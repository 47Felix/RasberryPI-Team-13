"""Flask demo: standard vs. diversity-aware feed ranking side by side.

Case 3 (DTEW Hamburg 2026, digi&demo e.V.): feed/recommender design against
filter-bubble reinforcement. See ObsidianGehirn/10 DTEW Workshop/ for the
full problem statements (PS1 for persona "Mia", PS2 for persona "Tom").
"""

import hashlib
import json
from pathlib import Path

from flask import Flask, render_template, request

from ranking import Post, diversity_aware_feed, diversity_score, standard_feed

app = Flask(__name__)

DATA_PATH = Path(__file__).parent / "data" / "posts.json"

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
    """Deterministic, stable-looking like/reply/repost counts per post so the
    feed doesn't look like an empty developer fixture. Not randomized per
    request (hashlib, not random) so the numbers don't jump on every reload.
    """
    digest = int(hashlib.sha256(post_id.encode()).hexdigest(), 16)
    return {
        "likes": 20 + digest % 260,
        "comments": 2 + (digest // 260) % 45,
        "reposts": 1 + (digest // 11_700) % 20,
    }


def _decorate_feed(feed: list[dict]) -> list[dict]:
    decorated = []
    for index, item in enumerate(feed):
        post = item["post"]
        meta = AUTHOR_META.get((post.topic, post.perspective), DEFAULT_AUTHOR_META)
        decorated.append(
            {
                **item,
                "avatar": meta["avatar"],
                "author": meta["name"],
                "handle": meta["handle"],
                "time_label": TIME_LABELS[min(index, len(TIME_LABELS) - 1)],
                **_fake_engagement(post.id),
            }
        )
    return decorated


def load_posts() -> list[Post]:
    with open(DATA_PATH, encoding="utf-8") as f:
        raw = json.load(f)
    return [Post(**item) for item in raw]


def _parse_diversity_every(raw: str | None) -> int:
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return DEFAULT_DIVERSITY_EVERY
    return max(MIN_DIVERSITY_EVERY, min(value, MAX_DIVERSITY_EVERY))


@app.route("/")
def index():
    posts = load_posts()

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

    return render_template(
        "index.html",
        posts=posts,
        seed_id=seed_id,
        persona=persona,
        mix=diversity_every,
        mode=mode,
        feed_items=_decorate_feed(active_feed),
        feed_score=diversity_score(active_feed, seed_post),
    )


if __name__ == "__main__":
    app.run(debug=True, port=5050)
