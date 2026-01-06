import pytest
from pydeeplinks.handlers.linkedin import LinkedInHandler


@pytest.mark.parametrize(
    "url, url_type, expected_id",
    [
        ("https://www.linkedin.com/in/kishandev2509", "profile", "kishandev2509"),
        ("https://www.linkedin.com/company/google", "company", "google"),
        ("https://www.linkedin.com/jobs/view/4327981894", "job", "4327981894"),
        ("https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4327981894", "job", "4327981894"),
        ("https://www.linkedin.com/feed/update/urn:li:activity:7413905712164134912", "urn:li:activity", "7413905712164134912"),
        (
            "https://www.linkedin.com/posts/sundarpichai_what-i-loved-about-the-launch-of-gemini-3-activity-7399275754376548352-NN1b",
            "urn:li:activity",
            "sundarpichai_what-i-loved-about-the-launch-of-gemini-3-activity-7399275754376548352-NN1b",
        ),
    ],
)
def test_linkedin_deep_link_generation(url, url_type, expected_id):
    handler = LinkedInHandler(url)
    match = handler.match_pattern()

    assert match is not None

    assert match.get("url_type") == url_type
    assert match.get("id") == expected_id

    try:
        deep_links = handler.generate_url(match)
    except AttributeError:
        pytest.fail("Implementation raised AttributeError, likely due to dict/object mismatch in generate_url")

    web_deeplink = url.replace("https://", "").replace("http://", "")

    assert deep_links["ios"] == f"linkedin://{url_type}/{expected_id}"
    assert deep_links["android"] == f"intent://{web_deeplink.replace('www.', '')}#Intent;scheme=https;package=com.linkedin.android;end"
    assert deep_links["web"] == web_deeplink


def test_invalid_urls():
    invalid_urls = [
        "https://www.google.com",
        "https://linkedin.com",
        "https://www.linkedin.com/in/",
    ]
    for url in invalid_urls:
        handler = LinkedInHandler(url)
        assert handler.match_pattern() is None
