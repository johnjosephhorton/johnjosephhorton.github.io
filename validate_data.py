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


def unique_ids(rows, table, column="id"):
    ids = [row[column] for row in rows]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if "" in ids:
        raise ValueError(f"data/{table}.csv: every row needs a {column}")
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


def check_urls(rows, table, column="url", allow_empty=True, require_unique=True):
    invalid = []
    for index, row in enumerate(rows, start=2):
        value = row.get(column, "")
        if not value and allow_empty:
            continue
        is_web_url = value.startswith(("https://", "http://"))
        is_local_file = not is_web_url and (DATA_DIR.parent / value).is_file()
        if not (is_web_url or is_local_file):
            invalid.append(str(index))
    if invalid:
        raise ValueError(
            f"data/{table}.csv: invalid {column} values on rows: "
            + ", ".join(invalid)
        )

    if require_unique:
        values = [row.get(column, "") for row in rows if row.get(column, "")]
        duplicates = sorted({value for value in values if values.count(value) > 1})
        if duplicates:
            raise ValueError(f"data/{table}.csv: duplicate {column} values")


def main():
    papers = read_table("papers", {"id", "title", "status", "google_scholar"})
    people = read_table("people", {"id", "first", "last", "url"})
    paper_ids = unique_ids(papers, "papers")
    missing_scholar = [row["id"] for row in papers if not row["google_scholar"]]
    if missing_scholar:
        raise ValueError(
            "data/papers.csv: missing google_scholar links: "
            + ", ".join(missing_scholar)
        )
    people_ids = unique_ids(people, "people")
    for row in people:
        for column in ("first", "last"):
            if row[column] != row[column].strip():
                raise ValueError(
                    f"data/people.csv: whitespace around {column} for {row['id']}"
                )
    check_urls(people, "people")

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
        check_urls(rows, table)

    coauthors = read_table("coauthors", {"paper_id", "people_id"})
    check_reference(coauthors, "paper_id", paper_ids, "coauthors")
    check_reference(coauthors, "people_id", people_ids, "coauthors")

    publications = read_table(
        "publication_info",
        {
            "publication_id",
            "paper_id",
            "publication_type",
            "title",
            "venue",
            "publication_date",
            "volume",
            "issue",
            "pages",
            "doi",
            "url",
        },
    )
    unique_ids(publications, "publication_info", "publication_id")
    check_reference(publications, "paper_id", paper_ids, "publication_info")

    read_table("basic_info", {"name", "bio", "twitter_handle", "twitter_url"})
    for table in ("jobs", "talks", "education", "affiliations", "awards"):
        rows = read_table(table, {"url"})
        check_urls(rows, table, require_unique=table not in {"jobs", "affiliations"})
    for table in ("grants", "service", "reviewing"):
        read_table(table, set())

    courses = read_table("courses", {"id", "course_title", "institution", "role"})
    course_ids = unique_ids(courses, "courses")
    teaching = read_table("teaching", {"year", "semester", "id", "sections"})
    check_reference(teaching, "id", course_ids, "teaching")

    print(f"Validated {len(papers)} papers and {len(people)} people.")


if __name__ == "__main__":
    main()
