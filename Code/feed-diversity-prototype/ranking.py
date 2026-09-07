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


def _sorted_by_similarity(candidates, pred):
    return sorted((c for c in candidates if pred(c[0])), key=lambda pair: pair[1], reverse=True)


def standard_feed(posts: list[Post], seed_id: str, limit: int = 8):
    """Bubble-reinforcing ranking, like a typical 'For You' feed: same
    perspective as the seed post first, regardless of topic, before anything
    that would introduce a counter-perspective. Within each tier, still
    ordered by similarity.

    Raw cosine similarity alone isn't a reliable stand-in for "reinforces the
    bubble": on a small dataset, a counter-perspective post on the same topic
    often shares just as much vocabulary as a same-perspective one (both
    posts about "Windkraft-Ausbau" score similarly regardless of stance), so
    ranking by similarity alone let counter-perspective and unrelated-topic
    posts crowd out a feed that's supposed to look one-sided. Perspective
    match is the actual signal being demonstrated here, similarity only
    orders within it.
    """
    seed_post = next(p for p in posts if p.id == seed_id)
    candidates = _similarities_to_seed(posts, seed_id)

    same_perspective = _sorted_by_similarity(candidates, lambda p: p.perspective == seed_post.perspective)
    other_perspective = _sorted_by_similarity(candidates, lambda p: p.perspective != seed_post.perspective)
    ranked = same_perspective + other_perspective

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

    same_perspective = iter(
        _sorted_by_similarity(candidates, lambda p: p.topic == seed_post.topic and p.perspective == seed_post.perspective)
    )
    counter_perspective = iter(
        _sorted_by_similarity(candidates, lambda p: p.topic == seed_post.topic and p.perspective != seed_post.perspective)
    )
    other_topics = iter(_sorted_by_similarity(candidates, lambda p: p.topic != seed_post.topic))

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


def suggest_category(title: str, content: str, posts: list[Post]) -> str | None:
    """Suggests a topic for a not-yet-saved post by TF-IDF similarity against
    the existing posts, so the "new post" form can pre-select a category
    instead of asking users to categorize their own text from scratch. Users
    can still override the suggestion. Returns None if there's nothing to
    compare against yet.
    """
    if not posts:
        return None
    vectorizer = TfidfVectorizer()
    corpus = [f"{p.title} {p.text}" for p in posts] + [f"{title} {content}"]
    matrix = vectorizer.fit_transform(corpus)
    similarities = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
    return posts[similarities.argmax()].topic


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
