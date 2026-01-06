from pydeeplinks.handlers.discord import DiscordHandler
import pytest


@pytest.mark.parametrize(
    "url, url_type, guild, channel, invite",
    [
        (
            "https://discord.com/channels/1451197679739863177/1451197680259829793",
            "channels",
            "1451197679739863177",
            "1451197680259829793",
            None,
        ),
        ("https://discord.gg/MWwnUKaq", "invite", None, None, "MWwnUKaq"),
    ],
)
def test_discord_deep_link_generation(url, url_type, guild, channel, invite):
    handler = DiscordHandler(url)
    match = handler.match_pattern()

    assert match is not None

    assert match.get("url_type") == url_type
    assert match.get("guild") == guild
    assert match.get("channel") == channel
    assert match.get("invite") == invite

    try:
        deep_links = handler.generate_url(match)
    except AttributeError:
        pytest.fail("Implementation raised AttributeError, likely due to dict/object mismatch in generate_url")

    web_deeplink = url.replace("https://", "").replace("http://", "")

    assert deep_links["web"] == web_deeplink
    assert deep_links["android"] == f"intent://{web_deeplink.replace('www.', '')}#Intent;scheme=discord;package=com.discord;end"

    if url_type == "channels":
        assert deep_links["ios"] == f"discord://{url_type}/{guild}/{channel}"
    elif url_type == "invite":
        assert deep_links["ios"] == f"discord://{url_type}/{invite}"


def test_invalid_urls():
    invalid_urls = [
        "https://www.google.com",
        "https://discord.com",
        "https://www.discord.com/channels/",
    ]
    for url in invalid_urls:
        handler = DiscordHandler(url)
        assert handler.match_pattern() is None
