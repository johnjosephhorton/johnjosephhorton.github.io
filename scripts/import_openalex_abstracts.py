"""Import exact-title OpenAlex abstracts into local paper metadata.

Usage: python3 scripts/import_openalex_abstracts.py OPENALEX_JSON
The input is a saved OpenAlex works response for John J. Horton's ORCID.
Only exact normalized-title matches with an abstract are accepted.
"""
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

def normalize(value):
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", ascii_value.lower())

source = Path(sys.argv[1])
works = json.loads(source.read_text(encoding="utf-8"))["results"]
by_title = {normalize(work["title"]): work for work in works}
rows = []
with Path("data/papers.csv").open(newline="", encoding="utf-8") as handle:
    for paper in csv.DictReader(handle):
        work = by_title.get(normalize(paper["title"]))
        inverted = work.get("abstract_inverted_index") if work else None
        if not inverted:
            continue
        ordered = sorted((position, word) for word, positions in inverted.items() for position in positions)
        rows.append({
            "paper_id": paper["id"],
            "abstract": " ".join(word for _, word in ordered),
            "source_url": work["id"],
        })
with Path("data/paper_abstracts.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["paper_id", "abstract", "source_url"], lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
print(f"Imported {len(rows)} exact-title abstracts")
