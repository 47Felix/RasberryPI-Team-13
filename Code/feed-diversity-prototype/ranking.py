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


def dominant_perspective(perspectives: list[str]) -> str | None:
    """Returns whichever perspective ('pro'/'contra') occurs more often in
    the given list - meant to be every liked post's perspective for one
    account, so the feed can learn "this account leans contra" the same way
    a real engagement-based recommender would. None if there's no signal yet
    (no likes) or it's an exact tie, in which case standard_feed()/
    diversity_aware_feed() fall back to the seed post's own perspective.
    """
    if not perspectives:
        return None
    pro = perspectives.count("pro")
    contra = perspectives.count("contra")
    if pro == contra:
        return None
    return "pro" if pro > contra else "contra"


def standard_feed(posts: list[Post], seed_id: str, limit: int = 8, preferred_perspective: str | None = None):
    """Bubble-reinforcing ranking, like a typical 'For You' feed: one
    perspective first, regardless of topic, before anything that would
    introduce a counter-perspective. Within each tier, still ordered by
    similarity.

    Which perspective that is comes from `preferred_perspective` (the
    account's own like history, see dominant_perspective()) when given,
    otherwise from the seed post - so once an account has liked enough
    posts one way, the feed reinforces *that* lean on every seed post, not
    just whichever one happens to be selected. This is what makes the
    reinforcement self-sustaining instead of a one-off per seed post.

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
    bias_perspective = preferred_perspective or seed_post.perspective
    candidates = _similarities_to_seed(posts, seed_id)

    same_perspective = _sorted_by_similarity(candidates, lambda p: p.perspective == bias_perspective)
    other_perspective = _sorted_by_similarity(candidates, lambda p: p.perspective != bias_perspective)
    ranked = same_perspective + other_perspective

    return [
        {"post": post, "score": score, "is_diverse_pick": False}
        for post, score in ranked[:limit]
    ]


def diversity_aware_feed(
    posts: list[Post],
    seed_id: str,
    limit: int = 8,
    diversity_every: int = 3,
    preferred_perspective: str | None = None,
):
    """Same similarity base, but deliberately mixes in topically-related
    counter-perspective posts every `diversity_every`-th slot, so the feed
    stays relevant (same topic) while avoiding pure echo-chamber reinforcement.

    Uses the same `preferred_perspective` (account like history) as
    standard_feed() to decide which side counts as "home" vs. "counter" -
    so this interrupts the account's actual reinforced lean, not just the
    current seed post's perspective.
    """
    seed_post = next(p for p in posts if p.id == seed_id)
    bias_perspective = preferred_perspective or seed_post.perspective
    candidates = _similarities_to_seed(posts, seed_id)

    same_perspective = iter(
        _sorted_by_similarity(candidates, lambda p: p.topic == seed_post.topic and p.perspective == bias_perspective)
    )
    counter_perspective = iter(
        _sorted_by_similarity(candidates, lambda p: p.topic == seed_post.topic and p.perspective != bias_perspective)
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
        is_diverse_pick = post.topic == seed_post.topic and post.perspective != bias_perspective
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


def diversity_score_for_perspective(feed: list[dict], perspective: str) -> float:
    """Share (0-100) of shown posts whose perspective differs from
    `perspective`. A crude but visible stand-in for the "how do we measure
    perspective diversity" gap called out as critical point 6 in DTEW 0209 -
    Kritische Punkte, Problem Statements und Ideation.md.
    """
    if not feed:
        return 0.0
    differing = sum(1 for item in feed if item["post"].perspective != perspective)
    return round(100 * differing / len(feed), 1)


def diversity_score(feed: list[dict], seed_post: Post) -> float:
    """Same as diversity_score_for_perspective(), measured against the seed
    post's own perspective - kept as a convenience wrapper for callers that
    don't track an account-level bias_perspective (see standard_feed())."""
    return diversity_score_for_perspective(feed, seed_post.perspective)
