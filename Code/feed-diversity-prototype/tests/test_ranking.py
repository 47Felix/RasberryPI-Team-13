import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ranking import Post, diversity_aware_feed, standard_feed

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
