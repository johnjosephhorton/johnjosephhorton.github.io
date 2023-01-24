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
versions = 1168415698
video=271310994
slides=948566042
twitter_thread=2079299800
code=803104615
citations=930144785
basic_info=447736295

BASE_URL="https://docs.google.com/spreadsheets/d/$(key)/export?format=csv&gid="

inputs =


inputs += citations.csv
citations.csv:
	wget --output-file="logs.csv" $(BASE_URL)$(citations) -O $@

inputs += basic_info.csv
basic_info.csv:
	wget --output-file="logs.csv" $(BASE_URL)$(basic_info) -O $@

inputs += twitter_thread.csv
twitter_thread.csv:
	wget --output-file="logs.csv" $(BASE_URL)$(twitter_thread) -O $@

inputs += code.csv
code.csv:
	wget --output-file="logs.csv" $(BASE_URL)$(code) -O $@

inputs += slides.csv
slides.csv:
	wget --output-file="logs.csv" $(BASE_URL)$(slides) -O $@

inputs += video.csv
video.csv:
	wget --output-file="logs.csv" $(BASE_URL)$(video) -O $@

inputs += versions.csv
versions.csv:
	wget --output-file="logs.csv" $(BASE_URL)$(versions) -O $@

inputs += media.csv
media.csv:
	wget --output-file="logs.csv" "https://docs.google.com/spreadsheets/d/$(key)/export?format=csv&gid=$(media)" -O "media.csv"

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

index.html: research.md
	pandoc research.md -o index.html
	firefox index.html

website: index.html
	firefox index.html

update:
	git add . 
	git commit -m "Updates"
	git push origin master

