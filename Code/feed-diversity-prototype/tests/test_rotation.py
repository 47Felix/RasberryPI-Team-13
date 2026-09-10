"""Feed rotation planning (_rotation_plan in app.py): a plain page reload has
to keep surfacing posts the viewer hasn't been shown yet, and must never
freeze on the same top slice once most of the catalogue has been seen (Felix,
2026-09-10 - "post refreshing only works sometimes, I keep seeing the same
posts after a refresh").
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import MIN_UNSEEN_FOR_ROTATION, _rotation_plan

# Newest first, same order as db.fetch_posts() / app.index().
POST_IDS = [f"p{i:02d}" for i in range(30)]


def test_first_load_has_no_seen_history_and_no_exclusions():
    seed_id, exclude_ids, seen_after, rotation_active = _rotation_plan(POST_IDS, [], None)
    assert seed_id == "p00"  # newest
    assert exclude_ids is None
    assert seen_after == []
    assert rotation_active is False


def test_reload_pins_seed_to_newest_unseen_and_hides_seen_posts():
    seen = ["p00", "p01", "p02"]
    seed_id, exclude_ids, seen_after, rotation_active = _rotation_plan(POST_IDS, seen, None)
    assert seed_id == "p03"
    assert exclude_ids == {"p00", "p01", "p02"}
    assert rotation_active is True
    assert seen_after == seen


def test_seed_is_never_in_its_own_exclude_set():
    # Whole catalogue seen except one post -> that post becomes the seed and
    # must not also be filtered out of the candidate pool.
    seen = POST_IDS[1:]
    seed_id, exclude_ids, _, _ = _rotation_plan(POST_IDS, seen, None)
    assert seed_id == "p00"
    assert "p00" not in (exclude_ids or set())


def test_catalogue_almost_exhausted_starts_a_fresh_cycle_instead_of_freezing():
    # Fewer than MIN_UNSEEN_FOR_ROTATION posts still unseen: the old code
    # switched rotation off here and returned the identical top slice on every
    # further reload. Now the seen history is cleared and rotation restarts.
    unseen_left = MIN_UNSEEN_FOR_ROTATION - 1
    seen = POST_IDS[unseen_left:]
    seed_id, exclude_ids, seen_after, rotation_active = _rotation_plan(POST_IDS, seen, None)
    assert seed_id == "p00"
    assert exclude_ids is None
    assert seen_after == []
    assert rotation_active is False


def test_explicit_seed_pins_the_feed_and_disables_rotation():
    seen = ["p00", "p01"]
    seed_id, exclude_ids, seen_after, rotation_active = _rotation_plan(POST_IDS, seen, "p07")
    assert seed_id == "p07"
    assert exclude_ids is None
    assert rotation_active is False
    assert seen_after == seen  # still tracked, just not acted on


def test_explicit_seed_that_no_longer_exists_falls_back_to_rotation():
    seed_id, exclude_ids, _, rotation_active = _rotation_plan(POST_IDS, ["p00"], "deleted")
    assert seed_id == "p01"
    assert exclude_ids == {"p00"}
    assert rotation_active is True


def test_stale_seen_ids_not_in_the_catalogue_are_ignored():
    seed_id, exclude_ids, seen_after, _ = _rotation_plan(POST_IDS, ["gone1", "gone2", "p00"], None)
    assert seed_id == "p01"
    assert exclude_ids == {"p00"}
    assert "gone1" not in seen_after and "gone2" not in seen_after


def test_repeated_reloads_keep_advancing_and_never_get_stuck():
    # Simulate app.index()'s session bookkeeping across many reloads: every
    # reload must either show a not-recently-seen post as its seed or have
    # legitimately wrapped around to a fresh cycle - it must never return the
    # exact same (seed, feed body) twice in a row once rotation is going.
    seen: list[str] = []
    feed_size = MIN_UNSEEN_FOR_ROTATION - 1
    previous_view = None
    fresh_cycles = 0
    for _ in range(60):
        seed_id, exclude_ids, seen, _ = _rotation_plan(POST_IDS, seen, None)
        body = [pid for pid in POST_IDS if pid != seed_id and pid not in (exclude_ids or set())][:feed_size]
        view = (seed_id, tuple(body))
        if exclude_ids is None and seed_id == "p00":
            fresh_cycles += 1
        else:
            assert view != previous_view, "feed froze on the same slice"
        previous_view = view
        shown = [seed_id] + body
        seen = (seen + [pid for pid in shown if pid not in seen])[-60:]
    # It kept cycling rather than dead-ending on one slice.
    assert fresh_cycles >= 2
