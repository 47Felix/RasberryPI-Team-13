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
    standard_feed,
    suggest_category,
)

POSTS = [
    Post(
        "seed",
        "Windkraft-Ausbau",
        "Windkraft und die Energiewende sind zentral fuer den Klimaschutz. "
        "Der Ausbau von Windkraft muss beschleunigt werden.",
        "klima",
        "pro",
    ),
    Post(
        "same-perspective",
        "Energiewende voranbringen",
        "Der Ausbau der Energiewende inklusive Windkraft ist entscheidend, "
        "um die Klimaziele zu erreichen.",
        "klima",
        "pro",
    ),
    Post(
        "counter-perspective",
        "Kosten des Ausbaus",
        "Windkraftanlagen veraendern die Landschaft und die Kosten fuer den "
        "Ausbau sind zu hoch.",
        "klima",
        "contra",
    ),
    Post(
        "unrelated",
        "Wochenendwetter",
        "Das Wetter am Wochenende wird sonnig und mild.",
        "sonstiges",
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


def test_standard_feed_stays_within_seed_perspective_even_when_the_topic_runs_out():
    # Only one other same-topic/same-perspective post exists, so a naive
    # global similarity ranking would have to pad the rest of the feed with
    # whatever scores next-highest - which, on a small dataset, is often a
    # same-topic counter-perspective post rather than an unrelated topic
    # (shared topic vocabulary outweighs perspective). That defeats the
    # entire premise of a "bubble-reinforcing" feed, so perspective match
    # must win over raw similarity.
    posts = [
        Post("seed", "Windkraft-Ausbau", "Windkraft Energiewende Klimaschutz Ausbau", "klima", "pro"),
        Post("pro-1", "Solar-Ausbau", "Windkraft Energiewende Klimaschutz Solar Ausbau", "klima", "pro"),
        Post("contra-1", "Kosten des Ausbaus", "Windkraft Energiewende Klimaschutz Kosten Ausbau", "klima", "contra"),
        Post("other-pro-1", "Mindestlohn erhoehen", "Mindestlohn stuetzt Kaufkraft", "wirtschaft", "pro"),
        Post("other-pro-2", "Vier-Tage-Woche", "Vier Tage Woche Produktivitaet", "wirtschaft", "pro"),
    ]
    feed = standard_feed(posts, seed_id="seed", limit=3)
    assert all(item["post"].perspective == "pro" for item in feed)


def test_diversity_feed_injects_a_counter_perspective_post():
    feed = diversity_aware_feed(POSTS, seed_id="seed", limit=3, diversity_every=2)
    diverse_items = [item for item in feed if item["is_diverse_pick"]]
    assert diverse_items
    assert all(item["post"].perspective == "contra" for item in diverse_items)
    assert all(item["post"].topic == "klima" for item in diverse_items)


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
        Post("seed", "Windkraft-Ausbau", "Windkraft Energiewende Klimaschutz Ausbau", "klima", "pro"),
        Post("pro-1", "Solar-Ausbau", "Windkraft Energiewende Klimaschutz Solar Ausbau", "klima", "pro"),
        Post("pro-2", "Netzausbau", "Windkraft Energiewende Klimaschutz Netz Ausbau", "klima", "pro"),
        Post("pro-3", "Speicher-Ausbau", "Windkraft Energiewende Klimaschutz Speicher Ausbau", "klima", "pro"),
        Post("contra-1", "Kosten des Ausbaus", "Windkraft Kosten Landschaft teuer", "klima", "contra"),
    ]
    seed_post = posts[0]

    standard = standard_feed(posts, seed_id="seed", limit=3)
    diverse = diversity_aware_feed(posts, seed_id="seed", limit=3, diversity_every=2)

    assert diversity_score(standard, seed_post) == 0.0
    assert diversity_score(diverse, seed_post) > 0.0


def test_suggest_category_picks_the_most_similar_existing_post_topic():
    topic = suggest_category(
        "Windkraft-Debatte",
        "Windkraft und die Energiewende sind zentral fuer den Klimaschutz.",
        POSTS,
    )
    assert topic == "klima"


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
    # the seed's own topic ("klima") - the feed must reinforce the account's
    # history, not just this one post, otherwise the bubble wouldn't be
    # self-sustaining across seed posts.
    feed = standard_feed(POSTS, seed_id="seed", preferred_perspective_by_topic={"klima": "contra"})
    assert feed[0]["post"].perspective == "contra"


def test_diversity_aware_feed_interrupts_the_preferred_perspective_not_just_the_seed():
    feed = diversity_aware_feed(
        POSTS, seed_id="seed", limit=3, diversity_every=2, preferred_perspective_by_topic={"klima": "contra"}
    )
    diverse_items = [item for item in feed if item["is_diverse_pick"]]
    assert diverse_items
    assert all(item["post"].perspective == "pro" for item in diverse_items)


def test_dominant_political_label_picks_the_majority():
    assert dominant_political_label(["links", "links", "rechts"]) == "links"


def test_dominant_political_label_is_none_without_signal_or_on_a_tie():
    assert dominant_political_label([]) is None
    assert dominant_political_label(["links", "rechts"]) is None
    assert dominant_political_label(["links", "rechts", "mitte"]) is None


def test_dominant_political_label_ignores_unlabeled_posts():
    assert dominant_political_label([None, None, "links"]) == "links"


POLITICAL_POSTS = [
    Post("seed", "Windkraft-Ausbau", "Windkraft Energiewende Klimaschutz Ausbau", "klima", "pro", "links"),
    # Same perspective as seed, but a different political label.
    Post("pro-other-label", "Solar-Ausbau", "Windkraft Energiewende Klimaschutz Solar Ausbau", "klima", "pro", "rechts"),
    # Same perspective and same political label as seed - the strongest "home" match.
    Post("pro-same-label", "Netzausbau", "Windkraft Energiewende Klimaschutz Netz Ausbau", "klima", "pro", "links"),
    # Opposite perspective, same political label - a softer counter-signal.
    Post("contra-same-label", "Kosten des Ausbaus", "Windkraft Energiewende Klimaschutz Kosten Ausbau", "klima", "contra", "links"),
    # Opposite perspective AND opposite political label - the strongest possible counter-signal.
    Post("contra-other-label", "Landschaftsschutz", "Windkraft Energiewende Klimaschutz Landschaft Ausbau", "klima", "contra", "rechts"),
]


def test_standard_feed_ranks_matching_political_label_ahead_of_same_perspective_only():
    feed = standard_feed(POLITICAL_POSTS, seed_id="seed", limit=5)
    same_perspective_ids = [item["post"].id for item in feed if item["post"].perspective == "pro"]
    assert same_perspective_ids[0] == "pro-same-label"
    assert "pro-other-label" in same_perspective_ids[1:]


def test_standard_feed_uses_preferred_political_label_over_the_seeds_own():
    feed = standard_feed(
        POLITICAL_POSTS, seed_id="seed", limit=5, preferred_political_label="rechts"
    )
    same_perspective_ids = [item["post"].id for item in feed if item["post"].perspective == "pro"]
    assert same_perspective_ids[0] == "pro-other-label"


def test_diversity_aware_feed_prefers_the_double_counter_pick():
    feed = diversity_aware_feed(POLITICAL_POSTS, seed_id="seed", limit=1, diversity_every=1)
    assert feed[0]["post"].id == "contra-other-label"
    assert feed[0]["is_diverse_pick"] is True


def test_diversity_aware_feed_marks_a_political_only_difference_as_diverse():
    # Only same-perspective posts and one that differs solely on political
    # label are in reach - the diversity slot should still surface it and
    # flag it, not silently fall back to a same-perspective/same-label post.
    posts = [
        Post("seed", "Windkraft-Ausbau", "Windkraft Energiewende Klimaschutz Ausbau", "klima", "pro", "links"),
        Post("pro-same-label", "Netzausbau", "Windkraft Energiewende Klimaschutz Netz Ausbau", "klima", "pro", "links"),
        Post("pro-other-label", "Solar-Ausbau", "Windkraft Energiewende Klimaschutz Solar Ausbau", "klima", "pro", "rechts"),
    ]
    feed = diversity_aware_feed(posts, seed_id="seed", limit=2, diversity_every=2)
    assert feed[1]["post"].id == "pro-other-label"
    assert feed[1]["is_diverse_pick"] is True


def test_diversity_score_for_political_label_reflects_share_of_differing_posts():
    feed = [
        {"post": POLITICAL_POSTS[2], "score": 0.9, "is_diverse_pick": False},  # same label
        {"post": POLITICAL_POSTS[4], "score": 0.5, "is_diverse_pick": True},  # differing label
    ]
    assert diversity_score_for_political_label(feed, "links") == 50.0


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
    trend = political_bubble_trend(["links", "links", "links"])
    assert [point["dominant_share"] for point in trend] == [100.0, 100.0, 100.0]
    assert [point["index"] for point in trend] == [1, 2, 3]


def test_political_bubble_trend_drops_back_when_a_counter_like_comes_in():
    trend = political_bubble_trend(["links", "links", "links", "rechts"])
    assert trend[2]["dominant_share"] == 100.0
    assert trend[3]["dominant_share"] == 75.0


def test_political_bubble_trend_handles_three_way_splits():
    # links/mitte/rechts each once - no majority yet, current like's own
    # count (1) is still the running max, same "not yet dominant" signal as
    # bubble_trend()'s two-way tie.
    trend = political_bubble_trend(["links", "mitte", "rechts"])
    assert [point["dominant_share"] for point in trend] == [100.0, 50.0, pytest.approx(33.3, abs=0.1)]


def test_political_bubble_trend_skips_unlabeled_likes():
    # A like on a post from before political_label existed (or left unset)
    # carries no signal for this axis - skipped entirely, not counted as a
    # fourth "no label" bucket and not consuming an index slot.
    trend = political_bubble_trend(["links", None, "links"])
    assert [point["index"] for point in trend] == [1, 2]
    assert [point["dominant_share"] for point in trend] == [100.0, 100.0]
