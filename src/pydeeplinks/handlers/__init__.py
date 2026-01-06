from .youtube import YouTubeHandler
from .linkedin import LinkedInHandler
from ..data_types import HandlerType

handlers_list: list[type[HandlerType]] = [
    YouTubeHandler,
    LinkedInHandler,
]

__all__ = ["handlers_list", "YouTubeHandler", "LinkedInHandler"]
