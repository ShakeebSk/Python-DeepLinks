import re

from ..data_types import DeepLinkUrls, HandlerMatch, HandlerType


class FacebookMatch(HandlerMatch):
    expected_url: str


class FacebookHandler(HandlerType[FacebookMatch]):
    name = "facebook"
    patterns = [
        ("all", re.compile(r"(?:(?:www|m)\.)?facebook\.com/(.+)")),
    ]

    def match_pattern(self) -> FacebookMatch | None:
        for url_type, pattern in self.patterns:
            match = re.match(pattern, self.url)
            if match:
                return FacebookMatch(expected_url=match.group(1))
        return None

    def generate_url(self, match_result: FacebookMatch) -> DeepLinkUrls:
        expected_result = "facebook.com/" + match_result["expected_url"]
        return DeepLinkUrls(
            web=self.url,
            ios=f"fb://facewebmodal/f?href={expected_result}",
            android=f"intent://{expected_result}#Intent;scheme=https;package=com.facebook.katana;end",
        )
