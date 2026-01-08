from pydeeplinks.handlers.facebook import FacebookHandler
import pytest


@pytest.mark.parametrize(
    "url, expected_url",
    [
        ("https://www.facebook.com/GoogleIndia/", "GoogleIndia/"),
        ("https://m.facebook.com/GoogleIndia/", "GoogleIndia/"),
        ("https://www.facebook.com/GitHub/", "GitHub/"),
        ("https://m.facebook.com/GitHub/", "GitHub/"),
    ],
)
def test_facebook_deep_link_generation(url, expected_url):
    handler = FacebookHandler(url)
    match = handler.match_pattern()
    expected_result ="facebook.com/" + expected_url

    assert match is not None
    assert match.get("expected_url") == expected_url

    try:
        deep_links = handler.generate_url(match)
    except AttributeError:
        pytest.fail("Implementation raised AttributeError, likely due to dict/object mismatch in generate_url")


    assert deep_links["web"] == url.replace("https://", "").replace("http://", "")
    assert deep_links["ios"] == f"fb://facewebmodal/f?href={expected_result}"
    assert deep_links["android"] == f"intent://{expected_result}#Intent;scheme=https;package=com.facebook.katana;end"


def test_invalid_urls():
    invalid_urls = [
        "https://www.google.com",
        "https://www.facebook.com/",
    ]
    for url in invalid_urls:
        handler = FacebookHandler(url)
        assert handler.match_pattern() is None
