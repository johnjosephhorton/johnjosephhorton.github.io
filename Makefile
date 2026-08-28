
.PHONY: build validate links website pdf FORCE

LAST_UPDATED ?= $(shell git log -1 --format=%cs 2>/dev/null || date +%F)

validate:
	python3 validate_data.py

links:
	python3 check_links.py

website.md: templates/website.md create_website.py $(wildcard data/*.csv)
	python3 create_website.py

index.html: website.md templates/template.html FORCE
	pandoc website.md --metadata pagetitle="John Horton's Academic Website" --metadata lastupdated="$(LAST_UPDATED)" -s --template=templates/template.html -o index.html

pdf:
	pandoc website.md -o cv.pdf

website: index.html
	open index.html

build: validate index.html

FORCE:
