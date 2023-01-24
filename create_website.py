import jinja2
import csv
from jinja2 import FileSystemLoader
import collections 


PREFERRED_VERSION_KEY = "jjh"
    
def googleScholarURL(key):
    return "https://scholar.google.com/citations?view_op=view_citation&hl=en&&citation_for_view=" + key

def make_link(title, url):
    return f"[{title}]({url})"

class Entity:
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)
            
class Paper(Entity):
    def add_coauthors(self, coauthors, people):
        self.coauthors = [people[coauthor.people_id] for coauthor in coauthors if coauthor.paper_id == self.id]
       
    def add_media(self, media):
        self._media = [m for m in media if m.paper_id == self.id]

    def add_slides(self, slides):
        self._slides = [s for s in slides if s.paper_id == self.id]

    def add_twitter_thread(self, twitter_thread):
        self._twitter_thread = [t for t in twitter_thread if t.paper_id == self.id]

    def add_code(self, code):
        self._code = [c for c in code if c.paper_id == self.id]

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

    def add_video(self, videos):
        self._videos = [v for v in videos if v.paper_id == self.id]

    @property
    def slides_line(self):
        if self._slides:
            return "".join(["(" + make_link(index + 1, obj.url) + ")" for index, obj in enumerate(self._videos)])
        else:
            return None

    @property
    def video_line(self):
        if self._videos:
            return "".join(["(" + make_link(index + 1, obj.url) + ")" for index, obj in enumerate(self._videos)])
        else:
            return None

    @property
    def twitter_thread_line(self):
        if self._twitter_thread:
            return "".join(["(" + make_link(index + 1, obj.url) + ")" for index, obj in enumerate(self._twitter_thread)])
        else:
            return None

    @property
    def code_line(self):
        if self._code:
            return "".join(["(" + make_link(index + 1, obj.url) + ")" for index, obj in enumerate(self._code)])
        else:
            return None
        
    @property
    def version_line(self):
        if self._versions:
            return "".join(["(" + make_link(obj.type, obj.url) + ")" for obj in self._versions])
        else:
            return None
        
    @property
    def media_line(self):
        if self._media:
            return "".join(["(" + m.display + ")" for m in self._media])
        else:
            return None
        
    def __init__(self, dictionary):
        super(Paper, self).__init__(dictionary)
        if self.google_scholar != '':
            self.gs_url = googleScholarURL(self.google_scholar)
        else:
            self.gs_url = None
            
    def __repr__(self):
        return "<" + self.title + ">"

    @property
    def google_scholar_url(self):
        if self.gs_url: 
            return "(" + make_link("gs", self.gs_url) + ")"
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
            return ", ".join(names[0:(number_coauthors-1)]) + " and " +  names[number_coauthors-1]
        if number_coauthors == 1:
            return names[0]


def get_csv(name):
    outcome = [] 
    with open(name, "r") as f:
        raw = csv.reader(f)
        header = next(raw)
        [outcome.append(dict(zip(header, row))) for row in raw]
    return outcome

    
class Person(Entity):
    def __repr__(self):
        return "<" + self.first + self.last + ">"

    @property
    def full_name(self):
        name = self.first + " " + self.last
        return make_link(name, self.url) if self.url else name


class Media(Entity):
    @property
    def display_full(self):
        #return f"[\"{self.story_name}\"]({self.url}), {self.publication}, {self.date}"
        return make_link(title = f"\"{self.story_name}\"", url = self.url) + f"{self.publication}, {self.date}"
    
    @property
    def display(self):
        return make_link(self.publication, self.url)


class Collection:

    def __init__(self, ObjectType, filename):
        self.items = collections.deque()
        [self.items.append(ObjectType(p)) for p in get_csv(filename)]

    def add_item(self, item):
        self.items.append(item)
    
    def __iter__(self):
        return iter(self.items)

                                            
coauthors = Collection(Entity, "coauthors.csv")
awards = Collection(Entity, "awards.csv")
jobs = Collection(Entity, "jobs.csv")
media = Collection(Media, "media.csv")
education = Collection(Entity, "education.csv")
talks = Collection(Entity, "talks.csv")
versions = Collection(Entity, "versions.csv")
slides = Collection(Entity, "slides.csv")
twitter_thread = Collection(Entity, "twitter_thread.csv")
code = Collection(Entity, "code.csv")

video = Collection(Entity, "video.csv")

people = {p['id'] : Person(p) for p in  get_csv("people.csv")}
papers = {p['id'] : Paper(p) for p in  get_csv("papers.csv")}

basic_info = Entity(get_csv("basic_info.csv")[0])

for id, paper in papers.items():
    paper.add_coauthors(coauthors, people)
    paper.add_media(media)
    paper.add_versions(versions)
    paper.add_video(video)
    paper.add_slides(slides)
    paper.add_twitter_thread(twitter_thread)
    paper.add_code(code)

environment = jinja2.Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("research.md")
           
with open("research.md", "w") as f:
     f.write(template.render(
         jobs = jobs,
         basic_info = basic_info, 
         talks = talks,
         awards = awards, 
         education = education, 
         papers = list(papers.values()))
     )


    
