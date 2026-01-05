from .data_types import DeepLinkUrls
from .handlers import handlers_list
from .handlers.unknown import UnknownHandler


def generate_deep_link(url: str) -> DeepLinkUrls:
    for handler in handlers_list:
        handler_instance = handler(url)
        match_result = handler_instance.match_pattern()
        if match_result:
            return handler_instance.generate_url(match_result)
    return UnknownHandler(url).generate_url({})


if __name__ == "__main__":
    import sys

    print(generate_deep_link(sys.argv[1]))
