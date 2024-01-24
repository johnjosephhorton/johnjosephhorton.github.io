
.PHONY: refresh

refresh:
	python3 pull_data.py

data/my_database.db: pull_data.py
	python3 pull_data.py

website.md: templates/website.md create_website.py data/my_database.db
	python3.9 create_website.py

index.html: website.md style.css
	pandoc website.md --metadata pagetitle="John Horton's Academic Website" -s --css style.css -o index.html

website: index.html
	firefox index.html

update:
	git add -u
	git commit -m "Updates"
	git push origin master

