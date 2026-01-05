import pytest
from pydeeplinks.handlers.youtube import YouTubeHandler


@pytest.mark.parametrize(
    "url, expected_id, expected_timestamp",
    [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ", None),
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ", None),
        ("https://www.youtube.com/shorts/dQw4w9WgXcQ", "dQw4w9WgXcQ", None),
        ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ", None),
        ("https://www.youtube.com/live/dQw4w9WgXcQ", "dQw4w9WgXcQ", None),
        ("https://youtu.be/dQw4w9WgXcQ?t=42s", "dQw4w9WgXcQ", 42),
        ("https://youtu.be/dQw4w9WgXcQ?t=1m30s", "dQw4w9WgXcQ", 90),
        ("https://youtu.be/dQw4w9WgXcQ?t=1h1m1s", "dQw4w9WgXcQ", 3661),
        ("https://youtu.be/dQw4w9WgXcQ?t=120", "dQw4w9WgXcQ", 120),
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&start=120", "dQw4w9WgXcQ", 120),
    ],
)
def test_youtube_deep_link_generation(url, expected_id, expected_timestamp):
    handler = YouTubeHandler(url)
    match = handler.match_pattern()

    assert match is not None

    video_id = match.get("video_id")
    timestamp = match.get("timestamp")

    assert video_id == expected_id
    assert timestamp == expected_timestamp

    try:
        deep_links = handler.generate_url(match)
    except AttributeError:
        pytest.fail(
            "Implementation raised AttributeError, likely due to dict/object mismatch in generate_url"
        )

    if expected_timestamp:
        expected_suffix = f"v={expected_id}&t={expected_timestamp}"
    else:
        expected_suffix = f"v={expected_id}"

    assert expected_suffix in deep_links["ios"]
    assert expected_suffix in deep_links["android"]
    assert "vnd.youtube://" in deep_links["ios"]
    assert "intent://" in deep_links["android"]
    assert (
        deep_links["web"].startswith("www")
        or deep_links["web"].startswith("youtube")
        or "youtu.be" in deep_links["web"]
    )


def test_invalid_urls():
    invalid_urls = [
        "https://www.google.com",
        "https://youtube.com",  # no video id
        "https://www.youtube.com/watch",  # no v param
    ]
    for url in invalid_urls:
        handler = YouTubeHandler(url)
        assert handler.match_pattern() is None
        assert handler.match_pattern() is None
