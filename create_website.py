import jinja2
import csv
from jinja2 import FileSystemLoader


environment = jinja2.Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("research.md")

def googleScholarURL(key):
        return "https://scholar.google.com/citations?view_op=view_citation&hl=en&&citation_for_view=" + key

class Paper:
    def __init__(self, row):
        self.title = row["title"]
        self.status = row["status"]
        self.identifier = row["identifier"]
        self.google_scholar = row["google_scholar"]
        if self.google_scholar != '':
            self.gs_url = googleScholarURL(self.google_scholar)
        else:
            self.gs_url = ""

    def add_coauthors(self, coauthors, people):
        self.coauthors = []
        for coauthor in coauthors:
            if coauthor["paper"] == self.identifier:
                self.coauthors.append(coauthor)


    def __repr__(self):
        return "<paper:" + self.title

# 1. Add coauthors as necessary
    
def GetCSV(name):
    outcome = [] 
    with open(name, "r") as f:
        raw = csv.reader(f)
        header = next(raw)
        [outcome.append(dict(zip(header, row))) for row in raw]
    return outcome
         
    

people = GetCSV("people.csv")
papers = GetCSV("papers.csv")
coauthors = GetCSV("coauthors.csv")

P = [Paper(p) for p in papers]
[p.add_coauthors(coauthors, people) for p in P]


with open("research.md", "w") as f:
    f.write(template.render(papers = P))

    


    
