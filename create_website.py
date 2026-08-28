import jinja2
from jinja2 import FileSystemLoader
import collections
import csv
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import parse_qs, urlparse

PREFERRED_VERSION_KEY = "jjh"


def googleScholarURL(key):
    if key.startswith("http://") or key.startswith("https://"):
        return key
    return (
        "https://scholar.google.com/citations?view_op=view_citation&hl=en&&citation_for_view="
        + key
    )


def make_link(title, url):
    return f"[{title}]({url})"


class Entity:
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)

    def __str__(self):
        pairs = [f"{k}: {v}" for k, v in self.__dict__.items()]
        return f"{pairs}"


class Paper(Entity):
    def add_coauthors(self, coauthors, people):
        self.coauthors = [
            people[coauthor.people_id]
            for coauthor in coauthors
            if coauthor.paper_id == self.id
        ]

    def add_media(self, media):
        self._media = [m for m in media if m.paper_id == self.id]

    def add_slides(self, slides):
        self._slides = [s for s in slides if s.paper_id == self.id]

    def add_twitter_thread(self, twitter_thread):
        self._twitter_thread = [t for t in twitter_thread if t.paper_id == self.id]

    def add_code(self, code):
        self._code = [c for c in code if c.paper_id == self.id]

    def add_video(self, videos):
        self._videos = [v for v in videos if v.paper_id == self.id]

    def add_versions(self, versions):
        versions = [v for v in versions if v.paper_id == self.id]
        self._versions = collections.deque()
        has_preferred_version = False
        for v in versions:
            if v.type == PREFERRED_VERSION_KEY:
                preferred_version = v
                has_preferred_version = True
            else:
                self._versions.append(v)
        if has_preferred_version:
            self._versions.appendleft(preferred_version)

    def add_publications(self, publications):
        self.publications = [p for p in publications if p.paper_id == self.id]

    @property
    def primary_publication(self):
        return self.publications[0] if self.publications else None

    @property
    def publication_label(self):
        publication_type = self.primary_publication.publication_type
        if publication_type.startswith("forthcoming-"):
            return "Forthcoming"
        if publication_type == "working-paper":
            return "Working paper"
        return "Published"

    @property
    def show_status(self):
        """Keep active statuses, but do not repeat a primary publication venue."""
        is_primary_publication = self.published not in ("", "0", "0.0")
        generic_working_status = self.status in {
            "Working paper",
            self.primary_publication.venue if self.primary_publication else "",
        }
        return bool(self.status) and not (
            self.primary_publication
            and (is_primary_publication or generic_working_status)
        )

    @property
    def slides_line(self):
        if self._slides:
            return "".join(
                [
                    "(" + make_link(index + 1, obj.url) + ")"
                    for index, obj in enumerate(self._slides)
                ]
            )
        else:
            return None

    @property
    def video_line(self):
        if self._videos:
            return "".join(
                [
                    "(" + make_link(index + 1, obj.url) + ")"
                    for index, obj in enumerate(self._videos)
                ]
            )
        else:
            return None

    @property
    def video_embeds(self):
        """Return privacy-enhanced YouTube embed URLs for verified videos."""
        embeds = []
        for video in self._videos:
            parsed = urlparse(video.url)
            query = parse_qs(parsed.query)
            hostname = parsed.netloc.lower().removeprefix("www.")
            video_id = None
            if hostname == "youtu.be":
                video_id = parsed.path.strip("/").split("/")[0]
            elif hostname in {"youtube.com", "m.youtube.com"}:
                if parsed.path == "/watch":
                    video_id = query.get("v", [None])[0]
                elif parsed.path.startswith(("/embed/", "/shorts/")):
                    video_id = parsed.path.strip("/").split("/")[1]
            if video_id and re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
                embed_url = "https://www.youtube-nocookie.com/embed/" + video_id
                start = query.get("t", [""])[0].removesuffix("s")
                if start.isdigit():
                    embed_url += "?start=" + start
                embeds.append(
                    Entity(
                        {
                            "url": video.url,
                            "embed_url": embed_url,
                            "title": video.topic
                            or f"John J. Horton presents {self.title}",
                        }
                    )
                )
        return embeds

    @property
    def twitter_thread_line(self):
        if self._twitter_thread:
            return "".join(
                [
                    "(" + make_link(index + 1, obj.url) + ")"
                    for index, obj in enumerate(self._twitter_thread)
                ]
            )
        else:
            return None

    @property
    def code_line(self):
        if self._code:
            return "".join(
                [
                    "(" + make_link(index + 1, obj.url) + ")"
                    for index, obj in enumerate(self._code)
                ]
            )
        else:
            return None

    @property
    def version_line(self):
        return self._format_version_line()

    @property
    def detail_version_line(self):
        return self._format_version_line(local_prefix="../../")

    def _format_version_line(self, local_prefix=""):
        if self._versions:
            labels = {
                "arxiv": "arXiv",
                "nber": "NBER",
                "jjh": "PDF",
                "ssrn": "SSRN",
                "acmec": "ACM EC",
                "acm": "ACM",
                "jole": "JOLE",
                "isr": "ISR",
                "mansci": "Management Science",
                "mit": "MIT",
                "coauthor": "PDF",
            }
            return " · ".join(
                make_link(
                    labels.get(obj.type.lower(), obj.type),
                    obj.url
                    if obj.url.startswith(("http://", "https://"))
                    else local_prefix + obj.url,
                )
                for obj in self._versions
            )
        else:
            return None

    @property
    def has_additional_links(self):
        return any(
            (
                self.google_scholar_url,
                self.media_line,
                self.video_line,
                self.slides_line,
                self.twitter_thread_line,
                self.code_line,
            )
        )

    @property
    def media_line(self):
        if self._media:
            return "".join(["(" + m.display + ")" for m in self._media])
        else:
            return None

    def __init__(self, dictionary):
        super(Paper, self).__init__(dictionary)
        if self.google_scholar:
            self.gs_url = googleScholarURL(self.google_scholar)
        else:
            self.gs_url = None

    def __repr__(self):
        return "<" + self.title + ">"

    @property
    def google_scholar_url(self):
        if self.gs_url:
            return "(" + make_link("Google Scholar", self.gs_url) + ")"
        else:
            return None

    @property
    def coauthored(self):
        return len(self.coauthors) > 0

    @property
    def with_line(self):
        """Create a 'with' line for coauthored papers"""
        number_coauthors = len(self.coauthors)
        names = [person.full_name for person in self.coauthors]
        if number_coauthors == 2:
            return names[0] + " and " + names[1]
        if number_coauthors > 2:
            return (
                ", ".join(names[0 : (number_coauthors - 1)])
                + " and "
                + names[number_coauthors - 1]
            )
        if number_coauthors == 1:
            return names[0]


def get_table_data(table_name, data_dir="data"):
    """Read one of the version-controlled CSV tables."""
    path = Path(data_dir) / f"{table_name}.csv"
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def get_csv(name):
    if name.endswith(".csv"):
        name = name.replace(".csv", "")
    return get_table_data(name)


class Person(Entity):
    def __repr__(self):
        return "<" + self.first + self.last + ">"

    @property
    def full_name(self):
        name = self.first + " " + self.last
        return make_link(name, self.url) if self.url else name

    @property
    def plain_name(self):
        return self.first + " " + self.last


class Media(Entity):
    @property
    def display_full(self):
        # return f"[\"{self.story_name}\"]({self.url}), {self.publication}, {self.date}"
        return (
            make_link(title=f'"{self.story_name}"', url=self.url)
            + f"{self.publication}, {self.date}"
        )

    @property
    def display(self):
        return make_link(self.publication, self.url)


class Publication(Entity):
    @property
    def citation(self):
        details = self.venue
        if self.volume:
            details += f" {self.volume}"
            if self.issue:
                details += f"({self.issue})"
        if self.pages:
            details += f": {self.pages}"
        year = self.publication_date[:4]
        if year:
            details += f" ({year})"
        return make_link(details, self.url) if self.url else details


class Collection:
    def __init__(self, ObjectType, filename):
        self.items = collections.deque()
        [self.items.append(ObjectType(p)) for p in get_csv(filename)]

    def add_item(self, item):
        self.items.append(item)

    def __iter__(self):
        return iter(self.items)


fields = [
    "coauthors",
    "awards",
    "jobs",
    "media",
    "education",
    "talks",
    "versions",
    "slides",
    "twitter_thread",
    "code",
    "video",
    "grants",
]

# entities = {field: Collection(Entity, field) for field in fields}

coauthors = Collection(Entity, "coauthors")
awards = Collection(Entity, "awards")
jobs = Collection(Entity, "jobs")
affiliations = Collection(Entity, "affiliations")
media = Collection(Media, "media")
education = Collection(Entity, "education")
talks = Collection(Entity, "talks")
versions = Collection(Entity, "versions")
slides = Collection(Entity, "slides")
twitter_threads = Collection(Entity, "twitter_threads")
code = Collection(Entity, "code")
video = Collection(Entity, "video")
grants = Collection(Entity, "grants")
service = Collection(Entity, "service")
reviewing = Collection(Entity, "reviewing")
ventures = Collection(Entity, "ventures")
publications = Collection(Publication, "publication_info")
paper_page_rows = get_csv("paper_pages.csv")
paper_presentations = Collection(Entity, "paper_presentations")
paper_updates = {
    row["paper_id"]: row["last_updated"] for row in get_csv("paper_updates.csv")
}

course_by_id = {course["id"]: course for course in get_csv("courses.csv")}
teaching_by_term = collections.OrderedDict()
for row in get_csv("teaching.csv"):
    key = (row["year"], row["semester"], row["id"])
    if key in teaching_by_term:
        teaching_by_term[key]["sections"] = str(
            int(teaching_by_term[key]["sections"]) + int(row["sections"])
        )
        continue
    course = course_by_id[row["id"]]
    teaching_by_term[key] = {
        **row,
        "course_title": course["course_title"],
        "institution": course["institution"],
        "role": course["role"],
    }
teaching_by_course = collections.OrderedDict()
for row in teaching_by_term.values():
    course_id = row["id"]
    if course_id not in teaching_by_course:
        teaching_by_course[course_id] = {
            "course_title": row["course_title"],
            "institution": row["institution"],
            "role": row["role"],
            "terms": [],
        }
    term = f'{row["semester"]} {row["year"]}'
    if row["sections"] != "1":
        term += f' ({row["sections"]} sections)'
    teaching_by_course[course_id]["terms"].append(term)
teaching_courses = [Entity(row) for row in teaching_by_course.values()]

people = {p["id"]: Person(p) for p in get_csv("people.csv")}
papers = {p["id"]: Paper(p) for p in get_csv("papers.csv")}
basic_info = Entity(get_csv("basic_info.csv")[0])


for id, paper in papers.items():
    paper.page_url = ""
    paper.last_updated = paper_updates[paper.id]
    paper.add_coauthors(coauthors, people)
    paper.add_media(media)
    paper.add_versions(versions)
    paper.add_video(video)
    paper.add_slides(slides)
    paper.add_twitter_thread(twitter_threads)
    paper.add_code(code)
    paper.add_publications(publications)

def slugify(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


paper_page_template = jinja2.Environment(
    loader=FileSystemLoader("templates/")
).get_template("paper.md")
paper_page_overrides = {row["paper_id"]: row for row in paper_page_rows}
for paper in papers.values():
    row = {
        "paper_id": paper.id,
        "slug": slugify(paper.title),
        "year": paper.last_updated[:4],
        "summary": "",
        **paper_page_overrides.get(paper.id, {}),
    }
    paper.page_url = f'papers/{row["slug"]}/index.html'
    authors = ["Horton, John J."] + [
        f"{person.last}, {person.first}" for person in paper.coauthors
    ]
    citation_key = f'horton{row["year"]}{row["slug"].replace("-", "")}'
    row["bibtex"] = "\n".join(
        [
            f"@misc{{{citation_key},",
            f'  title = {{{{{paper.title}}}}},',
            f'  author = {{{" and ".join(authors)}}},',
            f'  year = {{{row["year"]}}},',
            f'  url = {{https://john-joseph-horton.com/papers/{row["slug"]}/}}',
            "}",
        ]
    )
    page = Entity(row)
    presentations = [
        item for item in paper_presentations if item.paper_id == paper.id
    ]
    paper_markdown = paper_page_template.render(
        paper=paper, page=page, presentations=presentations
    )
    paper_markdown = (
        "\n".join(line.rstrip() for line in paper_markdown.splitlines()) + "\n"
    )
    output_dir = Path("papers") / row["slug"]
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.md").write_text(paper_markdown, encoding="utf-8")
    (output_dir / "paper-markdown.js").write_text(
        "window.PAGE_MARKDOWN = "
        + json.dumps(paper_markdown, ensure_ascii=False)
        + ";\n",
        encoding="utf-8",
    )

environment = jinja2.Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("website.md")

d = {
    "jobs": jobs,
    "affiliations": affiliations,
    "basic_info": basic_info,
    "ventures": ventures,
    "talks": talks,
    "awards": awards,
    "education": education,
    "papers": sorted(
        papers.values(), key=lambda paper: paper.last_updated, reverse=True
    ),
    "grants": grants,
    "service": service,
    "reviewing": reviewing,
    "teaching": teaching_courses,
}

rendered = template.render(**d)
rendered = "\n".join(line.rstrip() for line in rendered.splitlines()) + "\n"
with open("website.md", "w", encoding="utf-8") as f:
    f.write(rendered)

# Keep an exact copy available to the static page's copy button. Loading a
# JavaScript asset works both on GitHub Pages and in a local file:// preview.
with open("page-markdown.js", "w", encoding="utf-8") as f:
    f.write("window.PAGE_MARKDOWN = " + json.dumps(rendered, ensure_ascii=False) + ";\n")
