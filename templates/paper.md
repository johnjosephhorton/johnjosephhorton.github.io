---
title: "{{ paper.title }}"
description: >-
  {{ page.description | replace('\n', ' ') }}
canonical: "https://john-joseph-horton.com/papers/{{ page.slug }}/"
---

[← John J. Horton’s research](../../index.html#research)

# {{ paper.title }}

{% for author in paper.authors %}{% if not loop.first %}, {% endif %}{{ author.full_name }}{% endfor %}

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

{% if paper.video_embeds %}## Video

{% for video in paper.video_embeds %}<div class="video-embed">
<iframe src="{{ video.embed_url }}" title="{{ video.title }}" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>
{% endfor %}{% endif %}

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
