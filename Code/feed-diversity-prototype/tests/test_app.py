"""End-to-end route tests using Flask's test client against a mocked `db`
layer (no Supabase needed - see NIGHTLY_TASK.md, every past nightly session
ran an equivalent check by hand but never committed it as a repeatable test).
Covers the routes that previously had zero automated coverage: `/`, both
feed modes, `/dashboard` (locked and unlocked), `/login`, `/register`, and
the accessibility attributes added alongside this test (aria-current on the
active tab, aria-pressed/aria-expanded on the like/comments toggle buttons).
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app as app_module
from ranking import Post

POSTS = [
    Post("p1", "Wind Power Expansion", "Speed up wind power expansion for the climate.", "climate", "pro", "left"),
    Post("p2", "Cost of the Expansion", "Wind turbines change the landscape, cost is too high.", "climate", "contra", "right"),
    Post("p3", "Bike Lanes Everywhere", "Cities should prioritize bike lanes over car lanes.", "transport", "pro", "left"),
    Post("p4", "Cars Remain Essential", "Car traffic remains essential for many commuters.", "transport", "contra", "right"),
]


def _row(post):
    return {
        "post": post,
        "author": {"name": "Demo Author", "handle": "@demo", "avatar": "📰"},
        "likes": 3,
        "comments": 1,
    }


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(app_module.db, "is_configured", lambda: True)
    monkeypatch.setattr(app_module.db, "auth_configured", lambda: True)
    monkeypatch.setattr(app_module.db, "fetch_posts", lambda: [_row(p) for p in POSTS])
    monkeypatch.setattr(app_module.db, "fetch_categories", lambda: ["climate", "transport"])
    monkeypatch.setattr(app_module.db, "fetch_topic_stances", lambda: {})
    monkeypatch.setattr(app_module.db, "fetch_liked_history", lambda user_id: [])
    monkeypatch.setattr(app_module.db, "fetch_liked_post_ids", lambda user_id, post_ids: set())
    monkeypatch.setattr(app_module.db, "fetch_commented_history", lambda user_id: [])
    monkeypatch.setattr(app_module.db, "fetch_commented_political_labels", lambda user_id: [])
    monkeypatch.setattr(app_module.db, "fetch_profile", lambda user_id: {})
    monkeypatch.setattr(app_module.db, "fetch_all_profiles", lambda: [])
    monkeypatch.setattr(app_module.fediverse, "fetch_public_posts", lambda topic: [])
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as test_client:
        yield test_client


def test_index_standard_mode_renders_posts(client):
    response = client.get("/?mode=standard")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Wind Power Expansion" in body or "Bike Lanes Everywhere" in body
    assert 'aria-current="page"' in body


def test_index_diversity_mode_renders_posts(client):
    response = client.get("/?mode=diversity")
    assert response.status_code == 200
    assert b"Diversity-aware" in response.data


def test_index_active_tab_has_aria_current_on_the_selected_mode_only(client):
    body = client.get("/?mode=standard").get_data(as_text=True)
    # Exactly one tab is marked current - the mode actually being viewed -
    # and it's the Standard tab's own <a>, not the unrelated "Standard" in
    # the "What is this?" blurb above the tab bar.
    assert body.count('aria-current="page"') == 1
    assert re.search(r'<a[^>]*aria-current="page"[^>]*>Standard<', body)
    assert not re.search(r'<a[^>]*aria-current="page"[^>]*>Diversity-aware<', body)


def test_index_like_button_has_aria_pressed_and_label(client):
    body = client.get("/").get_data(as_text=True)
    assert 'aria-pressed="false"' in body
    assert 'aria-label="Like this post' in body


def test_index_comments_toggle_has_aria_expanded_false_initially(client):
    body = client.get("/").get_data(as_text=True)
    assert 'aria-expanded="false"' in body


def test_index_empty_catalogue_shows_empty_state(client, monkeypatch):
    monkeypatch.setattr(app_module.db, "fetch_posts", lambda: [])
    response = client.get("/")
    assert response.status_code == 200
    assert b"No posts found." in response.data


def test_dashboard_locked_without_token(client, monkeypatch):
    monkeypatch.setenv("ADMIN_DASHBOARD_TOKEN", "secret-token")
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert b"Missing/incorrect access token" in response.data


def test_dashboard_disabled_when_not_configured(client, monkeypatch):
    monkeypatch.delenv("ADMIN_DASHBOARD_TOKEN", raising=False)
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert b"isn't set" in response.data


def test_login_page_renders(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_register_page_renders(client):
    response = client.get("/register")
    assert response.status_code == 200


def test_latest_post_id_endpoint(client, monkeypatch):
    monkeypatch.setattr(app_module.db, "fetch_latest_post_id", lambda: "p1")
    response = client.get("/posts/latest-id")
    assert response.status_code == 200
    assert response.get_json() == {"id": "p1"}


def test_like_requires_login(client):
    response = client.post("/posts/p1/like")
    assert response.status_code == 401


def test_comment_post_requires_login(client):
    response = client.post("/posts/p1/comments", json={"content": "hi"})
    assert response.status_code == 401
