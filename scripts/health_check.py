#!/usr/bin/env python3
"""HTTP health probe: GET {base}/api/status."""

import argparse
import sys
import urllib.error
import urllib.request


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.strip())
    p.add_argument("url", help="Base URL, e.g. https://api.example.com")
    p.add_argument("--timeout", type=float, default=5.0)
    args = p.parse_args()
    target = args.url.rstrip("/") + "/api/status"
    try:
        with urllib.request.urlopen(target, timeout=args.timeout) as resp:
            sys.exit(0 if resp.status == 200 else 1)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
        sys.exit(1)


if __name__ == "__main__":
    main()
