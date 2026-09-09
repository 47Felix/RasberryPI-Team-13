import sys
import time
from pathlib import Path
from unittest.mock import patch

import pytest
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import fediverse


@pytest.fixture(autouse=True)
def _clear_fediverse_cache():
    # Every test below calls fetch_public_posts("klima", ...) - without
    # this, whichever test runs first would populate the cache and every
    # later test would silently get its result back instead of hitting the
    # mocked requests.get() they each set up.
    fediverse.clear_cache()
    yield
    fediverse.clear_cache()


class _FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code}")

    def json(self):
        return self._payload


def test_fetch_public_posts_returns_empty_for_unmapped_topic():
    assert fediverse.fetch_public_posts("unbekanntes-thema") == []


@patch("fediverse.requests.get")
def test_fetch_public_posts_strips_html_and_maps_fields(mock_get):
    mock_get.return_value = _FakeResponse(
        [
            {
                "content": "<p>Hallo <b>Welt</b>!</p>",
                "url": "https://mastodon.social/@someone/123",
                "account": {"acct": "someone@mastodon.social"},
                "created_at": "2026-09-07T10:00:00.000Z",
            }
        ]
    )
    posts = fediverse.fetch_public_posts("klima")
    assert posts == [
        {
            "content": "Hallo Welt !",
            "url": "https://mastodon.social/@someone/123",
            "account_handle": "someone@mastodon.social",
            "created_at": "2026-09-07T10:00:00.000Z",
        }
    ]


@patch("fediverse.requests.get")
def test_fetch_public_posts_drops_a_non_http_url(mock_get):
    mock_get.return_value = _FakeResponse(
        [{"content": "x", "url": "javascript:alert(1)", "account": {"acct": "a"}, "created_at": ""}]
    )
    posts = fediverse.fetch_public_posts("klima")
    assert posts[0]["url"] == ""


@patch("fediverse.requests.get", side_effect=requests.ConnectionError)
def test_fetch_public_posts_fails_open_on_network_error(mock_get):
    assert fediverse.fetch_public_posts("klima") == []


@patch("fediverse.requests.get")
def test_fetch_public_posts_fails_open_on_http_error(mock_get):
    mock_get.return_value = _FakeResponse([], status_code=503)
    assert fediverse.fetch_public_posts("klima") == []


@patch("fediverse.requests.get")
def test_fetch_public_posts_fails_open_on_unexpected_response_shape(mock_get):
    mock_get.return_value = _FakeResponse({"error": "not a list"})
    assert fediverse.fetch_public_posts("klima") == []


@patch("fediverse.requests.get")
def test_fetch_public_posts_respects_the_limit(mock_get):
    mock_get.return_value = _FakeResponse(
        [{"content": f"post {i}", "url": "", "account": {}, "created_at": ""} for i in range(10)]
    )
    posts = fediverse.fetch_public_posts("klima", limit=2)
    assert len(posts) == 2


@patch("fediverse.requests.get")
def test_fetch_public_posts_uses_the_cache_on_a_second_call(mock_get):
    mock_get.return_value = _FakeResponse(
        [{"content": "a", "url": "", "account": {}, "created_at": ""}]
    )
    first = fediverse.fetch_public_posts("klima")
    second = fediverse.fetch_public_posts("klima")
    assert first == second
    assert mock_get.call_count == 1


@patch("fediverse.requests.get")
def test_fetch_public_posts_refetches_after_the_cache_expires(mock_get):
    mock_get.return_value = _FakeResponse(
        [{"content": "a", "url": "", "account": {}, "created_at": ""}]
    )
    fediverse.fetch_public_posts("klima")
    with patch("fediverse.time.monotonic", return_value=time.monotonic() + fediverse.CACHE_TTL_SECONDS + 1):
        fediverse.fetch_public_posts("klima")
    assert mock_get.call_count == 2


@patch("fediverse.requests.get")
def test_fetch_public_posts_serves_stale_cache_when_a_later_fetch_fails(mock_get):
    mock_get.return_value = _FakeResponse(
        [{"content": "a", "url": "", "account": {}, "created_at": ""}]
    )
    first = fediverse.fetch_public_posts("klima")

    mock_get.side_effect = requests.ConnectionError
    with patch("fediverse.time.monotonic", return_value=time.monotonic() + fediverse.CACHE_TTL_SECONDS + 1):
        second = fediverse.fetch_public_posts("klima")

    assert second == first
    assert second != []
