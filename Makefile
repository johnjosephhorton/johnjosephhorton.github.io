
.PHONY: build validate website pdf

validate:
	python3 validate_data.py

website.md: templates/website.md create_website.py $(wildcard data/*.csv)
	python3 create_website.py

index.html: website.md templates/template.html
	pandoc website.md --metadata pagetitle="John Horton's Academic Website" -s --template=templates/template.html -o index.html

pdf:
	pandoc website.md -o cv.pdf

website: index.html
	open index.html

build: validate index.html
