"""Flask demo: standard vs. diversity-aware feed ranking side by side.

Case 3 (DTEW Hamburg 2026, digi&demo e.V.): feed/recommender design against
filter-bubble reinforcement. See ObsidianGehirn/10 DTEW Workshop/ for the
full problem statements (PS1 for persona "Mia", PS2 for persona "Tom").
"""

import json
from pathlib import Path

from flask import Flask, render_template, request

from ranking import Post, diversity_aware_feed, standard_feed

app = Flask(__name__)

DATA_PATH = Path(__file__).parent / "data" / "posts.json"

# Quick persona presets so the demo directly maps back to Mia/Tom instead of
# requiring visitors to guess a meaningful seed post from the dropdown.
PERSONA_SEEDS = {
    "mia": "klima-1",  # Mia: only ever sees "pro" climate posts, doesn't notice the bubble
    "tom": "wirtschaft-3",  # Tom: stuck in "contra" economy posts, wants out
}


def load_posts() -> list[Post]:
    with open(DATA_PATH, encoding="utf-8") as f:
        raw = json.load(f)
    return [Post(**item) for item in raw]


@app.route("/")
def index():
    posts = load_posts()

    persona = request.args.get("persona")
    seed_id = PERSONA_SEEDS.get(persona, request.args.get("seed_id", posts[0].id))
    if seed_id not in {p.id for p in posts}:
        seed_id = posts[0].id

    return render_template(
        "index.html",
        posts=posts,
        seed_id=seed_id,
        persona=persona,
        standard_feed=standard_feed(posts, seed_id),
        diverse_feed=diversity_aware_feed(posts, seed_id),
    )


if __name__ == "__main__":
    app.run(debug=True, port=5050)
