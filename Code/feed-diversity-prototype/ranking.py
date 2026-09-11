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
    # User-chosen label ('left'/'center'/'right'), independent of the topic
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


def dominant_perspective_by_topic(engagement: list[dict]) -> dict[str, str]:
    """Same idea as dominant_perspective(), but keyed per topic instead of
    collapsed into one account-wide lean. `engagement` is every liked/
    commented post for one account, each as {"topic":..., "perspective":...}
    (see db.fetch_liked_history()/fetch_commented_history()).

    A single global lean was the original design (see git history), but it
    conflated unrelated topics: an account that likes "transport pro" posts and
    "digital contra" posts isn't reliably "pro" or "contra" in general, those
    are two independent stances. Grouping by topic first, then taking the
    majority within each group the same way dominant_perspective() always
    did, lets standard_feed()/diversity_aware_feed() reinforce/counter each
    topic on its own terms. A topic with no entries or an exact tie is
    simply absent from the returned dict, same semantics as None for the
    single-topic case.
    """
    perspectives_by_topic: dict[str, list[str]] = {}
    for entry in engagement:
        topic = entry.get("topic")
        perspective = entry.get("perspective")
        if not topic or not perspective:
            continue
        perspectives_by_topic.setdefault(topic, []).append(perspective)

    result = {}
    for topic, perspectives in perspectives_by_topic.items():
        dominant = dominant_perspective(perspectives)
        if dominant:
            result[topic] = dominant
    return result


def dominant_political_label(labels: list[str]) -> str | None:
    """Same idea as dominant_perspective(), but for the independent
    'left'/'center'/'right' self-labeling from Post.political_label (see
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


def political_label_ratio(
    labels_in_order: list[str | None], recent_boost: float = 2.0, recent_window: int = 3
) -> dict[str, float]:
    """Weighted share of each political_label ('left'/'center'/'right') across
    a chronological (oldest-first) like history - lets standard_feed() mix
    the feed roughly proportionally to how one-sided an account's real
    engagement is (e.g. a 60/40 like split shows up as a roughly 60/40 feed),
    instead of dominant_political_label()'s all-or-nothing winner take-all
    (one label ahead by a single like used to flip the entire feed to that
    side - see git history/user feedback 2026-09-10).

    The most recent `recent_window` *labeled* likes count `recent_boost`
    times as much as older ones, so a recent change in taste shows up faster
    than one stale early like would otherwise allow - position in the
    filtered (labeled-only) sequence decides "recent", not raw list index,
    matching how dominant_political_label() already ignores unlabeled
    entries. Weighting is done by position, not by comparing label strings
    directly, since Python interns short string literals - comparing by
    identity would wrongly treat every occurrence of a repeated label as
    "the same" recent entry.

    Returns {} if there's no labeled entry at all (no signal yet) - callers
    should fall back to seed-post-based ranking in that case, same as when
    dominant_political_label() returns None.
    """
    labeled = [label for label in labels_in_order if label]
    if not labeled:
        return {}
    recent_cutoff = len(labeled) - recent_window
    weights: dict[str, float] = {}
    total = 0.0
    for index, label in enumerate(labeled):
        weight = recent_boost if index >= recent_cutoff else 1.0
        weights[label] = weights.get(label, 0.0) + weight
        total += weight
    return {label: weight / total for label, weight in weights.items()}


def _largest_remainder_slots(ratio: dict[str, float], total_slots: int) -> dict[str, int]:
    """Splits `total_slots` across ratio's keys proportionally to their
    share, rounded so the counts always sum to exactly `total_slots` (plain
    round() on each share independently can overshoot/undershoot by a slot
    since the rounded parts don't necessarily add back up)."""
    raw = {label: share * total_slots for label, share in ratio.items()}
    slots = {label: int(value) for label, value in raw.items()}
    remainder = total_slots - sum(slots.values())
    by_leftover_fraction = sorted(ratio, key=lambda label: raw[label] - slots[label], reverse=True)
    for label in by_leftover_fraction[:remainder]:
        slots[label] += 1
    return slots


def _interleave_by_share(buckets: dict[str, list], slots: dict[str, int]) -> list:
    """Round-robin merge of each label's bucket that spreads its `slots[label]`
    picks roughly evenly across the whole output instead of one contiguous
    block per label (all of it clustered by dict/candidate order) - purely
    cosmetic ordering within what's otherwise still a similarity-sorted,
    proportionally-sized selection per label. At each step, picks whichever
    label has used up the smallest fraction of its own allotment so far, the
    same idea as proportional fair-queueing schedulers.
    """
    result = []
    taken = {label: 0 for label in slots}
    total = sum(min(slots[label], len(buckets.get(label, []))) for label in slots)
    for _ in range(total):
        label = min(
            (l for l in slots if taken[l] < slots[l] and taken[l] < len(buckets.get(l, []))),
            key=lambda l: (taken[l] + 1) / slots[l] if slots[l] else 1.0,
        )
        result.append(buckets[label][taken[label]])
        taken[label] += 1
    return result


def standard_feed(
    posts: list[Post],
    seed_id: str,
    limit: int = 8,
    preferred_perspective_by_topic: dict[str, str] | None = None,
    preferred_political_label: str | None = None,
    preferred_political_ratio: dict[str, float] | None = None,
    exclude_ids: set[str] | None = None,
):
    """Bubble-reinforcing ranking, like a typical 'For You' feed: posts that
    match the account's own stance *for their own topic* first, before
    anything that would introduce a counter-perspective on that topic.
    Within each tier, still ordered by similarity.

    `preferred_perspective_by_topic` (from the account's own like/comment
    history, see dominant_perspective_by_topic()) maps topic -> 'pro'/
    'contra'. This is deliberately per-topic instead of one account-wide
    label: an account can be "pro" on transport and "contra" on digital at the
    same time, and a single global lean would either flatten that into one
    arbitrary side or (worse) apply e.g. the transport-pro reinforcement to
    digital posts too, which has nothing to do with what the account
    actually likes there. A topic missing from the map (no engagement yet)
    falls back to the seed post's own perspective, but only for posts that
    share the seed's topic - there is no sane fallback for an unrelated
    topic, so those are simply ranked by similarity alone, in neither the
    "matches" nor the "differs" tier.

    Raw cosine similarity alone isn't a reliable stand-in for "reinforces the
    bubble": on a small dataset, a counter-perspective post on the same topic
    often shares just as much vocabulary as a same-perspective one (both
    posts about "wind power expansion" score similarly regardless of stance), so
    ranking by similarity alone let counter-perspective and unrelated-topic
    posts crowd out a feed that's supposed to look one-sided. Perspective
    match is a real signal being demonstrated here, similarity only orders
    within it - but as of 2026-09-10 (Felix) it's the *secondary* one, see
    below.

    `preferred_political_label`/the seed post's own `political_label`
    ('left'/'center'/'right', see dominant_political_label()) is the
    primary sort axis: posts matching the account's political lean rank
    ahead of posts that merely match its pro/contra stance on the topic,
    which is now only a tiebreak within (and after) the political-label
    split. Independent axis, still account-wide (political identity isn't
    topic-specific the way a pro/contra stance is). Posts without a
    political_label (legacy rows) never count as a match, same treatment as
    diversity_score_for_political_label(). If there's no political signal at
    all (bias_political is None - no engagement, no seed label), ranking
    falls back to perspective-only, exactly as it did before this axis
    existed.

    `preferred_political_ratio` (see political_label_ratio()), when given,
    takes priority over `preferred_political_label` and replaces the
    winner-take-all split above with a proportional mix matching the
    account's actual like ratio (e.g. 60% left / 40% right in produces
    roughly that same split in the feed, not 100% left just because left
    happens to be ahead). Empty/None keeps the old single-label behavior.

    `exclude_ids` drops those post ids from the candidate pool before
    ranking - used by app.py to rotate a plain page reload on to posts the
    viewer hasn't been shown yet (see index()). None/empty keeps every post,
    so existing callers and tests are unaffected.
    """
    seed_post = next(p for p in posts if p.id == seed_id)
    preferred_perspective_by_topic = preferred_perspective_by_topic or {}
    bias_political = preferred_political_label or seed_post.political_label
    candidates = _similarities_to_seed(posts, seed_id)
    if exclude_ids:
        candidates = [c for c in candidates if c[0].id not in exclude_ids]

    def topic_bias(post: Post) -> str | None:
        by_topic = preferred_perspective_by_topic.get(post.topic)
        if by_topic:
            return by_topic
        return seed_post.perspective if post.topic == seed_post.topic else None

    def matches_perspective(post: Post) -> bool:
        bias = topic_bias(post)
        return bias is not None and post.perspective == bias

    def matches_political(post: Post) -> bool:
        return bias_political is not None and post.political_label == bias_political

    def differs_political(post: Post) -> bool:
        return (
            bias_political is not None
            and post.political_label is not None
            and post.political_label != bias_political
        )

    if preferred_political_ratio:
        # Proportional mix instead of a single winner: e.g. a 60/40 real like
        # split shows up as a roughly 60/40 feed, not a 100% one once "right"
        # merely has one more like than "left" (dominant_political_label()'s
        # all-or-nothing winner - see git history/user feedback 2026-09-10).
        buckets: dict[str, list] = {}
        for label in preferred_political_ratio:
            bucket = _sorted_by_similarity(candidates, lambda p, label=label: p.political_label == label)
            # Stable sort: within a label's bucket, a post that also matches
            # the topic's perspective bias still ranks first - same
            # secondary-axis tiebreak as the winner-take-all branch below.
            bucket.sort(key=lambda pair: matches_perspective(pair[0]), reverse=True)
            buckets[label] = bucket
        slots = _largest_remainder_slots(preferred_political_ratio, limit)
        ranked = _interleave_by_share(buckets, slots)
        used_ids = {post.id for post, _ in ranked}
        remaining = [c for c in candidates if c[0].id not in used_ids]
        # Same fallback tiers as the winner-take-all branch, restricted to
        # whatever's left after the proportional picks above (only reached
        # if a label's bucket ran dry before using up its full slot count).
        no_signal = _sorted_by_similarity(remaining, lambda p: p.political_label is None)
        other_political = _sorted_by_similarity(
            remaining, lambda p: p.political_label is not None and p.political_label not in preferred_political_ratio
        )
        ranked = ranked + no_signal + other_political
    elif bias_political:
        same_both = _sorted_by_similarity(candidates, lambda p: matches_political(p) and matches_perspective(p))
        same_political_only = _sorted_by_similarity(
            candidates, lambda p: matches_political(p) and not matches_perspective(p)
        )
        ranked = same_both + same_political_only
        # Posts with no political_label at all (legacy rows) can't match or
        # differ - rank them ahead of confirmed counter-label posts (nothing
        # here actively opposes the account's lean) but behind anything that
        # actually shares it, same "no signal" treatment topic_bias() below
        # gets when there's no political axis to compare against at all.
        no_signal = _sorted_by_similarity(candidates, lambda p: p.political_label is None)
        other_political = _sorted_by_similarity(candidates, differs_political)
        ranked = ranked + no_signal + other_political
    else:
        # No political signal to sort by at all - fall back to the old
        # perspective-only ranking (topic_bias() 3-way split).
        ranked = _sorted_by_similarity(candidates, matches_perspective)
        no_signal = _sorted_by_similarity(candidates, lambda p: topic_bias(p) is None)
        other_perspective = _sorted_by_similarity(candidates, lambda p: not matches_perspective(p) and topic_bias(p) is not None)
        ranked = ranked + no_signal + other_perspective

    return [
        {"post": post, "score": score, "is_diverse_pick": False}
        for post, score in ranked[:limit]
    ]


def diversity_aware_feed(
    posts: list[Post],
    seed_id: str,
    limit: int = 8,
    diversity_every: int = 3,
    preferred_perspective_by_topic: dict[str, str] | None = None,
    preferred_political_label: str | None = None,
    exclude_ids: set[str] | None = None,
    liked_ids: set[str] | None = None,
):
    """Same similarity base, but deliberately mixes in topically-related
    counter-perspective posts every `diversity_every`-th slot, so the feed
    stays relevant (same topic) while avoiding pure echo-chamber reinforcement.

    Every slot in this feed is already restricted to "same topic as the seed
    post" vs. "other topics" (see `same_topic()` below), so the relevant bias
    is just the seed's own topic: `preferred_perspective_by_topic` (from the
    account's own like/comment history, see dominant_perspective_by_topic())
    is looked up for `seed_post.topic` specifically, falling back to the seed
    post's own perspective if that topic has no engagement signal yet - e.g.
    if the account leans "pro" on transport, a transport-seeded diversity feed
    counters with transport "contra" posts, regardless of what the account
    thinks about digital or any other topic.

    `preferred_political_label`/the seed post's `political_label` adds a
    second, independent, still account-wide axis the same way it does in
    standard_feed() (political identity isn't topic-specific) - and as of
    2026-09-10 (Felix) it's the *primary* one, perspective is the secondary
    tiebreak, mirroring the swap in standard_feed(). When it's set,
    same-topic candidates split into four groups instead of two
    (matches/differs on perspective, crossed with matches/differs on
    political label). A diversity slot prefers a post that differs on
    *both* axes ("double counter") over one that differs on the political
    label only, over one that only differs on perspective - the strongest
    available counter-signal on the primary axis wins the slot. A post
    lacking a political_label counts as "differs" from any bias_political
    value (there's nothing to match), never as agreeing by default.

    `exclude_ids` drops those post ids before ranking, same as in
    standard_feed() - lets a plain reload rotate on to unseen posts.

    `liked_ids` only drops posts from the *reinforcing* tiers (`same_both`,
    same-topic-and-perspective-and-label; and `other_topics`, unrelated
    topics) - not from the three counter/diversity tiers below. Those only
    have a handful of candidates per topic to begin with (one topic times
    one perspective times one political label), so also hiding already-liked
    ones there used to run them dry once an account had liked most of a
    topic's counter content, silently degrading diversity slots to unmarked
    reinforcing posts instead (see user report 2026-09-11). Showing a
    counter-perspective post you've already liked again is still more useful
    here than showing none at all.
    """
    seed_post = next(p for p in posts if p.id == seed_id)
    preferred_perspective_by_topic = preferred_perspective_by_topic or {}
    bias_perspective = preferred_perspective_by_topic.get(seed_post.topic) or seed_post.perspective
    bias_political = preferred_political_label or seed_post.political_label
    candidates = _similarities_to_seed(posts, seed_id)
    if exclude_ids:
        candidates = [c for c in candidates if c[0].id not in exclude_ids]
    reinforcing_candidates = candidates
    if liked_ids:
        reinforcing_candidates = [c for c in candidates if c[0].id not in liked_ids]

    def same_topic(p):
        return p.topic == seed_post.topic

    def matches_political(p):
        return bias_political is not None and p.political_label == bias_political

    if bias_political:
        same_both = iter(
            _sorted_by_similarity(reinforcing_candidates, lambda p: same_topic(p) and p.perspective == bias_perspective and matches_political(p))
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
        same_both = iter(_sorted_by_similarity(reinforcing_candidates, lambda p: same_topic(p) and p.perspective == bias_perspective))
        same_persp_diff_pol = iter([])
        diff_persp_same_pol = iter(_sorted_by_similarity(candidates, lambda p: same_topic(p) and p.perspective != bias_perspective))
        double_counter = iter([])

    other_topics = iter(_sorted_by_similarity(reinforcing_candidates, lambda p: not same_topic(p)))

    feed = []
    while len(feed) < limit:
        is_diversity_slot = (len(feed) + 1) % diversity_every == 0
        picked = None
        if is_diversity_slot:
            # Primary axis (political label) differing wins the slot before
            # a post that only differs on the secondary axis (perspective).
            picked = next(double_counter, None) or next(same_persp_diff_pol, None) or next(diff_persp_same_pol, None)

        if picked is None:
            # Same ordering principle for the non-diversity fallback: a
            # primary-axis (political) match outranks a secondary-axis
            # (perspective) match when both are on offer.
            picked = (
                next(same_both, None)
                or next(other_topics, None)
                or next(diff_persp_same_pol, None)
                or next(same_persp_diff_pol, None)
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


def political_bubble_trend(liked_political_labels_in_order: list[str | None]) -> list[dict]:
    """Same idea as bubble_trend(), for the independent political_label axis
    (see NIGHTLY_TASK.md - the perspective-only trend view left this second
    dimension from PR #113 without a trend of its own).

    Three possible labels ('left'/'center'/'right') instead of two, so this
    can't reuse bubble_trend()'s pro/contra counters directly - tracks a
    count per label seen so far and takes whichever is highest at each
    point, same "share of likes-so-far matching the current majority"
    definition. A tie for the top spot (all counts equal, e.g. after the
    very first like, or 1/1 left-vs-right) shows as `dominant_count /
    index` using whichever tied label is counted first - functionally the
    same "not yet dominant" signal as bubble_trend()'s explicit 50/50
    tie-break, just without special-casing exactly two options.

    `liked_political_labels_in_order` is the political_label of every liked
    post, oldest first - entries with no label (liked before this field
    existed, or the author left it unset) are skipped entirely rather than
    counted as a fourth "no label" bucket, matching how
    dominant_political_label() already ignores them. The `index` in each
    returned point therefore counts labeled likes only, not every like.
    """
    trend = []
    counts: dict[str, int] = {}
    index = 0
    for label in liked_political_labels_in_order:
        if not label:
            continue
        counts[label] = counts.get(label, 0) + 1
        index += 1
        dominant_count = max(counts.values())
        share = 100 * dominant_count / index
        trend.append({"index": index, "political_label": label, "dominant_share": round(share, 1)})
    return trend
