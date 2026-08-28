
.PHONY: build validate links website serve paper-pages pdf FORCE

LAST_UPDATED ?= $(shell git log -1 --format=%cs 2>/dev/null || date +%F)

validate:
	python3 validate_data.py

links:
	python3 check_links.py

website.md: templates/website.md templates/paper.md create_website.py $(wildcard data/*.csv)
	python3 create_website.py

index.html: website.md templates/template.html FORCE
	pandoc website.md --metadata pagetitle="John Horton's Academic Website" --metadata lastupdated="$(LAST_UPDATED)" -s --template=templates/template.html -o index.html

paper-pages: website.md templates/paper.html
	@for source in papers/*/index.md; do \
		pandoc "$$source" --metadata lastupdated="$(LAST_UPDATED)" -s --template=templates/paper.html -o "$${source%.md}.html"; \
	done

pdf:
	pandoc website.md -o cv.pdf

website: index.html
	open index.html

# YouTube embeds require an HTTP Referer, which file:// previews cannot provide.
serve: build
	@echo "Preview: http://127.0.0.1:8000/"
	python3 -m http.server 8000 --bind 127.0.0.1

build: validate index.html paper-pages

FORCE:
