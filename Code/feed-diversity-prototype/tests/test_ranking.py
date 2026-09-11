import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ranking import (
    Post,
    bubble_trend,
    diversity_aware_feed,
    diversity_score,
    diversity_score_for_political_label,
    dominant_perspective,
    dominant_political_label,
    political_bubble_trend,
    political_label_ratio,
    standard_feed,
    suggest_category,
)

POSTS = [
    Post(
        "seed",
        "Wind Power Expansion",
        "Wind power and the energy transition are central to climate "
        "protection. Wind power expansion needs to be sped up.",
        "climate",
        "pro",
    ),
    Post(
        "same-perspective",
        "Advance the Energy Transition",
        "Expanding the energy transition, wind power included, is crucial "
        "to reaching our climate targets.",
        "climate",
        "pro",
    ),
    Post(
        "counter-perspective",
        "Cost of the Expansion",
        "Wind turbines change the landscape and the cost of expansion "
        "is too high.",
        "climate",
        "contra",
    ),
    Post(
        "unrelated",
        "Weekend Weather",
        "The weather this weekend will be sunny and mild.",
        "other",
        "neutral",
    ),
]


def test_standard_feed_excludes_the_seed_post():
    feed = standard_feed(POSTS, seed_id="seed")
    assert all(item["post"].id != "seed" for item in feed)


def test_standard_feed_reinforces_the_bubble():
    feed = standard_feed(POSTS, seed_id="seed")
    assert feed[0]["post"].perspective == "pro"
    assert all(item["is_diverse_pick"] is False for item in feed)


def test_standard_feed_exclude_ids_drops_seen_posts():
    # app.py passes exclude_ids so a plain page reload rotates the feed on to
    # posts the viewer hasn't been shown yet.
    feed = standard_feed(POSTS, seed_id="seed", exclude_ids={"same-perspective"})
    assert all(item["post"].id != "same-perspective" for item in feed)
    assert {"counter-perspective", "unrelated"} & {item["post"].id for item in feed}


def test_exclude_ids_none_changes_nothing():
    assert [i["post"].id for i in standard_feed(POSTS, seed_id="seed")] == [
        i["post"].id for i in standard_feed(POSTS, seed_id="seed", exclude_ids=None)
    ]


def test_diversity_aware_feed_exclude_ids_drops_seen_posts():
    feed = diversity_aware_feed(POSTS, seed_id="seed", limit=3, exclude_ids={"counter-perspective"})
    assert all(item["post"].id != "counter-perspective" for item in feed)


def test_diversity_aware_feed_ignores_liked_ids_for_the_diversity_slot():
    # The only counter-perspective post in POSTS is already liked. Unlike
    # exclude_ids, liked_ids must not remove it from the diversity-marked
    # tiers - there's only ever a handful of counter candidates per topic,
    # so hiding liked ones there would silently turn diversity slots into
    # unmarked reinforcing posts once an account had liked most of them
    # (reported live 2026-09-11).
    feed = diversity_aware_feed(
        POSTS, seed_id="seed", limit=3, diversity_every=1, liked_ids={"counter-perspective"}
    )
    diverse_items = [item for item in feed if item["is_diverse_pick"]]
    assert diverse_items
    assert any(item["post"].id == "counter-perspective" for item in diverse_items)


def test_diversity_aware_feed_liked_ids_still_drops_reinforcing_posts():
    feed = diversity_aware_feed(
        POSTS, seed_id="seed", limit=3, diversity_every=99, liked_ids={"same-perspective"}
    )
    assert all(item["post"].id != "same-perspective" for item in feed)


def test_diversity_aware_feed_rotates_diversity_slots_across_topics():
    # An account with a known bias on three separate topics used to get all
    # of its diversity slots spent countering the seed's own single topic
    # every time - reported live 2026-09-11 ("alle 3 diversity posts waren
    # zur gleichen Kategorie"). With diversity_every=1 every slot is a
    # diversity slot, so the three diverse picks below must land on three
    # different topics, not just repeat "climate" (the seed's topic) three
    # times.
    posts = [
        Post("seed", "Wind Power Expansion", "Wind power energy transition climate protection expansion", "climate", "pro"),
        Post("climate-contra", "Cost of the Expansion", "Wind power cost of the climate expansion is too high", "climate", "contra"),
        Post("economy-contra", "Minimum Wage Concerns", "Raising the minimum wage risks economy jobs", "economy", "contra"),
        Post("transport-contra", "Car-Free City Doubts", "A car-free city center hurts transport access", "transport", "contra"),
    ]
    feed = diversity_aware_feed(
        posts,
        seed_id="seed",
        limit=3,
        diversity_every=1,
        preferred_perspective_by_topic={"climate": "pro", "economy": "pro", "transport": "pro"},
    )
    diverse_topics = [item["post"].topic for item in feed if item["is_diverse_pick"]]
    assert set(diverse_topics) == {"climate", "economy", "transport"}


def test_standard_feed_stays_within_seed_perspective_even_when_the_topic_runs_out():
    # Only one other same-topic/same-perspective post exists, so a naive
    # global similarity ranking would have to pad the rest of the feed with
    # whatever scores next-highest - which, on a small dataset, is often a
    # same-topic counter-perspective post rather than an unrelated topic
    # (shared topic vocabulary outweighs perspective). That defeats the
    # entire premise of a "bubble-reinforcing" feed, so perspective match
    # must win over raw similarity.
    posts = [
        Post("seed", "Wind Power Expansion", "Wind power energy transition climate protection expansion", "climate", "pro"),
        Post("pro-1", "Solar Expansion", "Wind power energy transition climate protection solar expansion", "climate", "pro"),
        Post("contra-1", "Cost of the Expansion", "Wind power energy transition climate protection cost expansion", "climate", "contra"),
        Post("other-pro-1", "Raise the Minimum Wage", "Minimum wage supports purchasing power", "economy", "pro"),
        Post("other-pro-2", "Four-Day Week", "Four day week productivity", "economy", "pro"),
    ]
    feed = standard_feed(posts, seed_id="seed", limit=3)
    assert all(item["post"].perspective == "pro" for item in feed)


def test_similarity_ranking_prefers_genuine_topic_match_over_a_shared_incidental_word():
    # Regression test for a real quality bug found on the ~250-post seed
    # dataset (2026-09-10, Felix's algorithm-review brief): a plain,
    # unweighted TF-IDF vectorizer let an unrelated post that merely shares
    # one word with the seed's title ("speed") outrank a post genuinely
    # about the same subject, because a short post's few body words gave
    # the title's on-topic vocabulary no extra weight. See _post_text()/
    # _tfidf_matrix() in ranking.py for the fix (title counted twice,
    # English stop words, word bigrams).
    posts = [
        Post(
            "seed", "Speed up wind power expansion",
            "Expanding wind power is central to the energy transition.", "climate", "pro",
        ),
        Post(
            "on-topic", "Fast-track onshore wind approvals",
            "Onshore wind projects need faster planning approval to expand capacity.", "climate", "pro",
        ),
        Post(
            "off-topic-shared-word", "Time limits speed re-entry to work",
            "Shorter benefit time limits speed re-entry to the labour market.", "welfare", "pro",
        ),
    ]
    feed = standard_feed(posts, seed_id="seed", limit=2)
    assert feed[0]["post"].id == "on-topic"


def test_standard_feed_is_deterministic_across_repeated_calls():
    # Live-demo requirement (see NIGHTLY_TASK.md): identical input must
    # always produce the identical feed order, not depend on incidental
    # dict/set iteration order.
    runs = {
        tuple(item["post"].id for item in standard_feed(POLITICAL_POSTS, seed_id="seed", limit=5))
        for _ in range(5)
    }
    assert len(runs) == 1


def test_diversity_aware_feed_is_deterministic_across_repeated_calls():
    runs = {
        tuple(
            item["post"].id
            for item in diversity_aware_feed(POLITICAL_POSTS, seed_id="seed", limit=5, diversity_every=2)
        )
        for _ in range(5)
    }
    assert len(runs) == 1


def test_standard_feed_with_zero_signal_and_no_labels_does_not_crash_and_stays_sane():
    # Full cold start: no preferred_* args, and the seed post itself
    # predates political_label (None) - the feed must still render instead
    # of erroring out, with the same-perspective post ranked first.
    posts = [
        Post("seed", "A Neutral Title", "Some neutral body text about a topic.", "climate", "pro", None),
        Post("same", "Related Title", "Some related body text about the same topic.", "climate", "pro", None),
        Post("counter", "Counter Title", "Some counter body text about the same topic.", "climate", "contra", None),
    ]
    feed = standard_feed(posts, seed_id="seed", limit=2)
    assert feed[0]["post"].id == "same"


def test_diversity_feed_injects_a_counter_perspective_post():
    feed = diversity_aware_feed(POSTS, seed_id="seed", limit=3, diversity_every=2)
    diverse_items = [item for item in feed if item["is_diverse_pick"]]
    assert diverse_items
    assert all(item["post"].perspective == "contra" for item in diverse_items)
    assert all(item["post"].topic == "climate" for item in diverse_items)


def test_diversity_feed_still_returns_requested_amount_when_possible():
    feed = diversity_aware_feed(POSTS, seed_id="seed", limit=3)
    assert len(feed) == 3


def test_diversity_score_is_zero_when_no_perspective_differs():
    seed_post = POSTS[0]
    same_perspective_feed = [
        {"post": POSTS[1], "score": 0.9, "is_diverse_pick": False},
    ]
    assert diversity_score(same_perspective_feed, seed_post) == 0.0


def test_diversity_score_reflects_share_of_differing_posts():
    seed_post = POSTS[0]
    mixed_feed = [
        {"post": POSTS[1], "score": 0.9, "is_diverse_pick": False},  # same perspective
        {"post": POSTS[2], "score": 0.7, "is_diverse_pick": True},  # differing
    ]
    assert diversity_score(mixed_feed, seed_post) == 50.0


def test_diversity_score_of_empty_feed_is_zero():
    assert diversity_score([], POSTS[0]) == 0.0


def test_diversity_aware_feed_scores_higher_than_standard_feed():
    # Enough same-perspective posts that the single counter-perspective post
    # (lowest similarity) would fall outside a limit=3 standard feed entirely,
    # so this only passes if diversity-aware ranking actually forces it in.
    posts = [
        Post("seed", "Wind Power Expansion", "Wind power energy transition climate protection expansion", "climate", "pro"),
        Post("pro-1", "Solar Expansion", "Wind power energy transition climate protection solar expansion", "climate", "pro"),
        Post("pro-2", "Grid Expansion", "Wind power energy transition climate protection grid expansion", "climate", "pro"),
        Post("pro-3", "Storage Expansion", "Wind power energy transition climate protection storage expansion", "climate", "pro"),
        Post("contra-1", "Cost of the Expansion", "Wind power cost landscape expensive", "climate", "contra"),
    ]
    seed_post = posts[0]

    standard = standard_feed(posts, seed_id="seed", limit=3)
    diverse = diversity_aware_feed(posts, seed_id="seed", limit=3, diversity_every=2)

    assert diversity_score(standard, seed_post) == 0.0
    assert diversity_score(diverse, seed_post) > 0.0


def test_suggest_category_picks_the_most_similar_existing_post_topic():
    topic = suggest_category(
        "Wind Power Debate",
        "Wind power and the energy transition are central to climate protection.",
        POSTS,
    )
    assert topic == "climate"


def test_suggest_category_returns_none_without_any_posts_to_compare():
    assert suggest_category("Titel", "Text", []) is None


def test_dominant_perspective_picks_the_majority():
    assert dominant_perspective(["contra", "contra", "pro"]) == "contra"
    assert dominant_perspective(["pro", "pro", "pro", "contra"]) == "pro"


def test_dominant_perspective_is_none_without_signal_or_on_a_tie():
    assert dominant_perspective([]) is None
    assert dominant_perspective(["pro", "contra"]) is None


def test_standard_feed_follows_preferred_perspective_over_the_seed_posts_own():
    # Seed post is "pro", but the account's like history leans "contra" on
    # the seed's own topic ("climate") - the feed must reinforce the account's
    # history, not just this one post, otherwise the bubble wouldn't be
    # self-sustaining across seed posts.
    feed = standard_feed(POSTS, seed_id="seed", preferred_perspective_by_topic={"climate": "contra"})
    assert feed[0]["post"].perspective == "contra"


def test_diversity_aware_feed_interrupts_the_preferred_perspective_not_just_the_seed():
    feed = diversity_aware_feed(
        POSTS, seed_id="seed", limit=3, diversity_every=2, preferred_perspective_by_topic={"climate": "contra"}
    )
    diverse_items = [item for item in feed if item["is_diverse_pick"]]
    assert diverse_items
    assert all(item["post"].perspective == "pro" for item in diverse_items)


def test_dominant_political_label_picks_the_majority():
    assert dominant_political_label(["left", "left", "right"]) == "left"


def test_dominant_political_label_is_none_without_signal_or_on_a_tie():
    assert dominant_political_label([]) is None
    assert dominant_political_label(["left", "right"]) is None
    assert dominant_political_label(["left", "right", "center"]) is None


def test_dominant_political_label_ignores_unlabeled_posts():
    assert dominant_political_label([None, None, "left"]) == "left"


POLITICAL_POSTS = [
    Post("seed", "Wind Power Expansion", "Wind power energy transition climate protection expansion", "climate", "pro", "left"),
    # Same perspective as seed, but a different political label.
    Post("pro-other-label", "Solar Expansion", "Wind power energy transition climate protection solar expansion", "climate", "pro", "right"),
    # Same perspective and same political label as seed - the strongest "home" match.
    Post("pro-same-label", "Grid Expansion", "Wind power energy transition climate protection grid expansion", "climate", "pro", "left"),
    # Opposite perspective, same political label - a softer counter-signal.
    Post("contra-same-label", "Cost of the Expansion", "Wind power energy transition climate protection cost expansion", "climate", "contra", "left"),
    # Opposite perspective AND opposite political label - the strongest possible counter-signal.
    Post("contra-other-label", "Landscape Protection", "Wind power energy transition climate protection landscape expansion", "climate", "contra", "right"),
]


def test_standard_feed_ranks_matching_political_label_ahead_of_same_perspective_only():
    feed = standard_feed(POLITICAL_POSTS, seed_id="seed", limit=5)
    same_perspective_ids = [item["post"].id for item in feed if item["post"].perspective == "pro"]
    assert same_perspective_ids[0] == "pro-same-label"
    assert "pro-other-label" in same_perspective_ids[1:]


def test_standard_feed_uses_preferred_political_label_over_the_seeds_own():
    feed = standard_feed(
        POLITICAL_POSTS, seed_id="seed", limit=5, preferred_political_label="right"
    )
    same_perspective_ids = [item["post"].id for item in feed if item["post"].perspective == "pro"]
    assert same_perspective_ids[0] == "pro-other-label"


def test_standard_feed_prioritizes_political_label_match_over_perspective_match():
    # Ranking sorts primarily by political lean (left/center/right) as of
    # 2026-09-10 (Felix) - pro/contra is now only the secondary tiebreak.
    # contra-same-label differs on perspective but matches the seed's
    # political label; pro-other-label matches perspective but differs
    # politically. The political match must now win.
    feed = standard_feed(POLITICAL_POSTS, seed_id="seed", limit=5)
    ids = [item["post"].id for item in feed]
    assert ids.index("contra-same-label") < ids.index("pro-other-label")


def test_diversity_aware_feed_prefers_the_double_counter_pick():
    feed = diversity_aware_feed(POLITICAL_POSTS, seed_id="seed", limit=1, diversity_every=1)
    assert feed[0]["post"].id == "contra-other-label"
    assert feed[0]["is_diverse_pick"] is True


def test_diversity_aware_feed_prefers_a_political_only_counter_over_a_perspective_only_counter():
    # When both a political-only counter and a perspective-only counter are
    # available for the same diversity slot, the political-only one must win
    # now that political label is the primary axis (see standard_feed swap
    # above) - pro-other-label (differs politically, same perspective)
    # should be picked over contra-same-label (differs on perspective only).
    posts = [
        Post("seed", "Wind Power Expansion", "Wind power energy transition climate protection expansion", "climate", "pro", "left"),
        Post("pro-same-label", "Grid Expansion", "Wind power energy transition climate protection grid expansion", "climate", "pro", "left"),
        Post("pro-other-label", "Solar Expansion", "Wind power energy transition climate protection solar expansion", "climate", "pro", "right"),
        Post("contra-same-label", "Cost of the Expansion", "Wind power energy transition climate protection cost expansion", "climate", "contra", "left"),
    ]
    feed = diversity_aware_feed(posts, seed_id="seed", limit=2, diversity_every=2)
    assert feed[1]["post"].id == "pro-other-label"
    assert feed[1]["is_diverse_pick"] is True


def test_diversity_aware_feed_marks_a_political_only_difference_as_diverse():
    # Only same-perspective posts and one that differs solely on political
    # label are in reach - the diversity slot should still surface it and
    # flag it, not silently fall back to a same-perspective/same-label post.
    posts = [
        Post("seed", "Wind Power Expansion", "Wind power energy transition climate protection expansion", "climate", "pro", "left"),
        Post("pro-same-label", "Grid Expansion", "Wind power energy transition climate protection grid expansion", "climate", "pro", "left"),
        Post("pro-other-label", "Solar Expansion", "Wind power energy transition climate protection solar expansion", "climate", "pro", "right"),
    ]
    feed = diversity_aware_feed(posts, seed_id="seed", limit=2, diversity_every=2)
    assert feed[1]["post"].id == "pro-other-label"
    assert feed[1]["is_diverse_pick"] is True


def test_diversity_score_for_political_label_reflects_share_of_differing_posts():
    feed = [
        {"post": POLITICAL_POSTS[2], "score": 0.9, "is_diverse_pick": False},  # same label
        {"post": POLITICAL_POSTS[4], "score": 0.5, "is_diverse_pick": True},  # differing label
    ]
    assert diversity_score_for_political_label(feed, "left") == 50.0


def test_diversity_score_for_political_label_is_zero_without_a_label_signal():
    feed = [{"post": POLITICAL_POSTS[2], "score": 0.9, "is_diverse_pick": False}]
    assert diversity_score_for_political_label(feed, None) == 0.0


def test_bubble_trend_is_empty_without_any_likes():
    assert bubble_trend([]) == []


def test_bubble_trend_climbs_toward_one_hundred_as_one_side_reinforces():
    trend = bubble_trend(["pro", "pro", "pro"])
    assert [point["dominant_share"] for point in trend] == [100.0, 100.0, 100.0]
    assert [point["index"] for point in trend] == [1, 2, 3]


def test_bubble_trend_drops_back_toward_fifty_when_a_counter_like_comes_in():
    # Three "pro" likes tighten the bubble to 100%, a "contra" like right
    # after loosens it back toward 50/50 - the whole point is that this is
    # visible as movement, not just a final snapshot number.
    trend = bubble_trend(["pro", "pro", "pro", "contra"])
    assert trend[2]["dominant_share"] == 100.0
    assert trend[3]["dominant_share"] == 75.0


def test_bubble_trend_treats_a_tie_as_fifty_fifty():
    trend = bubble_trend(["pro", "contra"])
    assert trend[-1]["dominant_share"] == 50.0


def test_political_bubble_trend_is_empty_without_any_likes():
    assert political_bubble_trend([]) == []


def test_political_bubble_trend_climbs_toward_one_hundred_as_one_side_reinforces():
    trend = political_bubble_trend(["left", "left", "left"])
    assert [point["dominant_share"] for point in trend] == [100.0, 100.0, 100.0]
    assert [point["index"] for point in trend] == [1, 2, 3]


def test_political_bubble_trend_drops_back_when_a_counter_like_comes_in():
    trend = political_bubble_trend(["left", "left", "left", "right"])
    assert trend[2]["dominant_share"] == 100.0
    assert trend[3]["dominant_share"] == 75.0


def test_political_bubble_trend_handles_three_way_splits():
    # left/center/right each once - no majority yet, current like's own
    # count (1) is still the running max, same "not yet dominant" signal as
    # bubble_trend()'s two-way tie.
    trend = political_bubble_trend(["left", "center", "right"])
    assert [point["dominant_share"] for point in trend] == [100.0, 50.0, pytest.approx(33.3, abs=0.1)]


def test_political_bubble_trend_skips_unlabeled_likes():
    # A like on a post from before political_label existed (or left unset)
    # carries no signal for this axis - skipped entirely, not counted as a
    # fourth "no label" bucket and not consuming an index slot.
    trend = political_bubble_trend(["left", None, "left"])
    assert [point["index"] for point in trend] == [1, 2]
    assert [point["dominant_share"] for point in trend] == [100.0, 100.0]


def test_political_label_ratio_is_empty_without_signal():
    assert political_label_ratio([]) == {}
    assert political_label_ratio([None, None]) == {}


def test_political_label_ratio_reflects_the_plain_split_with_no_recent_likes_to_boost():
    # recent_window=0 disables the recency boost entirely, isolating the
    # plain-count behavior: 3 left / 2 right should come out as 60/40, not
    # collapsed into a single winner like dominant_political_label() would.
    ratio = political_label_ratio(["left", "left", "left", "right", "right"], recent_window=0)
    assert ratio["left"] == pytest.approx(0.6)
    assert ratio["right"] == pytest.approx(0.4)


def test_political_label_ratio_lets_recent_likes_outweigh_an_older_majority():
    # 5 old "left" likes, then 3 recent "right" ones. Plain counting would
    # call this 5/3 in favor of left, but the boosted recent window should
    # tip the weighted ratio the other way - a recent change in taste should
    # show up before it's technically the numeric majority.
    labels = ["left"] * 5 + ["right"] * 3
    ratio = political_label_ratio(labels, recent_boost=2.0, recent_window=3)
    assert ratio["right"] > ratio["left"]


def test_political_label_ratio_ignores_unlabeled_entries():
    assert political_label_ratio([None, "left", None, "right"], recent_window=0) == {
        "left": pytest.approx(0.5),
        "right": pytest.approx(0.5),
    }


RATIO_POSTS = [Post("seed", "Wind Power Expansion", "Wind power energy transition climate protection expansion", "climate", "pro", "left")] + [
    Post(f"left-{i}", f"Left Post {i}", "Wind power energy transition climate protection expansion topic", "climate", "pro", "left")
    for i in range(6)
] + [
    Post(f"right-{i}", f"Right Post {i}", "Wind power energy transition climate protection expansion topic", "climate", "pro", "right")
    for i in range(6)
]


def test_standard_feed_mixes_proportionally_instead_of_all_or_nothing():
    # A 60/40 ratio must not collapse into a 100% "right" feed just because
    # right happens to be ahead (the bug report this fixes: one extra like
    # on one side used to flip the entire standard feed to that side).
    feed = standard_feed(RATIO_POSTS, seed_id="seed", limit=10, preferred_political_ratio={"left": 0.6, "right": 0.4})
    labels = [item["post"].political_label for item in feed]
    assert labels.count("left") == 6
    assert labels.count("right") == 4


def test_standard_feed_ratio_slots_are_spread_out_not_clumped_in_one_block():
    # The minority label shouldn't be pushed entirely to one end of the feed
    # - _interleave_by_share should distribute its slots across the output.
    feed = standard_feed(RATIO_POSTS, seed_id="seed", limit=10, preferred_political_ratio={"left": 0.6, "right": 0.4})
    right_positions = [i for i, item in enumerate(feed) if item["post"].political_label == "right"]
    assert min(right_positions) < 5
    assert max(right_positions) >= 5


def test_standard_feed_ratio_takes_priority_over_the_single_label_fallback():
    # When both are given, the proportional ratio wins - preferred_political_label
    # alone would produce a 100%-left feed here.
    feed = standard_feed(
        RATIO_POSTS,
        seed_id="seed",
        limit=10,
        preferred_political_label="left",
        preferred_political_ratio={"left": 0.5, "right": 0.5},
    )
    labels = [item["post"].political_label for item in feed]
    assert labels.count("left") == 5
    assert labels.count("right") == 5
