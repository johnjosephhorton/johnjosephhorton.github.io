#!/usr/bin/env python3
"""Refresh the locally stored Expected Parrot writing feed."""

import csv
import email.utils
import html
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

FEED_URL = "https://blog.expectedparrot.com/feed"
OUTPUT = Path("data/writing.csv")


def clean(value):
    return " ".join(html.unescape(value or "").split())


with urllib.request.urlopen(FEED_URL, timeout=30) as response:
    root = ET.fromstring(response.read())

rows = []
for item in root.findall("./channel/item")[:3]:
    parsed_date = email.utils.parsedate_to_datetime(item.findtext("pubDate"))
    rows.append(
        {
            "title": clean(item.findtext("title")),
            "description": clean(item.findtext("description")),
            "url": clean(item.findtext("link")),
            "date": parsed_date.date().isoformat(),
        }
    )

with OUTPUT.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["title", "description", "url", "date"], lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

print(f"Recorded {len(rows)} posts in {OUTPUT}.")
