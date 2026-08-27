# John Horton's academic website

This repository contains both the source data and the generated static website.
It does not require Google Sheets, a database, or network access to build.

## Editing content

The CSV files in `data/` are the source of truth. Each file represents one kind
of record:

- `basic_info.csv` contains the name, biography, and profile links.
- `papers.csv` contains one row per paper, keyed by `id`.
- `people.csv` contains coauthor details, keyed by `id`.
- `coauthors.csv` connects papers to people using `paper_id` and `people_id`.
- `versions.csv`, `media.csv`, `slides.csv`, `video.csv`,
  `twitter_threads.csv`, and `code.csv` connect resources to a `paper_id`.
- `publication_info.csv` contains one row per formal publication, keyed by
  `publication_id` and connected to a paper by `paper_id`. It records the
  official title, publication type, venue, date, volume, issue, pages, DOI,
  and canonical URL. A paper may have multiple publication rows.
- `jobs.csv`, `awards.csv`, `grants.csv`, `talks.csv`, and `education.csv`
  populate the other visible sections.
- Google Scholar links live in the `google_scholar` column of `papers.csv`;
  keeping them with their papers avoids a second, conflicting citation table.
- The remaining CSV files preserve local CV data that is not currently shown
  on the homepage.

Keep IDs stable when editing relationships. Use UTF-8 CSV with a header row,
and leave an optional value empty rather than removing its column.

## Building

Install Python 3.10+, Jinja2, and Pandoc. With Poetry:

```sh
poetry install
poetry run make build
```

Or, if Jinja2 is already installed:

```sh
make build
```

The build has two stages:

1. `create_website.py` renders `templates/website.md` using the local CSVs.
2. Pandoc renders `website.md` into the published `index.html` using
   `templates/template.html`.

Both `website.md` and `index.html` are generated files, but they are committed
so GitHub Pages can publish the repository without a server-side build.
`page-markdown.js` packages the same Markdown for the page's copy button and
also works when `index.html` is opened directly from the filesystem.
The HTML footer uses the latest Git commit date locally; the deployment workflow
stamps it again from the exact commit being published.

Run `make validate` after editing CSVs to catch duplicate IDs and broken
relationships. `make build` runs this check automatically.

Run `make website` on macOS to build and open the page locally. Run
`make pdf` to produce `cv.pdf`.

## Publishing

Push a rebuilt `index.html` to `master`. The workflow in
`.github/workflows/static.yml` deploys it to GitHub Pages.

The Google Sheets importer was retired after the latest data was migrated to
the CSV files on August 26, 2026.
