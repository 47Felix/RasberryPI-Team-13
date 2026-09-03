"""Flask demo: standard vs. diversity-aware feed ranking side by side.

Case 3 (DTEW Hamburg 2026, digi&demo e.V.): feed/recommender design against
filter-bubble reinforcement. See ObsidianGehirn/10 DTEW Workshop/ for the
full problem statements (PS1 for persona "Mia", PS2 for persona "Tom").
"""

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

    standard = standard_feed(posts, seed_id)
    diverse = diversity_aware_feed(posts, seed_id, diversity_every=diversity_every)

    return render_template(
        "index.html",
        posts=posts,
        seed_id=seed_id,
        persona=persona,
        mix=diversity_every,
        standard_feed=standard,
        diverse_feed=diverse,
        standard_score=diversity_score(standard, seed_post),
        diverse_score=diversity_score(diverse, seed_post),
    )


if __name__ == "__main__":
    app.run(debug=True, port=5050)
