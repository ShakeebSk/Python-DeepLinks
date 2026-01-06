import re

from ..data_types import DeepLinkUrls, HandlerMatch, HandlerType


class YouTubeMatch(HandlerMatch):
    video_id: str
    timestamp: int | None


class YouTubeHandler(HandlerType[YouTubeMatch]):
    name = "youtube"
    patterns = [
        re.compile(r"(?:(?:www|m)\.)?youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})"),
        re.compile(r"youtu\.be/([a-zA-Z0-9_-]{11})"),
        re.compile(r"(?:(?:www|m)\.)?youtube\.com/shorts/([a-zA-Z0-9_-]{11})"),
        re.compile(r"(?:(?:www|m)\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})"),
        re.compile(r"(?:(?:www|m)\.)?youtube\.com/live/([a-zA-Z0-9_-]{11})"),
    ]

    def extract_id(self) -> str | None:
        for pattern in self.patterns:
            match = re.match(pattern, self.url)
            if match:
                return match.group(1)
        return None

    def extract_timestamp(self) -> str | None:
        tmatch = re.search(r"[?&]t=(?:(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s?)?)", self.url)
        if tmatch:
            hours = int(tmatch.group(1) or 0)
            minutes = int(tmatch.group(2) or 0)
            seconds = int(tmatch.group(3) or 0)
            total_seconds = hours * 3600 + minutes * 60 + seconds
            return str(total_seconds)

        start_match = re.search(r"[?&]start=(\d+)", self.url)
        if start_match:
            return start_match.group(1)

        return None

    def match_pattern(self) -> YouTubeMatch | None:
        video_id = self.extract_id()
        timestamp = self.extract_timestamp()

        if not video_id:
            return None

        return YouTubeMatch(
            video_id=video_id,
            timestamp=int(timestamp) if timestamp else None,
        )

    def generate_url(self, match_result: YouTubeMatch) -> DeepLinkUrls:
        if match_result["timestamp"]:
            return DeepLinkUrls(
                web=self.url,
                ios=f"vnd.youtube://watch?v={match_result['video_id']}&t={match_result['timestamp']}",
                android=f"intent://watch?v={match_result['video_id']}&t={match_result['timestamp']}#Intent;scheme=vnd.youtube;package=com.google.android.youtube;end",
            )

        return DeepLinkUrls(
            web=self.url,
            ios=f"vnd.youtube://watch?v={match_result['video_id']}",
            android=f"intent://watch?v={match_result['video_id']}#Intent;scheme=vnd.youtube;package=com.google.android.youtube;end",
        )
