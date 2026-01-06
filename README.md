# Python-DeepLinks
A Python backend companion library that converts standard web URLs into platform-specific deep links. It generates Android intent links, iOS deep links, and web fallbacks for server-side use cases.

## Installation

Since this package is not yet published on PyPI, you can install it directly from the source:

```bash
git clone https://github.com/ShakeebSk/Python-DeepLinks.git
cd Python-DeepLinks
pip install .
```

## Basic Usage

```python
from pydeeplinks import generate_deep_link

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
links = generate_deep_link(url)

print(links)
```

For more comprehensive documentation, API references, and supported platforms, please check the [package README](src/pydeeplinks/README.md).

## Features

- **Android Intent Generation**: Creates `intent://` URIs for robust app launching on Android.
- **iOS Deep Links**: Maps web domains to iOS-specific deep link formats (custom schemes or universal links).
- **Web Fallbacks**: Ensures users are redirected to the browser if the app is not supported.
- **Extensible Handlers**: Easily add support for new domains/platforms.

## Supported Platforms

- **YouTube**: Standard videos and shorts.
- **LinkedIn**: Profiles and company pages.
- **Discord**: Channels and Invite links.

## License

MIT
