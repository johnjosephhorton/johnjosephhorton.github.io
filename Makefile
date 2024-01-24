
data/my_database.db: pull_data.py
	python3 new_pull_data.py

research.md: templates/research.md create_website.py data/my_database.db
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

