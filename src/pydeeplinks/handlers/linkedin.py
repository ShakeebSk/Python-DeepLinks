import re

from ..data_types import DeepLinkUrls, HandlerMatch, HandlerType


class LinkedInMatch(HandlerMatch):
    url_type: str
    id: str


class LinkedInHandler(HandlerType[LinkedInMatch]):
    name = "linkedin"
    patterns = [
        ("profile", re.compile(r"(?:(?:www)\.)?linkedin\.com/in/([^/?#]+)")),
        ("company", re.compile(r"(?:(?:www)\.)?linkedin\.com/company/([^/?#]+)")),
        ("job", re.compile(r"(?:(?:www)\.)?linkedin\.com/jobs/view/([^/?#]+)")),
        ("job", re.compile(r"(?:(?:www)\.)?linkedin\.com/jobs/collections/recommended/\?currentJobId=([^/?#]+)")),
        ("urn:li:activity", re.compile(r"(?:(?:www)\.)?linkedin\.com/posts/([^/?#]+)")),
        ("urn:li:activity", re.compile(r"(?:(?:www)\.)?linkedin\.com/feed/update/(?:urn:li:activity:)?([^/?#]+)")),
    ]

    def match_pattern(self) -> LinkedInMatch | None:
        for url_type, pattern in self.patterns:
            match = re.match(pattern, self.url)
            if match:
                return LinkedInMatch(url_type=url_type, id=match.group(1))
        return None

    def generate_url(self, match_result: LinkedInMatch) -> DeepLinkUrls:
        android_deeplink = re.sub(r"^(https?://)?www\.", "", self.url)
        return DeepLinkUrls(
            web=self.url,
            ios=f"linkedin://{match_result['url_type']}/{match_result['id']}",
            android=f"intent://{android_deeplink}#Intent;scheme=https;package=com.linkedin.android;end",
        )
