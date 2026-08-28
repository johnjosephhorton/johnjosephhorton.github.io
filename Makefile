
.PHONY: build validate links website serve paper-pages standalone-pages refresh-writing pdf FORCE

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

standalone-pages: bio.md expected-parrot.md templates/page.html
	pandoc bio.md --metadata title="Bio & Press Materials" --metadata description="Official biographies, headshot, curriculum vitae, and profile links for John J. Horton." --metadata canonical="https://john-joseph-horton.com/bio.html" --metadata lastupdated="$(LAST_UPDATED)" -s --template=templates/page.html -o bio.html
	pandoc expected-parrot.md --metadata title="Expected Parrot" --metadata description="John J. Horton on Expected Parrot and the open-source building blocks for automated social science." --metadata canonical="https://john-joseph-horton.com/expected-parrot.html" --metadata lastupdated="$(LAST_UPDATED)" -s --template=templates/page.html -o expected-parrot.html

refresh-writing:
	python3 scripts/update_writing_feed.py

pdf:
	pandoc website.md --pdf-engine=xelatex -o cv.pdf

website: index.html
	open index.html

# YouTube embeds require an HTTP Referer, which file:// previews cannot provide.
serve: build
	@echo "Preview: http://127.0.0.1:8000/"
	python3 -m http.server 8000 --bind 127.0.0.1

build: validate index.html paper-pages standalone-pages

FORCE:
