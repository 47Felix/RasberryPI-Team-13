"""Two feed ranking modes for the Case-3 filter-bubble prototype.

Both modes reuse the same TF-IDF + cosine-similarity content-based approach
(scikit-learn) instead of a self-trained model, per the team's feasibility
decision (see ObsidianGehirn/10 DTEW Workshop/Team 13 - Digitale Demokratie.md).
"""

from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Post:
    id: str
    title: str
    text: str
    topic: str
    perspective: str


def _similarities_to_seed(posts: list[Post], seed_id: str):
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(f"{p.title} {p.text}" for p in posts)
    ids = [p.id for p in posts]
    seed_idx = ids.index(seed_id)
    sims = cosine_similarity(matrix[seed_idx], matrix).flatten()
    return [(posts[i], sims[i]) for i in range(len(posts)) if posts[i].id != seed_id]


def standard_feed(posts: list[Post], seed_id: str, limit: int = 8):
    """Pure-similarity ranking: bubble-reinforcing, like a typical 'For You' feed."""
    candidates = _similarities_to_seed(posts, seed_id)
    ranked = sorted(candidates, key=lambda pair: pair[1], reverse=True)
    return [
        {"post": post, "score": score, "is_diverse_pick": False}
        for post, score in ranked[:limit]
    ]


def diversity_aware_feed(
    posts: list[Post], seed_id: str, limit: int = 8, diversity_every: int = 3
):
    """Same similarity base, but deliberately mixes in topically-related
    counter-perspective posts every `diversity_every`-th slot, so the feed
    stays relevant (same topic) while avoiding pure echo-chamber reinforcement.
    """
    seed_post = next(p for p in posts if p.id == seed_id)
    candidates = _similarities_to_seed(posts, seed_id)

    def _sorted(pred):
        return sorted((c for c in candidates if pred(c[0])), key=lambda pair: pair[1], reverse=True)

    same_perspective = iter(
        _sorted(lambda p: p.topic == seed_post.topic and p.perspective == seed_post.perspective)
    )
    counter_perspective = iter(
        _sorted(lambda p: p.topic == seed_post.topic and p.perspective != seed_post.perspective)
    )
    other_topics = iter(_sorted(lambda p: p.topic != seed_post.topic))

    feed = []
    while len(feed) < limit:
        is_diversity_slot = (len(feed) + 1) % diversity_every == 0
        picked = next(counter_perspective, None) if is_diversity_slot else None

        if picked is None:
            picked = next(same_perspective, None) or next(other_topics, None) or next(counter_perspective, None)

        if picked is None:
            break

        post, score = picked
        is_diverse_pick = post.topic == seed_post.topic and post.perspective != seed_post.perspective
        feed.append({"post": post, "score": score, "is_diverse_pick": is_diverse_pick})

    return feed


def diversity_score(feed: list[dict], seed_post: Post) -> float:
    """Share (0-100) of shown posts whose perspective differs from the seed
    post's perspective. A crude but visible stand-in for the "how do we
    measure perspective diversity" gap called out as critical point 6 in
    DTEW 0209 - Kritische Punkte, Problem Statements und Ideation.md.
    """
    if not feed:
        return 0.0
    differing = sum(1 for item in feed if item["post"].perspective != seed_post.perspective)
    return round(100 * differing / len(feed), 1)
