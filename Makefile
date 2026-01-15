
.PHONY: refresh

refresh:
	python3 pull_data.py

data/my_database.db: pull_data.py
	python3 pull_data.py

website.md: templates/website.md create_website.py data/my_database.db
	python create_website.py

index.html: website.md templates/template.html
	pandoc website.md --metadata pagetitle="John Horton's Academic Website" -s --template=templates/template.html -o index.html

pdf:
	pandoc website.md -o cv.pdf

website: index.html
	open index.html

update:
	git add -u
	git commit -m "Updates"
	git push origin master

