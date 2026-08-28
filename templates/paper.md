---
title: "{{ paper.title }}"
description: "{{ page.summary }}"
canonical: "https://john-joseph-horton.com/papers/{{ page.slug }}/"
---

[← John J. Horton’s research](../../index.html#research)

# {{ paper.title }}

John J. Horton{% for coauthor in paper.coauthors %}, {{ coauthor.full_name }}{% endfor %}

{% if paper.show_status %}**Status:** {{ paper.status }}{% endif %}

{% if paper.primary_publication %}**{{ paper.publication_label }}:** {{ paper.primary_publication.citation }}

{% endif %}
**Last updated:** {{ paper.last_updated }}

{% if page.summary %}
## Summary

{{ page.summary }}
{% endif %}

{% if paper.detail_version_line %}## Paper links

{{ paper.detail_version_line }}
{% endif %}

{% if presentations %}## Presentations

{% for presentation in presentations %}[{{ presentation.event }}]({{ presentation.url }}), {{ presentation.year }}
{% endfor %}{% endif %}

{% if paper._media %}## Coverage

{% for item in paper._media %}[{{ item.story_name }}]({{ item.url }}), {{ item.publication }}
{% endfor %}{% endif %}

## Cite

<div class="mb-3 flex items-center gap-3">
<button id="copy-bibtex" class="copy-button" type="button">Copy BibTeX</button>
<span id="bibtex-copy-status" class="text-sm text-gray-500" aria-live="polite"></span>
</div>

```bibtex
{{ page.bibtex }}
```

[Google Scholar]({{ paper.gs_url }})
