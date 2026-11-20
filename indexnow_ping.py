"""
Tell Bing (and Yandex, Seznam, Naver) about every URL in sitemap.xml via IndexNow.

Run after a push that adds or changes pages:

    cd financial-models-website && python3 indexnow_ping.py

The key file b92319c25c3b511f76c5c7958b72db16.txt at the site root proves we own the domain. Keep it.
"""

import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
KEY = "b92319c25c3b511f76c5c7958b72db16"


def main():
    urls = re.findall(r"<loc>([^<]+)</loc>", (ROOT / "sitemap.xml").read_text())
    body = json.dumps({"host": "sfsmodels.org", "key": KEY,
                       "keyLocation": f"https://sfsmodels.org/{KEY}.txt",
                       "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f"IndexNow: HTTP {r.status} for {len(urls)} URLs")


if __name__ == "__main__":
    main()
