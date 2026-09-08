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
    # User-chosen label ('links'/'mitte'/'rechts'), independent of the topic
    # pro/contra perspective above. None for posts created before this field
    # existed, or if the author didn't pick one - see dominant_political_label().
    political_label: str | None = None


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


def dominant_political_label(labels: list[str]) -> str | None:
    """Same idea as dominant_perspective(), but for the independent
    'links'/'mitte'/'rechts' self-labeling from Post.political_label (see
    README for why this is a user-chosen label, not an automatically
    detected one). Three options instead of two, so a majority can fail to
    exist in more ways than a plain tie: None whenever there's no signal
    (no liked posts with a label yet) or the top count is shared by more
    than one label.
    """
    labels = [label for label in labels if label]
    if not labels:
        return None
    counts: dict[str, int] = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    top_count = max(counts.values())
    leaders = [label for label, count in counts.items() if count == top_count]
    return leaders[0] if len(leaders) == 1 else None


def standard_feed(
    posts: list[Post],
    seed_id: str,
    limit: int = 8,
    preferred_perspective: str | None = None,
    preferred_political_label: str | None = None,
):
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

    `preferred_political_label`/the seed post's own `political_label`
    ('links'/'mitte'/'rechts', see dominant_political_label()) works as a
    second, independent axis on top of perspective: within the "same
    perspective" tier, posts that also match on political label are ranked
    ahead of ones that only match on perspective, so a feed that reinforces
    both a topical stance and a political lean looks even more one-sided
    than either signal alone. Posts without a political_label (legacy rows,
    or bias_political being None because there's no signal yet) simply skip
    this extra split and behave exactly as before.
    """
    seed_post = next(p for p in posts if p.id == seed_id)
    bias_perspective = preferred_perspective or seed_post.perspective
    bias_political = preferred_political_label or seed_post.political_label
    candidates = _similarities_to_seed(posts, seed_id)

    if bias_political:
        same_both = _sorted_by_similarity(
            candidates, lambda p: p.perspective == bias_perspective and p.political_label == bias_political
        )
        same_perspective_only = _sorted_by_similarity(
            candidates, lambda p: p.perspective == bias_perspective and p.political_label != bias_political
        )
        ranked = same_both + same_perspective_only
    else:
        ranked = _sorted_by_similarity(candidates, lambda p: p.perspective == bias_perspective)

    other_perspective = _sorted_by_similarity(candidates, lambda p: p.perspective != bias_perspective)
    ranked = ranked + other_perspective

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
    preferred_political_label: str | None = None,
):
    """Same similarity base, but deliberately mixes in topically-related
    counter-perspective posts every `diversity_every`-th slot, so the feed
    stays relevant (same topic) while avoiding pure echo-chamber reinforcement.

    Uses the same `preferred_perspective` (account like history) as
    standard_feed() to decide which side counts as "home" vs. "counter" -
    so this interrupts the account's actual reinforced lean, not just the
    current seed post's perspective.

    `preferred_political_label`/the seed post's `political_label` adds a
    second, independent axis the same way it does in standard_feed(). When
    it's set, same-topic candidates split into four groups instead of two
    (matches/differs on perspective, crossed with matches/differs on
    political label). A diversity slot prefers a post that differs on
    *both* axes ("double counter") over one that only differs on
    perspective, over one that only differs on the political label - the
    strongest available counter-signal wins the slot. A post lacking a
    political_label counts as "differs" from any bias_political value
    (there's nothing to match), never as agreeing by default.
    """
    seed_post = next(p for p in posts if p.id == seed_id)
    bias_perspective = preferred_perspective or seed_post.perspective
    bias_political = preferred_political_label or seed_post.political_label
    candidates = _similarities_to_seed(posts, seed_id)

    def same_topic(p):
        return p.topic == seed_post.topic

    def matches_political(p):
        return bias_political is not None and p.political_label == bias_political

    if bias_political:
        same_both = iter(
            _sorted_by_similarity(candidates, lambda p: same_topic(p) and p.perspective == bias_perspective and matches_political(p))
        )
        same_persp_diff_pol = iter(
            _sorted_by_similarity(candidates, lambda p: same_topic(p) and p.perspective == bias_perspective and not matches_political(p))
        )
        diff_persp_same_pol = iter(
            _sorted_by_similarity(candidates, lambda p: same_topic(p) and p.perspective != bias_perspective and matches_political(p))
        )
        double_counter = iter(
            _sorted_by_similarity(candidates, lambda p: same_topic(p) and p.perspective != bias_perspective and not matches_political(p))
        )
    else:
        same_both = iter(_sorted_by_similarity(candidates, lambda p: same_topic(p) and p.perspective == bias_perspective))
        same_persp_diff_pol = iter([])
        diff_persp_same_pol = iter(_sorted_by_similarity(candidates, lambda p: same_topic(p) and p.perspective != bias_perspective))
        double_counter = iter([])

    other_topics = iter(_sorted_by_similarity(candidates, lambda p: not same_topic(p)))

    feed = []
    while len(feed) < limit:
        is_diversity_slot = (len(feed) + 1) % diversity_every == 0
        picked = None
        if is_diversity_slot:
            picked = next(double_counter, None) or next(diff_persp_same_pol, None) or next(same_persp_diff_pol, None)

        if picked is None:
            picked = (
                next(same_both, None)
                or next(other_topics, None)
                or next(same_persp_diff_pol, None)
                or next(diff_persp_same_pol, None)
                or next(double_counter, None)
            )

        if picked is None:
            break

        post, score = picked
        is_diverse_pick = same_topic(post) and (post.perspective != bias_perspective or (bias_political is not None and not matches_political(post)))
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


def diversity_score_for_political_label(feed: list[dict], political_label: str | None) -> float:
    """Same idea as diversity_score_for_perspective(), for the independent
    political_label axis. A post without a label counts as differing (there
    is nothing to match), same as the "differs" treatment used throughout
    diversity_aware_feed(). Returns 0.0 if there's no political_label signal
    to measure against (political_label is None) so callers can skip
    displaying this score rather than showing a misleading 100%.
    """
    if not feed or political_label is None:
        return 0.0
    differing = sum(1 for item in feed if item["post"].political_label != political_label)
    return round(100 * differing / len(feed), 1)


def bubble_trend(liked_perspectives_in_order: list[str]) -> list[dict]:
    """Tracks how one-sided an account's own like history has become over
    time - critical point 6 in DTEW 0209 (measuring perspective diversity)
    asked for this to be visible across a session, not just as a single
    per-feed-view score.

    `liked_perspectives_in_order` is the perspective of every post the
    account has liked, oldest first. For each like (1-indexed), returns the
    share (0-100) of likes-so-far that match whichever perspective is
    dominant *at that point* - so the sequence shows the bubble either
    tightening (share climbing toward 100) or loosening (share drifting back
    toward 50) as more likes come in. A tie at any point counts as 50/50,
    matching dominant_perspective()'s own tie-breaking.
    """
    trend = []
    pro_count = 0
    contra_count = 0
    for index, perspective in enumerate(liked_perspectives_in_order, start=1):
        if perspective == "pro":
            pro_count += 1
        elif perspective == "contra":
            contra_count += 1
        dominant_count = max(pro_count, contra_count)
        share = 100 * dominant_count / index
        trend.append({"index": index, "perspective": perspective, "dominant_share": round(share, 1)})
    return trend
