"""Generate a social-preview PNG for every paper from local CSV data."""
import csv
import re
import textwrap
import unicodedata
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

def slugify(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")

people = {r["id"]: f'{r["first"]} {r["last"]}' for r in csv.DictReader(open("data/people.csv"))}
people["john"] = "John J. Horton"
orders = {r["paper_id"]: r["author_ids"].split(";") for r in csv.DictReader(open("data/paper_author_order.csv"))}
papers = list(csv.DictReader(open("data/papers.csv")))
output = Path("images/papers"); output.mkdir(parents=True, exist_ok=True)
font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
bold_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
title_font = ImageFont.truetype(bold_path, 54)
author_font = ImageFont.truetype(font_path, 27)
label_font = ImageFont.truetype(bold_path, 23)
for paper in papers:
    image = Image.new("RGB", (1200, 630), "#f5f7fa")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((72, 64, 1128, 566), radius=28, fill="white", outline="#e4e7ec", width=2)
    draw.rounded_rectangle((72, 64, 88, 566), radius=8, fill="#175cd3")
    title_lines = textwrap.wrap(paper["title"], width=35)[:4]
    y = 125
    for line in title_lines:
        draw.text((140, y), line, font=title_font, fill="#172033")
        y += 66
    authors = ", ".join(people[i] for i in orders[paper["id"]])
    author_lines = textwrap.wrap(authors, width=72)[:2]
    y = max(y + 18, 425)
    for line in author_lines:
        draw.text((143, y), line, font=author_font, fill="#475467")
        y += 37
    draw.text((143, 520), "JOHN-JOSEPH-HORTON.COM", font=label_font, fill="#175cd3")
    image.save(output / f'{slugify(paper["title"])}.png', optimize=True)
print(f"Generated {len(papers)} paper social cards")
