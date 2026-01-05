from ..data_types import DeepLinkUrls, HandlerMatch, HandlerType


class UnknownHandler(HandlerType[HandlerMatch]):
    def match_pattern(self) -> None:
        return None

    def generate_url(self, match: HandlerMatch | None) -> DeepLinkUrls:
        return DeepLinkUrls(
            android=self.url,
            ios=self.url,
            web=self.url,
        )
