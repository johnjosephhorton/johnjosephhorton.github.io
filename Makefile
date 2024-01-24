
.PHONY: refresh

refresh:
	python3 pull_data.py

data/my_database.db: pull_data.py
	python3 pull_data.py

research.md: templates/research.md create_website.py data/my_database.db
	python3.9 create_website.py

research.pdf: research.md
	pandoc research.md -o research.pdf
	evince research.pdf

index.html: research.md style.css
	#pandoc research.md -o index.html
	pandoc research.md --metadata pagetitle="John Horton Academic Website" -s --css style.css -o index.html
	firefox index.html

website: index.html
	firefox index.html

update:
	git add -u
	git commit -m "Updates"
	git push origin master

