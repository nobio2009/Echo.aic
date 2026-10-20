import re
import webbrowser
from urllib.parse import urlparse

def register(assistant):
    def open_url(argument=""):
        url=argument.strip()
        if url.lower().startswith("open "): url=url[5:].strip()
        if not url: return "Usage: run openurl https://example.com"
        if not re.match(r"^https?://",url,re.I): url="https://"+url
        parsed=urlparse(url)
        if parsed.scheme not in {"http","https"} or not parsed.netloc: return "Please provide a valid http(s) URL."
        webbrowser.open(url)
        return f"Asked the default browser to open {url}."
    assistant.command("openurl", "Open a supplied HTTP(S) URL in the default browser.", open_url)
