import jinja2
import csv
from jinja2 import FileSystemLoader

def googleScholarURL(key):
    return "https://scholar.google.com/citations?view_op=view_citation&hl=en&&citation_for_view=" + key


class Entity:
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)

class Paper(Entity):
    def add_coauthors(self, coauthors, people):
        self.coauthors = [people[coauthor.people_id] for coauthor in list(coauthors.values()) if coauthor.paper_id == self.id]

    def add_media(self, media):
        self.media = ";".join([m.display for m in media if m.paper_id == self.id])

    @property
    def media_line(self):
        if self.media == []:
            return ""
        else:
            return ";".join([m.display for m in self.media])
        
    def __init__(self, dictionary):
        super(Paper, self).__init__(dictionary)
        if self.google_scholar != '':
            self.gs_url = googleScholarURL(self.google_scholar)
        else:
            self.gs_url = ""

    def __repr__(self):
        return "<" + self.title + ">"

    @property 
    def with_line(self):
        """Create a 'with' line for coauthored papers"""
        number_coauthors = len(self.coauthors)
        names = [person.full_name for person in self.coauthors]
        if number_coauthors == 2:
            return names[0] + " and " + names[1]
        if number_coauthors > 2:
            return ", ".join(names[0:(number_coauthors-2)]) + " and " +  names[number_coauthors-1]
        if number_coauthors == 1:
            return names[0]


def GetCSV(name):
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
        return self.first + " " + self.last


class Media(Entity):
    @property
    def display(self):
        return f"[\"{self.story_name}\"]({self.url}), {self.publication}, {self.date}"
    
people = {p['id'] : Person(p) for p in  GetCSV("people.csv")}
papers = {p['id'] : Paper(p) for p in  GetCSV("papers.csv")}
coauthors = {p['people_id'] : Entity(p) for p in GetCSV("coauthors.csv")}

awards = [Entity(p) for p in GetCSV("awards.csv")]
jobs = [Entity(p) for p in GetCSV("jobs.csv")]

media = [Media(p) for p in GetCSV("media.csv")]


education = [Entity(p) for p in GetCSV("education.csv")]

talks = [Entity(p) for p in GetCSV("talks.csv")]

awards = [Entity(p) for p in GetCSV("awards.csv")]

#keys = [m.paper_id for m in media]

for id, paper in papers.items():
    paper.add_coauthors(coauthors, people)
    paper.add_media(media)

environment = jinja2.Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("research.md")

           
with open("research.md", "w") as f:
     f.write(template.render(
         jobs = jobs,
         talks = talks,
         awards = awards, 
         education = education, 
         papers = list(papers.values())))


    
