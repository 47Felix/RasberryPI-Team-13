import sys
from pathlib import Path
from unittest.mock import patch

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import fediverse


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
