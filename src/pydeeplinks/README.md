# PyDeepLinks

A Python backend companion library that converts standard web URLs into platform-specific deep links. It generates Android intent links, iOS deep links, and web fallbacks for server-side use cases.

## Installation

You can install the package from source:
<!-- 
```bash
pip install pydeeplinks
```

Or install from source:
 -->
```bash
git clone https://github.com/ShakeebSk/Python-DeepLinks.git
cd Python-DeepLinks
pip install .
```

## Usage

The primary entry point for the library is the `generate_deep_link` function.

```python
from pydeeplinks import generate_deep_link

# Example: YouTube URL
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
links = generate_deep_link(url)

print(links)
# Output:
# {
#     'web': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
#     'ios': 'vnd.youtube://watch/dQw4w9WgXcQ', 
#     'android': 'intent://watch?v=dQw4w9WgXcQ#Intent;package=com.google.android.youtube;scheme=https;end'
# }
```

## API Reference

### `generate_deep_link(url: str) -> DeepLinkUrls`

Takes a standard web URL and returns a dictionary containing deep links for various platforms.

**Arguments:**
- `url` (str): The web URL to process.

**Returns:**
- `DeepLinkUrls`: A dictionary with keys for `web`, `ios`, and `android`.

### `DeepLinkUrls`

A `TypedDict` defining the structure of the returned deep links.

```python
class DeepLinkUrls(TypedDict):
    web: str      # The original or fallback web URL
    ios: str      # The iOS Universal Link or Custom Scheme
    android: str  # The Android Intent URI
```

## Supported Platforms

Currently supported platforms include:

- **LinkedIn**: Generates `linkedin://` for iOS and `intent://` for Android.
    ```python
    url = "https://www.linkedin.com/in/kishandev2509/"
    links = generate_deep_link(url)
    print(links)
    # Output:
    # {
    #     "web": "https://www.linkedin.com/in/kishandev2509/",
    #     "ios": "linkedin://profile/kishandev2509",
    #     "android": "intent://www.linkedin.com/in/kishandev2509/#Intent;scheme=https;package=com.linkedin.android;end"
    # }
    ```
- **YouTube**: Generates `vnd.youtube://` for iOS and `intent://` for Android.
    ```python
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    links = generate_deep_link(url)
    print(links)
    # Output:
    # {
    #     "web": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    #     "ios": "vnd.youtube://watch/dQw4w9WgXcQ", 
    #     "android": "intent://watch?v=dQw4w9WgXcQ#Intent;scheme=vnd.youtube;package=com.google.android.youtube;end"
    # }
    ```
- **Discord**: Generates `discord://` for iOS and `intent://` for Android.
    ```python
    url = "https://discord.gg/MWwnUKaq"
    links = generate_deep_link(url)
    print(links)
    # Output:
    # {
    #     "web": "https://discord.gg/MWwnUKaq",
    #     "ios": "discord://invite/MWwnUKaq",
    #     "android": "intent://discord.gg/MWwnUKaq#Intent;scheme=discord;package=com.discord;end"
    # }
    ```
- **Unknown/Generic**: Fallback for unsupported URLs, returning the original URL for all keys.
    ```python
    url = "https://www.google.com/"
    links = generate_deep_link(url)
    print(links)
    # Output:
    # {
    #     "web": "https://www.google.com/",
    #     "ios": "https://www.google.com/", 
    #     "android": "https://www.google.com/"
    # }
    ```

## Extending

You can add support for new platforms by creating a new `HandlerType` and registering it in the `handlers_list`.

(See `src/pydeeplinks/handlers/` for examples).
