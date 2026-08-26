"""Check the local CSV data before publishing the site."""

import csv
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"


def read_table(name, required_columns):
    path = DATA_DIR / f"{name}.csv"
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        columns = set(reader.fieldnames or [])
        missing = set(required_columns) - columns
        if missing:
            raise ValueError(f"{path}: missing columns: {', '.join(sorted(missing))}")
        return list(reader)


def unique_ids(rows, table):
    ids = [row["id"] for row in rows]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if "" in ids:
        raise ValueError(f"data/{table}.csv: every row needs an id")
    if duplicates:
        raise ValueError(f"data/{table}.csv: duplicate ids: {', '.join(duplicates)}")
    return set(ids)


def check_reference(rows, column, valid_ids, table, allow_empty=False):
    invalid = sorted(
        {
            row[column]
            for row in rows
            if row[column] not in valid_ids and not (allow_empty and not row[column])
        }
    )
    if invalid:
        raise ValueError(
            f"data/{table}.csv: unknown {column} values: {', '.join(invalid)}"
        )


def main():
    papers = read_table("papers", {"id", "title", "status", "google_scholar"})
    people = read_table("people", {"id", "first", "last", "url"})
    paper_ids = unique_ids(papers, "papers")
    people_ids = unique_ids(people, "people")

    relationships = {
        "versions": {"paper_id", "type", "url"},
        "media": {"paper_id", "publication", "url"},
        "slides": {"paper_id", "url"},
        "video": {"paper_id", "url"},
        "twitter_threads": {"paper_id", "url"},
        "code": {"paper_id", "url"},
    }
    for table, columns in relationships.items():
        rows = read_table(table, columns)
        check_reference(
            rows, "paper_id", paper_ids, table, allow_empty=table in {"slides", "video"}
        )

    coauthors = read_table("coauthors", {"paper_id", "people_id"})
    check_reference(coauthors, "paper_id", paper_ids, "coauthors")
    check_reference(coauthors, "people_id", people_ids, "coauthors")

    read_table("basic_info", {"name", "bio", "twitter_handle", "twitter_url"})
    for table in ("jobs", "awards", "grants", "talks", "education"):
        read_table(table, set())

    print(f"Validated {len(papers)} papers and {len(people)} people.")


if __name__ == "__main__":
    main()
