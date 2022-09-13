papers.csv:
	wget --output-file="logs.csv" "https://docs.google.com/spreadsheets/d/1EqL3ArudCVWcmJZd2NgC8rK_diIk7dyH4Ws2TRKRBnU/export?format=csv&gid=0" -O "papers.csv"

people.csv: 
	wget --output-file="logs.csv" "https://docs.google.com/spreadsheets/d/1EqL3ArudCVWcmJZd2NgC8rK_diIk7dyH4Ws2TRKRBnU/export?format=csv&gid=1368934588" -O "people.csv"

coauthors.csv:
	wget --output-file="logs.csv" "https://docs.google.com/spreadsheets/d/1EqL3ArudCVWcmJZd2NgC8rK_diIk7dyH4Ws2TRKRBnU/export?format=csv&gid=1092188089" -O "coauthors.csv"

research.md: papers.csv templates/research.md
	python3.9 create_website.py

research.pdf: research.md
	pandoc research.md -o research.pdf
	evince research.pdf

website:
	git add . 
	git commit -m "Updates"
	git push origin master

