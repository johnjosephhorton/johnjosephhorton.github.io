key = 1EqL3ArudCVWcmJZd2NgC8rK_diIk7dyH4Ws2TRKRBnU
papers = 0
people = 1368934588
coauthors = 1092188089
jobs = 1728652724
education = 766554254
talks = 2121579384
service = 206986886
reviewing = 1182607084
awards = 1383290929
media = 746656087

inputs =

# inputs += media.csv
# media.csv:
# 	wget --output-file="logs.csv" "https://docs.google.com/spreadsheets/d/$(key)/export?format=csv&gid=$(media)" -O "media.csv"


inputs += awards.csv
awards.csv:
	wget --output-file="logs.csv" "https://docs.google.com/spreadsheets/d/$(key)/export?format=csv&gid=$(awards)" -O "awards.csv"


inputs += service.csv
service.csv:
	wget --output-file="logs.csv" "https://docs.google.com/spreadsheets/d/$(key)/export?format=csv&gid=$(service)" -O "service.csv"

inputs += reviewing.csv
reviewing.csv:
	wget --output-file="logs.csv" "https://docs.google.com/spreadsheets/d/$(key)/export?format=csv&gid=$(reviewing)" -O "reviewing.csv"


talks.csv:
	wget --output-file="logs.csv" "https://docs.google.com/spreadsheets/d/$(key)/export?format=csv&gid=$(talks)" -O "talks.csv"
inputs += talks.csv


education.csv:
	wget --output-file="logs.csv" "https://docs.google.com/spreadsheets/d/$(key)/export?format=csv&gid=$(education)" -O "education.csv"
inputs += education.csv

papers.csv:
	wget --output-file="logs.csv" "https://docs.google.com/spreadsheets/d/$(key)/export?format=csv&gid=$(papers)" -O "papers.csv"

inputs += papers.csv

jobs.csv:
	wget --output-file="logs.csv" "https://docs.google.com/spreadsheets/d/$(key)/export?format=csv&gid=$(jobs)" -O "jobs.csv"

inputs += jobs.csv

people.csv: 
	wget --output-file="logs.csv" "https://docs.google.com/spreadsheets/d/$(key)/export?format=csv&gid=$(people)" -O "people.csv"

inputs += people.csv

coauthors.csv:
	wget --output-file="logs.csv" "https://docs.google.com/spreadsheets/d/$(key)/export?format=csv&gid=$(coauthors)" -O "coauthors.csv"

inputs += coauthors.csv

research.md: $(inputs) templates/research.md create_website.py
	python3.9 create_website.py

research.pdf: research.md
	pandoc research.md -o research.pdf
	evince research.pdf

website:
	git add . 
	git commit -m "Updates"
	git push origin master

