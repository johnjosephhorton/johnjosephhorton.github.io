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

    paper_pages = read_table("paper_pages", {"paper_id", "slug", "year", "summary"})
    check_reference(paper_pages, "paper_id", paper_ids, "paper_pages")
    unique_ids(paper_pages, "paper_pages", column="paper_id")
    unique_ids(paper_pages, "paper_pages", column="slug")
    abstracts = read_table("paper_abstracts", {"paper_id", "abstract", "source_url"})
    abstract_ids = unique_ids(abstracts, "paper_abstracts", column="paper_id")
    check_reference(abstracts, "paper_id", paper_ids, "paper_abstracts")
    check_urls(abstracts, "paper_abstracts", column="source_url", require_unique=False)
    summary_ids = {row["paper_id"] for row in paper_pages if row["summary"]}
    missing_summaries = sorted(paper_ids - abstract_ids - summary_ids)
    if missing_summaries:
        raise ValueError("Missing paper abstracts/summaries: " + ", ".join(missing_summaries))
    author_orders = read_table("paper_author_order", {"paper_id", "author_ids"})
    order_ids = unique_ids(author_orders, "paper_author_order", column="paper_id")
    check_reference(author_orders, "paper_id", paper_ids, "paper_author_order")
    valid_author_ids = people_ids | {"john"}
    for row in author_orders:
        unknown = set(row["author_ids"].split(";")) - valid_author_ids
        if unknown:
            raise ValueError(f"data/paper_author_order.csv: unknown authors for {row['paper_id']}: {', '.join(sorted(unknown))}")
    if paper_ids != order_ids:
        raise ValueError("data/paper_author_order.csv must cover every paper")
    topics = read_table("paper_topics", {"paper_id", "topic", "selected"})
    topic_ids = unique_ids(topics, "paper_topics", column="paper_id")
    check_reference(topics, "paper_id", paper_ids, "paper_topics")
    if paper_ids != topic_ids:
        raise ValueError("data/paper_topics.csv must cover every paper")
    paper_presentations = read_table(
        "paper_presentations", {"paper_id", "event", "year", "url"}
    )
    check_reference(paper_presentations, "paper_id", paper_ids, "paper_presentations")
    check_urls(paper_presentations, "paper_presentations")

    paper_updates = read_table("paper_updates", {"paper_id", "last_updated"})
    update_ids = unique_ids(paper_updates, "paper_updates", column="paper_id")
    check_reference(paper_updates, "paper_id", paper_ids, "paper_updates")
    missing_updates = sorted(paper_ids - update_ids)
    if missing_updates:
        raise ValueError(
            "data/paper_updates.csv: missing papers: " + ", ".join(missing_updates)
        )
    invalid_updates = [
        row["paper_id"]
        for row in paper_updates
        if len(row["last_updated"]) not in {4, 7, 10}
        or not all(part.isdigit() for part in row["last_updated"].split("-"))
    ]
    if invalid_updates:
        raise ValueError(
            "data/paper_updates.csv: invalid dates: " + ", ".join(invalid_updates)
        )

    read_table("basic_info", {"name", "bio", "twitter_handle", "twitter_url"})
    for table in ("jobs", "talks", "education", "affiliations", "awards"):
        rows = read_table(table, {"url"})
        check_urls(rows, table, require_unique=table not in {"jobs", "affiliations"})
    for table in ("grants", "service", "reviewing"):
        read_table(table, set())

    ventures = read_table(
        "ventures",
        {
            "name",
            "description",
            "url",
            "logo",
            "package",
            "package_url",
            "blog",
            "blog_url",
            "backer",
            "backer_url",
            "backer_logo",
            "support",
        },
    )
    check_urls(ventures, "ventures")
    check_urls(ventures, "ventures", column="logo")
    check_urls(ventures, "ventures", column="package_url")
    check_urls(ventures, "ventures", column="blog_url")
    check_urls(ventures, "ventures", column="backer_url")
    check_urls(ventures, "ventures", column="backer_logo")

    courses = read_table("courses", {"id", "course_title", "institution", "role"})
    course_ids = unique_ids(courses, "courses")
    teaching = read_table("teaching", {"year", "semester", "id", "sections"})
    check_reference(teaching, "id", course_ids, "teaching")

    print(f"Validated {len(papers)} papers and {len(people)} people.")


if __name__ == "__main__":
    main()
