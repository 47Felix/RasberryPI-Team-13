import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ranking import Post, diversity_aware_feed, diversity_score, standard_feed, suggest_category

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
