#!/usr/bin/env python3
"""Resolve favicon/apple-touch-icon URL from HTML. Args: base_url html_path → print absolute icon URL."""
from __future__ import annotations

import re
import sys
import urllib.parse


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: resolve-icon-url.py <base_url> <html_path>", file=sys.stderr)
        sys.exit(2)
    base, path = sys.argv[1], sys.argv[2]
    html = open(path, "r", encoding="utf-8", errors="ignore").read()
    patterns = [
        r'<link[^>]+rel=["\']apple-touch-icon["\'][^>]+href=["\']([^"\']+)["\']',
        r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']apple-touch-icon["\']',
        r'<link[^>]+rel=["\'](?:shortcut )?icon["\'][^>]+href=["\']([^"\']+)["\']',
        r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\'](?:shortcut )?icon["\']',
    ]
    href = None
    for p in patterns:
        m = re.search(p, html, re.I)
        if m:
            href = m.group(1).strip()
            break
    if not href:
        print(urllib.parse.urljoin(base + "/", "favicon.ico"))
    else:
        print(urllib.parse.urljoin(base + "/", href))


if __name__ == "__main__":
    main()
