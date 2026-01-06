import re
from typing import Literal

from ..data_types import DeepLinkUrls, HandlerMatch, HandlerType


class DiscordMatch(HandlerMatch):
    url_type: Literal["channels", "invite"]
    guild: str | None
    channel: str | None
    invite: str | None


class DiscordHandler(HandlerType[DiscordMatch]):
    name = "discord"
    patterns = [
        ("channels", re.compile(r"^(?:www\.)?discord\.com\/channels\/([^\/?#]+)\/([^\/?#]+)$")),
        ("invite", re.compile(r"^(?:www\.)?(?:discord\.gg|discord\.com\/invite)\/([^\/?#]+)$")),
    ]

    def match_pattern(self) -> DiscordMatch | None:
        for url_type, pattern in self.patterns:
            match = pattern.match(self.url)
            if match:
                if url_type == "channels":
                    return DiscordMatch(url_type="channels", guild=match.group(1), channel=match.group(2), invite=None)
                elif url_type == "invite":
                    return DiscordMatch(url_type="invite", guild=None, channel=None, invite=match.group(1))
        return None

    def generate_url(self, match_result: DiscordMatch) -> DeepLinkUrls:
        if match_result["url_type"] == "channels":
            ios_deeplink = f"discord://channels/{match_result['guild']}/{match_result['channel']}"
        elif match_result["url_type"] == "invite":
            ios_deeplink = f"discord://invite/{match_result['invite']}"

        return DeepLinkUrls(
            web=self.url,
            ios=ios_deeplink,
            android=f"intent://{self.url.replace('www.', '')}#Intent;scheme=discord;package=com.discord;end",
        )
